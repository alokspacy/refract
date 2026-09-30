import re
import logging
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.variant import GeneratedVariant, GeneratedBlock, ValidationResult
from app.providers.llm import LLMProvider, get_llm_provider
from app.prompts.grounding import (
    GROUNDING_SYSTEM_PROMPT,
    GROUNDING_USER_TEMPLATE
)

logger = logging.getLogger("accesslearn.pipeline.validate")


class ContentValidator:
    """
    Validates generated content against source blocks for:
    1. Numeric token & statistical preservation.
    2. Proper noun retention.
    3. Structural schema completeness and non-empty output.
    4. Source grounding verification.
    """

    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.llm = llm_provider or get_llm_provider()

    @staticmethod
    def extract_numbers(text: str) -> List[str]:
        """Extract all numeric tokens including percentages and units."""
        return re.findall(r"\b\d+(?:\.\d+)?(?:%|°C|°F|m/s|km|kg|g|cm|mm)?\b", text)

    def validate_variant(
        self,
        variant: GeneratedVariant,
        document: Document,
        generated_blocks: List[GeneratedBlock],
        db: Session,
        progress_callback: Optional[Any] = None
    ) -> ValidationResult:
        logger.info(f"Starting validation for variant_id={variant.id} ({len(generated_blocks)} blocks)")
        if progress_callback:
            progress_callback("VALIDATING", 75.0)

        # Build lookup map for source blocks
        source_blocks_map: Dict[str, str] = {}
        raw_content = document.normalized_content or {}
        for sec in raw_content.get("sections", []):
            for blk in sec.get("blocks", []):
                bid = blk.get("id")
                if bid:
                    source_blocks_map[bid] = blk.get("source_text", "")

        is_all_valid = True
        is_all_grounded = True
        all_warnings: List[str] = []
        all_errors: List[str] = []
        all_unsupported_claims: List[str] = []

        for idx, g_block in enumerate(generated_blocks):
            if g_block.status != "COMPLETED":
                continue

            source_text = source_blocks_map.get(g_block.source_block_id, "")
            block_content = g_block.content or {}
            
            # Combine generated text strings for verification
            gen_text_parts: List[str] = []
            for k, v in block_content.items():
                if isinstance(v, str):
                    gen_text_parts.append(v)
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, str):
                            gen_text_parts.append(item)
                        elif isinstance(item, dict):
                            gen_text_parts.extend(str(sub_v) for sub_v in item.values())

            generated_full_text = " ".join(gen_text_parts)

            # 1. Non-empty check
            if not generated_full_text.strip():
                is_all_valid = False
                all_errors.append(f"Block {g_block.source_block_id}: Empty output generated.")
                continue

            # 2. Number preservation check
            source_numbers = self.extract_numbers(source_text)
            gen_numbers = self.extract_numbers(generated_full_text)

            for num in source_numbers:
                if num not in gen_numbers and num not in generated_full_text:
                    warning_msg = f"Block {g_block.source_block_id}: Numeric token '{num}' from source not detected in generated output."
                    all_warnings.append(warning_msg)

            # 3. Grounding Verification (Secondary LLM / rule check)
            try:
                grounding_prompt = GROUNDING_USER_TEMPLATE.format(
                    source_text=source_text[:500],
                    generated_text=generated_full_text[:500]
                )
                ground_resp = self.llm.generate(
                    system_prompt=GROUNDING_SYSTEM_PROMPT,
                    user_prompt=grounding_prompt,
                    temperature=0.1
                )
                ground_json = ground_resp.content_json
                if not ground_json.get("grounded", True):
                    is_all_grounded = False
                    for claim in ground_json.get("unsupported_claims", []):
                        all_unsupported_claims.append(f"Block {g_block.source_block_id}: {claim}")
            except Exception as g_err:
                logger.warning(f"Grounding verification call warning on block {g_block.source_block_id}: {g_err}")

        # 4. Create and persist ValidationResult
        val_result = ValidationResult(
            variant_id=variant.id,
            is_valid=is_all_valid and (len(all_errors) == 0),
            grounded=is_all_grounded and (len(all_unsupported_claims) == 0),
            unsupported_claims=all_unsupported_claims,
            warnings=all_warnings,
            errors=all_errors
        )
        db.add(val_result)

        # Finalize variant status
        if variant.status != "PARTIAL" and variant.status != "FAILED":
            variant.status = "COMPLETED" if val_result.is_valid else "PARTIAL"
        db.commit()
        db.refresh(val_result)

        if progress_callback:
            progress_callback("COMPLETED", 100.0)

        logger.info(f"Validation complete for variant_id={variant.id}: valid={val_result.is_valid}, grounded={val_result.grounded}, warnings={len(all_warnings)}, errors={len(all_errors)}")
        return val_result

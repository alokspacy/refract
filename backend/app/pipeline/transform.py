import logging
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.analysis import ContentAnalysis
from app.models.variant import GeneratedVariant, GeneratedBlock, ProviderUsage
from app.pipeline.planner import TransformationPlan, BlockTransformationPlan
from app.pipeline.cache import TransformationCacheManager
from app.profiles.registry import get_profile_registry
from app.providers.llm import LLMProvider, get_llm_provider

logger = logging.getLogger("accesslearn.pipeline.transform")


class TransformationEngine:
    """
    Executes transformation plans by invoking LLM providers or retrieving cached representations.
    Persists GeneratedBlocks with strict source block traceability and handles block-level retries.
    """

    def __init__(
        self,
        llm_provider: Optional[LLMProvider] = None,
        cache_manager: Optional[TransformationCacheManager] = None
    ):
        self.llm = llm_provider or get_llm_provider()
        self.cache = cache_manager or TransformationCacheManager()
        self.registry = get_profile_registry()

    def transform_variant(
        self,
        variant: GeneratedVariant,
        document: Document,
        analysis: Optional[ContentAnalysis],
        plan: TransformationPlan,
        db: Session,
        progress_callback: Optional[Any] = None
    ) -> List[GeneratedBlock]:
        logger.info(f"Executing transformation engine for variant_id={variant.id} ({len(plan.transformations)} blocks)")
        variant.status = "PROCESSING"
        db.commit()

        generated_blocks: List[GeneratedBlock] = []
        total_items = len(plan.transformations)
        failed_count = 0

        doc_title = document.original_filename
        subject = analysis.subject if analysis else "General"
        grade_hint = analysis.grade_hint if analysis else "Standard"
        if variant.metadata_overrides:
            subject = variant.metadata_overrides.get("subject", subject)
            grade_hint = variant.metadata_overrides.get("grade_hint", grade_hint)

        for idx, item in enumerate(plan.transformations):
            current_progress = 35.0 + (float(idx) / max(total_items, 1) * 35.0)  # Maps to 35% - 70%
            if progress_callback:
                progress_callback("TRANSFORMING", current_progress)

            profile_id = item.profile_ids[0] if item.profile_ids else "dyslexia"
            profile = self.registry.get_profile(profile_id)
            if not profile:
                logger.error(f"Profile not found: {profile_id}")
                continue

            model_name = getattr(self.llm, "default_model", "mock-gpt-4o")
            cache_key = self.cache.compute_cache_key(
                source_text=item.source_text,
                profile_id=profile.profile_id,
                profile_version=profile.version,
                prompt_version=profile.prompt_version,
                model=model_name
            )

            # 1. Check cache
            cached_content = self.cache.get_cached_content(db, cache_key)
            if cached_content:
                gen_block = GeneratedBlock(
                    variant_id=variant.id,
                    source_block_id=item.source_block_id,
                    profile_id=profile.profile_id,
                    content=cached_content,
                    status="COMPLETED",
                    prompt_version=profile.prompt_version,
                    model=model_name,
                    provider="cache"
                )
                db.add(gen_block)
                db.commit()
                db.refresh(gen_block)
                generated_blocks.append(gen_block)
                continue

            # 2. Invoke LLM Provider
            try:
                user_prompt = profile.build_user_prompt(
                    source_block_id=item.source_block_id,
                    source_text=item.source_text,
                    block_type=item.block_type,
                    document_title=doc_title,
                    subject=subject,
                    grade_hint=grade_hint
                )

                response = self.llm.generate(
                    system_prompt=profile.system_prompt,
                    user_prompt=user_prompt,
                    response_schema=profile.output_schema,
                    model=model_name,
                    temperature=0.2,
                    max_retries=1
                )

                # Validate against schema
                validated_obj = profile.validate_content(response.content_json)
                content_dict = validated_obj.model_dump()

                # Track usage
                usage = response.usage or {}
                usage_record = ProviderUsage(
                    provider=response.provider,
                    model=response.model,
                    operation=f"transform_{profile.profile_id}",
                    prompt_tokens=usage.get("prompt_tokens", 0),
                    completion_tokens=usage.get("completion_tokens", 0),
                    total_tokens=usage.get("total_tokens", 0),
                    estimated_cost_usd=usage.get("estimated_cost_usd", 0.0)
                )
                db.add(usage_record)

                # Store in cache
                self.cache.store_cached_content(
                    db=db,
                    source_text=item.source_text,
                    profile_id=profile.profile_id,
                    profile_version=profile.version,
                    prompt_version=profile.prompt_version,
                    model=model_name,
                    content=content_dict
                )

                gen_block = GeneratedBlock(
                    variant_id=variant.id,
                    source_block_id=item.source_block_id,
                    profile_id=profile.profile_id,
                    content=content_dict,
                    status="COMPLETED",
                    prompt_version=profile.prompt_version,
                    model=response.model,
                    provider=response.provider
                )
                db.add(gen_block)
                db.commit()
                db.refresh(gen_block)
                generated_blocks.append(gen_block)

            except Exception as block_err:
                logger.exception(f"Failed to transform block_id={item.source_block_id}: {block_err}")
                failed_count += 1
                gen_block = GeneratedBlock(
                    variant_id=variant.id,
                    source_block_id=item.source_block_id,
                    profile_id=profile.profile_id,
                    content={},
                    status="FAILED",
                    prompt_version=profile.prompt_version,
                    model=model_name,
                    provider=getattr(self.llm, "provider", "mock"),
                    error_message=str(block_err)
                )
                db.add(gen_block)
                db.commit()
                db.refresh(gen_block)
                generated_blocks.append(gen_block)

        # Update variant status based on block results
        if failed_count == 0:
            variant.status = "PROCESSING"  # Moves to validating stage next
        elif failed_count < len(plan.transformations):
            variant.status = "PARTIAL"
        else:
            variant.status = "FAILED"
        db.commit()

        logger.info(f"Transformation complete for variant_id={variant.id}: {len(generated_blocks) - failed_count} succeeded, {failed_count} failed")
        return generated_blocks

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from app.models.analysis import ContentAnalysis
from app.profiles.registry import get_profile_registry

logger = logging.getLogger("accesslearn.pipeline.planner")


@dataclass
class BlockTransformationPlan:
    source_block_id: str
    source_text: str
    block_type: str
    profile_ids: List[str]
    operation: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TransformationPlan:
    document_id: str
    profiles: List[Dict[str, str]]
    transformations: List[BlockTransformationPlan]


class AccessibilityPlanner:
    """
    Deterministic Accessibility Planner that maps source document blocks to profile transformations.
    Applies strict deterministic precedence rules without relying on LLM decision randomness.
    """

    def __init__(self):
        self.registry = get_profile_registry()

    def create_plan(
        self,
        document_id: str,
        normalized_content: Dict[str, Any],
        analysis: Optional[ContentAnalysis],
        profile_ids: List[str]
    ) -> TransformationPlan:
        logger.info(f"Creating transformation plan for document_id={document_id} with profiles={profile_ids}")
        
        # 1. Resolve and validate profiles
        ordered_profile_ids = self.registry.resolve_precedence(profile_ids)
        if not ordered_profile_ids:
            ordered_profile_ids = ["dyslexia"]

        profile_metadata = []
        for pid in ordered_profile_ids:
            prof = self.registry.get_profile(pid)
            if prof:
                profile_metadata.append({
                    "profile_id": prof.profile_id,
                    "profile_name": prof.name,
                    "profile_version": prof.version
                })

        # 2. Iterate through sections & blocks
        transformations: List[BlockTransformationPlan] = []
        sections = normalized_content.get("sections", [])

        for sec in sections:
            for blk in sec.get("blocks", []):
                blk_id = blk.get("id", "")
                blk_type = blk.get("type", "paragraph")
                text = (blk.get("source_text") or "").strip()

                if not text and blk_type != "image":
                    continue

                # Determine operation based on block type and target profiles
                for pid in ordered_profile_ids:
                    if pid == "dyslexia":
                        op = "plain_language_simplification"
                    elif pid == "cognitive":
                        op = "concept_scaffolding"
                    elif pid == "visual_basic":
                        op = "semantic_restructuring"
                    else:
                        op = "standard_transformation"

                    transformations.append(
                        BlockTransformationPlan(
                            source_block_id=blk_id,
                            source_text=text,
                            block_type=blk_type,
                            profile_ids=[pid],
                            operation=op,
                            metadata=blk.get("metadata", {})
                        )
                    )

        logger.info(f"Generated transformation plan: {len(transformations)} block transformations across {len(profile_metadata)} profiles")
        return TransformationPlan(
            document_id=document_id,
            profiles=profile_metadata,
            transformations=transformations
        )

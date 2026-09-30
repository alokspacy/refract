import logging
from typing import Any, Dict, List, Optional, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.job import ProcessingJob
from app.models.analysis import ContentAnalysis
from app.models.variant import GeneratedVariant, GeneratedBlock, ValidationResult
from app.profiles.registry import get_profile_registry
from app.pipeline.analyze import ContentAnalyzer
from app.pipeline.planner import AccessibilityPlanner
from app.pipeline.transform import TransformationEngine
from app.pipeline.validate import ContentValidator
from app.workers.tasks import analyze_document_job, generate_variant_job

logger = logging.getLogger("accesslearn.services.variant")


class VariantService:
    """
    Business logic for document analysis and accessibility variant lifecycle.
    """

    def __init__(self):
        self.analyzer = ContentAnalyzer()
        self.planner = AccessibilityPlanner()
        self.transformer = TransformationEngine()
        self.validator = ContentValidator()
        self.registry = get_profile_registry()

    def get_document_with_auth(self, db: Session, document_id: str, user_id: str) -> Document:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        if doc.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this document")
        return doc

    def analyze_document_request(
        self,
        db: Session,
        document_id: str,
        user_id: str
    ) -> Tuple[ContentAnalysis, ProcessingJob]:
        doc = self.get_document_with_auth(db, document_id, user_id)
        if not doc.normalized_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document has not completed Phase 2 extraction/normalization yet."
            )

        # Create job
        job = ProcessingJob(
            document_id=doc.id,
            status="QUEUED",
            current_stage="ANALYZING",
            progress=0.0
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        # Enqueue Celery task
        try:
            analyze_document_job.apply_async(
                kwargs={"job_id": job.id, "document_id": doc.id},
                retry=False
            )
            logger.info(f"Enqueued analyze_document_job={job.id} for document={doc.id}")
        except Exception as q_err:
            logger.warning(f"Celery queue dispatch skipped (worker offline): {q_err}")

        analysis = db.query(ContentAnalysis).filter(ContentAnalysis.document_id == doc.id).first()
        return analysis, job

    def get_document_analysis(self, db: Session, document_id: str, user_id: str) -> ContentAnalysis:
        doc = self.get_document_with_auth(db, document_id, user_id)
        analysis = db.query(ContentAnalysis).filter(ContentAnalysis.document_id == doc.id).first()
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not yet generated for this document. Call POST /documents/{id}/analyze first."
            )
        return analysis

    def create_variant_request(
        self,
        db: Session,
        document_id: str,
        user_id: str,
        profile_ids: List[str],
        metadata_overrides: Optional[Dict[str, Any]] = None
    ) -> Tuple[GeneratedVariant, ProcessingJob]:
        doc = self.get_document_with_auth(db, document_id, user_id)
        if not doc.normalized_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document normalized content is required to generate accessible variants."
            )

        # Validate profiles
        valid_profiles = self.registry.resolve_precedence(profile_ids)
        if not valid_profiles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one valid profile ID must be specified (dyslexia, cognitive, visual_basic)."
            )

        profile_versions = {}
        for pid in valid_profiles:
            p = self.registry.get_profile(pid)
            if p:
                profile_versions[pid] = p.version

        # Build readable name
        names = [self.registry.get_profile(pid).name for pid in valid_profiles if self.registry.get_profile(pid)]
        variant_name = f"{' + '.join(names)} Adaptation"

        # Create Variant record
        variant = GeneratedVariant(
            document_id=doc.id,
            name=variant_name,
            status="QUEUED",
            profile_ids=valid_profiles,
            profile_versions=profile_versions,
            metadata_overrides=metadata_overrides or {}
        )
        db.add(variant)
        db.commit()
        db.refresh(variant)

        # Create Job record
        job = ProcessingJob(
            document_id=doc.id,
            status="QUEUED",
            current_stage="ANALYZING",
            progress=0.0
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        # Enqueue Celery task
        from app.workers.tasks import generate_variant_job
        try:
            generate_variant_job.apply_async(
                kwargs={
                    "job_id": job.id,
                    "document_id": doc.id,
                    "variant_id": variant.id,
                    "profile_ids": valid_profiles,
                    "metadata_overrides": metadata_overrides
                },
                retry=False
            )
            logger.info(f"Enqueued generate_variant_job={job.id} for variant={variant.id}")
        except Exception as q_err:
            logger.warning(f"Celery queue dispatch skipped (worker offline): {q_err}")

        return variant, job

    def get_variant_with_auth(self, db: Session, variant_id: str, user_id: str) -> GeneratedVariant:
        variant = db.query(GeneratedVariant).filter(GeneratedVariant.id == variant_id).first()
        if not variant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Variant not found")
        
        # Verify ownership via document
        doc = db.query(Document).filter(Document.id == variant.document_id).first()
        if not doc or doc.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this variant")
        return variant

    def get_variant_blocks(self, db: Session, variant_id: str, user_id: str) -> List[GeneratedBlock]:
        variant = self.get_variant_with_auth(db, variant_id, user_id)
        blocks = db.query(GeneratedBlock).filter(GeneratedBlock.variant_id == variant.id).all()
        return blocks

    def get_variant_validation(self, db: Session, variant_id: str, user_id: str) -> ValidationResult:
        variant = self.get_variant_with_auth(db, variant_id, user_id)
        val = db.query(ValidationResult).filter(ValidationResult.variant_id == variant.id).first()
        if not val:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Validation result not found for this variant")
        return val


_variant_service_instance = VariantService()


def get_variant_service() -> VariantService:
    return _variant_service_instance

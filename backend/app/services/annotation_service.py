"""Service for managing educator annotations and reviews."""
from typing import List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.annotation import BlockAnnotation
from app.schemas.annotation import AnnotationCreate, VariantReviewSummary

class AnnotationService:
    def add_or_update(self, db: Session, variant_id: str, educator_id: str, data: AnnotationCreate) -> BlockAnnotation:
        existing = db.query(BlockAnnotation).filter(
            BlockAnnotation.variant_id == variant_id,
            BlockAnnotation.block_id == data.block_id
        ).first()

        if existing:
            existing.status = data.status
            existing.comment = data.comment
            existing.suggested_content = data.suggested_content
            existing.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(existing)
            return existing

        annotation = BlockAnnotation(
            variant_id=variant_id,
            block_id=data.block_id,
            educator_id=educator_id,
            status=data.status,
            comment=data.comment,
            suggested_content=data.suggested_content
        )
        db.add(annotation)
        db.commit()
        db.refresh(annotation)
        return annotation

    def get_summary(self, db: Session, variant_id: str, total_blocks: int = 10) -> VariantReviewSummary:
        records = db.query(BlockAnnotation).filter(BlockAnnotation.variant_id == variant_id).all()
        approved = sum(1 for r in records if r.status == "approved")
        flagged = sum(1 for r in records if r.status == "flagged")
        pending = max(0, total_blocks - (approved + flagged))
        rate = round((approved / max(total_blocks, 1)) * 100.0, 1)

        return VariantReviewSummary(
            variant_id=variant_id,
            total_blocks=total_blocks,
            approved_blocks=approved,
            flagged_blocks=flagged,
            pending_blocks=pending,
            approval_rate=rate,
            is_ready_for_publish=approved >= total_blocks and total_blocks > 0
        )

"""FastAPI router for educator reviews."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.annotation import AnnotationCreate, AnnotationResponse, VariantReviewSummary
from app.services.annotation_service import AnnotationService

router = APIRouter(prefix="/annotations", tags=["Educator Annotations"])
service = AnnotationService()

@router.post("/variants/{variant_id}/review", response_model=AnnotationResponse)
def submit_block_review(variant_id: str, payload: AnnotationCreate, db: Session = Depends(get_db)):
    """Record an educator's approval or revision feedback on a specific content block."""
    return service.add_or_update(db, variant_id, educator_id="educator-001", data=payload)

@router.get("/variants/{variant_id}/summary", response_model=VariantReviewSummary)
def get_variant_review_summary(variant_id: str, db: Session = Depends(get_db)):
    """Get overall educator approval metrics and readiness status."""
    return service.get_summary(db, variant_id)

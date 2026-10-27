"""FastAPI router for reading level assessments."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.assessment import ReadingAssessmentResponse
from app.services.assessment_service import AssessmentService

router = APIRouter(prefix="/assessment", tags=["Assessment"])
assessment_service = AssessmentService()

@router.post("/evaluate-text", response_model=ReadingAssessmentResponse)
def evaluate_raw_text(text: str):
    """Evaluate raw text for reading grade, syllable distributions, and Lexile score."""
    if not text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text cannot be empty")
    return assessment_service.evaluate_text(text)

@router.get("/documents/{document_id}", response_model=ReadingAssessmentResponse)
def evaluate_document_reading_level(document_id: str, db: Session = Depends(get_db)):
    """Evaluate an existing normalized document for readability level."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"Document {document_id} not found or not normalized"}
        )
    content_doc = ContentDocument.model_validate(doc.normalized_content)
    return assessment_service.evaluate_document(content_doc)

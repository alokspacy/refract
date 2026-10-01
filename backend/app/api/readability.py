"""FastAPI router for readability and complexity analysis."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.models.variant import GeneratedVariant
from app.schemas.readability import ReadabilityReport
from app.schemas.content import ContentDocument
from app.services.readability_service import ReadabilityService

router = APIRouter(prefix="/readability", tags=["Readability"])
service = ReadabilityService()

class AnalyzeTextPayload(BaseModel):
    text: str

@router.post("/analyze", response_model=ReadabilityReport)
def analyze_raw_text(payload: AnalyzeTextPayload):
    """Analyze readability metrics for any arbitrary text snippet."""
    return service.analyze_text(payload.text)

@router.get("/documents/{document_id}", response_model=ReadabilityReport)
def analyze_document(document_id: str, db: Session = Depends(get_db)):
    """Analyze readability of a normalized document's combined text."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"Document {document_id} not found or empty"}
        )
    content = ContentDocument.model_validate(doc.normalized_content)
    texts = []
    for s in content.sections:
        for b in s.blocks:
            if b.source_text:
                texts.append(b.source_text)
    combined = " ".join(texts)
    return service.analyze_text(combined)

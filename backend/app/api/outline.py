"""FastAPI router for document heading outline navigation."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.outline import DocumentOutline
from app.services.outline_service import OutlineService

router = APIRouter(prefix="/outline", tags=["Document Outline Navigation"])
service = OutlineService()

@router.post("/extract", response_model=DocumentOutline)
def extract_outline(doc: ContentDocument):
    """Extract accessible heading hierarchy for direct screen reader jumping."""
    return service.extract_outline(doc)

@router.get("/documents/{document_id}", response_model=DocumentOutline)
def get_document_outline(document_id: str, db: Session = Depends(get_db)):
    """Fetch structured heading outline from an existing document."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"Document {document_id} not found or not normalized"}
        )
    content_doc = ContentDocument.model_validate(doc.normalized_content)
    return service.extract_outline(content_doc)

"""FastAPI router for document cloning."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.clone import DocumentCloneRequest, DocumentCloneResponse
from app.services.clone_service import DocumentCloneService

router = APIRouter(prefix="/documents", tags=["Document Cloning"])

@router.post("/{document_id}/clone", response_model=DocumentCloneResponse)
def clone_document(document_id: str, req: DocumentCloneRequest, db: Session = Depends(get_db)):
    """Deep clone a document with regenerated UUIDs for custom tailoring."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(status_code=404, detail="Document not found")
    cd = ContentDocument.model_validate(doc.normalized_content)
    _, res = DocumentCloneService.clone_document(cd, req.new_title)
    return res

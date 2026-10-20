"""FastAPI router for concept mind maps."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.mindmap import MindMapNode
from app.services.mindmap_service import MindMapService

router = APIRouter(prefix="/mindmap", tags=["Concept Mind Map"])
service = MindMapService()

@router.get("/documents/{document_id}", response_model=MindMapNode)
def get_document_mindmap(document_id: str, db: Session = Depends(get_db)):
    """Generate visual concept hierarchy tree for a document."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(status_code=404, detail="Document not found")
    cd = ContentDocument.model_validate(doc.normalized_content)
    return service.build_mindmap(cd)

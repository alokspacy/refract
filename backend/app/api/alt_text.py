"""FastAPI router for accessible image alt-text auditing."""
from fastapi import APIRouter
from app.schemas.content import ContentDocument
from app.schemas.alt_text import DocumentAltTextReport
from app.services.alt_text_service import AltTextService

router = APIRouter(prefix="/alt-text", tags=["Image Accessibility"])
service = AltTextService()

@router.post("/audit", response_model=DocumentAltTextReport)
def audit_document_images(doc: ContentDocument):
    """Audit document images for missing alt attributes and synthesize descriptions."""
    return service.audit_and_generate(doc)

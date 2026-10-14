"""FastAPI router for multilingual accessibility translations."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.translation import TranslationDocumentResponse, LanguageCode
from app.services.translation_service import TranslationService

router = APIRouter(prefix="/translation", tags=["Translation"])
service = TranslationService()

@router.get("/documents/{document_id}", response_model=TranslationDocumentResponse)
def translate_document(document_id: str, lang: LanguageCode = LanguageCode.ES, db: Session = Depends(get_db)):
    """Translate document text into accessible target language."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(status_code=404, detail="Document not found")
    cd = ContentDocument.model_validate(doc.normalized_content)
    return service.translate_document(cd, lang)

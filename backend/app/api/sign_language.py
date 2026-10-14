"""FastAPI router for American Sign Language glossing."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.sign_language import SignLanguageDocumentResponse, ASLGlossSentence
from app.services.sign_language_service import SignLanguageService

router = APIRouter(prefix="/sign-language", tags=["Sign Language"])
service = SignLanguageService()

@router.post("/gloss-sentence", response_model=ASLGlossSentence)
def gloss_sentence(text: str):
    """Convert an English sentence into ASL grammatical gloss structure."""
    return service.to_asl_gloss(text)

@router.get("/documents/{document_id}", response_model=SignLanguageDocumentResponse)
def get_document_asl_gloss(document_id: str, db: Session = Depends(get_db)):
    """Retrieve full ASL gloss translation for a document."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(status_code=404, detail="Document not found")
    cd = ContentDocument.model_validate(doc.normalized_content)
    return service.convert_document(cd)

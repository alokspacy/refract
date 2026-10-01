"""FastAPI router for glossary and flashcard decks."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.glossary import FlashcardDeck
from app.services.glossary_service import GlossaryService

router = APIRouter(prefix="/glossary", tags=["Glossary & Flashcards"])
service = GlossaryService()

@router.get("/documents/{document_id}/flashcards", response_model=FlashcardDeck)
def get_or_generate_flashcards(document_id: str, db: Session = Depends(get_db)):
    """Generate or retrieve cognitive flashcard review deck."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(status_code=404, detail="Document not found")
    cd = ContentDocument.model_validate(doc.normalized_content)
    return service.generate_deck(cd)

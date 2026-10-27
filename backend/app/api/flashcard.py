"""FastAPI router for generating study flashcard decks."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.flashcard import FlashcardDeck
from app.services.flashcard_service import FlashcardService

router = APIRouter(prefix="/flashcards", tags=["Flashcards"])
service = FlashcardService()

@router.post("/generate", response_model=FlashcardDeck)
def generate_custom_flashcards(doc: ContentDocument, max_cards: int = 15):
    """Generate study flashcards from a content document payload."""
    return service.generate_deck(doc, max_cards=max_cards)

@router.get("/documents/{document_id}", response_model=FlashcardDeck)
def generate_document_flashcards(document_id: str, max_cards: int = 15, db: Session = Depends(get_db)):
    """Generate flashcards from an existing saved document."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"Document {document_id} not found or not normalized"}
        )
    content_doc = ContentDocument.model_validate(doc.normalized_content)
    return service.generate_deck(content_doc, max_cards=max_cards)

"""Schemas for flashcards and spaced repetition study decks."""
from typing import List, Optional
from pydantic import BaseModel, Field

class FlashcardItem(BaseModel):
    id: str
    front: str = Field(..., description="Prompt, concept, or question")
    back: str = Field(..., description="Explanation, definition, or answer")
    category: Optional[str] = "General"
    difficulty: Optional[str] = "Normal"

class FlashcardDeck(BaseModel):
    document_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    total_cards: int
    cards: List[FlashcardItem]

class FlashcardGenerationRequest(BaseModel):
    document_id: Optional[str] = None
    max_cards: int = Field(default=15, ge=3, le=50)
    include_glossary: bool = True

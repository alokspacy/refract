"""Schemas for smart flashcards and assistive glossary."""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class CardDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class FlashcardCard(BaseModel):
    id: str
    term: str
    definition: str
    simplified_definition: str
    phonetic_pronunciation: Optional[str] = None
    memory_cue: str = Field(..., description="Cognitive mnemonic or visual memory hook")
    example_sentence: str
    difficulty: CardDifficulty = CardDifficulty.MEDIUM

class FlashcardDeck(BaseModel):
    id: str
    document_id: str
    title: str
    total_cards: int
    cards: List[FlashcardCard] = Field(default_factory=list)

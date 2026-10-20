"""Automated glossary and flashcard generator."""
import uuid
import re
from typing import List
from app.schemas.glossary import FlashcardDeck, FlashcardCard, CardDifficulty
from app.schemas.content import ContentDocument

class GlossaryService:
    """Extracts key pedagogical vocabulary and constructs cognitive flashcards."""

    def generate_deck(self, doc: ContentDocument) -> FlashcardDeck:
        cards: List[FlashcardCard] = []

        if doc.glossary:
            for term, definition in doc.glossary.items():
                if term and len(term.strip()) > 1:
                    cards.append(self._create_card(term, definition))

        if not cards and doc.learning_objectives:
            for obj in doc.learning_objectives:
                words = re.findall(r'\b[A-Z][a-z]{3,}\b', obj)
                for w in words[:3]:
                    cards.append(self._create_card(w, f"Key scientific concept introduced in {doc.title}."))

        if not cards:
            clean_subj = doc.subject or "Core Foundation"
            cards.append(self._create_card(clean_subj, f"Foundational knowledge for {doc.title}."))

        return FlashcardDeck(
            id=str(uuid.uuid4()),
            document_id=doc.id,
            title=f"{doc.title} — Review Deck",
            total_cards=len(cards),
            cards=cards,
        )

    def _create_card(self, term: str, definition: str) -> FlashcardCard:
        return FlashcardCard(
            id=str(uuid.uuid4())[:8],
            term=term,
            definition=definition,
            simplified_definition=f"In simple words: {definition.lower()}",
            phonetic_pronunciation=f"/{term.lower()}/",
            memory_cue=f"Picture a symbol representing {term} when you review this concept.",
            example_sentence=f"We use {term} to explain this biological phenomenon.",
            difficulty=CardDifficulty.MEDIUM
        )

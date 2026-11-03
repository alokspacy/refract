"""Service generating study flashcard decks from content documents."""
import uuid
from typing import List
from app.schemas.content import ContentDocument, BlockType
from app.schemas.flashcard import FlashcardItem, FlashcardDeck

class FlashcardService:
    def generate_deck(self, doc: ContentDocument, max_cards: int = 15, include_glossary: bool = True) -> FlashcardDeck:
        cards: List[FlashcardItem] = []

        if include_glossary and doc.glossary:
            for term, defn in doc.glossary.items():
                if term and defn and term.strip() and defn.strip():
                    cards.append(FlashcardItem(
                        id=str(uuid.uuid4())[:8],
                        front=f"What is {term.strip()}?",
                        back=defn.strip(),
                        category="Glossary",
                        difficulty="Easy"
                    ))
                    if len(cards) >= max_cards:
                        break

        if len(cards) < max_cards and doc.sections:
            for sec in doc.sections:
                for idx, block in enumerate(sec.blocks):
                    if block.type == BlockType.HEADING and block.source_text and block.source_text.strip():
                        next_p = ""
                        for next_b in sec.blocks[idx + 1:idx + 3]:
                            if next_b.type == BlockType.PARAGRAPH and next_b.source_text and next_b.source_text.strip():
                                next_p = next_b.source_text.strip()
                                break
                        if next_p:
                            cards.append(FlashcardItem(
                                id=str(uuid.uuid4())[:8],
                                front=f"Explain: {block.source_text.strip()}",
                                back=next_p[:200] + ("..." if len(next_p) > 200 else ""),
                                category=sec.title or "Concept",
                                difficulty="Medium"
                            ))
                            if len(cards) >= max_cards:
                                break
                if len(cards) >= max_cards:
                    break

        if not cards:
            cards.append(FlashcardItem(
                id=str(uuid.uuid4())[:8],
                front=f"Overview of {doc.title or 'Document'}",
                back="Key concepts are currently being synthesized for this document.",
                category="General",
                difficulty="Easy"
            ))

        return FlashcardDeck(
            document_id=doc.id,
            title=f"Flashcards: {doc.title or 'Study Deck'}",
            description=f"Generated study deck containing {len(cards)} cards.",
            total_cards=len(cards),
            cards=cards
        )

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
                cards.append(FlashcardItem(
                    id=str(uuid.uuid4())[:8],
                    front=f"What is {term}?",
                    back=defn,
                    category="Glossary",
                    difficulty="Easy"
                ))
                if len(cards) >= max_cards:
                    break

        if len(cards) < max_cards:
            for sec in doc.sections:
                for idx, block in enumerate(sec.blocks):
                    if block.type == BlockType.HEADING and block.source_text:
                        next_p = ""
                        for next_b in sec.blocks[idx + 1:idx + 3]:
                            if next_b.type == BlockType.PARAGRAPH and next_b.source_text:
                                next_p = next_b.source_text
                                break
                        if next_p:
                            cards.append(FlashcardItem(
                                id=str(uuid.uuid4())[:8],
                                front=f"Explain: {block.source_text}",
                                back=next_p[:200] + ("..." if len(next_p) > 200 else ""),
                                category=sec.title or "Concept",
                                difficulty="Medium"
                            ))
                            if len(cards) >= max_cards:
                                break
                if len(cards) >= max_cards:
                    break

        return FlashcardDeck(
            document_id=doc.id,
            title=f"Flashcards: {doc.title}",
            description=f"Generated study deck containing {len(cards)} cards.",
            total_cards=len(cards),
            cards=cards
        )

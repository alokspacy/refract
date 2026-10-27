"""Tests for auto flashcard deck generation service."""
from app.services.flashcard_service import FlashcardService
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_flashcard_generation_from_glossary():
    service = FlashcardService()
    doc = ContentDocument(
        title="Physics Basics",
        glossary={"Gravity": "A force that attracts a body toward the center of the earth."},
        sections=[]
    )
    deck = service.generate_deck(doc, max_cards=5)
    assert deck.total_cards == 1
    assert "Gravity" in deck.cards[0].front
    assert "attracts" in deck.cards[0].back

def test_flashcard_generation_from_headings():
    service = FlashcardService()
    doc = ContentDocument(
        title="Cell Structure",
        sections=[
            Section(
                title="Organelles",
                blocks=[
                    ContentBlock(id="b1", type=BlockType.HEADING, source_text="Mitochondria"),
                    ContentBlock(id="b2", type=BlockType.PARAGRAPH, source_text="The powerhouse of the cell providing ATP energy.")
                ]
            )
        ]
    )
    deck = service.generate_deck(doc, max_cards=5)
    assert deck.total_cards == 1
    assert "Mitochondria" in deck.cards[0].front
    assert "powerhouse" in deck.cards[0].back

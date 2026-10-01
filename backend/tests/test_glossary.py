"""Unit tests for glossary generation."""
from app.services.glossary_service import GlossaryService
from tests.fixtures.glossary_mock import MOCK_GLOSSARY_DOC

def test_deck_generation_from_glossary():
    svc = GlossaryService()
    deck = svc.generate_deck(MOCK_GLOSSARY_DOC)
    assert deck.total_cards == 2
    terms = [c.term for c in deck.cards]
    assert "Mitochondria" in terms
    assert "Chloroplast" in terms
    assert all(c.memory_cue for c in deck.cards)
    assert all(c.simplified_definition for c in deck.cards)

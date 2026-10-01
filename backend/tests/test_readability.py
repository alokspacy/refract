"""Unit tests for readability service."""
from app.services.readability_service import ReadabilityService
from tests.fixtures.readability_texts import PRIMARY_TEXT, SCIENTIFIC_TEXT

def test_syllable_counter():
    svc = ReadabilityService()
    assert svc.count_syllables("cat") == 1
    assert svc.count_syllables("water") == 2
    assert svc.count_syllables("photosynthesis") >= 4

def test_primary_text_readability():
    svc = ReadabilityService()
    rep = svc.analyze_text(PRIMARY_TEXT)
    assert rep.scores.flesch_reading_ease >= 80.0
    assert rep.scores.flesch_kincaid_grade <= 4.0
    assert rep.cognitive_difficulty_label in ["Very Accessible", "Accessible"]

def test_scientific_text_readability():
    svc = ReadabilityService()
    rep = svc.analyze_text(SCIENTIFIC_TEXT)
    assert rep.scores.flesch_reading_ease <= 40.0
    assert rep.scores.flesch_kincaid_grade >= 12.0

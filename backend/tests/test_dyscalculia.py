"""Unit tests for dyscalculia adaptation service."""
from app.services.dyscalculia_service import DyscalculiaService

def test_digit_chunking_and_words():
    svc = DyscalculiaService()
    res = svc.format_digits("The school was founded in 1984 with 450 students.")
    assert len(res.numbers_detected) >= 2
    assert "1984" in res.adapted_text
    assert "450" in res.adapted_text

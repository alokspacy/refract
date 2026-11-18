"""Unit tests for phonetic respelling generator service."""
from app.services.phonetics_service import PhoneticsService

def test_phonetics_generation():
    service = PhoneticsService()
    res = service.generate_guide(["Photosynthesis", "Atom"])
    assert res.total_terms == 2
    assert "-" in res.entries[0].phonetic_respelling
    assert len(res.entries[0].syllables) >= 3

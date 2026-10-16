"""Unit tests for plain language service."""
from app.services.plain_language_service import PlainLanguageService

def test_jargon_simplification():
    svc = PlainLanguageService()
    res = svc.simplify_text("We utilize models to elucidate homeostasis.")
    assert "use" in res.simplified_text
    assert "explain" in res.simplified_text
    assert "internal balance" in res.simplified_text
    assert len(res.replacements_made) == 3

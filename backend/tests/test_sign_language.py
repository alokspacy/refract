"""Unit tests for ASL gloss transformation."""
from app.services.sign_language_service import SignLanguageService

def test_asl_gloss_wh_question():
    svc = SignLanguageService()
    res = svc.to_asl_gloss("Where is the school?")
    assert "WHERE" in res.asl_gloss_sequence
    assert res.sentence_type == "wh_question"
    assert res.tokens[-1].gloss == "WHERE"

def test_asl_gloss_topic_comment():
    svc = SignLanguageService()
    res = svc.to_asl_gloss("The student reads a book.")
    assert "STUDENT" in res.asl_gloss_sequence
    assert "BOOK" in res.asl_gloss_sequence

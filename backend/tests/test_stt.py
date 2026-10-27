"""Tests for speech transcription parser service."""
from app.services.stt_service import SpeechTranscriptionService

def test_timed_text_parsing():
    service = SpeechTranscriptionService()
    transcript = "Hello world welcome to accessible learning"
    res = service.parse_timed_text(transcript, duration_sec=10.0)
    assert res.job_id is not None
    assert len(res.tokens) == 6
    assert res.tokens[0].word == "Hello"
    assert res.tokens[-1].word == "learning"
    assert res.tokens[-1].end_sec <= 10.1

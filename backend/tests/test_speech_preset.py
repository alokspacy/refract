"""Unit tests for text-to-speech speed and prosody presets."""
from app.services.speech_preset_service import SpeechPresetService

def test_speech_presets():
    service = SpeechPresetService()
    presets = service.list_presets()
    assert len(presets) >= 4
    dyslexic = service.get_preset("dyslexic")
    assert dyslexic.rate == 0.8
    assert dyslexic.pause_between_sentences_ms == 800

"""Unit tests for WebVTT caption formatting service."""
from app.services.captions_service import CaptionsService
from app.schemas.captions import CaptionStylePreferences

def test_webvtt_generation():
    service = CaptionsService()
    cues = [{"start": 0.0, "end": 2.5, "text": "Welcome to AccessLearn."}]
    style = CaptionStylePreferences(text_color="#FFFF00", font_size_pct=125)
    vtt = service.build_webvtt(cues, style)
    assert vtt.startswith("WEBVTT")
    assert "00:00:00.000 --> 00:00:02.500" in vtt
    assert "color: #FFFF00;" in vtt
    assert "Welcome to AccessLearn." in vtt

"""Unit tests for WebVTT caption generator."""
from app.services.audio_service import AudioNarrationService
from app.schemas.content import ContentBlock, BlockType

def test_vtt_timestamp_formatter():
    assert AudioNarrationService._format_vtt_timestamp(0) == "00:00:00.000"
    assert AudioNarrationService._format_vtt_timestamp(1500) == "00:00:01.500"
    assert AudioNarrationService._format_vtt_timestamp(65000) == "00:01:05.000"

def test_vtt_generation_structure():
    svc = AudioNarrationService()
    blocks = [
        ContentBlock(type=BlockType.HEADING, source_text="Lesson One"),
        ContentBlock(type=BlockType.PARAGRAPH, source_text="This is an introductory lesson on cell biology.")
    ]
    pkg = svc.generate_narration("var-123", blocks)
    vtt = svc.render_webvtt(pkg.cues)
    assert vtt.startswith("WEBVTT")
    assert "00:00:00.000 -->" in vtt
    assert "Lesson One" in vtt
    assert "introductory lesson" in vtt

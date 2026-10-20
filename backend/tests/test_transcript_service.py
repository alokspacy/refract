"""Unit tests for transcript parser service."""
from app.services.transcript_service import TranscriptService

SAMPLE_VTT = """WEBVTT

1
00:00:01.000 --> 00:00:03.500
<v Dr. Jane>Welcome to cell biology.

2
00:00:04.000 --> 00:00:07.000
Today we explore chloroplasts.
"""

def test_vtt_parser_structure():
    svc = TranscriptService()
    doc = svc.parse_vtt("vid_101", "Cell Biology Intro", SAMPLE_VTT)
    assert doc.total_cues == 2
    assert doc.cues[0].speaker_label == "Dr. Jane"
    assert "cell biology" in doc.cues[0].text
    assert doc.cues[1].start_sec == 4.0

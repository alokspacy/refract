"""Unit tests for multimodal reading pace estimation service."""
from app.services.reading_pace_service import ReadingPaceService
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_reading_pace_calculation():
    service = ReadingPaceService()
    text = " ".join(["word"] * 300)
    doc = ContentDocument(
        title="History",
        sections=[Section(title="Ch 1", blocks=[ContentBlock(id="b1", type=BlockType.PARAGRAPH, source_text=text)])]
    )
    res = service.estimate_pace(doc, wpm_visual=150)
    assert res.word_count == 300
    assert res.visual_reading_minutes == 2.0
    assert res.braille_tactile_minutes > res.visual_reading_minutes

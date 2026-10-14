"""Unit tests for translation service."""
from app.services.translation_service import TranslationService
from app.schemas.translation import LanguageCode
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_translation_preserves_blocks():
    svc = TranslationService()
    doc = ContentDocument(
        title="Photosynthesis Basics",
        sections=[
            Section(
                title="S1",
                blocks=[ContentBlock(type=BlockType.PARAGRAPH, source_text="Plants convert light into chemical energy.")]
            )
        ]
    )
    res = svc.translate_document(doc, LanguageCode.ES)
    assert len(res.blocks) == 1
    assert "energía química" in res.blocks[0].translated_text
    assert res.is_rtl is False

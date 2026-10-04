"""Unit tests for Braille service."""
from app.services.braille_service import BrailleService
from app.schemas.braille import BrailleGrade
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_grade_1_letter_mapping():
    svc = BrailleService()
    res = svc.to_braille_unicode("cab", grade=BrailleGrade.GRADE_1)
    assert res == "⠉⠁⠃"

def test_grade_2_contractions():
    svc = BrailleService()
    # 'the' is contracted to ⠮
    res = svc.to_braille_unicode("the cat", grade=BrailleGrade.GRADE_2)
    assert "⠮" in res

def test_document_braille_translation():
    svc = BrailleService()
    doc = ContentDocument(
        title="Braille Unit",
        sections=[
            Section(title="Intro", blocks=[ContentBlock(type=BlockType.PARAGRAPH, source_text="the book")])
        ]
    )
    rep = svc.translate_document(doc)
    assert rep.total_braille_cells > 0
    assert len(rep.blocks) == 1
    assert "BRAILLE EDITION" in rep.raw_brf_content

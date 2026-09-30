import pytest
from app.parsers.pptx import PPTXParser
from tests.fixtures.generator import create_sample_pptx


def test_pptx_parser_slides_titles_and_notes():
    pptx_bytes = create_sample_pptx()
    parser = PPTXParser()
    assert parser.can_parse("application/vnd.openxmlformats-officedocument.presentationml.presentation", "astro.pptx") is True

    doc = parser.parse(pptx_bytes, "astro.pptx")
    assert doc.pages_or_slides_count == 2
    assert len(doc.sections) == 2

    # Slide 1 Check
    slide1_blocks = doc.sections[0].blocks
    assert any(b.page_or_slide == 1 for b in slide1_blocks)

    # Slide 2 Check (Title, List, Speaker notes)
    slide2_blocks = doc.sections[1].blocks
    assert any(b.page_or_slide == 2 for b in slide2_blocks)
    assert any("Stellar" in str(b.text) or "Stars" in str(b.text) for b in slide2_blocks)
    
    # Speaker Notes Check
    notes_block = next((b for b in slide2_blocks if b.metadata.get("is_speaker_notes")), None)
    assert notes_block is not None
    assert "hydrostatic equilibrium" in notes_block.text


def test_pptx_parser_corrupted_file_handling():
    parser = PPTXParser()
    with pytest.raises(ValueError) as exc:
        parser.parse(b"Corrupted pptx bytes", "fake.pptx")
    assert "Corrupted or invalid PPTX" in str(exc.value)

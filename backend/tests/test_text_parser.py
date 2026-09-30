import pytest
from app.parsers.text import TextParser
from tests.fixtures.generator import create_sample_txt


def test_text_parser_paragraphs_headings_and_lists():
    txt_bytes = create_sample_txt()
    parser = TextParser()
    assert parser.can_parse("text/plain", "notes.txt") is True

    doc = parser.parse(txt_bytes, "notes.txt")
    assert doc.title == "Introduction to Ecology"
    assert len(doc.sections) == 1

    blocks = doc.sections[0].blocks
    assert len(blocks) >= 3
    assert any(b.type == "heading" for b in blocks)
    assert any(b.type == "paragraph" for b in blocks)
    assert any(b.type == "list" for b in blocks)


def test_text_parser_latin1_encoding():
    latin_text = "Chapitre 1: Écosystème et Biodiversité\n\nLes forêts tropicales possèdent une grande variété d'espèces."
    latin_bytes = latin_text.encode("latin-1")
    parser = TextParser()
    doc = parser.parse(latin_bytes, "french_bio.txt")
    assert len(doc.sections[0].blocks) > 0
    assert "Écosystème" in doc.sections[0].blocks[0].text or "Écosystème" in doc.title

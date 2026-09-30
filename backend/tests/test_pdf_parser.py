import pytest
from app.parsers.pdf import PDFParser
from tests.fixtures.generator import create_sample_pdf, create_scanned_pdf


def test_pdf_parser_born_digital_extraction():
    pdf_bytes = create_sample_pdf()
    parser = PDFParser()
    assert parser.can_parse("application/pdf", "biology.pdf") is True

    doc = parser.parse(pdf_bytes, "biology.pdf")
    assert doc.title is not None
    assert doc.pages_or_slides_count == 2
    assert len(doc.sections) == 2
    assert doc.requires_ocr is False

    # Verify Page 1
    page1_blocks = doc.sections[0].blocks
    assert any(b.type == "heading" for b in page1_blocks)
    assert any(b.type == "paragraph" for b in page1_blocks)
    assert any(b.type == "list" for b in page1_blocks)

    # Verify Page 2
    page2_blocks = doc.sections[1].blocks
    assert len(page2_blocks) > 0
    assert any(b.page_or_slide == 2 for b in page2_blocks)


def test_pdf_parser_scanned_page_ocr_detection():
    scanned_bytes = create_scanned_pdf()
    parser = PDFParser()
    doc = parser.parse(scanned_bytes, "scanned_doc.pdf")

    assert doc.requires_ocr is True
    assert 1 in doc.ocr_pages
    assert len(doc.warnings) > 0
    assert "OCR fallback" in doc.warnings[0]


def test_pdf_parser_corrupted_file_handling():
    corrupted_bytes = b"%PDF-1.4\nCorrupted binary garbage that cannot be read as pdf"
    parser = PDFParser()
    with pytest.raises(ValueError) as exc_info:
        parser.parse(corrupted_bytes, "corrupted.pdf")
    assert "Corrupted or unreadable PDF" in str(exc_info.value)

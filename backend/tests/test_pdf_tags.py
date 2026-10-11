"""Unit tests for PDF/UA tag verification."""
from app.pipeline.pdf_tags import PdfTagValidator

def test_pdf_ua_validation():
    valid = PdfTagValidator.validate_tags([
        {"type": "StructTreeRoot"},
        {"tag": "H1", "title": "Main Title"},
        {"tag": "P", "content": "Sample paragraph"}
    ])
    assert valid["valid_pdf_ua"] is True
    assert len(valid["issues"]) == 0

def test_missing_struct_root():
    invalid = PdfTagValidator.validate_tags([
        {"tag": "P", "content": "Untagged text"}
    ])
    assert invalid["valid_pdf_ua"] is False

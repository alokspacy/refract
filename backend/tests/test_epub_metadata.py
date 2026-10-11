"""Unit tests for EPUB3 accessibility metadata generator."""
from app.services.epub_metadata import generate_epub_package_opf

def test_epub_opf_contains_accessibility_properties():
    opf = generate_epub_package_opf("Biology 101", "book-123", ["sec_0", "sec_1"])
    assert "Biology 101" in opf
    assert "schema:accessibilityHazard" in opf
    assert "structuralNavigation" in opf
    assert 'version="3.0"' in opf

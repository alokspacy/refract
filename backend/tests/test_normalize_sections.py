"""Unit tests for content normalizer."""
from app.pipeline.normalize import ContentNormalizer

def test_normalize_strips_empty_sections():
    norm = ContentNormalizer()
    doc = norm.normalize("Test Unit", [{"title": None, "blocks": []}])
    assert len(doc.sections) == 1
    assert doc.title == "Test Unit"

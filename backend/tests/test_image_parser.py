import pytest
from app.parsers.image import ImageParser
from tests.fixtures.generator import create_sample_image


def test_image_parser_png_metadata_and_ocr_flag():
    img_bytes = create_sample_image()
    parser = ImageParser()
    assert parser.can_parse("image/png", "diagram.png") is True

    doc = parser.parse(img_bytes, "diagram.png")
    assert doc.pages_or_slides_count == 1
    assert len(doc.assets) == 1
    assert doc.assets[0].mime_type == "image/png"
    assert doc.requires_ocr is True
    assert doc.ocr_pages == [1]

    # Verify image block
    assert len(doc.sections) == 1
    assert len(doc.sections[0].blocks) == 1
    img_block = doc.sections[0].blocks[0]
    assert img_block.type == "image"
    assert img_block.asset_id == doc.assets[0].asset_id
    assert img_block.metadata["width"] == 500
    assert img_block.metadata["height"] == 300


def test_image_parser_corrupted_file():
    parser = ImageParser()
    with pytest.raises(ValueError) as exc:
        parser.parse(b"Corrupted image non-png data", "bad.png")
    assert "Corrupted or invalid image" in str(exc.value)

import pytest
from pydantic import ValidationError
from app.schemas.content import BlockType, ContentBlock, ContentDocument, Section


def test_valid_content_document_schema():
    block1 = ContentBlock(
        type=BlockType.HEADING,
        source_text="Introduction to Photosynthesis",
        page_or_slide=1,
        metadata={"level": 1},
        accessibility_annotations={"heading_level": 1}
    )
    block2 = ContentBlock(
        type=BlockType.PARAGRAPH,
        source_text="Photosynthesis is the process by which green plants transform light energy into chemical energy.",
        page_or_slide=1
    )
    section = Section(
        title="Chapter 1",
        blocks=[block1, block2]
    )
    doc = ContentDocument(
        title="Biology Chapter 1 - Photosynthesis",
        subject="Science",
        grade_hint="9th Grade",
        learning_objectives=["Understand light reaction", "Understand Calvin cycle"],
        glossary={"chlorophyll": "Green photosynthetic pigment"},
        sections=[section]
    )

    assert doc.schema_version == "1.0.0"
    assert doc.title == "Biology Chapter 1 - Photosynthesis"
    assert len(doc.sections) == 1
    assert len(doc.sections[0].blocks) == 2
    assert doc.sections[0].blocks[0].type == BlockType.HEADING


def test_invalid_block_type_raises_validation_error():
    with pytest.raises(ValidationError):
        ContentBlock(
            type="invalid_custom_block_type",  # Not in BlockType enum
            source_text="Invalid text"
        )

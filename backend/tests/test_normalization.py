import pytest
from app.parsers.base import ExtractedBlock, ExtractedDocument, ExtractedSection
from app.pipeline.normalize import Normalizer, normalize_document
from app.schemas.content import BlockType, ContentDocument


def test_normalizer_converts_extracted_doc_to_content_doc():
    ext_doc = ExtractedDocument(
        title="Physics Lesson 1",
        source_language="en",
        sections=[
            ExtractedSection(
                title="Mechanics",
                blocks=[
                    ExtractedBlock(
                        type="heading",
                        text="Newton's Laws",
                        page_or_slide=1,
                        position=1,
                        bbox=[10.0, 20.0, 200.0, 50.0],
                        metadata={"heading_level": 1}
                    ),
                    ExtractedBlock(
                        type="paragraph",
                        text="An object at rest stays at rest unless acted upon by an external net force.",
                        page_or_slide=1,
                        position=2,
                        bbox=[10.0, 60.0, 500.0, 100.0]
                    )
                ]
            )
        ]
    )

    content_doc = normalize_document(ext_doc, document_id="doc_123")
    assert isinstance(content_doc, ContentDocument)
    assert content_doc.id == "doc_123"
    assert content_doc.schema_version == "1.0.0"
    assert content_doc.title == "Physics Lesson 1"
    assert len(content_doc.sections) == 1
    assert len(content_doc.sections[0].blocks) == 2

    # Check Block 1
    b1 = content_doc.sections[0].blocks[0]
    assert b1.type == BlockType.HEADING
    assert b1.source_text == "Newton's Laws"
    assert b1.page_or_slide == 1
    assert b1.metadata["bbox"] == [10.0, 20.0, 200.0, 50.0]
    assert b1.metadata["order"] == 1

    # Check Block 2
    b2 = content_doc.sections[0].blocks[1]
    assert b2.type == BlockType.PARAGRAPH
    assert "object at rest" in b2.source_text
    assert b2.page_or_slide == 1


def test_normalizer_handles_empty_sections_gracefully():
    empty_doc = ExtractedDocument(title="Empty Document", sections=[])
    content_doc = normalize_document(empty_doc)
    assert len(content_doc.sections) == 1
    assert content_doc.sections[0].blocks == []

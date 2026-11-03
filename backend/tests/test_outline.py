"""Unit tests for heading outline extraction service."""
from app.services.outline_service import OutlineService
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_extract_outline():
    service = OutlineService()
    doc = ContentDocument(
        title="Sample Book",
        sections=[
            Section(
                title="Chapter 1",
                blocks=[
                    ContentBlock(id="h1", type=BlockType.HEADING, source_text="Introduction", metadata={"level": 1}),
                    ContentBlock(id="p1", type=BlockType.PARAGRAPH, source_text="Welcome to the book."),
                    ContentBlock(id="h2", type=BlockType.HEADING, source_text="Overview", metadata={"level": 2})
                ]
            )
        ]
    )
    outline = service.extract_outline(doc)
    assert outline.total_headings == 2
    assert outline.headings[0].title == "Introduction"
    assert outline.headings[0].level == 1
    assert outline.headings[1].title == "Overview"
    assert outline.headings[1].level == 2

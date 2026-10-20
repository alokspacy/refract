"""Unit tests for document cloning service."""
from app.services.clone_service import DocumentCloneService
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_clone_generates_fresh_uuids():
    doc = ContentDocument(
        title="Original Material",
        sections=[
            Section(title="Sec 1", blocks=[ContentBlock(type=BlockType.PARAGRAPH, source_text="Sample line")])
        ]
    )
    cloned, res = DocumentCloneService.clone_document(doc, "Cloned Material")
    assert cloned.id != doc.id
    assert cloned.title == "Cloned Material"
    assert cloned.sections[0].blocks[0].id != doc.sections[0].blocks[0].id
    assert res.total_blocks_copied == 1

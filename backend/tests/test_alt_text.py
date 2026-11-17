"""Unit tests for image alt-text audit and generation service."""
from app.services.alt_text_service import AltTextService
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_alt_text_audit():
    service = AltTextService()
    doc = ContentDocument(
        title="Botany",
        sections=[
            Section(
                title="Leaf Structure",
                blocks=[
                    ContentBlock(id="img1", type=BlockType.IMAGE, source_text=""),
                    ContentBlock(id="img2", type=BlockType.IMAGE, alt_text="Chloroplast cross section")
                ]
            )
        ]
    )
    report = service.audit_and_generate(doc)
    assert report.total_images == 2
    assert report.missing_alt_count == 1
    assert "Leaf Structure" in report.items[0].short_alt
    assert report.items[1].short_alt == "Chloroplast cross section"

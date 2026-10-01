"""Unit tests for HTML export."""
from app.services.html_export_service import HtmlExportService
from app.schemas.content import ContentDocument, ContentBlock, Section, BlockType

def test_html_export_renders_content():
    svc = HtmlExportService()
    doc = ContentDocument(
        title="Physics 101",
        sections=[
            Section(title="Kinematics", blocks=[ContentBlock(type=BlockType.PARAGRAPH, source_text="Velocity equals distance over time.")])
        ]
    )
    rendered = svc.render_document(doc)
    assert "Physics 101" in rendered
    assert "Kinematics" in rendered
    assert "Velocity equals distance" in rendered

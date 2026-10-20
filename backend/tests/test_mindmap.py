"""Unit tests for mindmap service."""
from app.services.mindmap_service import MindMapService
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_mindmap_tree_hierarchy():
    svc = MindMapService()
    doc = ContentDocument(
        title="Cell Biology",
        sections=[
            Section(
                title="Organelles",
                blocks=[ContentBlock(type=BlockType.HEADING, source_text="Mitochondria")]
            )
        ]
    )
    tree = svc.build_mindmap(doc)
    assert tree.label == "Cell Biology"
    assert len(tree.children) == 1
    assert tree.children[0].label == "Organelles"
    assert tree.children[0].children[0].label == "Mitochondria"

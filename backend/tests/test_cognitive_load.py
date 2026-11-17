"""Unit tests for cognitive load analyzer service."""
from app.services.cognitive_load_service import CognitiveLoadService
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_cognitive_load_estimation():
    service = CognitiveLoadService()
    long_paragraph = " ".join(["concept"] * 150)
    doc = ContentDocument(
        title="Quantum Mechanics",
        sections=[
            Section(
                title="Wavefunctions",
                blocks=[ContentBlock(id="b1", type=BlockType.PARAGRAPH, source_text=long_paragraph)]
            )
        ]
    )
    res = service.analyze_load(doc)
    assert res.extraneous_load_score > 50.0
    assert len(res.bottlenecks) >= 1

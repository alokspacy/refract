"""Unit tests for text chunking service."""
from app.services.chunking_service import ChunkingService
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_document_chunking():
    svc = ChunkingService()
    doc = ContentDocument(
        title="Physics Principles",
        sections=[
            Section(
                title="Mechanics",
                blocks=[ContentBlock(type=BlockType.PARAGRAPH, source_text="Forces cause acceleration proportional to mass.")]
            )
        ]
    )
    res = svc.chunk_document(doc, max_words=50)
    assert res.total_chunks == 1
    assert "Forces cause acceleration" in res.chunks[0].content

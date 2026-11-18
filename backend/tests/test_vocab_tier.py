"""Unit tests for three-tier vocabulary classification service."""
from app.services.vocab_tier_service import VocabTierService
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_vocab_tier_classification():
    service = VocabTierService()
    doc = ContentDocument(
        title="Genetics",
        glossary={"Chromosome": "DNA structure"},
        sections=[
            Section(
                title="Intro",
                blocks=[ContentBlock(id="b1", type=BlockType.PARAGRAPH, source_text="A chromosome contains hereditary information.")]
            )
        ]
    )
    rep = service.analyze_document_tiers(doc)
    assert rep.tier_3_count == 1
    assert rep.tier_2_count >= 2

"""Tests for reading assessment service."""
from app.services.assessment_service import AssessmentService
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_assessment_simple_text():
    service = AssessmentService()
    text = "The cat sat on the mat. It was a sunny day. The dog ran fast."
    res = service.evaluate_text(text)
    assert res.metrics.word_count > 0
    assert res.metrics.sentence_count == 3
    assert res.lexile.score >= 200
    assert res.lexile.difficulty_band == "Beginner"

def test_assessment_complex_text():
    service = AssessmentService()
    text = "Photosynthesis encompasses multifaceted photochemical syntheses characterized by intracellular chlorophyll configurations."
    res = service.evaluate_text(text)
    assert res.metrics.complex_word_percentage > 10
    assert len(res.recommendations) > 0

def test_assessment_document():
    service = AssessmentService()
    doc = ContentDocument(
        title="Cellular Biology",
        sections=[
            Section(
                title="Introduction",
                blocks=[
                    ContentBlock(id="b1", type=BlockType.PARAGRAPH, source_text="Cells are the basic unit of all living organisms.")
                ]
            )
        ]
    )
    res = service.evaluate_document(doc)
    assert res.document_id == doc.id
    assert res.metrics.word_count > 5

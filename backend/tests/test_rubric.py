"""Unit tests for UDL comprehension rubric evaluation service."""
from app.services.rubric_service import RubricService
from app.schemas.content import ContentDocument, Section

def test_rubric_evaluation_exemplary():
    service = RubricService()
    doc = ContentDocument(
        title="Ecology",
        learning_objectives=["Understand food webs"],
        glossary={"Producer": "Autotrophic organism"},
        sections=[Section(title="Part 1"), Section(title="Part 2")]
    )
    report = service.evaluate_document(doc)
    assert report.overall_score >= 3.8
    assert report.mastery_level == "Exemplary"

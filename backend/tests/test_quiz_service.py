"""Unit tests for quiz generation service."""
from app.services.quiz_service import QuizService
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_quiz_generation_from_content():
    svc = QuizService()
    doc = ContentDocument(
        title="Genetics Intro",
        sections=[
            Section(
                title="DNA",
                blocks=[
                    ContentBlock(type=BlockType.PARAGRAPH, source_text="DNA carries genetic instructions for all living organisms.")
                ]
            )
        ]
    )
    quiz = svc.generate_quiz(doc)
    assert len(quiz.questions) >= 1
    assert any(q.options[0].is_correct for q in quiz.questions)
    assert "DNA" in quiz.questions[0].prompt or "DNA" in quiz.questions[0].options[0].text

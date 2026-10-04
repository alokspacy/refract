"""Automated comprehension check and quiz generator."""
import uuid
from typing import List
from app.schemas.quiz import ComprehensionQuiz, QuizQuestion, QuizOption, QuestionType
from app.schemas.content import ContentDocument, BlockType

class QuizService:
    """Generates accessible, low-cognitive-load self-check questions from lesson blocks."""

    def generate_quiz(self, doc: ContentDocument) -> ComprehensionQuiz:
        questions: List[QuizQuestion] = []
        qid = 1

        for sec in doc.sections:
            for b in sec.blocks:
                txt = b.source_text or ""
                if b.type == BlockType.PARAGRAPH and len(txt.split()) > 8:
                    words = txt.split()
                    key_concept = words[0] if words else "This topic"

                    questions.append(QuizQuestion(
                        id=f"q_{qid}",
                        block_id=b.id,
                        question_type=QuestionType.MULTIPLE_CHOICE,
                        prompt=f"What is the main idea discussed in: '{txt[:70]}...'?",
                        options=[
                            QuizOption(
                                id="opt_a",
                                text=f"It explains the core role of {key_concept.lower()}.",
                                is_correct=True,
                                explanation="Correct! This directly matches the primary concept."
                            ),
                            QuizOption(
                                id="opt_b",
                                text="It describes an unrelated historical date.",
                                is_correct=False,
                                explanation="Incorrect; review the highlighted paragraph above."
                            ),
                            QuizOption(
                                id="opt_c",
                                text="It disproves the lesson's main thesis.",
                                is_correct=False,
                                explanation="Incorrect; this paragraph supports the foundational lesson."
                            )
                        ],
                        hint="Reread the first sentence carefully."
                    ))
                    qid += 1
                    if len(questions) >= 4:
                        break
            if len(questions) >= 4:
                break

        if not questions:
            questions.append(QuizQuestion(
                id="q_1",
                question_type=QuestionType.TRUE_FALSE,
                prompt=f"True or False: {doc.title} is designed for accessible study.",
                options=[
                    QuizOption(id="t", text="True", is_correct=True, explanation="Correct!"),
                    QuizOption(id="f", text="False", is_correct=False, explanation="Incorrect.")
                ],
                hint="Recall the course title."
            ))

        return ComprehensionQuiz(
            id=str(uuid.uuid4())[:8],
            document_id=doc.id,
            title=f"{doc.title} — Comprehension Self-Check",
            questions=questions
        )

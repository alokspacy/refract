"""Schemas for cognitive comprehension self-checks."""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    CLOZE = "cloze"

class QuizOption(BaseModel):
    id: str
    text: str
    is_correct: bool
    explanation: str

class QuizQuestion(BaseModel):
    id: str
    block_id: Optional[str] = None
    question_type: QuestionType
    prompt: str
    options: List[QuizOption] = Field(default_factory=list)
    hint: Optional[str] = None

class ComprehensionQuiz(BaseModel):
    id: str
    document_id: str
    title: str
    questions: List[QuizQuestion] = Field(default_factory=list)

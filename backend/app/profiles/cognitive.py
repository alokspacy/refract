from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel, Field
from app.profiles.base import BaseProfile
from app.prompts.cognitive import (
    COGNITIVE_PROMPT_VERSION,
    COGNITIVE_SYSTEM_PROMPT,
    COGNITIVE_USER_TEMPLATE
)


class CognitiveTerm(BaseModel):
    term: str
    definition: str


class ComprehensionQuestion(BaseModel):
    question: str
    answer_hint: str


class CognitiveBlockOutput(BaseModel):
    source_block_id: str
    concept_title: str = Field(..., description="Single focus concept title")
    step_by_step: List[str] = Field(default_factory=list, description="Sequential numbered process breakdown")
    explanation: str = Field(..., description="Scaffolded, direct explanation")
    example: Optional[str] = Field(None, description="Intuitive real-world analogy or scenario")
    key_terms: List[CognitiveTerm] = Field(default_factory=list, description="Vocabulary reinforcement")
    recap: str = Field(..., description="1-2 sentence core takeaway")
    comprehension_questions: List[ComprehensionQuestion] = Field(default_factory=list, description="Self-check questions")


class CognitiveProfile(BaseProfile):
    profile_id = "cognitive"
    name = "Cognitive / Learning Accessibility"
    description = "Reduces cognitive load with one concept per chunk, step-by-step breakdown, intuitive examples, quick recaps, and comprehension check questions."
    version = "1.0.0"
    prompt_version = COGNITIVE_PROMPT_VERSION

    @property
    def output_schema(self) -> Type[BaseModel]:
        return CognitiveBlockOutput

    @property
    def system_prompt(self) -> str:
        return COGNITIVE_SYSTEM_PROMPT

    def build_user_prompt(
        self,
        source_block_id: str,
        source_text: str,
        block_type: str,
        document_title: str,
        subject: Optional[str] = None,
        grade_hint: Optional[str] = None,
        learning_objectives: Optional[List[str]] = None
    ) -> str:
        return COGNITIVE_USER_TEMPLATE.format(
            source_block_id=source_block_id,
            block_type=block_type,
            source_text=source_text,
            document_title=document_title or "Educational Lesson",
            subject=subject or "General Education",
            grade_hint=grade_hint or "Standard"
        )

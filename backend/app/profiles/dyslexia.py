from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel, Field
from app.profiles.base import BaseProfile
from app.prompts.dyslexia import (
    DYSLEXIA_PROMPT_VERSION,
    DYSLEXIA_SYSTEM_PROMPT,
    DYSLEXIA_USER_TEMPLATE
)


class TermDefinition(BaseModel):
    term: str = Field(..., description="Academic term preserved in context")
    definition: str = Field(..., description="Plain language explanation")


class DyslexiaBlockOutput(BaseModel):
    source_block_id: str
    title: str = Field(..., description="Clear section/chunk title")
    simplified_text: str = Field(..., description="Plain-language text with short sentence structures")
    key_points: List[str] = Field(default_factory=list, description="Bulleted key takeaways")
    important_terms: List[TermDefinition] = Field(default_factory=list, description="Preserved and defined academic terminology")
    example: Optional[str] = Field(None, description="Concrete supporting example where helpful")
    omitted_information: List[str] = Field(default_factory=list, description="Non-essential or repetitive text omitted")
    changed_information: List[str] = Field(default_factory=list, description="Sentence structure or phrasing changes made")


class DyslexiaProfile(BaseProfile):
    profile_id = "dyslexia"
    name = "Dyslexia / Reading Difficulty"
    description = "Transforms complex text into plain language with short sentences, clear chunking, bulleted key points, and terminology definitions."
    version = "1.0.0"
    prompt_version = DYSLEXIA_PROMPT_VERSION

    @property
    def output_schema(self) -> Type[BaseModel]:
        return DyslexiaBlockOutput

    @property
    def system_prompt(self) -> str:
        return DYSLEXIA_SYSTEM_PROMPT

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
        return DYSLEXIA_USER_TEMPLATE.format(
            source_block_id=source_block_id,
            block_type=block_type,
            source_text=source_text,
            document_title=document_title or "Educational Lesson",
            subject=subject or "General Education",
            grade_hint=grade_hint or "Standard"
        )

from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel, Field
from app.profiles.base import BaseProfile
from app.prompts.visual import (
    VISUAL_PROMPT_VERSION,
    VISUAL_SYSTEM_PROMPT,
    VISUAL_USER_TEMPLATE
)


class VisualBlockOutput(BaseModel):
    source_block_id: str
    semantic_type: str = Field("paragraph", description="heading, paragraph, list, table, or image")
    heading_level: Optional[int] = Field(None, description="Heading level 1-6 if heading")
    formatted_text: str = Field(..., description="Cleanly formatted text")
    items: List[str] = Field(default_factory=list, description="List items if list")
    requires_description: bool = Field(False, description="Flag for images requiring vision descriptions in Phase 4")


class VisualBasicProfile(BaseProfile):
    profile_id = "visual_basic"
    name = "Basic Visual Accessibility"
    description = "Provides clean semantic structuring, logical heading hierarchies, formatted lists, and responsive layouts."
    version = "1.0.0"
    prompt_version = VISUAL_PROMPT_VERSION

    @property
    def output_schema(self) -> Type[BaseModel]:
        return VisualBlockOutput

    @property
    def system_prompt(self) -> str:
        return VISUAL_SYSTEM_PROMPT

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
        return VISUAL_USER_TEMPLATE.format(
            source_block_id=source_block_id,
            block_type=block_type,
            source_text=source_text
        )

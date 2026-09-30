from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel


class BaseProfile(ABC):
    """
    Abstract definition of an Accessibility Profile.
    Contains transformation guidelines, prompt fragments, output schema, and validation rules.
    """

    profile_id: str
    name: str
    description: str
    version: str = "1.0.0"
    prompt_version: str = "1.0.0"

    @property
    @abstractmethod
    def output_schema(self) -> Type[BaseModel]:
        """The Pydantic schema required for generated blocks in this profile."""
        pass

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """The system instructions for the LLM transformation."""
        pass

    @abstractmethod
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
        """Construct the prompt sent to the LLM."""
        pass

    def validate_content(self, content: Dict[str, Any]) -> BaseModel:
        """Validate raw dictionary against this profile's output schema."""
        return self.output_schema.model_validate(content)

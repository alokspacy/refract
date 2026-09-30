import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel
from app.core.config import settings

logger = logging.getLogger("accesslearn.llm")


@dataclass
class LLMResponse:
    content_json: Dict[str, Any]
    raw_text: str
    usage: Dict[str, Any] = field(default_factory=lambda: {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "estimated_cost_usd": 0.0
    })
    model: str = "mock-model"
    provider: str = "mock"


class LLMProvider(ABC):
    """Abstract interface for LLM provider implementations (OpenAI, Anthropic, Mock)."""

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Optional[Type[BaseModel]] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_retries: int = 1
    ) -> LLMResponse:
        """
        Generate structured JSON from the model adhering to response_schema.
        """
        pass


def get_llm_provider() -> LLMProvider:
    """Factory creating LLM provider based on environment configuration."""
    provider_name = getattr(settings, "LLM_PROVIDER", "mock").lower()
    if provider_name == "openai":
        from app.providers.openai_llm import OpenAILLMProvider
        return OpenAILLMProvider()
    
    from app.providers.mock_llm import MockLLMProvider
    return MockLLMProvider()

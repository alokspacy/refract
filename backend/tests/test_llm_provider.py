import pytest
from pydantic import BaseModel, Field
from app.providers.mock_llm import MockLLMProvider
from app.providers.llm import get_llm_provider


class SampleOutputSchema(BaseModel):
    summary: str = Field(...)
    key_points: list[str] = Field(default_factory=list)


def test_mock_llm_provider_generation():
    provider = MockLLMProvider()
    response = provider.generate(
        system_prompt="You are an educational assistant.",
        user_prompt="Analyze the following normalized educational document: [Block ID: blk_1] (paragraph): Photosynthesis is how plants make energy.",
        model="mock-gpt-4o"
    )

    assert response is not None
    assert response.provider == "mock"
    assert "subject" in response.content_json
    assert response.content_json["subject"] == "Biology"
    assert len(response.content_json["learning_objectives"]) > 0
    assert response.usage["total_tokens"] > 0
    assert response.usage["estimated_cost_usd"] >= 0.0


def test_mock_llm_transient_retry_handling():
    provider = MockLLMProvider()
    provider.force_malformed_json_once = True

    # First attempt returns invalid json
    bad_resp = provider.generate(
        system_prompt="System",
        user_prompt="User"
    )
    assert bad_resp.raw_text == "INVALID_JSON_OUTPUT_<<<>>>"
    assert bad_resp.content_json == {}

    # Next attempt succeeds
    good_resp = provider.generate(
        system_prompt="System",
        user_prompt="DYSLEXIA: Photosynthesis"
    )
    assert "simplified_text" in good_resp.content_json


def test_get_llm_provider_factory():
    provider = get_llm_provider()
    assert provider is not None
    assert isinstance(provider, MockLLMProvider)

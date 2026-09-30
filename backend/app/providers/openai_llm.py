import json
import logging
import httpx
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel
from app.providers.llm import LLMProvider, LLMResponse
from app.core.config import settings

logger = logging.getLogger("accesslearn.openai_llm")


class OpenAILLMProvider(LLMProvider):
    """
    OpenAI and OpenAI-compatible LLM Provider using direct structured outputs / JSON mode.
    """

    def __init__(self):
        self.api_key = getattr(settings, "OPENAI_API_KEY", "") or ""
        self.api_base = getattr(settings, "OPENAI_API_BASE", "https://api.openai.com/v1") or "https://api.openai.com/v1"
        self.default_model = getattr(settings, "OPENAI_MODEL", "gpt-4o") or "gpt-4o"

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Optional[Type[BaseModel]] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_retries: int = 1
    ) -> LLMResponse:
        model_name = model or self.default_model
        
        if not self.api_key:
            logger.warning("OPENAI_API_KEY is not set. Falling back to MockLLMProvider behavior.")
            from app.providers.mock_llm import MockLLMProvider
            return MockLLMProvider().generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_schema=response_schema,
                model=model_name,
                temperature=temperature
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "response_format": {"type": "json_object"}
        }

        last_error = None
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"Calling OpenAI API (model={model_name}, attempt={attempt + 1})")
                with httpx.Client(timeout=60.0) as client:
                    resp = client.post(
                        f"{self.api_base.rstrip('/')}/chat/completions",
                        headers=headers,
                        json=payload
                    )
                    resp.raise_for_status()
                    data = resp.json()

                raw_text = data["choices"][0]["message"]["content"]
                content_json = json.loads(raw_text)
                
                # Optional validation against response_schema if provided
                if response_schema is not None:
                    _ = response_schema.model_validate(content_json)

                usage_data = data.get("usage", {})
                prompt_tokens = usage_data.get("prompt_tokens", 0)
                completion_tokens = usage_data.get("completion_tokens", 0)
                total_tokens = usage_data.get("total_tokens", prompt_tokens + completion_tokens)
                
                # Estimate cost for GPT-4o approx ($5/1M input, $15/1M output)
                cost = (prompt_tokens * 0.000005) + (completion_tokens * 0.000015)

                return LLMResponse(
                    content_json=content_json,
                    raw_text=raw_text,
                    usage={
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens,
                        "estimated_cost_usd": round(cost, 6)
                    },
                    model=model_name,
                    provider="openai"
                )

            except Exception as err:
                last_error = err
                logger.warning(f"OpenAI API call failed on attempt {attempt + 1}: {err}")
                if attempt < max_retries:
                    continue

        raise RuntimeError(f"OpenAI API failed after {max_retries + 1} attempts: {last_error}")

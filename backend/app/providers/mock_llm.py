import json
import re
import logging
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel
from app.providers.llm import LLMProvider, LLMResponse

logger = logging.getLogger("accesslearn.mock_llm")


class MockLLMProvider(LLMProvider):
    """
    Deterministic, offline Mock LLM Provider for development and automated testing.
    Outputs realistic structured JSON obeying target Pydantic schemas.
    """

    def __init__(self):
        self.force_malformed_json_once: bool = False
        self.force_failure_count: int = 0
        self.call_count: int = 0

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Optional[Type[BaseModel]] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_retries: int = 1
    ) -> LLMResponse:
        self.call_count += 1
        model_name = model or "mock-gpt-4o"
        logger.info(f"MockLLM generate called (call_count={self.call_count}, model={model_name})")

        # Simulate transient error for retry testing if requested
        if self.force_malformed_json_once:
            self.force_malformed_json_once = False
            logger.warning("Simulating transient malformed JSON from Mock LLM")
            return LLMResponse(
                content_json={},
                raw_text="INVALID_JSON_OUTPUT_<<<>>>",
                usage={"prompt_tokens": 50, "completion_tokens": 10, "total_tokens": 60, "estimated_cost_usd": 0.0001},
                model=model_name,
                provider="mock"
            )

        # 1. Content Analysis Operation
        if "Analyze the following normalized educational document" in user_prompt or "EXTRACT AND RETURN THE FOLLOWING JSON SCHEMA" in user_prompt:
            content_json = self._mock_analysis(user_prompt)
        
        # 2. Dyslexia Transformation
        elif "Dyslexia-friendly representation" in user_prompt or "DYSLEXIA" in system_prompt.upper() or "DYSLEXIA" in user_prompt.upper():
            content_json = self._mock_dyslexia(user_prompt)
            
        # 3. Cognitive Transformation
        elif "Cognitive-accessible representation" in user_prompt or "COGNITIVE" in system_prompt.upper() or "COGNITIVE" in user_prompt.upper():
            content_json = self._mock_cognitive(user_prompt)
            
        # 4. Basic Visual Structuring
        elif "Basic Visual Accessibility" in system_prompt or "visual semantic accessibility" in user_prompt or "VISUAL" in user_prompt.upper():
            content_json = self._mock_visual(user_prompt)
            
        # 5. Grounding Verifier
        elif "Source Grounding Verifier" in system_prompt or "Verify the grounding" in user_prompt:
            content_json = self._mock_grounding(user_prompt)
            
        else:
            # Generic structured response
            content_json = {
                "status": "success",
                "message": "Generic mock response",
                "summary": user_prompt[:100]
            }

        raw_text = json.dumps(content_json, indent=2)
        
        # Calculate simulated token usage
        prompt_tokens = len(system_prompt.split()) + len(user_prompt.split())
        completion_tokens = len(raw_text.split())
        total_tokens = prompt_tokens + completion_tokens
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
            provider="mock"
        )

    def _mock_analysis(self, prompt: str) -> Dict[str, Any]:
        """Generate realistic educational metadata based on keywords in document text."""
        # Isolate document title and blocks content to avoid matching prompt template example words
        doc_match = re.search(r"DOCUMENT TITLE:(.*?)(?=EXTRACT AND RETURN|$)", prompt, re.DOTALL | re.IGNORECASE)
        text_to_search = (doc_match.group(1).lower() if doc_match else prompt[:300].lower())

        subject = "Biology"
        if any(w in text_to_search for w in ["physics", "velocity", "force", "gravity"]):
            subject = "Physics"
        elif any(w in text_to_search for w in ["math", "equation", "algebra", "calculus"]):
            subject = "Mathematics"
        elif any(w in text_to_search for w in ["history", "war", "revolution", "century"]):
            subject = "History"
        elif any(w in text_to_search for w in ["computer", "code", "python", "algorithm"]):
            subject = "Computer Science"
        elif any(w in text_to_search for w in ["ecology", "ecosystem", "environment"]):
            subject = "Ecology"
        elif any(w in text_to_search for w in ["biology", "photosynthesis", "cell", "chlorophyll", "organism"]):
            subject = "Biology"

        # Check for block ID references in prompt
        block_ids = re.findall(r"\[Block ID:\s*([a-zA-Z0-9_-]+)\]", prompt) or ["blk_001"]

        return {
            "language": "en",
            "subject": subject,
            "grade_hint": "9-10",
            "complexity": "intermediate",
            "learning_objectives": [
                {
                    "id": "lo_1",
                    "text": f"Understand the primary scientific principles of {subject}.",
                    "inferred": False
                },
                {
                    "id": "lo_2",
                    "text": f"Analyze cellular processes and chemical reactions in {subject}.",
                    "inferred": True
                }
            ],
            "concepts": [
                {
                    "id": "concept_1",
                    "name": "Cellular Energetics" if subject == "Biology" else "Fundamental Laws",
                    "description": "The biological mechanisms by which living systems capture and transform energy.",
                    "source_block_ids": block_ids[:2]
                },
                {
                    "id": "concept_2",
                    "name": "Light Reactions",
                    "description": "Process producing ATP and NADPH in thylakoid membranes.",
                    "source_block_ids": [block_ids[0]] if block_ids else ["blk_001"]
                }
            ],
            "vocabulary": [
                {
                    "term": "Chlorophyll" if subject == "Biology" else "Kinetic Energy",
                    "definition": "The green pigment in plants that absorbs light energy for photosynthesis.",
                    "example": "Leaves appear green because chlorophyll reflects green wavelengths of light.",
                    "source_block_ids": [block_ids[0]] if block_ids else ["blk_001"]
                },
                {
                    "term": "Thylakoid",
                    "definition": "Membrane-bound compartments inside chloroplasts where light reactions occur.",
                    "example": "Light-dependent reactions occur across the thylakoid membrane.",
                    "source_block_ids": block_ids[:1]
                }
            ]
        }

    def _mock_dyslexia(self, prompt: str) -> Dict[str, Any]:
        """Generate plain language, short sentences, and highlighted vocabulary."""
        block_id_match = re.search(r"Block ID:\s*([a-zA-Z0-9_-]+)", prompt)
        block_id = block_id_match.group(1) if block_id_match else "blk_001"
        
        # Extract source text excerpt
        text_match = re.search(r"Text:\s*\n(.*?)(?=\nOUTPUT STRICT JSON|$)", prompt, re.DOTALL)
        source_text = text_match.group(1).strip() if text_match else "Photosynthesis is the essential biological mechanism converting light energy into chemical sugars."

        # Retain any numbers found in source text
        numbers = re.findall(r"\b\d+(?:\.\d+)?(?:%|°C|m/s|kg)?\b", source_text)

        simplified = "Photosynthesis is how green plants make food. They use sunlight to create chemical energy."
        if numbers:
            simplified += f" Essential values noted: {', '.join(numbers)}."

        return {
            "source_block_id": block_id,
            "title": "How Plants Make Energy",
            "simplified_text": simplified,
            "key_points": [
                "Plants use sunlight, water, and air to produce food.",
                "This process happens inside special plant cell parts called chloroplasts.",
                "Oxygen is released into the atmosphere as a helpful byproduct."
            ],
            "important_terms": [
                {
                    "term": "Photosynthesis",
                    "definition": "The natural process where plants make sugar from sunlight."
                },
                {
                    "term": "Chloroplast",
                    "definition": "The tiny part of a plant cell that catches sunlight."
                }
            ],
            "example": "Think of chloroplasts like solar panels on a house that catch sunlight and turn it into electricity.",
            "omitted_information": ["Complex multi-clause chemical formulas omitted for clarity."],
            "changed_information": ["Long passive sentences restructured into direct active sentences."]
        }

    def _mock_cognitive(self, prompt: str) -> Dict[str, Any]:
        """Generate structured step-by-step scaffolds and comprehension questions."""
        block_id_match = re.search(r"Block ID:\s*([a-zA-Z0-9_-]+)", prompt)
        block_id = block_id_match.group(1) if block_id_match else "blk_001"

        return {
            "source_block_id": block_id,
            "concept_title": "Energy Conversion in Plant Cells",
            "step_by_step": [
                "Step 1: Chlorophyll absorbs solar light energy inside the chloroplast.",
                "Step 2: Water molecules are split to generate energetic electrons and oxygen.",
                "Step 3: Carbon dioxide is fixed to create glucose sugar for growth."
            ],
            "explanation": "Plants cannot eat food like animals do. Instead, they act as self-sufficient producers by manufacturing carbohydrates directly from solar photons and water.",
            "example": "A greenhouse garden where light and water produce sweet fruits.",
            "key_terms": [
                {
                    "term": "Chlorophyll",
                    "definition": "Light-absorbing pigment."
                },
                {
                    "term": "Glucose",
                    "definition": "Sugar used as fuel."
                }
            ],
            "recap": "Photosynthesis converts sunlight into stored chemical glucose energy, releasing oxygen.",
            "comprehension_questions": [
                {
                    "question": "Where does the light absorption step take place inside plant cells?",
                    "answer_hint": "In the chloroplasts containing green chlorophyll."
                },
                {
                    "question": "What gas is released during photosynthesis that humans and animals breathe?",
                    "answer_hint": "Oxygen (O2)."
                }
            ]
        }

    def _mock_visual(self, prompt: str) -> Dict[str, Any]:
        """Generate structured visual formatting."""
        block_id_match = re.search(r"Block ID:\s*([a-zA-Z0-9_-]+)", prompt)
        block_id = block_id_match.group(1) if block_id_match else "blk_001"

        return {
            "source_block_id": block_id,
            "semantic_type": "paragraph",
            "heading_level": 2,
            "formatted_text": "Photosynthesis is the fundamental cellular reaction supporting planetary life.",
            "items": [],
            "requires_description": False
        }

    def _mock_grounding(self, prompt: str) -> Dict[str, Any]:
        """Verify factual grounding."""
        return {
            "grounded": True,
            "unsupported_claims": [],
            "warnings": []
        }

"""Schemas for plain language text simplification."""
from typing import List, Dict
from pydantic import BaseModel, Field

class JargonReplacement(BaseModel):
    original_term: str
    plain_alternative: str
    context_note: str

class PlainLanguageResponse(BaseModel):
    source_text: str
    simplified_text: str
    replacements_made: List[JargonReplacement] = Field(default_factory=list)
    reading_ease_improvement: float = 0.0

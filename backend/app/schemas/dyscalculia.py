"""Schemas for dyscalculia-accessible mathematical adaptations."""
from typing import List, Optional
from pydantic import BaseModel, Field

class NumberRepresentation(BaseModel):
    raw_number: str
    formatted_chunked: str
    spelled_out_words: str
    visual_dots_count: Optional[int] = None

class DyscalculiaBlockAdaptation(BaseModel):
    block_id: str
    source_text: str
    adapted_text: str
    numbers_detected: List[NumberRepresentation] = Field(default_factory=list)

"""Schemas for STEM equations and spoken math accessibility."""
from typing import Optional
from pydantic import BaseModel, Field

class MathAccessibleExpression(BaseModel):
    latex_source: str
    mathml: str
    spoken_clearspeak: str = Field(..., description="Human-like spoken English representation for screen readers")
    nemeth_braille: Optional[str] = Field(None, description="Nemeth Code Braille representation")
    complexity_level: str = "algebra"

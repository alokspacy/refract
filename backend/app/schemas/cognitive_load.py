"""Schemas for estimating intrinsic and extraneous cognitive load in lessons."""
from typing import List
from pydantic import BaseModel, Field

class CognitiveLoadEstimate(BaseModel):
    document_id: str
    intrinsic_load_score: float = Field(..., ge=0.0, le=100.0)
    extraneous_load_score: float = Field(..., ge=0.0, le=100.0)
    overall_load_band: str
    bottlenecks: List[str] = Field(default_factory=list)

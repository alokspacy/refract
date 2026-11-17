"""Schemas for accessible learning comprehension rubric evaluations."""
from typing import List
from pydantic import BaseModel, Field

class RubricCriterion(BaseModel):
    criterion_id: str
    title: str
    weight: float = Field(default=0.25, ge=0.0, le=1.0)
    score: int = Field(..., ge=1, le=4)
    feedback: str

class ComprehensionRubricReport(BaseModel):
    document_id: str
    overall_score: float
    mastery_level: str
    criteria: List[RubricCriterion]

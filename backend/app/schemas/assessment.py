"""Schemas for reading level assessment and readability scoring."""
from typing import List, Optional
from pydantic import BaseModel, Field

class LexileEstimate(BaseModel):
    score: int = Field(..., description="Estimated Lexile measure (e.g. 750L)")
    grade_equivalent: str = Field(..., description="US grade equivalent range, e.g. '4th-5th Grade'")
    difficulty_band: str = Field(..., description="Complexity band: Beginner, Intermediate, Advanced")

class AssessmentMetrics(BaseModel):
    word_count: int
    sentence_count: int
    syllable_count: int
    flesch_kincaid_grade: float
    gunning_fog_index: float
    average_sentence_length: float
    complex_word_percentage: float

class ReadingAssessmentResponse(BaseModel):
    document_id: Optional[str] = None
    lexile: LexileEstimate
    metrics: AssessmentMetrics
    recommendations: List[str] = Field(default_factory=list)

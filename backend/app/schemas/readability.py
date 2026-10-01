"""Schemas for readability and text complexity metrics."""
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.enums import ReadabilityGradeBand, CEFRLevel

class TextStatistics(BaseModel):
    character_count: int
    word_count: int
    sentence_count: int
    paragraph_count: int
    complex_word_count: int
    avg_words_per_sentence: float
    avg_syllables_per_word: float

class ReadabilityScores(BaseModel):
    flesch_reading_ease: float = Field(..., description="0-100 score; 90+ very easy, <30 very difficult")
    flesch_kincaid_grade: float = Field(..., description="US grade level equivalent")
    gunning_fog_index: float = Field(..., description="Years of formal education required")
    smog_index: float = Field(..., description="Simple Measure of Gobbledygook index")
    automated_readability_index: float

class ReadabilityReport(BaseModel):
    text_sample_preview: str
    statistics: TextStatistics
    scores: ReadabilityScores
    grade_band: ReadabilityGradeBand
    cefr_level: CEFRLevel
    cognitive_difficulty_label: str
    recommendations: List[str] = Field(default_factory=list)

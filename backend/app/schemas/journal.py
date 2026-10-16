"""Schemas for learner reflection and metacognitive journal entries."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ReflectionEntry(BaseModel):
    id: str
    document_id: str
    student_id: str
    takeaway_summary: str
    questions_remaining: Optional[str] = None
    confidence_rating: int = Field(..., ge=1, le=5)

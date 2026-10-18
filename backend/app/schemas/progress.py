"""Schemas for tracking learner reading progress and completion."""
from pydantic import BaseModel, Field

class ReadingProgressRecord(BaseModel):
    document_id: str
    user_id: str
    last_block_id: str
    percent_completed: float = Field(..., ge=0.0, le=100.0)
    reading_time_seconds: int = 0

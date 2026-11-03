"""Schemas for cognitive focus sessions and Pomodoro intervals."""
from typing import Optional
from pydantic import BaseModel, Field

class FocusSessionConfig(BaseModel):
    work_duration_minutes: int = Field(default=25, ge=5, le=60)
    short_break_minutes: int = Field(default=5, ge=1, le=15)
    long_break_minutes: int = Field(default=15, ge=5, le=30)
    intervals_before_long_break: int = Field(default=4, ge=2, le=8)
    chime_enabled: bool = True
    ambient_soundtrack: Optional[str] = None

class FocusSessionSummary(BaseModel):
    session_id: str
    total_focus_minutes: int
    completed_intervals: int
    breaks_taken: int
    distraction_flags: int = 0

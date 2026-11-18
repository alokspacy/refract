"""Schemas for non-speech auditory cues (earcons) supporting blind navigation."""
from typing import List
from pydantic import BaseModel, Field

class EarconCue(BaseModel):
    event_type: str
    frequency_hz: int = Field(..., ge=120, le=2000)
    duration_ms: int = Field(default=120, ge=30, le=1000)
    waveform: str = "sine"
    description: str

class EarconPalette(BaseModel):
    palette_name: str
    cues: List[EarconCue]

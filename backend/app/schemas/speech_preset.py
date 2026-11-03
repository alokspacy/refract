"""Schemas for voice synthesis speed, pitch, and prosody presets."""
from typing import Optional
from pydantic import BaseModel, Field

class SpeechPreset(BaseModel):
    preset_id: str
    name: str
    rate: float = Field(default=1.0, ge=0.5, le=3.0)
    pitch: float = Field(default=1.0, ge=0.5, le=2.0)
    volume: float = Field(default=1.0, ge=0.0, le=1.0)
    pause_between_sentences_ms: int = Field(default=400, ge=100, le=2000)
    highlight_active_word: bool = True
    voice_name: Optional[str] = None

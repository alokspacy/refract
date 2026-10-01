"""Schemas for audio narration and accessibility captions."""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class VoicePreset(str, Enum):
    CALM_STUDENT = "calm_student"
    EXPRESSIVE_TEACHER = "expressive_teacher"
    SLOW_DYSLEXIA = "slow_dyslexia"
    SCREEN_READER = "screen_reader"

class SubtitleCue(BaseModel):
    id: int
    start_ms: int
    end_ms: int
    text: str
    block_id: Optional[str] = None
    timestamp_vtt: str

class AudioNarrationPackage(BaseModel):
    variant_id: str
    track_id: str
    voice_preset: VoicePreset
    speaking_rate: float
    total_duration_sec: float
    cues_count: int
    audio_stream_url: str
    vtt_url: str
    cues: List[SubtitleCue] = Field(default_factory=list)

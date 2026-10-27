"""Schemas for speech-to-text recognition requests and transcription tokens."""
from typing import List, Optional
from pydantic import BaseModel, Field

class TranscriptionToken(BaseModel):
    word: str
    start_sec: float
    end_sec: float
    confidence: float = 1.0

class SpeechTranscriptionResult(BaseModel):
    job_id: str
    duration_sec: float
    language: str = "en"
    full_text: str
    tokens: List[TranscriptionToken] = Field(default_factory=list)

class STTJobRequest(BaseModel):
    audio_url: Optional[str] = None
    language_code: Optional[str] = "en"
    align_timestamps: bool = True

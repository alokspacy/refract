"""Schemas for accessible audio/video transcripts and speaker diarization."""
from typing import List, Optional
from pydantic import BaseModel, Field

class TranscriptCue(BaseModel):
    cue_id: int
    start_sec: float
    end_sec: float
    speaker_label: Optional[str] = None
    text: str

class MediaTranscriptDocument(BaseModel):
    media_id: str
    title: str
    language: str = "en"
    duration_seconds: float
    total_cues: int
    cues: List[TranscriptCue] = Field(default_factory=list)

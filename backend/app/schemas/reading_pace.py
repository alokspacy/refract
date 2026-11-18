"""Schemas for estimating reading duration across assistive modalities."""
from pydantic import BaseModel

class ReadingPaceEstimate(BaseModel):
    document_id: str
    word_count: int
    visual_reading_minutes: float
    tts_audio_minutes: float
    braille_tactile_minutes: float

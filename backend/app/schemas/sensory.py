"""Schemas for user sensory preferences and neurodiversity accommodations."""
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class MotionTolerance(str, Enum):
    NORMAL = "normal"
    REDUCED = "reduced"
    NONE = "none"

class ContrastPreference(str, Enum):
    STANDARD = "standard"
    HIGH = "high"
    INVERTED = "inverted"

class SensoryProfile(BaseModel):
    user_id: Optional[str] = None
    motion: MotionTolerance = MotionTolerance.NORMAL
    contrast: ContrastPreference = ContrastPreference.STANDARD
    autoplay_media: bool = False
    flash_suppression: bool = True
    audio_compression: bool = True
    volume_level_normalization: bool = True

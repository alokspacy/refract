"""Schemas for learner energy and sensory check-ins."""
from enum import Enum
from pydantic import BaseModel, Field

class EnergyLevel(str, Enum):
    HIGH_FOCUS = "high_focus"
    STEADY = "steady"
    OVERWHELMED = "overwhelmed"
    TIRED = "tired"

class LearnerCheckin(BaseModel):
    user_id: str
    energy_level: EnergyLevel
    recommended_profile: str
    recommended_reading_time_minutes: int

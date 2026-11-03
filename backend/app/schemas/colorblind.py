"""Schemas for color vision deficiency (CVD) simulation matrix and settings."""
from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class DeficiencyType(str, Enum):
    PROTANOPIA = "protanopia"       # Red-blind
    PROTANOMALY = "protanomaly"     # Red-weak
    DEUTERANOPIA = "deuteranopia"   # Green-blind
    DEUTERANOMALY = "deuteranomaly" # Green-weak
    TRITANOPIA = "tritanopia"       # Blue-blind
    TRITANOMALY = "tritanomaly"     # Blue-weak
    ACHROMATOPSIA = "achromatopsia" # Complete color blindness (monochrome)

class ColorMatrix(BaseModel):
    deficiency: DeficiencyType
    matrix: List[List[float]] = Field(..., description="3x3 color transformation matrix")
    svg_filter_id: str
    description: str

class SimulationRequest(BaseModel):
    deficiency: DeficiencyType
    severity: float = Field(default=1.0, ge=0.0, le=1.0)

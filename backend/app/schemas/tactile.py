"""Schemas for tactile graphic descriptions and blind accessibility."""
from typing import List, Optional
from pydantic import BaseModel, Field

class TactileLayer(BaseModel):
    layer_name: str
    raised_element_type: str  # outline, textured_fill, braille_label, axis
    description: str
    braille_legend: Optional[str] = None

class TactileGraphicDescription(BaseModel):
    asset_id: str
    title: str
    visual_overview: str
    tactile_exploration_guide: str
    orientation: str = "portrait"
    layers: List[TactileLayer] = Field(default_factory=list)
    key_findings: List[str] = Field(default_factory=list)

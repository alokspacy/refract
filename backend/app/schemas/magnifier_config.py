"""Schemas for low-vision screen magnifier lens geometry and color inversion."""
from pydantic import BaseModel, Field

class MagnifierLensConfig(BaseModel):
    zoom_factor: float = Field(default=2.0, ge=1.2, le=8.0)
    lens_width_px: int = Field(default=280, ge=120, le=600)
    lens_height_px: int = Field(default=160, ge=80, le=400)
    shape: str = "rounded-rectangle"
    invert_colors: bool = False
    smooth_panning: bool = True

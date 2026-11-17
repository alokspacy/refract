"""Schemas for FCC / WCAG compliant closed caption styling and WebVTT generation."""
from pydantic import BaseModel, Field

class CaptionStylePreferences(BaseModel):
    font_size_pct: int = Field(default=100, ge=50, le=200)
    background_color: str = "#000000"
    background_opacity: float = Field(default=0.8, ge=0.0, le=1.0)
    text_color: str = "#FFFFFF"
    edge_style: str = "drop-shadow"
    window_color: str = "transparent"

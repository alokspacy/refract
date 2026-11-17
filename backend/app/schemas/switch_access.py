"""Schemas for single-switch and dual-switch assistive scanning navigation."""
from pydantic import BaseModel, Field

class SwitchScanSettings(BaseModel):
    scan_interval_ms: int = Field(default=1200, ge=300, le=5000)
    cycles_before_pause: int = Field(default=3, ge=1, le=10)
    auto_restart: bool = True
    audio_beep_on_step: bool = False
    highlight_thickness_px: int = Field(default=4, ge=2, le=12)

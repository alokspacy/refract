"""Schemas for assistive eye-gaze tracking and dwell-click activation."""
from typing import List
from pydantic import BaseModel, Field

class CalibrationPoint(BaseModel):
    x_pct: float = Field(..., ge=0.0, le=100.0)
    y_pct: float = Field(..., ge=0.0, le=100.0)
    accuracy_ms: int = Field(default=120, ge=10, le=2000)

class GazeDwellConfig(BaseModel):
    dwell_time_ms: int = Field(default=800, ge=300, le=3000)
    smoothing_window: int = Field(default=5, ge=1, le=20)
    snap_radius_px: int = Field(default=44, ge=16, le=120)
    calibration_points: List[CalibrationPoint] = Field(default_factory=list)

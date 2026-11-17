"""Unit tests for eye-gaze dwell activation calculation service."""
from app.services.gaze_service import GazeService
from app.schemas.gaze import GazeDwellConfig

def test_gaze_dwell_trigger():
    service = GazeService()
    cfg = GazeDwellConfig(dwell_time_ms=800, snap_radius_px=50)
    res = service.check_target_hit(105, 105, 100, 100, duration_ms=900, config=cfg)
    assert res["within_radius"] is True
    assert res["dwell_triggered"] is True
    assert res["progress_pct"] == 100.0

def test_gaze_outside_radius():
    service = GazeService()
    cfg = GazeDwellConfig(dwell_time_ms=800, snap_radius_px=30)
    res = service.check_target_hit(200, 200, 100, 100, duration_ms=1000, config=cfg)
    assert res["within_radius"] is False
    assert res["dwell_triggered"] is False

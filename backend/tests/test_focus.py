"""Unit tests for executive function focus session service."""
from app.services.focus_service import FocusSessionService
from app.schemas.focus import FocusSessionConfig

def test_create_focus_session():
    service = FocusSessionService()
    cfg = FocusSessionConfig(work_duration_minutes=25)
    sess = service.create_session(cfg)
    assert sess["session_id"] is not None
    assert sess["target_duration_sec"] == 1500

def test_compute_focus_summary():
    service = FocusSessionService()
    summary = service.compute_summary("test-123", intervals_completed=4, work_mins=25)
    assert summary.total_focus_minutes == 100
    assert summary.completed_intervals == 4
    assert summary.breaks_taken == 3

"""Unit tests for task decomposition service."""
from app.services.breakdown_service import TaskBreakdownService

def test_breakdown_steps():
    svc = TaskBreakdownService()
    res = svc.break_down_assignment("Read chapter 4 on cellular division.")
    assert len(res.steps) == 4
    assert res.total_estimated_minutes == 30
    assert res.steps[0].step_number == 1
    assert "chapter 4" in res.original_objective

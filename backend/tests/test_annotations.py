"""Unit tests for educator annotation service."""
from unittest.mock import MagicMock
from app.services.annotation_service import AnnotationService
from app.schemas.annotation import AnnotationCreate

def test_annotation_summary_calculation():
    svc = AnnotationService()
    db = MagicMock()
    # Mocking query return
    m1 = MagicMock(status="approved")
    m2 = MagicMock(status="flagged")
    db.query.return_value.filter.return_value.all.return_value = [m1, m2]

    summary = svc.get_summary(db, "var-test", total_blocks=4)
    assert summary.total_blocks == 4
    assert summary.approved_blocks == 1
    assert summary.flagged_blocks == 1
    assert summary.pending_blocks == 2
    assert summary.approval_rate == 25.0
    assert summary.is_ready_for_publish is False

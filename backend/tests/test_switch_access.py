"""Unit tests for switch access scanning service."""
from app.services.switch_access_service import SwitchAccessService
from app.schemas.switch_access import SwitchScanSettings

def test_switch_cycle_metrics():
    service = SwitchAccessService()
    cfg = SwitchScanSettings(scan_interval_ms=1000, cycles_before_pause=2)
    res = service.compute_cycle_metrics(element_count=15, settings=cfg)
    assert res["single_pass_seconds"] == 15.0
    assert res["full_loop_seconds"] == 30.0
    assert res["recommended_mode"] == "group_row_scan"

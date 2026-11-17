"""Service computing scan cycle durations for motor-impaired switch navigation."""
from app.schemas.switch_access import SwitchScanSettings

class SwitchAccessService:
    def compute_cycle_metrics(self, element_count: int, settings: SwitchScanSettings) -> dict:
        safe_count = max(1, element_count)
        single_pass_sec = round((safe_count * settings.scan_interval_ms) / 1000.0, 2)
        total_loop_sec = round(single_pass_sec * settings.cycles_before_pause, 2)
        return {
            "focusable_elements": safe_count,
            "single_pass_seconds": single_pass_sec,
            "full_loop_seconds": total_loop_sec,
            "recommended_mode": "group_row_scan" if safe_count > 12 else "linear_scan"
        }

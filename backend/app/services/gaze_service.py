"""Service calculating assistive eye-tracking dwell thresholds and target snapping."""
import math
from app.schemas.gaze import GazeDwellConfig

class GazeService:
    def check_target_hit(
        self,
        gaze_x: float,
        gaze_y: float,
        target_x: float,
        target_y: float,
        duration_ms: int,
        config: GazeDwellConfig
    ) -> dict:
        distance = math.hypot(gaze_x - target_x, gaze_y - target_y)
        within_radius = distance <= config.snap_radius_px
        triggered = within_radius and (duration_ms >= config.dwell_time_ms)
        progress_pct = min(100.0, round((duration_ms / max(1, config.dwell_time_ms)) * 100.0, 1)) if within_radius else 0.0

        return {
            "within_radius": within_radius,
            "distance_px": round(distance, 2),
            "progress_pct": progress_pct,
            "dwell_triggered": triggered
        }

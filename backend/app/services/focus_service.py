"""Service managing focus intervals and pacing for ADHD / neurodivergent learners."""
import uuid
from app.schemas.focus import FocusSessionConfig, FocusSessionSummary

class FocusSessionService:
    def create_session(self, config: FocusSessionConfig) -> dict:
        session_id = str(uuid.uuid4())[:8]
        return {
            "session_id": session_id,
            "status": "ready",
            "current_interval": 1,
            "config": config.model_dump(),
            "target_duration_sec": max(60, config.work_duration_minutes * 60)
        }

    def compute_summary(self, session_id: str, intervals_completed: int, work_mins: int) -> FocusSessionSummary:
        safe_intervals = max(0, intervals_completed)
        safe_mins = max(1, work_mins)
        return FocusSessionSummary(
            session_id=session_id,
            total_focus_minutes=safe_intervals * safe_mins,
            completed_intervals=safe_intervals,
            breaks_taken=max(0, safe_intervals - 1),
            distraction_flags=0
        )

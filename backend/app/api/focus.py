"""FastAPI router for cognitive focus sessions."""
from fastapi import APIRouter
from app.schemas.focus import FocusSessionConfig, FocusSessionSummary
from app.services.focus_service import FocusSessionService

router = APIRouter(prefix="/focus", tags=["Focus & Executive Function"])
service = FocusSessionService()

@router.post("/sessions")
def create_session(config: FocusSessionConfig):
    """Create a structured executive function focus interval session."""
    return service.create_session(config)

@router.post("/sessions/{session_id}/complete", response_model=FocusSessionSummary)
def complete_session(session_id: str, intervals_completed: int = 1, work_minutes: int = 25):
    """Log completed study interval and calculate cognitive pace statistics."""
    return service.compute_summary(session_id, intervals_completed, work_minutes)

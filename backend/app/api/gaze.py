"""FastAPI router for assistive eye-gaze dwell calculations."""
from fastapi import APIRouter
from app.schemas.gaze import GazeDwellConfig
from app.services.gaze_service import GazeService

router = APIRouter(prefix="/gaze", tags=["Eye Gaze Assistive Control"])
service = GazeService()

@router.post("/evaluate-dwell")
def evaluate_gaze_dwell(
    gaze_x: float,
    gaze_y: float,
    target_x: float,
    target_y: float,
    duration_ms: int,
    config: GazeDwellConfig
):
    """Evaluate whether user gaze coordinates satisfy dwell-click activation."""
    return service.check_target_hit(gaze_x, gaze_y, target_x, target_y, duration_ms, config)

"""FastAPI router for low-vision screen magnifier calculations."""
from fastapi import APIRouter
from app.schemas.magnifier_config import MagnifierLensConfig
from app.services.magnifier_service import MagnifierService

router = APIRouter(prefix="/magnifier", tags=["Low-Vision Magnifier"])
service = MagnifierService()

@router.post("/viewport")
def compute_magnifier_viewport(cursor_x: int, cursor_y: int, config: MagnifierLensConfig):
    """Calculate lens bounding box and CSS transform parameters."""
    return service.compute_viewport_bounds(cursor_x, cursor_y, config)

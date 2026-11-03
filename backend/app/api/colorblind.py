"""FastAPI router for color blindness simulation filters."""
from fastapi import APIRouter
from app.schemas.colorblind import DeficiencyType, ColorMatrix
from app.services.colorblind_service import ColorBlindService

router = APIRouter(prefix="/colorblind", tags=["Color Vision Deficiency"])
service = ColorBlindService()

@router.get("/matrix/{deficiency}", response_model=ColorMatrix)
def get_simulation_matrix(deficiency: DeficiencyType):
    """Retrieve color conversion matrix for specified CVD type."""
    return service.get_matrix(deficiency)

@router.get("/svg-filter/{deficiency}")
def get_svg_filter(deficiency: DeficiencyType):
    """Retrieve SVG feColorMatrix markup for real-time CSS filtering."""
    return {"filter_id": f"cvd-{deficiency.value}", "svg": service.generate_svg_filter(deficiency)}

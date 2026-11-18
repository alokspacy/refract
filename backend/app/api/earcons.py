"""FastAPI router for non-speech auditory earcon palettes."""
from fastapi import APIRouter
from app.schemas.earcons import EarconPalette
from app.services.earcons_service import EarconsService

router = APIRouter(prefix="/earcons", tags=["Auditory Earcon Cues"])
service = EarconsService()

@router.get("/palette", response_model=EarconPalette)
def get_earcon_palette():
    """Retrieve acoustic earcon synthesizer mappings for structural navigation."""
    return service.get_default_palette()

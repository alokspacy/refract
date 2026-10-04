"""FastAPI router for tactile graphics and blind accessibility."""
from fastapi import APIRouter
from app.schemas.tactile import TactileGraphicDescription
from app.services.tactile_service import TactileService

router = APIRouter(prefix="/tactile", tags=["Tactile Graphics"])
service = TactileService()

@router.get("/assets/{asset_id}", response_model=TactileGraphicDescription)
def get_tactile_description(asset_id: str, title: str = "Diagram"):
    """Get structured tactile description and exploration guide for an image asset."""
    return service.describe_image(asset_id, title, {})

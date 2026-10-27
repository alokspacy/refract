"""FastAPI router for sensory accommodations and hazard screening."""
from fastapi import APIRouter
from app.schemas.sensory import SensoryProfile
from app.schemas.content import ContentDocument
from app.services.sensory_service import SensoryService

router = APIRouter(prefix="/sensory", tags=["Sensory Accommodations"])
service = SensoryService()

@router.post("/inspect")
def inspect_sensory_hazards(doc: ContentDocument, profile: SensoryProfile):
    """Screen document for photosensitive flash hazards and recommend accommodations."""
    return service.inspect_content_hazards(doc, profile)

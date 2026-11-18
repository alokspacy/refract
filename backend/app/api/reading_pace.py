"""FastAPI router for multimodal reading duration estimates."""
from fastapi import APIRouter
from app.schemas.content import ContentDocument
from app.schemas.reading_pace import ReadingPaceEstimate
from app.services.reading_pace_service import ReadingPaceService

router = APIRouter(prefix="/reading-pace", tags=["Reading Pace Estimator"])
service = ReadingPaceService()

@router.post("/estimate", response_model=ReadingPaceEstimate)
def estimate_reading_duration(doc: ContentDocument, wpm_visual: int = 180):
    """Calculate expected completion time across visual, TTS, and Braille reading."""
    return service.estimate_pace(doc, wpm_visual=wpm_visual)

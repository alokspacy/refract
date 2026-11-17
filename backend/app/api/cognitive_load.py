"""FastAPI router for cognitive load analysis."""
from fastapi import APIRouter
from app.schemas.content import ContentDocument
from app.schemas.cognitive_load import CognitiveLoadEstimate
from app.services.cognitive_load_service import CognitiveLoadService

router = APIRouter(prefix="/cognitive-load", tags=["Cognitive Load Analysis"])
service = CognitiveLoadService()

@router.post("/analyze", response_model=CognitiveLoadEstimate)
def analyze_document_cognitive_load(doc: ContentDocument):
    """Estimate intrinsic and extraneous cognitive load for learning content."""
    return service.analyze_load(doc)

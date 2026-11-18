"""FastAPI router for AAC symbol board generation."""
from fastapi import APIRouter
from app.schemas.content import ContentDocument
from app.schemas.aac import AACCommunicationBoard
from app.services.aac_service import AACService

router = APIRouter(prefix="/aac", tags=["AAC Symbol Communication"])
service = AACService()

@router.post("/board", response_model=AACCommunicationBoard)
def create_aac_board(doc: ContentDocument, columns: int = 4):
    """Generate a core and fringe vocabulary AAC communication board for a lesson."""
    return service.generate_board(doc, columns=columns)

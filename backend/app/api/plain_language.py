"""FastAPI router for plain language text transformation."""
from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.plain_language import PlainLanguageResponse
from app.services.plain_language_service import PlainLanguageService

router = APIRouter(prefix="/plain-language", tags=["Plain Language Simplification"])
service = PlainLanguageService()

class TextPayload(BaseModel):
    text: str

@router.post("/simplify", response_model=PlainLanguageResponse)
def simplify_academic_text(payload: TextPayload):
    """Rewrite complex scholarly sentences into clear plain language."""
    return service.simplify_text(payload.text)

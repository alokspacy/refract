"""FastAPI router for phonetic pronunciation guides."""
from typing import List
from fastapi import APIRouter
from app.schemas.phonetics import PhoneticGuideResponse
from app.services.phonetics_service import PhoneticsService

router = APIRouter(prefix="/phonetics", tags=["Phonetic Pronunciation"])
service = PhoneticsService()

@router.post("/guide", response_model=PhoneticGuideResponse)
def build_phonetic_guide(terms: List[str]):
    """Generate syllable breakdowns and phonetic respellings for academic terms."""
    return service.generate_guide(terms)

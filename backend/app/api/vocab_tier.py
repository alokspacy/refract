"""FastAPI router for three-tier academic vocabulary analysis."""
from fastapi import APIRouter
from app.schemas.content import ContentDocument
from app.schemas.vocab_tier import VocabularyTierReport
from app.services.vocab_tier_service import VocabTierService

router = APIRouter(prefix="/vocab-tiers", tags=["Vocabulary Tiers"])
service = VocabTierService()

@router.post("/analyze", response_model=VocabularyTierReport)
def analyze_vocabulary_tiers(doc: ContentDocument):
    """Classify document vocabulary into Tier 1, Tier 2, and Tier 3 words."""
    return service.analyze_document_tiers(doc)

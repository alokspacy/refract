"""FastAPI router for UDL comprehension rubric evaluation."""
from fastapi import APIRouter
from app.schemas.content import ContentDocument
from app.schemas.rubric import ComprehensionRubricReport
from app.services.rubric_service import RubricService

router = APIRouter(prefix="/rubric", tags=["Comprehension Rubric"])
service = RubricService()

@router.post("/evaluate", response_model=ComprehensionRubricReport)
def evaluate_rubric(doc: ContentDocument):
    """Evaluate document scaffolding against UDL comprehension rubric."""
    return service.evaluate_document(doc)

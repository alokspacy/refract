"""FastAPI router for STEM math accessibility."""
from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.math_accessibility import MathAccessibleExpression
from app.services.math_service import MathService

router = APIRouter(prefix="/math", tags=["Math Accessibility"])
service = MathService()

class MathPayload(BaseModel):
    latex: str

@router.post("/translate", response_model=MathAccessibleExpression)
def translate_math_equation(payload: MathPayload):
    """Translate LaTeX formula into MathML and ClearSpeak spoken math."""
    return service.to_accessible_math(payload.latex)

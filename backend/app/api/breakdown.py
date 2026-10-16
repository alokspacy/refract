"""FastAPI router for cognitive task decomposition."""
from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.task_breakdown import TaskDecompositionResponse
from app.services.breakdown_service import TaskBreakdownService

router = APIRouter(prefix="/breakdown", tags=["Executive Function Breakdown"])
service = TaskBreakdownService()

class BreakdownRequest(BaseModel):
    assignment_prompt: str

@router.post("/", response_model=TaskDecompositionResponse)
def decompose_assignment(payload: BreakdownRequest):
    """Decompose an assignment into step-by-step checklist intervals."""
    return service.break_down_assignment(payload.assignment_prompt)

"""FastAPI router for accessible table linearization."""
from typing import List
from fastapi import APIRouter
from app.schemas.table_a11y import AccessibleTableSummary
from app.services.table_a11y_service import TableAccessibilityService

router = APIRouter(prefix="/table-a11y", tags=["Table Accessibility"])
service = TableAccessibilityService()

@router.post("/linearize", response_model=AccessibleTableSummary)
def linearize_data_table(block_id: str, caption: str, headers: List[str], rows: List[List[str]]):
    """Convert tabular rows into linearized narrative strings for screen readers."""
    return service.linearize_table(block_id, caption, headers, rows)

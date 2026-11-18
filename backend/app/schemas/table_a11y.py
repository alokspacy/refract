"""Schemas for linearizing complex data tables for screen readers."""
from typing import List
from pydantic import BaseModel

class LinearizedTableRow(BaseModel):
    row_index: int
    narrative_sentence: str

class AccessibleTableSummary(BaseModel):
    block_id: str
    caption: str
    headers: List[str]
    row_narratives: List[LinearizedTableRow]
    aria_summary: str

"""Schemas for cognitive task decomposition and executive function support."""
from typing import List, Optional
from pydantic import BaseModel, Field

class SubTaskStep(BaseModel):
    step_number: int
    title: str
    description: str
    estimated_minutes: int
    sensory_tip: Optional[str] = None
    is_completed: bool = False

class TaskDecompositionResponse(BaseModel):
    task_id: str
    original_objective: str
    total_estimated_minutes: int
    steps: List[SubTaskStep] = Field(default_factory=list)

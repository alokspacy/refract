"""Schemas for educator block review and approval."""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class AnnotationCreate(BaseModel):
    block_id: str
    status: str = Field(..., description="approved, flagged, or revised")
    comment: Optional[str] = None
    suggested_content: Optional[str] = None

class AnnotationResponse(BaseModel):
    id: str
    variant_id: str
    block_id: str
    educator_id: str
    status: str
    comment: Optional[str] = None
    suggested_content: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class VariantReviewSummary(BaseModel):
    variant_id: str
    total_blocks: int
    approved_blocks: int
    flagged_blocks: int
    pending_blocks: int
    approval_rate: float
    is_ready_for_publish: bool

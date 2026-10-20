"""Schemas for document cloning and adaptive branching."""
from typing import Optional, List
from pydantic import BaseModel, Field

class DocumentCloneRequest(BaseModel):
    new_title: Optional[str] = None
    target_profile_ids: List[str] = Field(default_factory=list)

class DocumentCloneResponse(BaseModel):
    original_document_id: str
    cloned_document_id: str
    cloned_title: str
    total_blocks_copied: int

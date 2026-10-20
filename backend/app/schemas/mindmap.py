"""Schemas for concept mind maps and visual hierarchy trees."""
from typing import List, Optional
from pydantic import BaseModel, Field

class MindMapNode(BaseModel):
    node_id: str
    label: str
    node_type: str = "concept"  # root, section, concept, vocabulary
    children: List['MindMapNode'] = Field(default_factory=list)
    memory_cue: Optional[str] = None

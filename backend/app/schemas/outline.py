"""Schemas for document heading outline hierarchy and jump targets."""
from typing import List, Optional
from pydantic import BaseModel

class HeadingEntry(BaseModel):
    block_id: str
    level: int
    title: str
    section_title: Optional[str] = None
    character_offset: Optional[int] = 0

class DocumentOutline(BaseModel):
    document_id: str
    title: str
    total_headings: int
    headings: List[HeadingEntry]

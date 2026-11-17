"""Schemas for accessible image alt-text and long descriptions."""
from typing import List, Optional
from pydantic import BaseModel, Field

class ImageDescriptionItem(BaseModel):
    block_id: str
    short_alt: str = Field(..., max_length=125, description="Concise screen reader alt text")
    long_description: Optional[str] = Field(None, description="Extended aria-describedby narrative")
    is_decorative: bool = False
    detected_labels: List[str] = Field(default_factory=list)

class DocumentAltTextReport(BaseModel):
    document_id: str
    total_images: int
    missing_alt_count: int
    items: List[ImageDescriptionItem]

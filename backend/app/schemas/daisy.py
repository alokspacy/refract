"""Schemas for DAISY digital talking book navigation manifests."""
from typing import List, Optional
from pydantic import BaseModel, Field

class DAISYNavPoint(BaseModel):
    id: str
    play_order: int
    heading_text: str
    content_src: str
    audio_clip_src: Optional[str] = None
    clip_begin: str = "00:00:00"
    clip_end: str = "00:01:00"

class DAISYManifestResponse(BaseModel):
    document_id: str
    title: str
    ncc_html: str = Field(..., description="Navigation Control Center (NCC) HTML markup")
    nav_points: List[DAISYNavPoint] = Field(default_factory=list)

"""FastAPI router for WebVTT closed caption generation."""
from typing import List, Dict
from fastapi import APIRouter, Response
from app.schemas.captions import CaptionStylePreferences
from app.services.captions_service import CaptionsService

router = APIRouter(prefix="/captions", tags=["Closed Captions"])
service = CaptionsService()

@router.post("/webvtt")
def export_webvtt(cues: List[Dict], style: CaptionStylePreferences = None):
    """Generate styled WebVTT caption track from timestamped cues."""
    vtt_data = service.build_webvtt(cues, style)
    return Response(content=vtt_data, media_type="text/vtt")

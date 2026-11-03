"""FastAPI router for speech rate and pitch playback presets."""
from typing import List
from fastapi import APIRouter
from app.schemas.speech_preset import SpeechPreset
from app.services.speech_preset_service import SpeechPresetService

router = APIRouter(prefix="/speech-presets", tags=["Speech Prosody Presets"])
service = SpeechPresetService()

@router.get("", response_model=List[SpeechPreset])
def list_presets():
    """List recommended audio synthesis pacing configurations."""
    return service.list_presets()

@router.get("/{preset_id}", response_model=SpeechPreset)
def get_preset(preset_id: str):
    """Retrieve speech playback preset by identifier."""
    return service.get_preset(preset_id)

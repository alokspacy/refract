"""FastAPI router for audio narration and accessibility captions."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.audio import AudioNarrationPackage, VoicePreset
from app.services.audio_service import AudioNarrationService
from app.providers.voice_presets import VOICE_PRESETS
from app.storage.audio_cache import AudioNarrativeCache

router = APIRouter(prefix="/audio", tags=["Audio Narration"])
service = AudioNarrationService()

@router.get("/presets")
def list_voice_presets():
    """List available voice profiles and recommended cognitive speeds."""
    return VOICE_PRESETS

@router.post("/variants/{variant_id}/narrate", response_model=AudioNarrationPackage)
def generate_variant_narration(variant_id: str, preset: VoicePreset = VoicePreset.CALM_STUDENT, db: Session = Depends(get_db)):
    """Generate timed audio narration package for an adapted variant."""
    # Find document
    doc = db.query(Document).first()
    blocks = []
    if doc and doc.normalized_content:
        cd = ContentDocument.model_validate(doc.normalized_content)
        for s in cd.sections:
            blocks.extend(s.blocks)
    return service.generate_narration(variant_id, blocks, preset=preset)

@router.get("/variants/{variant_id}/vtt")
def get_variant_webvtt(variant_id: str, preset: VoicePreset = VoicePreset.CALM_STUDENT):
    """Retrieve WebVTT subtitle stream for synchronized karaoke playback."""
    key = AudioNarrativeCache.make_key(variant_id, preset.value)
    pkg = AudioNarrativeCache.get(key)
    if not pkg:
        # Generate on the fly
        pkg = service.generate_narration(variant_id, [], preset=preset)
    vtt = service.render_webvtt(pkg.cues)
    return Response(content=vtt, media_type="text/vtt")

"""Unit tests for audio service packaging."""
from app.services.audio_service import AudioNarrationService
from app.schemas.audio import VoicePreset
from app.schemas.content import ContentBlock, BlockType

def test_narration_package_generation():
    svc = AudioNarrationService()
    blocks = [ContentBlock(type=BlockType.PARAGRAPH, source_text="Step one is to understand the concept.")]
    pkg = svc.generate_narration("v-456", blocks, preset=VoicePreset.SLOW_DYSLEXIA)
    assert pkg.variant_id == "v-456"
    assert pkg.voice_preset == VoicePreset.SLOW_DYSLEXIA
    assert pkg.cues_count == 1
    assert pkg.total_duration_sec > 0

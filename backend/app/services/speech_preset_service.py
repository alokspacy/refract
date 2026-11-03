"""Service storing and tailoring text-to-speech audio pacing presets."""
from typing import List
from app.schemas.speech_preset import SpeechPreset

DEFAULT_PRESETS: List[SpeechPreset] = [
    SpeechPreset(preset_id="relaxed", name="Relaxed Comprehension", rate=0.85, pitch=0.95, pause_between_sentences_ms=600),
    SpeechPreset(preset_id="standard", name="Standard Reading", rate=1.0, pitch=1.0, pause_between_sentences_ms=400),
    SpeechPreset(preset_id="fast", name="Speed Review", rate=1.5, pitch=1.05, pause_between_sentences_ms=250),
    SpeechPreset(preset_id="dyslexic", name="Dyslexia Paced", rate=0.8, pitch=1.0, pause_between_sentences_ms=800, highlight_active_word=True),
]

class SpeechPresetService:
    def list_presets(self) -> List[SpeechPreset]:
        return DEFAULT_PRESETS

    def get_preset(self, preset_id: str) -> SpeechPreset:
        for p in DEFAULT_PRESETS:
            if p.preset_id == preset_id:
                return p
        return DEFAULT_PRESETS[1]

"""Service mapping structural document transitions to non-speech earcon synth parameters."""
from app.schemas.earcons import EarconPalette, EarconCue

class EarconsService:
    def get_default_palette(self) -> EarconPalette:
        return EarconPalette(
            palette_name="Accessible Acoustic Landmarks",
            cues=[
                EarconCue(event_type="section_enter", frequency_hz=523, duration_ms=140, waveform="sine", description="Ascending chime when entering new section"),
                EarconCue(event_type="glossary_term", frequency_hz=659, duration_ms=90, waveform="triangle", description="Soft ping when encountering glossary term"),
                EarconCue(event_type="quiz_correct", frequency_hz=880, duration_ms=180, waveform="sine", description="Bright tone for correct answer"),
                EarconCue(event_type="boundary_alert", frequency_hz=220, duration_ms=150, waveform="sawtooth", description="Low tone at end of page"),
            ]
        )

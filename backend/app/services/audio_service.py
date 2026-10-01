"""Audio narration and WebVTT caption generator."""
import uuid
from typing import List
from app.schemas.audio import AudioNarrationPackage, SubtitleCue, VoicePreset
from app.schemas.content import ContentBlock
from app.providers.voice_presets import VOICE_PRESETS
from app.storage.audio_cache import AudioNarrativeCache

class AudioNarrationService:
    """Produces timed subtitle cues and synthesized speech metadata."""

    def generate_narration(self, variant_id: str, blocks: List[ContentBlock], preset: VoicePreset = VoicePreset.CALM_STUDENT) -> AudioNarrationPackage:
        cfg = VOICE_PRESETS.get(preset.value, VOICE_PRESETS["calm_student"])
        rate = cfg["speaking_rate"]
        pause_ms = cfg["pause_between_blocks_ms"]

        cues: List[SubtitleCue] = []
        current_time_ms = 0
        cue_id = 1

        for b in blocks:
            text = b.source_text or ""
            if not text.strip():
                continue

            words = text.split()
            # Average English word is ~280ms at 1.0x rate
            duration_ms = int((len(words) * 280) / rate)
            start_ms = current_time_ms
            end_ms = start_ms + duration_ms

            cues.append(SubtitleCue(
                id=cue_id,
                start_ms=start_ms,
                end_ms=end_ms,
                text=text,
                block_id=b.id,
                timestamp_vtt=f"{self._format_vtt_timestamp(start_ms)} --> {self._format_vtt_timestamp(end_ms)}"
            ))
            current_time_ms = end_ms + pause_ms
            cue_id += 1

        total_sec = round(current_time_ms / 1000.0, 2)
        pkg = AudioNarrationPackage(
            variant_id=variant_id,
            track_id=str(uuid.uuid4()),
            voice_preset=preset,
            speaking_rate=rate,
            total_duration_sec=total_sec,
            cues_count=len(cues),
            audio_stream_url=f"/api/audio/stream/{variant_id}?preset={preset.value}",
            vtt_url=f"/api/audio/{variant_id}/vtt?preset={preset.value}",
            cues=cues
        )
        cache_key = AudioNarrativeCache.make_key(variant_id, preset.value)
        AudioNarrativeCache.set(cache_key, pkg)
        return pkg

    def render_webvtt(self, cues: List[SubtitleCue]) -> str:
        lines = ["WEBVTT", ""]
        for c in cues:
            lines.append(str(c.id))
            lines.append(c.timestamp_vtt)
            lines.append(c.text)
            lines.append("")
        return "\n".join(lines)

    @staticmethod
    def _format_vtt_timestamp(ms: int) -> str:
        hours = ms // 3600000
        ms %= 3600000
        minutes = ms // 60000
        ms %= 60000
        seconds = ms // 1000
        millis = ms % 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"

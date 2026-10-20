"""Transcript parsing service supporting WebVTT and SRT."""
import re
from typing import List
from app.schemas.transcript import TranscriptCue, MediaTranscriptDocument

class TranscriptService:
    """Parses raw WebVTT and SRT subtitles into structured accessible cues."""

    def parse_vtt(self, media_id: str, title: str, vtt_text: str) -> MediaTranscriptDocument:
        cues: List[TranscriptCue] = []
        blocks = re.split(r'\n\s*\n', vtt_text.strip())

        cue_idx = 1
        max_time = 0.0

        for b in blocks:
            lines = [l.strip() for l in b.splitlines() if l.strip()]
            if not lines or lines[0].startswith("WEBVTT"):
                continue

            time_line_idx = 0
            if re.match(r'^\d+$', lines[0]):
                time_line_idx = 1

            if len(lines) <= time_line_idx:
                continue

            time_match = re.search(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})', lines[time_line_idx])
            if not time_match:
                continue

            start_sec = self._parse_timestamp(time_match.group(1))
            end_sec = self._parse_timestamp(time_match.group(2))
            max_time = max(max_time, end_sec)

            text_content = " ".join(lines[time_line_idx + 1:])
            speaker = None
            speaker_match = re.match(r'<v\s+([^>]+)>(.*)', text_content)
            if speaker_match:
                speaker = speaker_match.group(1)
                text_content = speaker_match.group(2)

            cues.append(TranscriptCue(
                cue_id=cue_idx,
                start_sec=start_sec,
                end_sec=end_sec,
                speaker_label=speaker,
                text=text_content
            ))
            cue_idx += 1

        return MediaTranscriptDocument(
            media_id=media_id,
            title=title,
            duration_seconds=round(max_time, 2),
            total_cues=len(cues),
            cues=cues
        )

    @staticmethod
    def _parse_timestamp(ts: str) -> float:
        parts = ts.split(":")
        hours = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds

"""Service exporting WebVTT closed captions with custom styling blocks."""
from typing import List, Dict
from app.schemas.captions import CaptionStylePreferences

class CaptionsService:
    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hrs:02d}:{mins:02d}:{secs:06.3f}"

    def build_webvtt(self, cues: List[Dict], style: CaptionStylePreferences = None) -> str:
        lines = ["WEBVTT", ""]
        if style:
            lines.extend([
                "STYLE",
                "::cue {",
                f"  color: {style.text_color};",
                f"  background-color: {style.background_color};",
                f"  font-size: {style.font_size_pct}%;",
                "}",
                ""
            ])

        for idx, cue in enumerate(cues, 1):
            start_str = self._format_timestamp(float(cue.get("start", 0.0)))
            end_str = self._format_timestamp(float(cue.get("end", 2.0)))
            text = str(cue.get("text", "")).strip()
            lines.append(f"{idx}")
            lines.append(f"{start_str} --> {end_str}")
            lines.append(text)
            lines.append("")

        return "\n".join(lines)

"""Service computing estimated completion times for visual, audio, and Braille reading."""
import re
from app.schemas.content import ContentDocument
from app.schemas.reading_pace import ReadingPaceEstimate

class ReadingPaceService:
    def estimate_pace(self, doc: ContentDocument, wpm_visual: int = 180) -> ReadingPaceEstimate:
        words = []
        for s in doc.sections:
            for b in s.blocks:
                if b.source_text:
                    words.extend(re.findall(r'\S+', b.source_text))

        count = max(1, len(words))
        safe_wpm = max(40, wpm_visual)

        return ReadingPaceEstimate(
            document_id=doc.id,
            word_count=count,
            visual_reading_minutes=round(count / safe_wpm, 1),
            tts_audio_minutes=round(count / 150.0, 1),
            braille_tactile_minutes=round(count / 95.0, 1)
        )

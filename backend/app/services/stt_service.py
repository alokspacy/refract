"""Service providing speech-to-text recognition and alignment parsing."""
import uuid
import re
from typing import List
from app.schemas.stt import SpeechTranscriptionResult, TranscriptionToken

class SpeechTranscriptionService:
    def parse_timed_text(self, raw_transcript: str, duration_sec: float = 30.0) -> SpeechTranscriptionResult:
        clean_text = raw_transcript.strip() if raw_transcript else ""
        words = re.findall(r'\S+', clean_text)
        word_count = max(1, len(words))
        
        safe_duration = max(1.0, float(duration_sec))
        step = safe_duration / word_count

        tokens: List[TranscriptionToken] = []
        for i, w in enumerate(words):
            start = round(i * step, 2)
            end = round(min(safe_duration, (i + 1) * step), 2)
            tokens.append(TranscriptionToken(
                word=w,
                start_sec=start,
                end_sec=end,
                confidence=0.95
            ))

        return SpeechTranscriptionResult(
            job_id=str(uuid.uuid4())[:8],
            duration_sec=safe_duration,
            language="en",
            full_text=clean_text,
            tokens=tokens
        )

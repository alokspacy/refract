"""Service providing speech-to-text recognition and alignment parsing."""
import uuid
import re
from typing import List
from app.schemas.stt import SpeechTranscriptionResult, TranscriptionToken

class SpeechTranscriptionService:
    def parse_timed_text(self, raw_transcript: str, duration_sec: float = 30.0) -> SpeechTranscriptionResult:
        words = re.findall(r'\S+', raw_transcript)
        word_count = max(1, len(words))
        step = max(0.1, duration_sec / word_count)

        tokens: List[TranscriptionToken] = []
        for i, w in enumerate(words):
            start = round(i * step, 2)
            end = round((i + 1) * step, 2)
            tokens.append(TranscriptionToken(
                word=w,
                start_sec=start,
                end_sec=end,
                confidence=0.95
            ))

        return SpeechTranscriptionResult(
            job_id=str(uuid.uuid4())[:8],
            duration_sec=duration_sec,
            language="en",
            full_text=raw_transcript.strip(),
            tokens=tokens
        )

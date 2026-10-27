"""FastAPI router for speech-to-text transcription."""
from fastapi import APIRouter, HTTPException, status
from app.schemas.stt import SpeechTranscriptionResult
from app.services.stt_service import SpeechTranscriptionService

router = APIRouter(prefix="/stt", tags=["Speech-To-Text"])
service = SpeechTranscriptionService()

@router.post("/align", response_model=SpeechTranscriptionResult)
def align_transcript(transcript: str, duration_seconds: float = 30.0):
    """Align raw text transcript with synthetic timestamp tokens for caption sync."""
    if not transcript.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transcript cannot be empty")
    return service.parse_timed_text(transcript, duration_sec=duration_seconds)

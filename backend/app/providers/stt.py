from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union


class STTProvider(ABC):
    """Abstract interface for future Speech-to-Text integrations."""

    @abstractmethod
    def transcribe(self, audio_data: Union[bytes, str], language: Optional[str] = None, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Transcribe audio into text with timestamps."""
        pass


class MockSTTProvider(STTProvider):
    """Mock Speech-to-Text Provider for testing in Phase 1."""

    def transcribe(self, audio_data: Union[bytes, str], language: Optional[str] = None, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {"transcript": "[Mock audio transcription]", "language": language or "en", "duration": 10.0}

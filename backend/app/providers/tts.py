from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class TTSProvider(ABC):
    """Abstract interface for future Text-to-Speech integrations."""

    @abstractmethod
    def synthesize(self, text: str, voice_id: Optional[str] = None, options: Optional[Dict[str, Any]] = None) -> bytes:
        """Synthesize text into audio bytes."""
        pass


class MockTTSProvider(TTSProvider):
    """Mock Text-to-Speech Provider for testing in Phase 1."""

    def synthesize(self, text: str, voice_id: Optional[str] = None, options: Optional[Dict[str, Any]] = None) -> bytes:
        return b"[Mock Synthesized Audio Bytes]"

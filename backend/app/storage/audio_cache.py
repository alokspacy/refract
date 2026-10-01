"""In-memory cache for audio narration packages."""
import hashlib
from typing import Dict, Optional
from app.schemas.audio import AudioNarrationPackage

class AudioNarrativeCache:
    _cache: Dict[str, AudioNarrationPackage] = {}

    @classmethod
    def get(cls, key: str) -> Optional[AudioNarrationPackage]:
        return cls._cache.get(key)

    @classmethod
    def set(cls, key: str, package: AudioNarrationPackage):
        cls._cache[key] = package

    @classmethod
    def make_key(cls, variant_id: str, preset: str) -> str:
        return hashlib.sha256(f"{variant_id}:{preset}".encode()).hexdigest()[:16]

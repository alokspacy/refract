"""Cache manager for block transformations using SHA-256 keys."""
import hashlib
from typing import Dict, Optional, Any

class TransformationCacheManager:
    _store: Dict[str, Any] = {}

    @staticmethod
    def compute_key(source_text: str, profile_id: str, prompt_version: str) -> str:
        payload = f"{source_text}:{profile_id}:{prompt_version}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        return cls._store.get(key)

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        cls._store[key] = value

    @classmethod
    def clear(cls) -> None:
        cls._store.clear()

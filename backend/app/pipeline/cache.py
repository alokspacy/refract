import hashlib
import json
import logging
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.models.variant import TransformationCache

logger = logging.getLogger("accesslearn.pipeline.cache")


class TransformationCacheManager:
    """
    Manages deterministic caching for AI block transformations.
    Prevents duplicate LLM invocations for identical source blocks and profile/prompt/model configurations.
    """

    @staticmethod
    def compute_cache_key(
        source_text: str,
        profile_id: str,
        profile_version: str,
        prompt_version: str,
        model: str
    ) -> str:
        raw_key = f"{source_text.strip()}|{profile_id}|{profile_version}|{prompt_version}|{model}"
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    @staticmethod
    def compute_source_hash(source_text: str) -> str:
        return hashlib.sha256(source_text.strip().encode("utf-8")).hexdigest()

    def get_cached_content(
        self,
        db: Session,
        cache_key: str
    ) -> Optional[Dict[str, Any]]:
        cache_entry = db.query(TransformationCache).filter(TransformationCache.cache_key == cache_key).first()
        if cache_entry:
            logger.info(f"Cache hit for key={cache_key[:12]}...")
            return cache_entry.content
        return None

    def store_cached_content(
        self,
        db: Session,
        source_text: str,
        profile_id: str,
        profile_version: str,
        prompt_version: str,
        model: str,
        content: Dict[str, Any]
    ) -> None:
        cache_key = self.compute_cache_key(source_text, profile_id, profile_version, prompt_version, model)
        source_hash = self.compute_source_hash(source_text)

        existing = db.query(TransformationCache).filter(TransformationCache.cache_key == cache_key).first()
        if not existing:
            new_entry = TransformationCache(
                cache_key=cache_key,
                source_hash=source_hash,
                profile_id=profile_id,
                profile_version=profile_version,
                prompt_version=prompt_version,
                model=model,
                content=content
            )
            db.add(new_entry)
            db.commit()
            logger.info(f"Stored transformation cache entry for key={cache_key[:12]}...")

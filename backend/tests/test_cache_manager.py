"""Unit tests for transformation cache manager."""
from app.pipeline.cache_manager import TransformationCacheManager

def test_cache_hit_and_miss():
    TransformationCacheManager.clear()
    key = TransformationCacheManager.compute_key("Sample text", "dyslexia", "v1.0")
    assert TransformationCacheManager.get(key) is None

    TransformationCacheManager.set(key, {"simplified": "Sample text"})
    assert TransformationCacheManager.get(key) == {"simplified": "Sample text"}

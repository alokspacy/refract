from app.core.config import settings
from app.providers.storage import StorageProvider
from app.storage.local import LocalStorageProvider
from app.storage.s3 import S3StorageProvider

_storage_instance = None


def get_storage_provider() -> StorageProvider:
    """Factory function returning the configured StorageProvider singleton."""
    global _storage_instance
    if _storage_instance is None:
        if settings.STORAGE_PROVIDER == "s3":
            _storage_instance = S3StorageProvider()
        else:
            _storage_instance = LocalStorageProvider(base_path=settings.LOCAL_STORAGE_PATH)
    return _storage_instance

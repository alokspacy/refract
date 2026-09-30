from abc import ABC, abstractmethod
from typing import BinaryIO, Optional, Union


class StorageProvider(ABC):
    """Abstract interface for file storage implementations (Local, S3, etc.)."""

    @abstractmethod
    def save(self, file_data: Union[bytes, BinaryIO], storage_key: str) -> str:
        """Save file data under storage_key. Returns the storage path/identifier."""
        pass

    @abstractmethod
    def get(self, storage_key: str) -> bytes:
        """Retrieve binary file contents for storage_key."""
        pass

    @abstractmethod
    def delete(self, storage_key: str) -> bool:
        """Delete file associated with storage_key."""
        pass

    @abstractmethod
    def exists(self, storage_key: str) -> bool:
        """Check if file exists under storage_key."""
        pass

    @abstractmethod
    def get_download_url(self, storage_key: str, expires_in: int = 3600) -> Optional[str]:
        """Generate a direct download URL or internal endpoint path if applicable."""
        pass

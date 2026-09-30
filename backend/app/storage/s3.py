from typing import BinaryIO, Optional, Union
from app.providers.storage import StorageProvider


class S3StorageProvider(StorageProvider):
    """S3-compatible storage provider stub for future cloud deployments."""

    def __init__(
        self,
        bucket_name: str = "accesslearn-storage",
        region_name: str = "us-east-1",
        endpoint_url: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
    ):
        self.bucket_name = bucket_name
        self.region_name = region_name
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key

    def save(self, file_data: Union[bytes, BinaryIO], storage_key: str) -> str:
        # Stub for S3 upload
        return f"s3://{self.bucket_name}/{storage_key}"

    def get(self, storage_key: str) -> bytes:
        raise NotImplementedError("S3 storage retrieval not configured in Phase 1.")

    def delete(self, storage_key: str) -> bool:
        return True

    def exists(self, storage_key: str) -> bool:
        return False

    def get_download_url(self, storage_key: str, expires_in: int = 3600) -> Optional[str]:
        return f"https://{self.bucket_name}.s3.amazonaws.com/{storage_key}"

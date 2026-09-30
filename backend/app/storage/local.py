import os
import shutil
from pathlib import Path
from typing import BinaryIO, Optional, Union
from app.providers.storage import StorageProvider


class LocalStorageProvider(StorageProvider):
    """Local filesystem implementation of StorageProvider with path-traversal safeguards."""

    def __init__(self, base_path: str = "./storage"):
        self.base_path = Path(base_path).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _resolve_safe_path(self, storage_key: str) -> Path:
        """Resolve storage key to absolute path and prevent directory traversal."""
        # Sanitize storage_key: strip leading slashes and prevent '..'
        clean_key = os.path.normpath(storage_key).lstrip(r"\/")
        if ".." in clean_key.split(os.sep):
            raise ValueError(f"Path traversal detected in storage key: {storage_key}")

        target_path = (self.base_path / clean_key).resolve()
        if not str(target_path).startswith(str(self.base_path)):
            raise ValueError(f"Resolved path outside storage root: {storage_key}")

        return target_path

    def save(self, file_data: Union[bytes, BinaryIO], storage_key: str) -> str:
        target_path = self._resolve_safe_path(storage_key)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(file_data, bytes):
            with open(target_path, "wb") as f:
                f.write(file_data)
        else:
            with open(target_path, "wb") as f:
                shutil.copyfileobj(file_data, f)

        return str(target_path)

    def get(self, storage_key: str) -> bytes:
        target_path = self._resolve_safe_path(storage_key)
        if not target_path.exists() or not target_path.is_file():
            raise FileNotFoundError(f"File not found: {storage_key}")

        with open(target_path, "rb") as f:
            return f.read()

    def delete(self, storage_key: str) -> bool:
        target_path = self._resolve_safe_path(storage_key)
        if target_path.exists() and target_path.is_file():
            target_path.unlink()
            return True
        return False

    def exists(self, storage_key: str) -> bool:
        try:
            target_path = self._resolve_safe_path(storage_key)
            return target_path.exists() and target_path.is_file()
        except ValueError:
            return False

    def get_download_url(self, storage_key: str, expires_in: int = 3600) -> Optional[str]:
        # For local development, files are accessed via protected backend endpoints
        return f"/documents/download/{storage_key}"

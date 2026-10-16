"""Document validation and ingestion service."""
import os
from typing import Set

ALLOWED_EXTENSIONS: Set[str] = {".pdf", ".docx", ".pptx", ".txt", ".png", ".jpg", ".jpeg"}
MAX_FILE_SIZE_BYTES: int = 50 * 1024 * 1024  # 50 MB

class DocumentService:
    @staticmethod
    def validate_filename(filename: str) -> bool:
        _, ext = os.path.splitext(filename.lower())
        return ext in ALLOWED_EXTENSIONS

    @staticmethod
    def validate_file_size(size_bytes: int) -> bool:
        return 0 < size_bytes <= MAX_FILE_SIZE_BYTES

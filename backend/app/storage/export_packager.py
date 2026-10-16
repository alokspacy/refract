"""Zip archive builder for educational packages with security checks."""
import io
import zipfile
import hashlib
import os
from typing import Dict

class ExportPackager:
    """Builds zip archives in memory, sanitized against directory traversal attacks."""

    @staticmethod
    def create_zip_archive(files: Dict[str, str | bytes]) -> bytes:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for filepath, content in files.items():
                # Sanitize filepath to prevent directory traversal
                clean_path = os.path.normpath(filepath).replace("\\", "/")
                if clean_path.startswith("../") or clean_path.startswith("/"):
                    clean_path = clean_path.lstrip("./").lstrip("/")

                if isinstance(content, str):
                    zf.writestr(clean_path, content.encode("utf-8"))
                else:
                    zf.writestr(clean_path, content)
        return buffer.getvalue()

    @staticmethod
    def compute_sha256(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

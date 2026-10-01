"""Zip archive builder for educational packages."""
import io
import zipfile
import hashlib
from typing import Dict

class ExportPackager:
    """Builds zip archives in memory or disk for export distribution."""

    @staticmethod
    def create_zip_archive(files: Dict[str, str | bytes]) -> bytes:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for filepath, content in files.items():
                if isinstance(content, str):
                    zf.writestr(filepath, content.encode("utf-8"))
                else:
                    zf.writestr(filepath, content)
        return buffer.getvalue()

    @staticmethod
    def compute_sha256(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

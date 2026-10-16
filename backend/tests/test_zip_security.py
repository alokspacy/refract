"""Unit tests for zip path sanitization."""
import zipfile
import io
from app.storage.export_packager import ExportPackager

def test_zip_path_traversal_prevention():
    zip_bytes = ExportPackager.create_zip_archive({"../../etc/passwd": "blocked"})
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    namelist = zf.namelist()
    assert not any(name.startswith("../") for name in namelist)

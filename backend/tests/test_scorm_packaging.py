"""Unit tests for SCORM packaging."""
import zipfile
import io
from app.services.scorm_service import ScormExportService
from app.schemas.content import ContentDocument

def test_scorm_zip_contains_manifest():
    svc = ScormExportService()
    doc = ContentDocument(title="Chemistry Module")
    zip_bytes = svc.create_scorm_package(doc, "chem-001")
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    namelist = zf.namelist()
    assert "imsmanifest.xml" in namelist
    assert "index.html" in namelist
    manifest_content = zf.read("imsmanifest.xml").decode("utf-8")
    assert "Chemistry Module" in manifest_content
    assert "chem-001" in manifest_content

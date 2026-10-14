"""Unit tests for master export bundling."""
import zipfile
import io
from app.services.bundle_service import BundleService
from app.schemas.content import ContentDocument

def test_master_bundle_contents():
    svc = BundleService()
    doc = ContentDocument(title="Master Unit")
    zip_bytes = svc.create_master_bundle(doc)
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    names = zf.namelist()
    assert "standalone/index.html" in names
    assert "braille/embosser.brf" in names
    assert "data/content.json" in names

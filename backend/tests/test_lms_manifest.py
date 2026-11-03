"""Unit tests for LMS manifest and SCORM packaging service."""
from app.services.lms_manifest_service import LMSManifestService
from app.schemas.content import ContentDocument

def test_build_imsmanifest_xml():
    service = LMSManifestService()
    doc = ContentDocument(title="Inclusive Chemistry 101")
    xml = service.build_imsmanifest_xml(doc)
    assert 'ADL SCORM' in xml
    assert 'Inclusive Chemistry 101' in xml
    assert 'WCAG 2.2 Level AA' in xml

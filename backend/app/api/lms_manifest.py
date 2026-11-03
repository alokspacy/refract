"""FastAPI router for LMS course package manifest generation."""
from fastapi import APIRouter, Response
from app.schemas.content import ContentDocument
from app.services.lms_manifest_service import LMSManifestService

router = APIRouter(prefix="/lms", tags=["LMS Packaging"])
service = LMSManifestService()

@router.post("/manifest-xml")
def generate_imsmanifest(doc: ContentDocument):
    """Generate compliant imsmanifest.xml file for SCORM 2004 LMS import."""
    xml_content = service.build_imsmanifest_xml(doc)
    return Response(content=xml_content, media_type="application/xml")

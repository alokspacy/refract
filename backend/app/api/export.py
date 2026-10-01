"""FastAPI router for educational exports."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.export import ExportPackageResponse, ExportRequest, ExportFormat
from app.services.export_service import ExportService

router = APIRouter(prefix="/export", tags=["Export"])
service = ExportService()

@router.get("/formats")
def list_supported_formats():
    """List available LMS and standalone accessible export formats."""
    return [
        {"format": ExportFormat.HTML5_STANDALONE, "description": "Standalone offline accessible HTML5 package"},
        {"format": ExportFormat.SCORM_12, "description": "SCORM 1.2 zip for Canvas, Blackboard, and Moodle"},
        {"format": ExportFormat.ACCESSIBLE_EPUB, "description": "EPUB3 with accessibility metadata"},
        {"format": ExportFormat.STRUCTURED_JSON, "description": "Normalized Content JSON with block traceability"}
    ]

@router.post("/package", response_model=ExportPackageResponse)
def create_export_package(req: ExportRequest, db: Session = Depends(get_db)):
    """Generate an accessible export bundle."""
    doc = db.query(Document).first()
    cd = ContentDocument.model_validate(doc.normalized_content) if doc and doc.normalized_content else ContentDocument(title="Educational Module")
    return service.generate_package(cd, req)

@router.get("/{package_id}/download")
def download_package(package_id: str):
    """Download compiled export zip archive."""
    data = service.get_package_bytes(package_id)
    if not data:
        raise HTTPException(status_code=404, detail="Export package not found or expired")
    return Response(content=data, media_type="application/zip", headers={"Content-Disposition": f'attachment; filename="export_{package_id}.zip"'})

"""FastAPI router for master bundle export downloads."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.services.bundle_service import BundleService

router = APIRouter(prefix="/bundle", tags=["Bundle Export"])
service = BundleService()

@router.get("/documents/{document_id}/all")
def download_master_bundle(document_id: str, db: Session = Depends(get_db)):
    """Download single zip containing HTML5, SCORM, Braille, and JSON formats."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(status_code=404, detail="Document not found")
    cd = ContentDocument.model_validate(doc.normalized_content)
    zip_bytes = service.create_master_bundle(cd)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="master_bundle_{document_id}.zip"'}
    )

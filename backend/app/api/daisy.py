"""FastAPI router for DAISY talking book manifests."""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.daisy import DAISYManifestResponse
from app.services.daisy_service import DaisyService

router = APIRouter(prefix="/daisy", tags=["DAISY Talking Book"])
service = DaisyService()

@router.get("/documents/{document_id}/ncc", response_model=DAISYManifestResponse)
def get_daisy_manifest(document_id: str, db: Session = Depends(get_db)):
    """Retrieve DAISY talking book NCC navigation manifest."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(status_code=404, detail="Document not found")
    cd = ContentDocument.model_validate(doc.normalized_content)
    return service.build_ncc(cd)

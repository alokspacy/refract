"""FastAPI router for Braille translation services."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.braille import BrailleDocumentResponse, BrailleGrade
from app.services.braille_service import BrailleService

router = APIRouter(prefix="/braille", tags=["Braille Translation"])
service = BrailleService()

@router.get("/documents/{document_id}", response_model=BrailleDocumentResponse)
def get_braille_version(document_id: str, grade: BrailleGrade = BrailleGrade.GRADE_2, db: Session = Depends(get_db)):
    """Retrieve complete Unified English Braille translation of a document."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(status_code=404, detail="Document not found or empty")
    cd = ContentDocument.model_validate(doc.normalized_content)
    return service.translate_document(cd, grade=grade)

@router.get("/documents/{document_id}/brf")
def download_brf_file(document_id: str, grade: BrailleGrade = BrailleGrade.GRADE_2, db: Session = Depends(get_db)):
    """Download standard Braille Ready Format (.brf) for embossers."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(status_code=404, detail="Document not found")
    cd = ContentDocument.model_validate(doc.normalized_content)
    rep = service.translate_document(cd, grade=grade)
    return Response(
        content=rep.raw_brf_content,
        media_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename="document_{document_id}.brf"'}
    )

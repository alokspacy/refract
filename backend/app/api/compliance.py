"""FastAPI router for WCAG compliance auditing."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.models.variant import GeneratedVariant
from app.schemas.compliance import WCAGAuditReport
from app.schemas.content import ContentDocument
from app.pipeline.compliance import WCAGComplianceEvaluator

router = APIRouter(prefix="/compliance", tags=["Compliance"])
evaluator = WCAGComplianceEvaluator()

@router.post("/evaluate", response_model=WCAGAuditReport)
def evaluate_custom_content(doc: ContentDocument):
    """Evaluate arbitrary ContentDocument for WCAG 2.2 AA/AAA compliance."""
    return evaluator.evaluate(doc)

@router.get("/documents/{document_id}", response_model=WCAGAuditReport)
def audit_document(document_id: str, db: Session = Depends(get_db)):
    """Audit an existing normalized document against WCAG standards."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"Document {document_id} not found or not normalized"}
        )
    content_doc = ContentDocument.model_validate(doc.normalized_content)
    return evaluator.evaluate(content_doc)

@router.get("/variants/{variant_id}", response_model=WCAGAuditReport)
def audit_variant(variant_id: str, db: Session = Depends(get_db)):
    """Audit an adapted variant against WCAG standards."""
    variant = db.query(GeneratedVariant).filter(GeneratedVariant.id == variant_id).first()
    if not variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"Variant {variant_id} not found"}
        )
    # Check parent document
    doc = db.query(Document).filter(Document.id == variant.document_id).first()
    content_doc = ContentDocument.model_validate(doc.normalized_content) if doc and doc.normalized_content else ContentDocument(title="Variant Content")
    return evaluator.evaluate(content_doc, variant_id=variant_id)

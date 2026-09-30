from typing import Any, Dict, List
from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db, get_storage
from app.models.job import ProcessingJob
from app.models.user import User
from app.providers.storage import StorageProvider
from app.schemas.document import DocumentListResponse, DocumentPreviewResponse, DocumentResponse
from app.schemas.job import JobResponse
from app.schemas.analysis import ContentAnalysisResponse
from app.schemas.variant import GeneratedVariantCreate
from app.services.document_service import DocumentService
from app.services.variant_service import get_variant_service

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload an educational document"
)
async def upload_document(
    file: UploadFile = File(..., description="Educational document file to upload"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    storage: StorageProvider = Depends(get_storage)
):
    """
    Securely upload an educational document (PDF, DOCX, PPTX, images, audio, video, etc.).
    Validates MIME type, file size, and extension, saves to secure storage, and creates initial processing job.
    """
    doc, job = await DocumentService.upload_document(
        db=db,
        user=current_user,
        file=file,
        storage=storage
    )
    res = DocumentResponse.model_validate(doc)
    res.latest_job_id = job.id
    return res


@router.get(
    "",
    response_model=DocumentListResponse,
    summary="List all uploaded documents for the current user"
)
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve all educational documents belonging to the authenticated user."""
    docs = DocumentService.list_user_documents(db=db, user=current_user)
    items = []
    for doc in docs:
        item = DocumentResponse.model_validate(doc)
        latest_job = db.query(ProcessingJob).filter(ProcessingJob.document_id == doc.id).order_by(ProcessingJob.created_at.desc()).first()
        if latest_job:
            item.latest_job_id = latest_job.id
        items.append(item)
    return DocumentListResponse(items=items, total=len(items))


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    summary="Get document details by ID"
)
def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve metadata for a specific document owned by the authenticated user."""
    doc = DocumentService.get_user_document(db=db, user=current_user, document_id=document_id)
    res = DocumentResponse.model_validate(doc)
    latest_job = db.query(ProcessingJob).filter(ProcessingJob.document_id == doc.id).order_by(ProcessingJob.created_at.desc()).first()
    if latest_job:
        res.latest_job_id = latest_job.id
    return res


@router.post(
    "/{document_id}/process",
    response_model=JobResponse,
    summary="Trigger asynchronous document extraction & normalization"
)
def process_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Asynchronously execute extraction, OCR (if needed), and normalization pipeline."""
    job = DocumentService.trigger_processing(db=db, user=current_user, document_id=document_id)
    return JobResponse.model_validate(job)


@router.get(
    "/{document_id}/content",
    response_model=Dict[str, Any],
    summary="Get normalized Content JSON schema"
)
def get_document_content(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve the normalized ContentDocument JSON schema representation."""
    return DocumentService.get_document_content(db=db, user=current_user, document_id=document_id)


@router.get(
    "/{document_id}/preview",
    response_model=DocumentPreviewResponse,
    summary="Get frontend-friendly document source preview"
)
def get_document_preview(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve structured source preview with sections, blocks, tables, and warnings."""
    return DocumentService.get_document_preview(db=db, user=current_user, document_id=document_id)


# =========================================================================
# Phase 3 AI Core Endpoints
# =========================================================================

@router.post(
    "/{document_id}/analyze",
    response_model=JobResponse,
    summary="Trigger asynchronous pedagogical content analysis"
)
def analyze_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Queue Phase 3 Content Analysis using LLM to extract subject, grade, learning objectives, concepts, and vocabulary.
    """
    service = get_variant_service()
    _, job = service.analyze_document_request(db=db, document_id=document_id, user_id=current_user.id)
    return JobResponse.model_validate(job)


@router.get(
    "/{document_id}/analysis",
    response_model=ContentAnalysisResponse,
    summary="Get pedagogical content analysis results"
)
def get_document_analysis(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve structured pedagogical analysis including learning objectives, concepts, and vocabulary.
    """
    service = get_variant_service()
    analysis = service.get_document_analysis(db=db, document_id=document_id, user_id=current_user.id)
    return ContentAnalysisResponse.model_validate(analysis)


@router.post(
    "/{document_id}/variants",
    status_code=status.HTTP_201_CREATED,
    summary="Generate accessible learning variant"
)
def create_document_variant(
    document_id: str,
    req: GeneratedVariantCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Queue accessible variant generation for selected profiles (Dyslexia, Cognitive, Basic Visual).
    """
    service = get_variant_service()
    variant, job = service.create_variant_request(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
        profile_ids=req.profile_ids,
        metadata_overrides=req.metadata_overrides
    )
    return {
        "variant_id": variant.id,
        "status": "QUEUED",
        "job_id": job.id,
        "name": variant.name,
        "profile_ids": variant.profile_ids
    }

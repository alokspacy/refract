import logging
import os
import re
import uuid
from typing import Any, Dict, List, Tuple
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.document import Document
from app.models.job import ProcessingJob
from app.models.user import User
from app.providers.storage import StorageProvider
from app.schemas.content import ContentDocument
from app.schemas.document import DocumentPreviewResponse

logger = logging.getLogger("accesslearn.documents")

DANGEROUS_EXTENSIONS = {
    "exe", "bat", "cmd", "sh", "bin", "msi", "com", "vbs", "ps1", "py", "php", "js", "html", "htm", "jar"
}

ALLOWED_MIME_MAP = {
    "pdf": ["application/pdf"],
    "docx": [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
        "application/octet-stream"
    ],
    "pptx": [
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.ms-powerpoint",
        "application/octet-stream"
    ],
    "png": ["image/png"],
    "jpg": ["image/jpeg", "image/jpg", "image/pjpeg"],
    "jpeg": ["image/jpeg", "image/jpg", "image/pjpeg"],
    "txt": ["text/plain", "application/octet-stream"],
    "mp3": ["audio/mpeg", "audio/mp3", "audio/x-mpeg-3"],
    "wav": ["audio/wav", "audio/x-wav", "audio/wave"],
    "mp4": ["video/mp4", "application/mp4"]
}


class DocumentService:
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to prevent directory traversal and remove special characters."""
        clean = os.path.basename(filename.replace("\\", "/"))
        clean = clean.replace("..", "")
        clean = re.sub(r"[^\w\.-]", "_", clean)
        if not clean or clean.startswith("."):
            clean = f"document_{uuid.uuid4().hex[:8]}{clean}"
        return clean

    @classmethod
    async def upload_document(
        cls,
        db: Session,
        user: User,
        file: UploadFile,
        storage: StorageProvider
    ) -> Tuple[Document, ProcessingJob]:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_FILENAME", "message": "Filename cannot be empty."}
            )

        safe_filename = cls.sanitize_filename(file.filename)
        ext = safe_filename.rsplit(".", 1)[-1].lower() if "." in safe_filename else ""

        # Check extension against forbidden / dangerous lists
        if ext in DANGEROUS_EXTENSIONS or ext not in [e.lower() for e in settings.ALLOWED_EXTENSIONS]:
            logger.warning(f"Rejected upload with forbidden/unsupported extension: {ext} by user={user.id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "UNSUPPORTED_FILE_TYPE",
                    "message": f"File extension '.{ext}' is not supported. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
                }
            )

        # Validate MIME type
        content_type = file.content_type.lower() if file.content_type else "application/octet-stream"
        expected_mimes = ALLOWED_MIME_MAP.get(ext, [])
        if expected_mimes and content_type not in expected_mimes and content_type != "application/octet-stream":
            logger.warning(f"MIME type mismatch for ext '{ext}': got '{content_type}'")
            if "javascript" in content_type or "executable" in content_type or "html" in content_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"code": "INVALID_MIME_TYPE", "message": f"MIME type '{content_type}' is forbidden."}
                )

        # Read content and validate file size
        max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        file_bytes = await file.read()
        file_size = len(file_bytes)

        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "EMPTY_FILE", "message": "The uploaded file is empty."}
            )

        if file_size > max_bytes:
            logger.warning(f"File size {file_size} exceeds max limit {max_bytes} for user={user.id}")
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail={
                    "code": "FILE_TOO_LARGE",
                    "message": f"The uploaded file exceeds the configured limit of {settings.MAX_FILE_SIZE_MB}MB."
                }
            )

        # Generate unique storage details
        doc_id = str(uuid.uuid4())
        stored_filename = f"{doc_id}_{safe_filename}"
        storage_key = f"users/{user.id}/{stored_filename}"

        # Save to storage provider
        try:
            storage.save(file_bytes, storage_key)
        except Exception as e:
            logger.exception(f"Storage error saving file {storage_key}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"code": "STORAGE_ERROR", "message": "Failed to persist uploaded document."}
            )

        # Create Document record
        doc = Document(
            id=doc_id,
            owner_id=user.id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            mime_type=content_type,
            file_size=file_size,
            storage_key=storage_key,
            status="UPLOADED",
            extraction_status="PENDING"
        )
        db.add(doc)

        # Create ProcessingJob record
        job_id = str(uuid.uuid4())
        job = ProcessingJob(
            id=job_id,
            document_id=doc.id,
            status="QUEUED",
            current_stage="EXTRACTING",
            progress=0.0
        )
        db.add(job)
        db.commit()
        db.refresh(doc)
        db.refresh(job)

        # Dispatch Celery background task
        try:
            from app.workers.tasks import process_document_job
            process_document_job.apply_async(args=[job.id, doc.id], retry=False)
            logger.info(f"Enqueued Celery job={job.id} for document={doc.id}")
        except Exception as e:
            logger.warning(f"Celery task dispatch skipped or failed (worker may be offline in dev/test): {str(e)}")

        logger.info(f"Document uploaded successfully: id={doc.id}, size={file_size}, user={user.id}")
        return doc, job

    @classmethod
    def trigger_processing(
        cls,
        db: Session,
        user: User,
        document_id: str
    ) -> ProcessingJob:
        doc = cls.get_user_document(db, user, document_id)
        
        # Create a new ProcessingJob
        job_id = str(uuid.uuid4())
        job = ProcessingJob(
            id=job_id,
            document_id=doc.id,
            status="QUEUED",
            current_stage="EXTRACTING",
            progress=0.0
        )
        doc.extraction_status = "PROCESSING"
        doc.status = "PROCESSING"
        db.add(job)
        db.commit()
        db.refresh(job)

        # Dispatch task
        try:
            from app.workers.tasks import process_document_job
            process_document_job.apply_async(args=[job.id, doc.id], retry=False)
            logger.info(f"Enqueued reprocessing Celery job={job.id} for document={doc.id}")
        except Exception as e:
            logger.warning(f"Celery dispatch failed: {str(e)}")

        return job

    @staticmethod
    def list_user_documents(db: Session, user: User) -> List[Document]:
        return db.query(Document).filter(Document.owner_id == user.id).order_by(Document.created_at.desc()).all()

    @staticmethod
    def get_user_document(db: Session, user: User, document_id: str) -> Document:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "DOCUMENT_NOT_FOUND", "message": "Document not found."}
            )
        if doc.owner_id != user.id:
            logger.warning(f"Unauthorized document access attempt: doc={document_id} by user={user.id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": "You do not have permission to access this document."}
            )
        return doc

    @classmethod
    def get_document_content(cls, db: Session, user: User, document_id: str) -> Dict[str, Any]:
        doc = cls.get_user_document(db, user, document_id)
        if not doc.normalized_content:
            if doc.extraction_status == "FAILED":
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={"code": "EXTRACTION_FAILED", "message": "Document extraction failed. Check job errors."}
                )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "CONTENT_NOT_READY", "message": f"Document content is not extracted yet (status: {doc.extraction_status})."}
            )
        return doc.normalized_content

    @classmethod
    def get_document_preview(cls, db: Session, user: User, document_id: str) -> DocumentPreviewResponse:
        doc = cls.get_user_document(db, user, document_id)
        if not doc.normalized_content:
            if doc.extraction_status == "FAILED":
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={"code": "EXTRACTION_FAILED", "message": "Document extraction failed."}
                )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "PREVIEW_NOT_READY", "message": f"Source preview is not available yet (status: {doc.extraction_status})."}
            )

        content = doc.normalized_content
        return DocumentPreviewResponse(
            document_id=doc.id,
            title=content.get("title", doc.original_filename),
            original_filename=doc.original_filename,
            mime_type=doc.mime_type,
            extraction_status=doc.extraction_status,
            extraction_warnings=doc.extraction_warnings or [],
            extracted_at=doc.extracted_at,
            sections=content.get("sections", []),
            schema_version=content.get("schema_version", "1.0.0")
        )

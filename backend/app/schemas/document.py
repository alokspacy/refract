from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.content import ContentDocument, Section


class DocumentResponse(BaseModel):
    id: str
    owner_id: str
    original_filename: str
    stored_filename: str
    mime_type: str
    file_size: int
    storage_key: str
    status: str
    extraction_status: str = "PENDING"
    extraction_warnings: Optional[List[str]] = None
    extracted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    latest_job_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class DocumentListResponse(BaseModel):
    items: List[DocumentResponse]
    total: int


class DocumentPreviewResponse(BaseModel):
    document_id: str
    title: str
    original_filename: str
    mime_type: str
    extraction_status: str
    extraction_warnings: List[str]
    extracted_at: Optional[datetime]
    sections: List[Section]
    schema_version: str = "1.0.0"

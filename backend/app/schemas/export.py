"""Schemas for educational package exports."""
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class ExportFormat(str, Enum):
    HTML5_STANDALONE = "html5_standalone"
    SCORM_12 = "scorm_12"
    SCORM_2004 = "scorm_2004"
    IMS_CONTENT_PACKAGE = "ims_cp"
    ACCESSIBLE_EPUB = "accessible_epub"
    STRUCTURED_JSON = "structured_json"

class ExportRequest(BaseModel):
    variant_id: str
    format: ExportFormat = ExportFormat.HTML5_STANDALONE
    include_audio: bool = True
    include_flashcards: bool = True
    theme: str = "high_contrast"

class ExportPackageResponse(BaseModel):
    package_id: str
    variant_id: str
    format: ExportFormat
    filename: str
    file_size_bytes: int
    download_url: str
    checksum_sha256: str
    created_at: str

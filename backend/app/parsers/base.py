from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field


class ExtractedAsset(BaseModel):
    asset_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "image"
    filename: str = ""
    mime_type: str = "image/png"
    data_bytes: Optional[bytes] = None
    storage_key: Optional[str] = None
    page_or_slide: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExtractedBlock(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # heading, paragraph, list, table, image, equation, media
    text: Optional[str] = None
    page_or_slide: Optional[int] = None
    position: Optional[int] = None
    bbox: Optional[List[float]] = None  # [x0, y0, x1, y1]
    asset_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExtractedSection(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    blocks: List[ExtractedBlock] = Field(default_factory=list)
    page_or_slide: Optional[int] = None


class ExtractedDocument(BaseModel):
    title: str = "Untitled Document"
    source_language: Optional[str] = "en"
    pages_or_slides_count: int = 1
    sections: List[ExtractedSection] = Field(default_factory=list)
    assets: List[ExtractedAsset] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
    requires_ocr: bool = False
    ocr_pages: List[int] = Field(default_factory=list)


class BaseParser(ABC):
    """Abstract base class for format-specific document parsers."""

    @abstractmethod
    def can_parse(self, mime_type: str, filename: str) -> bool:
        """Return True if this parser can handle the given MIME type or filename."""
        pass

    @abstractmethod
    def parse(self, file_bytes: bytes, filename: str, options: Optional[Dict[str, Any]] = None) -> ExtractedDocument:
        """Parse raw file bytes into a common intermediate ExtractedDocument representation."""
        pass

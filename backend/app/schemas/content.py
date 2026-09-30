import uuid
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class BlockType(str, Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST = "list"
    TABLE = "table"
    IMAGE = "image"
    EQUATION = "equation"
    MEDIA = "media"


class ContentBlock(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: BlockType
    source_text: Optional[str] = None
    source_asset_id: Optional[str] = None
    page_or_slide: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    accessibility_annotations: Dict[str, Any] = Field(default_factory=dict)


class Section(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    blocks: List[ContentBlock] = Field(default_factory=list)


class ContentDocument(BaseModel):
    schema_version: str = Field(default="1.0.0", description="Strict schema version for content normalization")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    source_language: str = Field(default="en")
    subject: Optional[str] = None
    grade_hint: Optional[str] = None
    learning_objectives: List[str] = Field(default_factory=list)
    glossary: Dict[str, str] = Field(default_factory=dict)
    sections: List[Section] = Field(default_factory=list)

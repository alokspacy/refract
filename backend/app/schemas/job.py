from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict


class JobStatusEnum(str, Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class JobStageEnum(str, Enum):
    FOUNDATION = "FOUNDATION"
    EXTRACTING = "EXTRACTING"
    OCR = "OCR"
    NORMALIZING = "NORMALIZING"
    UNDERSTANDING = "UNDERSTANDING"
    ANALYZING = "ANALYZING"
    PLANNING = "PLANNING"
    TRANSFORMING = "TRANSFORMING"
    ADAPTING = "ADAPTING"
    CREATING_AUDIO = "CREATING_AUDIO"
    CREATING_CAPTIONS = "CREATING_CAPTIONS"
    VALIDATING = "VALIDATING"
    READY = "READY"


class JobResponse(BaseModel):
    id: str
    document_id: str
    status: JobStatusEnum
    current_stage: str
    progress: float
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

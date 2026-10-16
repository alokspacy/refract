"""Schemas for automated event webhooks."""
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl

class WebhookEventType(str, Enum):
    DOCUMENT_INGESTED = "document.ingested"
    VARIANT_READY = "variant.ready"
    AUDIT_COMPLETED = "audit.completed"

class WebhookPayload(BaseModel):
    event_id: str
    event_type: WebhookEventType
    timestamp: datetime
    data: Dict[str, Any]

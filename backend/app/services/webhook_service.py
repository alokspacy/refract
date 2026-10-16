"""Webhook notification dispatching service."""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any
from app.schemas.webhook import WebhookPayload, WebhookEventType

class WebhookService:
    @staticmethod
    def build_event(event_type: WebhookEventType, data: Dict[str, Any]) -> WebhookPayload:
        return WebhookPayload(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            data=data
        )

"""Unit tests for webhook service."""
from app.services.webhook_service import WebhookService
from app.schemas.webhook import WebhookEventType

def test_webhook_event_structure():
    ev = WebhookService.build_event(WebhookEventType.AUDIT_COMPLETED, {"score": 96})
    assert ev.event_type == WebhookEventType.AUDIT_COMPLETED
    assert ev.data["score"] == 96

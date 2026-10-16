"""FastAPI router for institutional webhooks."""
from fastapi import APIRouter
from app.schemas.webhook import WebhookPayload, WebhookEventType
from app.services.webhook_service import WebhookService

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("/test-event", response_model=WebhookPayload)
def trigger_test_event():
    """Trigger sample webhook event for educational LMS listeners."""
    return WebhookService.build_event(WebhookEventType.VARIANT_READY, {"variant_id": "v-test", "status": "approved"})

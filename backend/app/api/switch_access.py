"""FastAPI router for assistive switch scanning configuration."""
from fastapi import APIRouter
from app.schemas.switch_access import SwitchScanSettings
from app.services.switch_access_service import SwitchAccessService

router = APIRouter(prefix="/switch-access", tags=["Switch Access Motor Control"])
service = SwitchAccessService()

@router.post("/metrics")
def calculate_scan_timing(element_count: int, settings: SwitchScanSettings):
    """Calculate scan loop timing and optimal scanning topology."""
    return service.compute_cycle_metrics(element_count, settings)

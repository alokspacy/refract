"""FastAPI router for enterprise school district tenants."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationResponse, SubscriptionTier

router = APIRouter(prefix="/organizations", tags=["Organizations & Licenses"])

TIER_LIMITS = {
    SubscriptionTier.FREE: 50,
    SubscriptionTier.EDUCATOR: 500,
    SubscriptionTier.SCHOOL: 5000,
    SubscriptionTier.DISTRICT: 50000,
}

@router.post("/", response_model=OrganizationResponse)
def create_organization(data: OrganizationCreate, db: Session = Depends(get_db)):
    """Register a new institution or school district."""
    limit = TIER_LIMITS.get(data.tier, 5000)
    org = Organization(
        name=data.name,
        domain=data.domain,
        contact_email=str(data.contact_email),
        tier=data.tier.value,
        monthly_page_limit=limit,
        monthly_pages_used=0,
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

@router.get("/{org_id}", response_model=OrganizationResponse)
def get_organization(org_id: str, db: Session = Depends(get_db)):
    """Get organization usage details and quota status."""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

"""Service tracking institution document transformation limits."""
from sqlalchemy.orm import Session
from app.models.organization import Organization

class QuotaExceededException(Exception):
    pass

class OrganizationSuspendedException(Exception):
    pass

class QuotaService:
    @staticmethod
    def check_and_increment(db: Session, org_id: str, page_count: int = 1) -> bool:
        org = db.query(Organization).filter(Organization.id == org_id).first()
        if not org:
            return False
        if not org.is_active:
            raise OrganizationSuspendedException(
                f"Organization {org.name} is currently suspended or inactive."
            )
        if org.monthly_pages_used + page_count > org.monthly_page_limit:
            raise QuotaExceededException(
                f"Organization {org.name} has exceeded its monthly limit of {org.monthly_page_limit} pages."
            )
        org.monthly_pages_used += page_count
        db.commit()
        return True

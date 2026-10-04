"""SQLAlchemy model for organization workspaces."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from app.db.database import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(128), nullable=False)
    domain = Column(String(128), nullable=True)
    contact_email = Column(String(128), nullable=False)
    tier = Column(String(32), default="school")
    monthly_page_limit = Column(Integer, default=5000)
    monthly_pages_used = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

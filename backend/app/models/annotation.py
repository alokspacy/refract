"""SQLAlchemy model for educator annotations and audit log."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, Enum as SQLEnum
from app.db.database import Base

class BlockAnnotation(Base):
    __tablename__ = "block_annotations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    variant_id = Column(String(36), nullable=False, index=True)
    block_id = Column(String(36), nullable=False, index=True)
    educator_id = Column(String(36), nullable=False)
    status = Column(String(32), default="pending")  # approved, flagged, revised
    comment = Column(Text, nullable=True)
    suggested_content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

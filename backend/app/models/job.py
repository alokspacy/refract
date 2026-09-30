import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), default="QUEUED", nullable=False, index=True)  # QUEUED, PROCESSING, COMPLETED, FAILED
    current_stage = Column(String(50), default="FOUNDATION", nullable=False)    # FOUNDATION (Phase 1)
    progress = Column(Float, default=0.0, nullable=False)                      # 0.0 to 100.0
    error_message = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    document = relationship("Document", back_populates="jobs")

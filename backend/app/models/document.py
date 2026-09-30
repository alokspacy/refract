import uuid
from datetime import datetime, timezone
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    storage_key = Column(String(255), unique=True, index=True, nullable=False)
    status = Column(String(50), default="UPLOADED", nullable=False, index=True)
    
    # Phase 2 Extraction & Normalization fields
    extraction_status = Column(String(50), default="PENDING", nullable=False, index=True)
    normalized_content = Column(JSON, nullable=True)
    extraction_warnings = Column(JSON, nullable=True)
    extracted_at = Column(DateTime(timezone=True), nullable=True)

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
    owner = relationship("User", back_populates="documents")
    jobs = relationship("ProcessingJob", back_populates="document", cascade="all, delete-orphan")

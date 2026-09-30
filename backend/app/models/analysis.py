import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from app.db.database import Base


class ContentAnalysis(Base):
    """
    Stores AI-extracted pedagogical and structural analysis of a normalized document.
    """
    __tablename__ = "content_analyses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    language = Column(String(10), nullable=False, default="en")
    subject = Column(String(100), nullable=True)
    grade_hint = Column(String(50), nullable=True)
    complexity = Column(String(50), nullable=False, default="intermediate")
    
    # Structured pedagogical metadata stored as JSON / JSONB
    learning_objectives = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)
    concepts = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)
    vocabulary = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)
    extra_metadata = Column(JSON().with_variant(JSONB, "postgresql"), nullable=True, default=dict)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

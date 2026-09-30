import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean, Float, Integer, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from app.db.database import Base


class GeneratedVariant(Base):
    """
    Represents an accessible learning transformation variant generated for a document.
    """
    __tablename__ = "generated_variants"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    status = Column(String(30), nullable=False, default="PENDING")  # PENDING, PROCESSING, COMPLETED, PARTIAL, FAILED
    
    profile_ids = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)
    profile_versions = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)
    metadata_overrides = Column(JSON().with_variant(JSONB, "postgresql"), nullable=True, default=dict)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class GeneratedBlock(Base):
    """
    A single generated accessible block linked with exact traceability to a source ContentBlock.
    """
    __tablename__ = "generated_blocks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    variant_id = Column(String(36), ForeignKey("generated_variants.id", ondelete="CASCADE"), nullable=False, index=True)
    source_block_id = Column(String(64), nullable=False, index=True)
    profile_id = Column(String(50), nullable=False, index=True)
    
    content = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)
    status = Column(String(30), nullable=False, default="PENDING")  # PENDING, PROCESSING, COMPLETED, FAILED
    
    prompt_version = Column(String(50), nullable=False, default="1.0.0")
    model = Column(String(100), nullable=False, default="mock-gpt-4o")
    provider = Column(String(50), nullable=False, default="mock")
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ValidationResult(Base):
    """
    Records the validation and grounding verification results for a generated variant or block.
    """
    __tablename__ = "validation_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    variant_id = Column(String(36), ForeignKey("generated_variants.id", ondelete="CASCADE"), nullable=False, index=True)
    block_id = Column(String(36), ForeignKey("generated_blocks.id", ondelete="CASCADE"), nullable=True, index=True)
    
    is_valid = Column(Boolean, nullable=False, default=True)
    grounded = Column(Boolean, nullable=False, default=True)
    
    unsupported_claims = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)
    warnings = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)
    errors = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class TransformationCache(Base):
    """
    Caches deterministic AI block transformations by source hash, profile version, prompt version, and model.
    """
    __tablename__ = "transformation_cache"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cache_key = Column(String(64), nullable=False, unique=True, index=True)  # SHA-256 hash
    source_hash = Column(String(64), nullable=False, index=True)
    profile_id = Column(String(50), nullable=False)
    profile_version = Column(String(50), nullable=False)
    prompt_version = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    
    content = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class ProviderUsage(Base):
    """
    Tracks token consumption and estimated API costs for LLM operations.
    """
    __tablename__ = "provider_usages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    operation = Column(String(100), nullable=False)
    
    prompt_tokens = Column(Integer, nullable=False, default=0)
    completion_tokens = Column(Integer, nullable=False, default=0)
    total_tokens = Column(Integer, nullable=False, default=0)
    estimated_cost_usd = Column(Float, nullable=False, default=0.0)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

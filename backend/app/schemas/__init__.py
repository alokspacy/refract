"""Schemas package exports."""
from app.schemas.auth import UserCreate, UserLogin, UserResponse, TokenResponse
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentListResponse
from app.schemas.content import ContentDocument, ContentBlock, Section, BlockType
from app.schemas.variant import GeneratedVariantResponse, GeneratedBlockResponse, ValidationResultResponse
from app.schemas.compliance import WCAGAuditReport, ComplianceViolation, WCAGLevel

__all__ = [
    "UserCreate", "UserLogin", "UserResponse", "TokenResponse",
    "DocumentCreate", "DocumentResponse", "DocumentListResponse",
    "ContentDocument", "ContentBlock", "Section", "BlockType",
    "GeneratedVariantResponse", "GeneratedBlockResponse", "ValidationResultResponse",
    "WCAGAuditReport", "ComplianceViolation", "WCAGLevel",
]

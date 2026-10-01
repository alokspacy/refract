"""Schemas package exports."""
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, UserResponse, TokenResponse
from app.schemas.document import DocumentResponse, DocumentListResponse
from app.schemas.content import ContentDocument, ContentBlock, Section, BlockType
from app.schemas.variant import GeneratedVariantResponse, GeneratedBlockResponse, ValidationResultResponse
from app.schemas.compliance import WCAGAuditReport, ComplianceViolation, WCAGLevel

__all__ = [
    "UserRegisterRequest", "UserLoginRequest", "UserResponse", "TokenResponse",
    "DocumentResponse", "DocumentListResponse",
    "ContentDocument", "ContentBlock", "Section", "BlockType",
    "GeneratedVariantResponse", "GeneratedBlockResponse", "ValidationResultResponse",
    "WCAGAuditReport", "ComplianceViolation", "WCAGLevel",
]

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ProfileInfoResponse(BaseModel):
    id: str
    name: str
    description: str
    version: str


class GeneratedVariantCreate(BaseModel):
    profile_ids: List[str] = Field(..., min_length=1, description="List of profile IDs to apply (dyslexia, cognitive, visual_basic)")
    metadata_overrides: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional teacher overrides for grade, language, etc.")


class GeneratedBlockResponse(BaseModel):
    id: str
    variant_id: str
    source_block_id: str
    profile_id: str
    content: Dict[str, Any]
    status: str
    prompt_version: str
    model: str
    provider: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ValidationResultResponse(BaseModel):
    id: str
    variant_id: str
    block_id: Optional[str] = None
    is_valid: bool
    grounded: bool
    unsupported_claims: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    created_at: datetime

    model_config = {"from_attributes": True}


class GeneratedVariantResponse(BaseModel):
    id: str
    document_id: str
    name: str
    status: str
    profile_ids: List[str]
    profile_versions: Dict[str, str]
    metadata_overrides: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    blocks_count: Optional[int] = 0

    model_config = {"from_attributes": True}


class VariantWithBlocksResponse(BaseModel):
    variant: GeneratedVariantResponse
    blocks: List[GeneratedBlockResponse]
    validation_summary: Optional[ValidationResultResponse] = None

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.api.auth import get_current_user
from app.schemas.variant import (
    GeneratedVariantResponse,
    GeneratedBlockResponse,
    ValidationResultResponse
)
from app.services.variant_service import get_variant_service

router = APIRouter(prefix="/variants", tags=["Accessible Variants"])


@router.get("/{variant_id}", response_model=GeneratedVariantResponse)
def get_variant_details(
    variant_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve metadata and processing status for an accessible variant.
    """
    service = get_variant_service()
    variant = service.get_variant_with_auth(db=db, variant_id=variant_id, user_id=current_user.id)
    blocks_count = len(variant.document.generated_variants) if hasattr(variant, 'document') else 0
    
    return GeneratedVariantResponse(
        id=variant.id,
        document_id=variant.document_id,
        name=variant.name,
        status=variant.status,
        profile_ids=variant.profile_ids or [],
        profile_versions=variant.profile_versions or {},
        metadata_overrides=variant.metadata_overrides,
        created_at=variant.created_at,
        updated_at=variant.updated_at,
        blocks_count=blocks_count
    )


@router.get("/{variant_id}/blocks", response_model=List[GeneratedBlockResponse])
def get_variant_blocks(
    variant_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all generated accessible blocks for a variant with source block traceability.
    """
    service = get_variant_service()
    blocks = service.get_variant_blocks(db=db, variant_id=variant_id, user_id=current_user.id)
    return [
        GeneratedBlockResponse.model_validate(b)
        for b in blocks
    ]


@router.get("/{variant_id}/validation", response_model=ValidationResultResponse)
def get_variant_validation(
    variant_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve validation and grounding verification results for a variant.
    """
    service = get_variant_service()
    val = service.get_variant_validation(db=db, variant_id=variant_id, user_id=current_user.id)
    return ValidationResultResponse(
        id=val.id,
        variant_id=val.variant_id,
        block_id=val.block_id,
        is_valid=val.is_valid,
        grounded=val.grounded,
        unsupported_claims=val.unsupported_claims or [],
        warnings=val.warnings or [],
        errors=val.errors or [],
        created_at=val.created_at
    )

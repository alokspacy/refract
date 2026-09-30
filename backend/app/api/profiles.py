from typing import List
from fastapi import APIRouter
from app.schemas.variant import ProfileInfoResponse
from app.profiles.registry import get_profile_registry

router = APIRouter(prefix="/profiles", tags=["Accessibility Profiles"])


@router.get("", response_model=List[ProfileInfoResponse])
def get_available_profiles():
    """
    Return all available Phase 3 accessibility transformation profiles.
    """
    registry = get_profile_registry()
    profiles = registry.list_profiles()
    return [
        ProfileInfoResponse(
            id=p.profile_id,
            name=p.name,
            description=p.description,
            version=p.version
        )
        for p in profiles
    ]

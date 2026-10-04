"""Schemas for multi-tenant institution workspaces and licensing."""
from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

class SubscriptionTier(str, Enum):
    FREE = "free"
    EDUCATOR = "educator"
    SCHOOL = "school"
    DISTRICT = "district"

class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    domain: Optional[str] = None
    contact_email: EmailStr
    tier: SubscriptionTier = SubscriptionTier.SCHOOL

class OrganizationResponse(BaseModel):
    id: str
    name: str
    domain: Optional[str] = None
    contact_email: str
    tier: SubscriptionTier
    monthly_page_limit: int
    monthly_pages_used: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

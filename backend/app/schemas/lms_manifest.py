"""Schemas for LMS standard export packages (SCORM 2004 / IMS Common Cartridge)."""
from typing import List
from pydantic import BaseModel, Field

class LMSResource(BaseModel):
    identifier: str
    type: str
    href: str

class LMSManifest(BaseModel):
    manifest_id: str
    title: str
    schema_version: str = "CAM 1.3"
    resources: List[LMSResource] = Field(default_factory=list)
    accessibility_conformance: str = "WCAG 2.2 Level AA"

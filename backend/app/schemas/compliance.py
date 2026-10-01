"""WCAG 2.2 accessibility compliance audit schema."""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class WCAGLevel(str, Enum):
    A = "A"
    AA = "AA"
    AAA = "AAA"

class WCAGPrinciple(str, Enum):
    PERCEIVABLE = "perceivable"
    OPERABLE = "operable"
    UNDERSTANDABLE = "understandable"
    ROBUST = "robust"

class ViolationSeverity(str, Enum):
    CRITICAL = "critical"
    SERIOUS = "serious"
    MODERATE = "moderate"
    MINOR = "minor"

class ComplianceViolation(BaseModel):
    rule_id: str
    criterion: str
    level: WCAGLevel
    severity: ViolationSeverity
    description: str
    block_id: Optional[str] = None
    page_or_slide: Optional[int] = None
    suggested_remediation: str

class ComplianceRuleResult(BaseModel):
    rule_id: str
    name: str
    criterion: str
    principle: WCAGPrinciple
    level: WCAGLevel
    passed: bool
    details: str

class WCAGAuditReport(BaseModel):
    document_id: Optional[str] = None
    variant_id: Optional[str] = None
    score: float = Field(..., ge=0.0, le=100.0, description="Overall compliance score out of 100")
    wcag_aa_compliant: bool
    wcag_aaa_compliant: bool
    passed_rules_count: int
    total_rules_count: int
    violations: List[ComplianceViolation] = Field(default_factory=list)
    remediation_recommendations: List[str] = Field(default_factory=list)
    evaluated_at: str

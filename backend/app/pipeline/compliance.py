"""WCAG 2.2 compliance evaluation pipeline."""
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.schemas.compliance import (
    WCAGAuditReport, ComplianceViolation, WCAGLevel,
    ViolationSeverity, WCAGPrinciple, ComplianceRuleResult
)
from app.schemas.content import ContentDocument, ContentBlock, BlockType

class WCAGComplianceEvaluator:
    """Evaluates ContentDocument or block collections against WCAG 2.2 AA/AAA rules."""

    def evaluate(self, doc: ContentDocument, variant_id: Optional[str] = None) -> WCAGAuditReport:
        violations: List[ComplianceViolation] = []
        rules_evaluated = 0
        rules_passed = 0

        all_blocks: List[ContentBlock] = []
        for sec in doc.sections:
            all_blocks.extend(sec.blocks)

        # 1. Non-text Content (1.1.1) - Image Alt Text
        rules_evaluated += 1
        img_violations = self._check_images(all_blocks)
        if not img_violations:
            rules_passed += 1
        else:
            violations.extend(img_violations)

        # 2. Headings and Labels (2.4.6) - Structural Hierarchy
        rules_evaluated += 1
        heading_violations = self._check_headings(all_blocks)
        if not heading_violations:
            rules_passed += 1
        else:
            violations.extend(heading_violations)

        # 3. Info and Relationships (1.3.1) - Tables & Lists
        rules_evaluated += 1
        struct_violations = self._check_structures(all_blocks)
        if not struct_violations:
            rules_passed += 1
        else:
            violations.extend(struct_violations)

        # 4. Reading Level (3.1.5) - Cognitive sentence complexity
        rules_evaluated += 1
        reading_violations = self._check_reading_complexity(all_blocks)
        if not reading_violations:
            rules_passed += 1
        else:
            violations.extend(reading_violations)

        score = round((rules_passed / max(rules_evaluated, 1)) * 100.0, 1)
        has_critical = any(v.severity == ViolationSeverity.CRITICAL for v in violations)
        has_serious = any(v.severity == ViolationSeverity.SERIOUS for v in violations)
        wcag_aa = not has_critical and not has_serious and score >= 80.0
        wcag_aaa = wcag_aa and len(violations) == 0 and score >= 95.0

        recs = [v.suggested_remediation for v in violations]
        if not recs:
            recs.append("Content adheres to tested WCAG 2.2 criteria.")

        return WCAGAuditReport(
            document_id=doc.id,
            variant_id=variant_id,
            score=score,
            wcag_aa_compliant=wcag_aa,
            wcag_aaa_compliant=wcag_aaa,
            passed_rules_count=rules_passed,
            total_rules_count=rules_evaluated,
            violations=violations,
            remediation_recommendations=recs,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )

    def _check_images(self, blocks: List[ContentBlock]) -> List[ComplianceViolation]:
        v = []
        for b in blocks:
            if b.type == BlockType.IMAGE:
                meta = b.metadata or {}
                alt = meta.get("alt") or meta.get("description") or b.source_text
                if not alt or len(str(alt).strip()) < 3:
                    v.append(ComplianceViolation(
                        rule_id="1.1.1",
                        criterion="Non-text Content",
                        level=WCAGLevel.A,
                        severity=ViolationSeverity.CRITICAL,
                        description="Image block is missing descriptive alternative text.",
                        block_id=b.id,
                        page_or_slide=b.page_or_slide,
                        suggested_remediation="Add concise, context-aware alt text describing image purpose.",
                    ))
        return v

    def _check_headings(self, blocks: List[ContentBlock]) -> List[ComplianceViolation]:
        v = []
        headings = [b for b in blocks if b.type == BlockType.HEADING]
        if not headings and len(blocks) > 5:
            v.append(ComplianceViolation(
                rule_id="2.4.6",
                criterion="Headings and Labels",
                level=WCAGLevel.AA,
                severity=ViolationSeverity.SERIOUS,
                description="Long document contains no heading landmarks for navigation.",
                suggested_remediation="Structure sections with descriptive H1, H2, and H3 headings.",
            ))
        return v

    def _check_structures(self, blocks: List[ContentBlock]) -> List[ComplianceViolation]:
        v = []
        for b in blocks:
            if b.type == BlockType.TABLE:
                meta = b.metadata or {}
                headers = meta.get("headers") or []
                if not headers:
                    v.append(ComplianceViolation(
                        rule_id="1.3.1",
                        criterion="Info and Relationships",
                        level=WCAGLevel.A,
                        severity=ViolationSeverity.SERIOUS,
                        description="Data table does not define explicit header row/columns.",
                        block_id=b.id,
                        page_or_slide=b.page_or_slide,
                        suggested_remediation="Mark first row or first column as table header (th).",
                    ))
        return v

    def _check_reading_complexity(self, blocks: List[ContentBlock]) -> List[ComplianceViolation]:
        v = []
        for b in blocks:
            if b.type == BlockType.PARAGRAPH and b.source_text:
                sentences = [s.strip() for s in b.source_text.split(".") if s.strip()]
                long_sentences = [s for s in sentences if len(s.split()) > 35]
                if long_sentences:
                    v.append(ComplianceViolation(
                        rule_id="3.1.5",
                        criterion="Reading Level",
                        level=WCAGLevel.AAA,
                        severity=ViolationSeverity.MODERATE,
                        description=f"Paragraph contains overly long sentence ({len(long_sentences[0].split())} words).",
                        block_id=b.id,
                        page_or_slide=b.page_or_slide,
                        suggested_remediation="Break compound sentences into shorter statements under 22 words.",
                    ))
        return v

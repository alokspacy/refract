"""Unit tests for WCAG compliance evaluation."""
import pytest
from app.pipeline.compliance import WCAGComplianceEvaluator
from app.schemas.compliance import ViolationSeverity
from tests.fixtures.compliance_samples import make_clean_document, make_violating_document

def test_clean_document_passes_wcag_aa():
    evaluator = WCAGComplianceEvaluator()
    doc = make_clean_document()
    report = evaluator.evaluate(doc)
    assert report.wcag_aa_compliant is True
    assert report.score >= 80.0
    assert len(report.violations) == 0

def test_violating_document_triggers_warnings():
    evaluator = WCAGComplianceEvaluator()
    doc = make_violating_document()
    report = evaluator.evaluate(doc)
    assert report.wcag_aa_compliant is False
    assert len(report.violations) > 0
    # Must flag image missing alt text
    rule_ids = [v.rule_id for v in report.violations]
    assert "1.1.1" in rule_ids
    # Must flag table missing headers
    assert "1.3.1" in rule_ids

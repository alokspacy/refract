"""Unit tests for organization quota enforcement."""
import pytest
from unittest.mock import MagicMock
from app.services.quota_service import QuotaService, QuotaExceededException
from app.models.organization import Organization

def test_quota_increment_under_limit():
    db = MagicMock()
    org = Organization(name="Greenwood High", monthly_page_limit=100, monthly_pages_used=20, is_active=True)
    db.query.return_value.filter.return_value.first.return_value = org

    res = QuotaService.check_and_increment(db, "org-1", page_count=5)
    assert res is True
    assert org.monthly_pages_used == 25

def test_quota_exceeded_raises_error():
    db = MagicMock()
    org = Organization(name="Greenwood High", monthly_page_limit=100, monthly_pages_used=98, is_active=True)
    db.query.return_value.filter.return_value.first.return_value = org

    with pytest.raises(QuotaExceededException):
        QuotaService.check_and_increment(db, "org-1", page_count=5)

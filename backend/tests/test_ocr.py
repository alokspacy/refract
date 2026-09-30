import pytest
from app.providers.mock_ocr import MockOCRProvider
from app.providers.ocr import get_ocr_provider


def test_mock_ocr_provider_extraction():
    provider = MockOCRProvider()
    results = provider.extract(b"dummy image bytes")

    assert len(results) >= 2
    assert all("text" in item for item in results)
    assert all("confidence" in item for item in results)
    assert all(item["confidence"] >= 0.90 for item in results)
    assert any("Photosynthesis" in item["text"] for item in results)


def test_get_ocr_provider_factory():
    provider_mock = get_ocr_provider("mock")
    assert isinstance(provider_mock, MockOCRProvider)

    provider_default = get_ocr_provider()
    assert isinstance(provider_default, MockOCRProvider)

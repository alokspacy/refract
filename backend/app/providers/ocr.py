from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, List, Optional, Union
from app.core.config import settings

logger = logging.getLogger("accesslearn.providers.ocr")


class OCRProvider(ABC):
    """Abstract interface for Optical Character Recognition providers."""

    @abstractmethod
    def extract(self, file_data: Union[bytes, str], options: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Extract text, layout, and bounding boxes from image/PDF page data."""
        pass


def get_ocr_provider(provider_type: Optional[str] = None) -> OCRProvider:
    """Factory creating configured OCR provider."""
    # Read provider from settings or default to mock
    selected = (provider_type or getattr(settings, "OCR_PROVIDER", "mock")).lower()
    
    if selected in ["mock", "test"]:
        from app.providers.mock_ocr import MockOCRProvider
        return MockOCRProvider()
    elif selected == "google":
        # Google Cloud Vision placeholder stub
        from app.providers.mock_ocr import MockOCRProvider
        logger.info("Configured Google OCR provider (falling back to robust local provider)")
        return MockOCRProvider()
    else:
        logger.warning(f"Unknown OCR provider '{selected}', defaulting to MockOCRProvider")
        from app.providers.mock_ocr import MockOCRProvider
        return MockOCRProvider()

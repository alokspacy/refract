import logging
from typing import Any, Dict, List, Optional, Union
from app.providers.ocr import OCRProvider

logger = logging.getLogger("accesslearn.providers.ocr.mock")


class MockOCRProvider(OCRProvider):
    """Mock OCR Provider for offline development and fast automated tests."""

    def extract(self, file_data: Union[bytes, str], options: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        logger.info("Executing Mock OCR text extraction")
        # Generate realistic educational text blocks with bounding boxes and confidence
        return [
            {
                "text": "Cellular Respiration and Photosynthesis",
                "bbox": [50.0, 40.0, 500.0, 70.0],
                "confidence": 0.98,
                "type": "heading"
            },
            {
                "text": "Photosynthesis is the biochemical process by which green plants and certain other organisms transform light energy into chemical energy stored in glucose molecules.",
                "bbox": [50.0, 80.0, 550.0, 140.0],
                "confidence": 0.96,
                "type": "paragraph"
            },
            {
                "text": "1. Light-dependent reactions convert sunlight and water into ATP and NADPH.",
                "bbox": [50.0, 150.0, 530.0, 180.0],
                "confidence": 0.94,
                "type": "list"
            },
            {
                "text": "2. The Calvin cycle uses ATP and NADPH to fix carbon dioxide into sugars.",
                "bbox": [50.0, 190.0, 530.0, 220.0],
                "confidence": 0.95,
                "type": "list"
            }
        ]

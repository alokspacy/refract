import io
import logging
import os
import uuid
from typing import Any, Dict, Optional
from PIL import Image as PILImage

from app.parsers.base import BaseParser, ExtractedAsset, ExtractedBlock, ExtractedDocument, ExtractedSection

logger = logging.getLogger("accesslearn.parsers.image")


class ImageParser(BaseParser):
    """Parser for standalone educational images (PNG, JPG, JPEG)."""

    def can_parse(self, mime_type: str, filename: str) -> bool:
        ext = os.path.splitext(filename)[1].lower().lstrip(".")
        return mime_type.startswith("image/") or ext in ["png", "jpg", "jpeg"]

    def parse(self, file_bytes: bytes, filename: str, options: Optional[Dict[str, Any]] = None) -> ExtractedDocument:
        logger.info(f"Starting image parsing for {filename} ({len(file_bytes)} bytes)")

        try:
            pil_img = PILImage.open(io.BytesIO(file_bytes))
            width, height = pil_img.size
            img_format = pil_img.format.lower() if pil_img.format else "png"
        except Exception as e:
            logger.error(f"Failed to open image file {filename}: {e}")
            raise ValueError(f"Corrupted or invalid image file: {e}")

        doc_title = os.path.splitext(filename)[0].replace("_", " ").title()
        asset_id = str(uuid.uuid4())

        asset = ExtractedAsset(
            asset_id=asset_id,
            type="image",
            filename=filename,
            mime_type=f"image/{img_format}",
            data_bytes=file_bytes,
            page_or_slide=1,
            metadata={"width": width, "height": height, "format": img_format}
        )

        image_block = ExtractedBlock(
            type="image",
            text=f"[Educational Image: {filename}]",
            page_or_slide=1,
            position=1,
            asset_id=asset_id,
            bbox=[0.0, 0.0, float(width), float(height)],
            metadata={"width": width, "height": height, "format": img_format, "source_type": "image"}
        )

        section = ExtractedSection(
            title=doc_title,
            blocks=[image_block],
            page_or_slide=1
        )

        extracted_doc = ExtractedDocument(
            title=doc_title,
            source_language="en",
            pages_or_slides_count=1,
            sections=[section],
            assets=[asset],
            metadata={"width": width, "height": height, "format": img_format, "source_type": "image"},
            requires_ocr=True,
            ocr_pages=[1]
        )

        logger.info(f"Image parsed: {width}x{height} {img_format}, flagged for OCR")
        return extracted_doc

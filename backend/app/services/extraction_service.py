from datetime import datetime, timezone
import logging
from typing import Any, Callable, Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.document import Document
from app.parsers.base import ExtractedBlock, ExtractedDocument, ExtractedSection
from app.parsers.registry import get_parser
from app.pipeline.normalize import normalize_document
from app.providers.ocr import OCRProvider, get_ocr_provider
from app.providers.storage import StorageProvider
from app.schemas.content import ContentDocument
from app.services.asset_service import AssetService

logger = logging.getLogger("accesslearn.services.extraction")


class ExtractionService:
    """Orchestrates document extraction, OCR fallback, normalization, and persistence."""

    def __init__(self, storage: StorageProvider, ocr_provider: Optional[OCRProvider] = None):
        self.storage = storage
        self.ocr_provider = ocr_provider or get_ocr_provider()

    def process_document(
        self,
        document: Document,
        db: Session,
        progress_callback: Optional[Callable[[str, int], None]] = None
    ) -> ContentDocument:
        logger.info(f"Starting extraction processing for Document ID={document.id} ({document.original_filename})")

        # Stage 1: Extraction (25%)
        if progress_callback:
            progress_callback("EXTRACTING", 25)

        document.extraction_status = "PROCESSING"
        document.status = "PROCESSING"
        db.commit()

        # Retrieve file bytes
        file_bytes = self.storage.get(document.storage_key)

        # Resolve Parser & Parse
        parser = get_parser(document.mime_type, document.original_filename)
        extracted_doc: ExtractedDocument = parser.parse(file_bytes, document.original_filename)

        # Persist extracted assets
        if extracted_doc.assets:
            AssetService.persist_extracted_assets(
                assets=extracted_doc.assets,
                user_id=document.owner_id,
                document_id=document.id,
                storage=self.storage
            )

        # Stage 2: OCR Fallback if required (50%)
        if extracted_doc.requires_ocr:
            logger.info(f"Document {document.id} requires OCR processing for pages {extracted_doc.ocr_pages}")
            if progress_callback:
                progress_callback("OCR", 50)

            try:
                # Execute OCR extraction
                ocr_results = self.ocr_provider.extract(file_bytes)
                logger.info(f"OCR completed: received {len(ocr_results)} text blocks")

                # Integrate OCR blocks into corresponding page section
                for item in ocr_results:
                    page_num = item.get("page", 1)
                    block_type = item.get("type", "paragraph")
                    ocr_block = ExtractedBlock(
                        type=block_type,
                        text=item.get("text", ""),
                        page_or_slide=page_num,
                        bbox=item.get("bbox"),
                        metadata={
                            "ocr_confidence": item.get("confidence", 0.95),
                            "is_ocr": True,
                            "source_type": "ocr"
                        }
                    )
                    
                    # Find or create corresponding section
                    target_sec = None
                    for sec in extracted_doc.sections:
                        if sec.page_or_slide == page_num:
                            target_sec = sec
                            break

                    if target_sec:
                        target_sec.blocks.append(ocr_block)
                    else:
                        extracted_doc.sections.append(
                            ExtractedSection(
                                title=f"Page {page_num} (OCR)",
                                blocks=[ocr_block],
                                page_or_slide=page_num
                            )
                        )

            except Exception as ocr_err:
                logger.error(f"OCR extraction failed for document {document.id}: {ocr_err}")
                extracted_doc.warnings.append(f"OCR processing failed: {str(ocr_err)}")

        # Stage 3: Normalization (75%)
        if progress_callback:
            progress_callback("NORMALIZING", 75)

        content_doc = normalize_document(extracted_doc, document_id=document.id)

        # Stage 4: Store & Complete
        document.normalized_content = content_doc.model_dump()
        document.extraction_warnings = extracted_doc.warnings
        document.extraction_status = "COMPLETED"
        document.status = "READY"
        document.extracted_at = datetime.now(timezone.utc)
        db.commit()

        if progress_callback:
            progress_callback("COMPLETED", 100)

        logger.info(f"Document {document.id} extraction & normalization completed successfully")
        return content_doc

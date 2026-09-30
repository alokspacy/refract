import logging
import uuid
from typing import Optional
from app.parsers.base import ExtractedDocument
from app.schemas.content import BlockType, ContentBlock, ContentDocument, Section

logger = logging.getLogger("accesslearn.pipeline.normalize")


class Normalizer:
    """Converts intermediate ExtractedDocument into strict ContentDocument JSON representation."""

    @staticmethod
    def normalize(extracted_doc: ExtractedDocument, document_id: Optional[str] = None) -> ContentDocument:
        logger.info(f"Normalizing ExtractedDocument '{extracted_doc.title}' (sections={len(extracted_doc.sections)})")

        doc_id = document_id or str(uuid.uuid4())
        normalized_sections = []

        for sec_idx, ext_sec in enumerate(extracted_doc.sections):
            section_id = ext_sec.id if ext_sec.id else str(uuid.uuid4())
            normalized_blocks = []

            for blk_idx, ext_blk in enumerate(ext_sec.blocks):
                # Safe BlockType mapping
                try:
                    block_type = BlockType(ext_blk.type.lower())
                except ValueError:
                    logger.warning(f"Unknown block type '{ext_blk.type}', falling back to PARAGRAPH")
                    block_type = BlockType.PARAGRAPH

                block_id = ext_blk.id if ext_blk.id else str(uuid.uuid4())
                
                # Assemble metadata with full traceability
                block_meta = dict(ext_blk.metadata) if ext_blk.metadata else {}
                if ext_blk.bbox:
                    block_meta["bbox"] = ext_blk.bbox
                if ext_blk.position is not None:
                    block_meta["order"] = ext_blk.position
                else:
                    block_meta["order"] = blk_idx + 1

                content_block = ContentBlock(
                    id=block_id,
                    type=block_type,
                    source_text=ext_blk.text,
                    source_asset_id=ext_blk.asset_id,
                    page_or_slide=ext_blk.page_or_slide,
                    metadata=block_meta,
                    accessibility_annotations={}
                )
                normalized_blocks.append(content_block)

            normalized_sections.append(
                Section(
                    id=section_id,
                    title=ext_sec.title or f"Section {sec_idx + 1}",
                    blocks=normalized_blocks
                )
            )

        # Fallback if no sections were created
        if not normalized_sections:
            normalized_sections.append(
                Section(
                    id=str(uuid.uuid4()),
                    title=extracted_doc.title,
                    blocks=[]
                )
            )

        content_doc = ContentDocument(
            schema_version="1.0.0",
            id=doc_id,
            title=extracted_doc.title,
            source_language=extracted_doc.source_language or "en",
            subject=None,
            grade_hint=None,
            learning_objectives=[],
            glossary={},
            sections=normalized_sections
        )

        logger.info(f"Normalization complete for document {doc_id}: {len(normalized_sections)} sections")
        return content_doc


def normalize_document(extracted_doc: ExtractedDocument, document_id: Optional[str] = None) -> ContentDocument:
    return Normalizer.normalize(extracted_doc, document_id)

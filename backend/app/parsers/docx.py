import io
import logging
import os
import uuid
from typing import Any, Dict, List, Optional
import docx
from docx.document import Document as DocxDocument
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph

from app.parsers.base import BaseParser, ExtractedAsset, ExtractedBlock, ExtractedDocument, ExtractedSection

logger = logging.getLogger("accesslearn.parsers.docx")


class DOCXParser(BaseParser):
    """Parser for Microsoft Word (.docx) documents."""

    def can_parse(self, mime_type: str, filename: str) -> bool:
        ext = os.path.splitext(filename)[1].lower().lstrip(".")
        return "wordprocessingml" in mime_type or mime_type == "application/msword" or ext in ["docx", "doc"]

    def parse(self, file_bytes: bytes, filename: str, options: Optional[Dict[str, Any]] = None) -> ExtractedDocument:
        logger.info(f"Starting DOCX parsing for {filename} ({len(file_bytes)} bytes)")
        
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
        except Exception as e:
            logger.error(f"Failed to open DOCX document {filename}: {e}")
            raise ValueError(f"Corrupted or invalid DOCX document: {e}")

        # Extract title from core properties or filename
        title = doc.core_properties.title if doc.core_properties and doc.core_properties.title else None
        if not title or not title.strip():
            title = os.path.splitext(filename)[0].replace("_", " ").title()

        extracted_doc = ExtractedDocument(
            title=title,
            source_language="en",
            pages_or_slides_count=1,
            metadata={
                "source_type": "docx",
                "author": doc.core_properties.author if doc.core_properties else None,
                "created": str(doc.core_properties.created) if doc.core_properties and doc.core_properties.created else None,
            }
        )

        all_assets: List[ExtractedAsset] = []
        current_section = ExtractedSection(title=title, blocks=[], page_or_slide=1)
        sections: List[ExtractedSection] = []

        # Extract embedded images from document parts
        extracted_rids = {}
        for r_id, rel in doc.part.rels.items():
            if "image" in rel.target_ref:
                try:
                    img_part = rel.target_part
                    img_bytes = img_part.blob
                    img_name = os.path.basename(rel.target_ref)
                    ext = os.path.splitext(img_name)[1].lstrip(".").lower() or "png"
                    asset_id = str(uuid.uuid4())
                    asset = ExtractedAsset(
                        asset_id=asset_id,
                        type="image",
                        filename=f"docx_img_{len(all_assets) + 1}.{ext}",
                        mime_type=f"image/{ext}",
                        data_bytes=img_bytes,
                        page_or_slide=1,
                        metadata={"docx_part": img_name}
                    )
                    all_assets.append(asset)
                    extracted_rids[r_id] = asset
                except Exception as rel_err:
                    logger.warning(f"Failed to extract image relation {r_id}: {rel_err}")

        # Iterate through paragraphs and tables in document body order
        position = 1
        for child in doc.element.body:
            if isinstance(child, CT_P):
                p = Paragraph(child, doc)
                text = p.text.strip()
                style_name = p.style.name if p.style else ""

                # Check for embedded drawing / image references in paragraph xml
                for r_id in child.xpath('.//a:blip/@r:embed'):
                    if r_id in extracted_rids:
                        asset = extracted_rids[r_id]
                        current_section.blocks.append(
                            ExtractedBlock(
                                type="image",
                                text="[Embedded Document Image]",
                                page_or_slide=1,
                                position=position,
                                asset_id=asset.asset_id,
                                metadata={"asset_filename": asset.filename, "source_type": "docx"}
                            )
                        )
                        position += 1

                if not text:
                    continue

                # Heading detection
                if style_name.startswith("Heading") or style_name.lower().startswith("title"):
                    # Extract heading level
                    level = 1
                    try:
                        level = int(style_name.split()[-1])
                    except (ValueError, IndexError):
                        level = 1

                    # Start new section on major headings (Heading 1) if current section has blocks
                    if level == 1 and current_section.blocks:
                        sections.append(current_section)
                        current_section = ExtractedSection(title=text, blocks=[], page_or_slide=1)

                    current_section.blocks.append(
                        ExtractedBlock(
                            type="heading",
                            text=text,
                            page_or_slide=1,
                            position=position,
                            metadata={"heading_level": level, "style_name": style_name, "source_type": "docx"}
                        )
                    )
                    position += 1

                # List detection
                elif style_name.startswith("List") or text.startswith(("•", "-", "*", "–")):
                    current_section.blocks.append(
                        ExtractedBlock(
                            type="list",
                            text=text,
                            page_or_slide=1,
                            position=position,
                            metadata={"style_name": style_name, "source_type": "docx"}
                        )
                    )
                    position += 1

                # Paragraph
                else:
                    current_section.blocks.append(
                        ExtractedBlock(
                            type="paragraph",
                            text=text,
                            page_or_slide=1,
                            position=position,
                            metadata={"style_name": style_name, "source_type": "docx"}
                        )
                    )
                    position += 1

            elif isinstance(child, CT_Tbl):
                table = Table(child, doc)
                matrix = []
                for row in table.rows:
                    row_cells = [cell.text.strip() for cell in row.cells]
                    # De-duplicate merged cells in python-docx
                    matrix.append(row_cells)

                if matrix:
                    headers = matrix[0] if len(matrix) > 1 else []
                    rows = matrix[1:] if len(matrix) > 1 else matrix
                    current_section.blocks.append(
                        ExtractedBlock(
                            type="table",
                            page_or_slide=1,
                            position=position,
                            metadata={
                                "headers": headers,
                                "rows": rows,
                                "row_count": len(matrix),
                                "col_count": len(matrix[0]) if matrix else 0,
                                "source_type": "docx"
                            }
                        )
                    )
                    position += 1

        if current_section.blocks:
            sections.append(current_section)

        if not sections:
            sections.append(ExtractedSection(title=title, blocks=[], page_or_slide=1))

        extracted_doc.sections = sections
        extracted_doc.assets = all_assets
        logger.info(f"DOCX parsed: {len(sections)} sections, {len(all_assets)} assets")
        return extracted_doc

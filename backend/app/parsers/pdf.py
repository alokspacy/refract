import logging
import os
import uuid
from typing import Any, Dict, List, Optional
import fitz  # PyMuPDF

from app.parsers.base import BaseParser, ExtractedAsset, ExtractedBlock, ExtractedDocument, ExtractedSection

logger = logging.getLogger("accesslearn.parsers.pdf")


class PDFParser(BaseParser):
    """Primary parser for PDF educational documents using PyMuPDF."""

    def can_parse(self, mime_type: str, filename: str) -> bool:
        ext = os.path.splitext(filename)[1].lower().lstrip(".")
        return mime_type == "application/pdf" or ext == "pdf"

    def parse(self, file_bytes: bytes, filename: str, options: Optional[Dict[str, Any]] = None) -> ExtractedDocument:
        logger.info(f"Starting PDF parsing for {filename} ({len(file_bytes)} bytes)")
        
        try:
            pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
        except Exception as e:
            logger.error(f"Failed to open PDF document {filename}: {e}")
            raise ValueError(f"Corrupted or unreadable PDF document: {e}")

        if pdf_doc.is_encrypted:
            logger.warning(f"Encrypted PDF detected: {filename}")
            raise ValueError("Encrypted or password-protected PDF files cannot be processed without credentials.")

        doc_title = pdf_doc.metadata.get("title") if pdf_doc.metadata else None
        if not doc_title or not doc_title.strip():
            doc_title = os.path.splitext(filename)[0].replace("_", " ").title()

        extracted_doc = ExtractedDocument(
            title=doc_title,
            source_language="en",
            pages_or_slides_count=len(pdf_doc),
            metadata={
                "source_type": "pdf",
                "page_count": len(pdf_doc),
                "pdf_metadata": {k: str(v) for k, v in (pdf_doc.metadata or {}).items() if v}
            }
        )

        all_sections: List[ExtractedSection] = []
        all_assets: List[ExtractedAsset] = []
        ocr_pages: List[int] = []

        for page_idx in range(len(pdf_doc)):
            page_num = page_idx + 1
            page = pdf_doc[page_idx]
            page_rect = page.rect
            page_width, page_height = page_rect.width, page_rect.height

            section_blocks: List[ExtractedBlock] = []
            page_text_len = 0

            # 1. Extract structured text using PyMuPDF dict mode
            text_dict = page.get_text("dict")
            blocks = text_dict.get("blocks", [])

            # Compute median font size on page to detect headings
            font_sizes = []
            for b in blocks:
                if "lines" in b:
                    for line in b["lines"]:
                        for span in line.get("spans", []):
                            if span.get("text", "").strip():
                                font_sizes.append(span.get("size", 10.0))
            median_size = (sum(font_sizes) / len(font_sizes)) if font_sizes else 11.0

            # 2. Extract Tables (PyMuPDF table detection)
            table_bboxes = []
            try:
                tables = page.find_tables()
                if tables and hasattr(tables, "tables"):
                    for tbl in tables.tables:
                        t_bbox = list(tbl.bbox)
                        table_bboxes.append(t_bbox)
                        extracted_table = tbl.extract()
                        if extracted_table:
                            headers = extracted_table[0] if len(extracted_table) > 1 else []
                            rows = extracted_table[1:] if len(extracted_table) > 1 else extracted_table
                            section_blocks.append(
                                ExtractedBlock(
                                    type="table",
                                    page_or_slide=page_num,
                                    position=len(section_blocks) + 1,
                                    bbox=[round(coord, 2) for coord in t_bbox],
                                    metadata={
                                        "headers": headers,
                                        "rows": rows,
                                        "row_count": len(extracted_table),
                                        "col_count": len(headers) if headers else (len(extracted_table[0]) if extracted_table else 0),
                                        "source_type": "pdf"
                                    }
                                )
                            )
            except Exception as tbl_err:
                logger.warning(f"Table detection skipped on page {page_num}: {tbl_err}")

            # Helper to test if a block overlaps with an extracted table
            def is_inside_table(bbox):
                for tb in table_bboxes:
                    if (bbox[0] >= tb[0] - 2 and bbox[1] >= tb[1] - 2 and 
                        bbox[2] <= tb[2] + 2 and bbox[3] <= tb[3] + 2):
                        return True
                return False

            # 3. Process Text Blocks
            for b in blocks:
                b_type = b.get("type", 0)
                bbox = [round(coord, 2) for coord in b.get("bbox", [0, 0, 0, 0])]

                if is_inside_table(bbox):
                    continue

                if b_type == 0:  # Text block
                    block_text_lines = []
                    max_block_font_size = 0.0
                    is_bold = False

                    for line in b.get("lines", []):
                        line_text = "".join(span.get("text", "") for span in line.get("spans", []))
                        for span in line.get("spans", []):
                            max_block_font_size = max(max_block_font_size, span.get("size", 0.0))
                            if "bold" in span.get("font", "").lower() or span.get("flags", 0) & 2:
                                is_bold = True
                        if line_text.strip():
                            block_text_lines.append(line_text.strip())

                    full_text = " ".join(block_text_lines).strip()
                    if not full_text:
                        continue

                    page_text_len += len(full_text)

                    # Determine block type
                    # Heading heuristic: font size noticeably larger than median or bold on short standalone line
                    if (max_block_font_size >= median_size * 1.25 or (is_bold and len(full_text) < 100)) and len(full_text) < 200:
                        level = 1 if max_block_font_size >= median_size * 1.5 else (2 if max_block_font_size >= median_size * 1.2 else 3)
                        section_blocks.append(
                            ExtractedBlock(
                                type="heading",
                                text=full_text,
                                page_or_slide=page_num,
                                position=len(section_blocks) + 1,
                                bbox=bbox,
                                metadata={"heading_level": level, "font_size": max_block_font_size, "source_type": "pdf"}
                            )
                        )
                    # List heuristic: starts with bullet, dash, or numbered prefix or contains bullet lines
                    elif (
                        any(line.strip().startswith(("•", "-", "*", "–", "—", "\u2022", "\u25cf", "\u25cb", "\u25aa")) for line in block_text_lines)
                        or full_text.lstrip().startswith(("•", "-", "*", "–", "—", "\u2022"))
                        or (len(full_text) > 3 and full_text[0].isdigit() and full_text[1:3] in [". ", ") "])
                    ):
                        section_blocks.append(
                            ExtractedBlock(
                                type="list",
                                text=full_text,
                                page_or_slide=page_num,
                                position=len(section_blocks) + 1,
                                bbox=bbox,
                                metadata={"source_type": "pdf"}
                            )
                        )
                    else:
                        section_blocks.append(
                            ExtractedBlock(
                                type="paragraph",
                                text=full_text,
                                page_or_slide=page_num,
                                position=len(section_blocks) + 1,
                                bbox=bbox,
                                metadata={"source_type": "pdf"}
                            )
                        )

            # 4. Extract Embedded Images
            image_list = page.get_images(full=True)
            for img_idx, img_info in enumerate(image_list):
                xref = img_info[0]
                try:
                    base_img = pdf_doc.extract_image(xref)
                    img_bytes = base_img.get("image")
                    img_ext = base_img.get("ext", "png")
                    if img_bytes and len(img_bytes) > 500:  # Skip tiny icons/decorations
                        asset_id = str(uuid.uuid4())
                        asset = ExtractedAsset(
                            asset_id=asset_id,
                            type="image",
                            filename=f"page_{page_num}_img_{img_idx + 1}.{img_ext}",
                            mime_type=f"image/{img_ext}",
                            data_bytes=img_bytes,
                            page_or_slide=page_num,
                            metadata={"width": base_img.get("width"), "height": base_img.get("height")}
                        )
                        all_assets.append(asset)
                        section_blocks.append(
                            ExtractedBlock(
                                type="image",
                                text=f"[Image on page {page_num}]",
                                page_or_slide=page_num,
                                position=len(section_blocks) + 1,
                                asset_id=asset_id,
                                metadata={
                                    "asset_filename": asset.filename,
                                    "width": base_img.get("width"),
                                    "height": base_img.get("height"),
                                    "source_type": "pdf"
                                }
                            )
                        )
                except Exception as img_err:
                    logger.warning(f"Could not extract image xref {xref} on page {page_num}: {img_err}")
                    extracted_doc.warnings.append(f"Page {page_num}: image extraction failed for xref {xref}.")

            # 5. Check if Page Requires OCR Fallback (Text-poor or scanned page)
            if page_text_len < 50 and len(image_list) > 0:
                logger.info(f"Page {page_num} flagged for OCR: text_len={page_text_len}, images={len(image_list)}")
                ocr_pages.append(page_num)
                extracted_doc.warnings.append(f"Page {page_num} contains minimal selectable text ({page_text_len} chars) and was marked for OCR fallback.")

            # Create page section
            section_title = f"Page {page_num}"
            # If first block is a heading, use it as title
            if section_blocks and section_blocks[0].type == "heading" and section_blocks[0].text:
                section_title = f"Page {page_num}: {section_blocks[0].text}"

            all_sections.append(
                ExtractedSection(
                    title=section_title,
                    blocks=section_blocks,
                    page_or_slide=page_num
                )
            )

        extracted_doc.sections = all_sections
        extracted_doc.assets = all_assets
        extracted_doc.ocr_pages = ocr_pages
        extracted_doc.requires_ocr = len(ocr_pages) > 0

        logger.info(f"PDF parsed: {len(all_sections)} pages/sections, {len(all_assets)} assets, requires_ocr={extracted_doc.requires_ocr}")
        return extracted_doc

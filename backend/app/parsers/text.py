import logging
import os
import re
from typing import Any, Dict, Optional

from app.parsers.base import BaseParser, ExtractedBlock, ExtractedDocument, ExtractedSection

logger = logging.getLogger("accesslearn.parsers.text")


class TextParser(BaseParser):
    """Parser for plain text (.txt) educational documents."""

    def can_parse(self, mime_type: str, filename: str) -> bool:
        ext = os.path.splitext(filename)[1].lower().lstrip(".")
        return mime_type == "text/plain" or ext in ["txt", "text", "md"]

    def parse(self, file_bytes: bytes, filename: str, options: Optional[Dict[str, Any]] = None) -> ExtractedDocument:
        logger.info(f"Starting plain text parsing for {filename} ({len(file_bytes)} bytes)")

        # Safe encoding detection
        text = None
        for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
            try:
                text = file_bytes.decode(enc)
                break
            except UnicodeDecodeError:
                continue

        if text is None:
            text = file_bytes.decode("utf-8", errors="replace")

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        raw_paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

        doc_title = os.path.splitext(filename)[0].replace("_", " ").title()
        if raw_paragraphs and len(raw_paragraphs[0]) < 80 and "\n" not in raw_paragraphs[0]:
            clean_first = raw_paragraphs[0].lstrip("#= ").strip()
            if clean_first:
                doc_title = clean_first

        blocks = []
        for idx, para in enumerate(raw_paragraphs):
            pos = idx + 1
            # Check for heading heuristic (short line, no period at end, or markdown heading)
            if para.startswith(("#", "==")) or (len(para) < 80 and not para.endswith((".", "!", "?")) and "\n" not in para):
                clean_heading = para.lstrip("#=").strip()
                blocks.append(
                    ExtractedBlock(
                        type="heading",
                        text=clean_heading,
                        page_or_slide=1,
                        position=pos,
                        metadata={"heading_level": 1 if idx == 0 else 2, "source_type": "text"}
                    )
                )
            # Check for list
            elif any(line.strip().startswith(("•", "-", "*", "1.", "2.", "3.")) for line in para.split("\n")):
                blocks.append(
                    ExtractedBlock(
                        type="list",
                        text=para,
                        page_or_slide=1,
                        position=pos,
                        metadata={"source_type": "text"}
                    )
                )
            else:
                blocks.append(
                    ExtractedBlock(
                        type="paragraph",
                        text=para,
                        page_or_slide=1,
                        position=pos,
                        metadata={"source_type": "text"}
                    )
                )

        section = ExtractedSection(
            title=doc_title,
            blocks=blocks,
            page_or_slide=1
        )

        extracted_doc = ExtractedDocument(
            title=doc_title,
            source_language="en",
            pages_or_slides_count=1,
            sections=[section],
            metadata={"source_type": "text", "paragraph_count": len(blocks)}
        )

        logger.info(f"Text parsed: {len(blocks)} blocks")
        return extracted_doc

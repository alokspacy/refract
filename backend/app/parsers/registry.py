import logging
from typing import List, Optional
from app.parsers.base import BaseParser
from app.parsers.pdf import PDFParser
from app.parsers.docx import DOCXParser
from app.parsers.pptx import PPTXParser
from app.parsers.image import ImageParser
from app.parsers.text import TextParser

logger = logging.getLogger("accesslearn.parsers.registry")


class ParserRegistry:
    """Registry maintaining available document parsers and resolving appropriate parser."""

    def __init__(self):
        self._parsers: List[BaseParser] = [
            PDFParser(),
            DOCXParser(),
            PPTXParser(),
            ImageParser(),
            TextParser(),
        ]

    def register_parser(self, parser: BaseParser):
        self._parsers.insert(0, parser)

    def get_parser(self, mime_type: str, filename: str) -> BaseParser:
        for parser in self._parsers:
            if parser.can_parse(mime_type, filename):
                logger.debug(f"Resolved parser {parser.__class__.__name__} for {filename} ({mime_type})")
                return parser

        logger.error(f"No parser found for MIME '{mime_type}' and file '{filename}'")
        raise ValueError(f"Unsupported document format for extraction: '{mime_type}' ({filename})")


# Singleton instance
parser_registry = ParserRegistry()


def get_parser(mime_type: str, filename: str) -> BaseParser:
    return parser_registry.get_parser(mime_type, filename)

"""Normalizer pipeline: converts ExtractedDocument to ContentDocument JSON."""
from typing import List
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

class ContentNormalizer:
    """Normalizes extracted content into stable ContentDocument schema."""

    def normalize(self, title: str, sections_data: List[dict]) -> ContentDocument:
        cleaned_sections: List[Section] = []

        for s in sections_data:
            blocks: List[ContentBlock] = []
            for b in s.get("blocks", []):
                # Ensure text is clean and type is valid
                b_type = b.get("type", "paragraph")
                blocks.append(ContentBlock(
                    type=BlockType(b_type),
                    source_text=b.get("source_text", "").strip(),
                    metadata=b.get("metadata", {})
                ))

            # Only preserve section if it has blocks or a distinct title
            if blocks or s.get("title"):
                cleaned_sections.append(Section(
                    title=s.get("title"),
                    blocks=blocks
                ))

        if not cleaned_sections:
            cleaned_sections.append(Section(title="Main", blocks=[]))

        return ContentDocument(
            title=title,
            sections=cleaned_sections
        )

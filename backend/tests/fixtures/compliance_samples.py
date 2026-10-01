"""Test fixtures for WCAG accessibility evaluation."""
from app.schemas.content import ContentDocument, ContentBlock, Section, BlockType

def make_clean_document() -> ContentDocument:
    return ContentDocument(
        title="Accessible Science Unit",
        sections=[
            Section(
                title="Introduction",
                blocks=[
                    ContentBlock(type=BlockType.HEADING, source_text="Photosynthesis Basics"),
                    ContentBlock(type=BlockType.PARAGRAPH, source_text="Plants convert light into chemical energy."),
                    ContentBlock(
                        type=BlockType.IMAGE,
                        source_text="Leaf diagram",
                        metadata={"alt": "Cross section diagram of plant leaf showing chloroplasts"}
                    ),
                    ContentBlock(
                        type=BlockType.TABLE,
                        source_text="Inputs and outputs",
                        metadata={"headers": ["Input", "Output"], "rows": [["CO2 + Light", "Glucose + O2"]]}
                    )
                ]
            )
        ]
    )

def make_violating_document() -> ContentDocument:
    return ContentDocument(
        title="Unstructured Document",
        sections=[
            Section(
                title="Bad Section",
                blocks=[
                    ContentBlock(type=BlockType.PARAGRAPH, source_text="No headings in this entire block collection."),
                    ContentBlock(type=BlockType.IMAGE, source_text="", metadata={}),
                    ContentBlock(type=BlockType.TABLE, source_text="", metadata={})
                ]
            )
        ]
    )

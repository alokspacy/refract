"""Service extracting structured heading outlines for screen reader navigation."""
from app.schemas.content import ContentDocument, BlockType
from app.schemas.outline import DocumentOutline, HeadingEntry

class OutlineService:
    def extract_outline(self, doc: ContentDocument) -> DocumentOutline:
        entries = []
        char_counter = 0

        for sec in doc.sections:
            for b in sec.blocks:
                text_len = len(b.source_text) if b.source_text else 0
                if b.type == BlockType.HEADING and b.source_text:
                    lvl = 2
                    if b.metadata and "level" in b.metadata:
                        lvl = int(b.metadata["level"])
                    entries.append(HeadingEntry(
                        block_id=b.id,
                        level=lvl,
                        title=b.source_text.strip(),
                        section_title=sec.title,
                        character_offset=char_counter
                    ))
                char_counter += text_len

        return DocumentOutline(
            document_id=doc.id,
            title=doc.title,
            total_headings=len(entries),
            headings=entries
        )

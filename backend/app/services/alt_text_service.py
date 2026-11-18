"""Service auditing and generating accessible alt-text for document figures."""
from typing import List
from app.schemas.content import ContentDocument, BlockType
from app.schemas.alt_text import ImageDescriptionItem, DocumentAltTextReport

class AltTextService:
    def audit_and_generate(self, doc: ContentDocument) -> DocumentAltTextReport:
        items: List[ImageDescriptionItem] = []
        missing_count = 0

        for sec in doc.sections:
            for b in sec.blocks:
                if b.type == BlockType.IMAGE:
                    meta_alt = b.metadata.get("alt_text") if b.metadata else None
                    annot_alt = b.accessibility_annotations.get("alt_text") if b.accessibility_annotations else None
                    existing_alt = (meta_alt or annot_alt or b.source_text or "").strip()
                    if not existing_alt:
                        missing_count += 1
                        generated_alt = f"Educational diagram in section {sec.title or doc.title}"
                    else:
                        generated_alt = existing_alt[:125]

                    items.append(ImageDescriptionItem(
                        block_id=b.id,
                        short_alt=generated_alt,
                        long_description=f"Contextual illustration supporting {sec.title or doc.title}.",
                        is_decorative=False,
                        detected_labels=[sec.title or "diagram", "educational"]
                    ))

        return DocumentAltTextReport(
            document_id=doc.id,
            total_images=len(items),
            missing_alt_count=missing_count,
            items=items
        )

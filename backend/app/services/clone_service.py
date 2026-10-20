"""Service deep copying documents and regenerating block UUIDs."""
import uuid
import copy
from app.schemas.content import ContentDocument, Section, ContentBlock
from app.schemas.clone import DocumentCloneResponse

class DocumentCloneService:
    @staticmethod
    def clone_document(doc: ContentDocument, new_title: str = None) -> (ContentDocument, DocumentCloneResponse):
        new_id = str(uuid.uuid4())
        cloned_title = new_title or f"{doc.title} (Clone)"

        cloned_sections = []
        copied_blocks = 0

        for sec in doc.sections:
            new_blocks = []
            for b in sec.blocks:
                new_b = copy.deepcopy(b)
                new_b.id = str(uuid.uuid4())
                new_blocks.append(new_b)
                copied_blocks += 1

            new_sec = Section(
                id=str(uuid.uuid4()),
                title=sec.title,
                blocks=new_blocks
            )
            cloned_sections.append(new_sec)

        cloned_doc = ContentDocument(
            schema_version=doc.schema_version,
            id=new_id,
            title=cloned_title,
            source_language=doc.source_language,
            subject=doc.subject,
            grade_hint=doc.grade_hint,
            learning_objectives=list(doc.learning_objectives),
            glossary=dict(doc.glossary),
            sections=cloned_sections
        )

        res = DocumentCloneResponse(
            original_document_id=doc.id,
            cloned_document_id=new_id,
            cloned_title=cloned_title,
            total_blocks_copied=copied_blocks
        )
        return cloned_doc, res

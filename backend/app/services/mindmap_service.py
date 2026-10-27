"""Concept mindmap generation service."""
import uuid
from app.schemas.content import ContentDocument, BlockType
from app.schemas.mindmap import MindMapNode

class MindMapService:
    """Extracts structural hierarchies into hierarchical concept mind map trees."""

    def build_mindmap(self, doc: ContentDocument) -> MindMapNode:
        root_title = doc.title.strip() if doc.title and doc.title.strip() else "Document Mindmap"
        root = MindMapNode(
            node_id="root",
            label=root_title,
            node_type="root",
            children=[]
        )

        if not doc.sections:
            return root

        for sec in doc.sections:
            sec_node = MindMapNode(
                node_id=str(uuid.uuid4())[:8],
                label=sec.title.strip() if sec.title and sec.title.strip() else "Section",
                node_type="section",
                children=[]
            )

            heading_found = False
            for b in sec.blocks:
                if b.type == BlockType.HEADING and b.source_text and b.source_text.strip():
                    heading_found = True
                    sec_node.children.append(MindMapNode(
                        node_id=str(uuid.uuid4())[:8],
                        label=b.source_text.strip(),
                        node_type="concept"
                    ))

            # Fallback concept if section has only paragraphs
            if not heading_found:
                for b in sec.blocks:
                    if b.type == BlockType.PARAGRAPH and b.source_text and b.source_text.strip():
                        preview = b.source_text.strip()[:40]
                        sec_node.children.append(MindMapNode(
                            node_id=str(uuid.uuid4())[:8],
                            label=f"{preview}...",
                            node_type="concept"
                        ))
                        break

            root.children.append(sec_node)

        return root

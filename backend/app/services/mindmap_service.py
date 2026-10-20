"""Concept mindmap generation service."""
import uuid
from app.schemas.content import ContentDocument, BlockType
from app.schemas.mindmap import MindMapNode

class MindMapService:
    """Extracts structural hierarchies into hierarchical concept mind map trees."""

    def build_mindmap(self, doc: ContentDocument) -> MindMapNode:
        root = MindMapNode(
            node_id="root",
            label=doc.title,
            node_type="root",
            children=[]
        )

        for sec in doc.sections:
            sec_node = MindMapNode(
                node_id=str(uuid.uuid4())[:8],
                label=sec.title or "Section",
                node_type="section",
                children=[]
            )

            for b in sec.blocks:
                if b.type == BlockType.HEADING and b.source_text:
                    sec_node.children.append(MindMapNode(
                        node_id=str(uuid.uuid4())[:8],
                        label=b.source_text,
                        node_type="concept"
                    ))

            root.children.append(sec_node)

        return root

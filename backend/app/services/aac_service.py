"""Service generating core and fringe vocabulary AAC symbol boards from lessons."""
import uuid
from typing import List
from app.schemas.content import ContentDocument
from app.schemas.aac import AACCommunicationBoard, AACSymbolCell

CORE_CELLS = [
    ("I want", "I want to learn more", "social", "#fef08a"),
    ("Help", "Please help me understand this", "social", "#fecaca"),
    ("Repeat", "Can we repeat this section?", "verb", "#bbf7d0"),
    ("Question", "I have a question", "question", "#bfdbfe"),
]

class AACService:
    def generate_board(self, doc: ContentDocument, columns: int = 4) -> AACCommunicationBoard:
        cells: List[AACSymbolCell] = []

        for label, phrase, cat, color in CORE_CELLS:
            cells.append(AACSymbolCell(
                cell_id=str(uuid.uuid4())[:8],
                label=label,
                speech_phrase=phrase,
                category=cat,
                color_hex=color
            ))

        for term, definition in list(doc.glossary.items())[:8]:
            cells.append(AACSymbolCell(
                cell_id=str(uuid.uuid4())[:8],
                label=term,
                speech_phrase=f"{term} means {definition}",
                category="noun",
                color_hex="#fed7aa"
            ))

        return AACCommunicationBoard(
            board_id=str(uuid.uuid4())[:8],
            title=f"AAC Board: {doc.title}",
            grid_columns=columns,
            cells=cells
        )

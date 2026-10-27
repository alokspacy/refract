"""Service bundling study materials (flashcards, glossaries, notes) into markdown/JSON."""
import json
from app.schemas.content import ContentDocument
from app.services.flashcard_service import FlashcardService

class StudyMaterialExporter:
    def __init__(self):
        self.flashcard_service = FlashcardService()

    def export_markdown_study_guide(self, doc: ContentDocument) -> str:
        lines = [
            f"# Study Guide: {doc.title}",
            "",
            "## Summary & Objectives"
        ]
        if doc.learning_objectives:
            for obj in doc.learning_objectives:
                lines.append(f"- {obj}")
        else:
            lines.append("- Master core conceptual fundamentals")
        lines.append("")

        deck = self.flashcard_service.generate_deck(doc, max_cards=20)
        lines.append("## Flashcards Review")
        for i, card in enumerate(deck.cards, 1):
            lines.append(f"### Card {i}: {card.front}")
            lines.append(f"**Answer**: {card.back}")
            lines.append("")

        if doc.glossary:
            lines.append("## Key Vocabulary Glossary")
            for term, definition in doc.glossary.items():
                lines.append(f"- **{term}**: {definition}")
            lines.append("")

        return "\n".join(lines)

    def export_json_study_pack(self, doc: ContentDocument) -> dict:
        deck = self.flashcard_service.generate_deck(doc, max_cards=30)
        return {
            "document_id": doc.id,
            "title": doc.title,
            "objectives": doc.learning_objectives,
            "glossary": doc.glossary,
            "flashcards": [c.model_dump() for c in deck.cards]
        }

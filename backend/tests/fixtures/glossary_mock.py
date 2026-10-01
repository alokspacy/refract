"""Glossary test fixtures."""
from app.schemas.content import ContentDocument

MOCK_GLOSSARY_DOC = ContentDocument(
    title="Cell Biology 101",
    learning_objectives=["Understand Mitochondria and Chloroplast functions."],
    glossary={
        "Mitochondria": "The powerhouse of eukaryotic cells that generates ATP.",
        "Chloroplast": "Plastid containing chlorophyll in which photosynthesis takes place."
    }
)

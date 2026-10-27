# AccessLearn AI - API Documentation

## Readability & Assessment
- `POST /assessment/evaluate-text` - Evaluates raw text for reading grade, syllable distributions, and Lexile score.
- `GET /assessment/documents/{document_id}` - Evaluates an existing normalized document for readability level.

## Study Flashcards
- `POST /flashcards/generate` - Automatically extracts question-answer pairs and glossary cards from content.
- `GET /flashcards/documents/{document_id}` - Generates an interactive flashcard deck for a document.

## Speech-to-Text & Transcripts
- `POST /stt/align` - Aligns raw transcript strings with word timestamp tokens for synchronized playback.

## Sensory & Neurodiversity Accommodations
- `POST /sensory/inspect` - Screens documents for photosensitive flashing hazards and recommends accommodations.

## Mind Maps & Document Cloning
- `POST /mindmap/generate` - Generates hierarchical concept mind map tree from document structure.
- `POST /clone/documents/{document_id}` - Deep clones a normalized document with regenerated block identifiers.

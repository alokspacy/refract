# AccessLearn AI - API Documentation

## Readability & Assessment
- `POST /assessment/evaluate-text` - Evaluates raw text for reading grade, syllable distributions, and Lexile score.
- `GET /assessment/documents/{document_id}` - Evaluates an existing normalized document for readability level.

## Color Vision Deficiency (CVD) Simulation
- `GET /colorblind/matrix/{deficiency}` - Generates 3x3 color deficiency simulation matrix.
- `GET /colorblind/svg-filter/{deficiency}` - Returns SVG feColorMatrix markup for live CSS filter previews.

## Focus & Executive Function
- `POST /focus/sessions` - Configures structured Pomodoro focus and rest interval pacing.
- `POST /focus/sessions/{session_id}/complete` - Logs completed study intervals and tracks cognitive endurance.

## Document Outline & Screen Reader Navigation
- `POST /outline/extract` - Extracts structured H1-H6 heading hierarchy for jumping.
- `GET /outline/documents/{document_id}` - Retrieves heading outline for a stored document.

## Speech Synthesis Presets
- `GET /speech-presets` - Returns voice rate and pitch configurations (Relaxed, Standard, Fast, Dyslexia Paced).

## Learning Management System (LMS) Packaging
- `POST /lms/manifest-xml` - Generates SCORM 2004 4th Edition compliant imsmanifest.xml.

## Study Flashcards & Mindmaps
- `POST /flashcards/generate` - Automatically extracts question-answer pairs and glossary cards from content.
- `POST /mindmap/generate` - Generates hierarchical concept mind map tree from document structure.
- `POST /clone/documents/{document_id}` - Deep clones a normalized document with regenerated block identifiers.

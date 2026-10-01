# AccessLearn AI — Extended API Specification

## 1. Compliance Audit API
- `POST /api/compliance/evaluate`: Audits raw ContentDocument for WCAG 2.2 AA/AAA rules.
- `GET /api/compliance/documents/{id}`: Audits a normalized document.
- `GET /api/compliance/variants/{id}`: Audits an adapted variant.

## 2. Readability & Metrics API
- `POST /api/readability/analyze`: Computes Flesch-Kincaid, Gunning Fog, and CEFR grade levels.
- `GET /api/readability/documents/{id}`: Aggregated readability metrics for document text.

## 3. Audio Narration & Captions API (Phase 4)
- `GET /api/audio/presets`: Returns voice profiles (calm, slow dyslexia, screen reader).
- `POST /api/audio/variants/{id}/narrate`: Synthesizes audio package with cue timings.
- `GET /api/audio/variants/{id}/vtt`: Streams WebVTT caption file for karaoke synchronization.

## 4. Multi-Modal Export API (Phase 5)
- `GET /api/export/formats`: Lists available distribution targets (HTML5, SCORM, EPUB3).
- `POST /api/export/package`: Packages adapted content into a downloadable bundle.
- `GET /api/export/{id}/download`: Streams zip archive package.

## 5. Smart Flashcards & Glossary API
- `GET /api/glossary/documents/{id}/flashcards`: Generates cognitive review deck with memory cues.

## 6. Educator Review & Annotation API
- `POST /api/annotations/variants/{id}/review`: Records educator block approval or suggested edit.
- `GET /api/annotations/variants/{id}/summary`: Returns approval rate and publish readiness.

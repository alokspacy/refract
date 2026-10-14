# AccessLearn AI — Extended API Reference

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
- `GET /api/bundle/documents/{id}/all`: Downloads master zip archive with all formats.

## 5. STEM Math & ClearSpeak API
- `POST /api/math/translate`: Translates LaTeX equations into accessible MathML and ClearSpeak spoken representations.

## 6. Braille Translation API (UEB)
- `GET /api/braille/documents/{id}`: Produces Unified English Braille Grade 1 and Grade 2 translations.
- `GET /api/braille/documents/{id}/brf`: Downloads standard Braille Ready Format (.brf) embosser file.

## 7. American Sign Language (ASL) Glossing API
- `POST /api/sign-language/gloss-sentence`: Converts English into ASL Topic-Comment grammatical gloss.
- `GET /api/sign-language/documents/{id}`: Generates full ASL gloss translation for a document.

## 8. Multilingual Accessibility Translation API
- `GET /api/translation/documents/{id}`: Translates content into ES, FR, AR, ZH, HI, DE while preserving block structure.

## 9. Multi-Tenant Enterprise Quota API
- `POST /api/organizations/`: Registers school district workspaces.
- `GET /api/organizations/{id}`: Retrieves monthly page usage and quota limits.

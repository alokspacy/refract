# AccessLearn AI — Extended API Specification

## 1. Compliance Audit API
- `POST /api/compliance/evaluate`: Audits raw ContentDocument for WCAG 2.2 AA/AAA rules.
- `GET /api/compliance/documents/{id}`: Audits a normalized document.
- `GET /api/compliance/variants/{id}`: Audits an adapted variant.

## 2. Readability & Metrics API
- `POST /api/readability/analyze`: Computes Flesch-Kincaid, Gunning Fog, and CEFR grade levels.
- `GET /api/readability/documents/{id}`: Aggregated readability metrics for document text.

## 3. Executive Function & Task Decomposition API
- `POST /api/breakdown/`: Decomposes assignments into bite-sized pacing intervals.

## 4. Plain Language Rewriter API
- `POST /api/plain-language/simplify`: Replaces scholarly jargon with plain terminology.

## 5. Webhooks & LMS Events API
- `POST /api/webhooks/test-event`: Dispatches test integration events to registered endpoints.

## 6. Multi-Modal Export & Master Bundle API
- `GET /api/export/formats`: Lists available distribution targets (HTML5, SCORM, EPUB3).
- `GET /api/bundle/documents/{id}/all`: Streams master zip archive with all accessible formats.

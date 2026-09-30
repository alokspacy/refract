# AccessLearn AI — AI Engine for Automatic Accessible Educational Content

**AccessLearn AI** is an enterprise-grade accessible learning platform designed to ingest educational materials across standard formats (PDF, Word DOCX, PowerPoint PPTX, Images, and Text) and transform them into normalized, structured, traceable, and WCAG 2.1 AA compliant learning formats.

---

## Current Status: Phase 3 Completed (AI Core & Accessibility Transformation Engine)

| Phase | Description | Status |
|---|---|---|
| **Phase 1: Foundation** | FastAPI backend, PostgreSQL, Redis, Celery, JWT auth, secure storage, and Next.js frontend | **COMPLETED** |
| **Phase 2: Document Extraction & Normalization** | Multi-format parsers (PDF, DOCX, PPTX, Image, TXT), OCR fallback, common intermediate representation, normalization into Content JSON, asset persistence, and source preview | **COMPLETED** |
| **Phase 3: AI Core & Transformation Engine** | Managed LLM provider, pedagogical content analysis, learning objectives/concepts/vocabulary extraction, deterministic accessibility planner, Dyslexia/Cognitive/Visual profiles, grounding validation & numeric preservation, transformation caching, and Variant Studio | **COMPLETED** |
| **Phase 4: Multi-Modal Adaptation** | Blind accessibility with tactile/alt-text descriptions, audio/speech transformations (TTS/STT), SRT/VTT | *Scheduled* |
| **Phase 5: Educator Studio & Export** | Review editor, interactive block regeneration, approval workflows, accessible EPUB/PDF/HTML5/Audio exports | *Scheduled* |

---

## Phase 3 AI Core & Transformation Architecture

```text
Normalized Content JSON (v1.0.0)
             │
             ▼
[1. Content Analysis Engine] (Language, Subject, Grade, Learning Objectives, Concepts, Vocabulary)
             │
             ▼
[2. Accessibility Planner] (Deterministic Precedence: Cognitive -> Dyslexia -> Visual)
             │
             ▼
[3. Transformation Engine] (Per-Block LLM Transformation + Versioned Prompts + SHA-256 Caching)
             │
             ▼
[4. Validation & Grounding Engine] (Numeric Token Preservation, Anti-Hallucination & Grounding Check)
             │
             ▼
[5. Traceable Generated Variant & Blocks] (PostgreSQL JSONB + 1-to-1 Source Block Mapping)
```

```text
Uploaded Educational Material (PDF, DOCX, PPTX, PNG, JPG, TXT)
                         │
                         ▼
             [Parser Registry & Factory]
                         │
      ┌──────────────────┼──────────────────┬─────────────────┐
      ▼                  ▼                  ▼                 ▼
 [PyMuPDF Parser]   [DOCX Parser]     [PPTX Parser]     [Image / TXT]
  - Headings         - Paragraphs      - Slide sequence  - Pillow meta
  - Paragraphs       - Lists           - Text frames     - Paragraphs
  - Lists            - Tables          - Tables          - OCR flag
  - Tables           - Embedded parts  - Speaker notes
  - Images           - Order           - Slide shapes
  - Scanned check
      │
      ├───────► [Requires OCR?] ──(Yes)──► [OCRProvider / MockOCR]
      │                                       (Preserves BBox & Conf)
      ▼
 [Common Extraction Intermediate Representation]
  - ExtractedDocument (title, sections, blocks, assets, metadata, warnings)
  - ExtractedBlock (id, type, page_or_slide, bbox, order, asset_id)
      │
      ▼
 [Normalizer Pipeline]
  - Transforms to ContentDocument JSON Schema v1.0.0
  - Stable UUIDs & Traceability references
      │
      ▼
 [PostgreSQL 16 Storage (JSONB)]
  - Document.normalized_content
  - Document.extraction_warnings
  - Document.extracted_at
      │
      ▼
 [Frontend Source Preview Studio]
  - Page-by-page & Slide-by-slide viewer
  - Live Traceability Inspector (BBox, IDs, Page references)
  - Raw Content JSON viewer
```

---

## Supported Formats & Capabilities

| Format | Parser Engine | Extracted Structures | Embedded Assets | OCR Fallback |
|---|---|---|---|---|
| **PDF** | PyMuPDF (`fitz`) | Headings, Paragraphs, Lists, Tables (`find_tables`), Page numbers, Bounding boxes | Extracted to Storage | Automatic on low-text / scanned pages |
| **DOCX** | `python-docx` | Headings (`Heading 1-6`), Paragraphs, Bullet/Numbered lists, Table matrices | Extracted from doc parts | N/A |
| **PPTX** | `python-pptx` | Slide order, Slide titles, Text frames, Bullet hierarchies, Tables, Speaker notes | Extracted from picture shapes | N/A |
| **PNG/JPG** | `Pillow` | Dimensions, Color format, Image block | Full image asset | Always routed to OCR provider |
| **TXT** | Native Python | UTF-8/Latin-1 normalization, Paragraph segmentation, Markdown headings | N/A | N/A |

---

## Quickstart with Docker Compose

1. Clone the repository and navigate to the project directory:
   ```bash
   cd refract
   ```

2. Start the 5-container stack:
   ```bash
   docker compose up --build
   ```

3. Access the services:
   - **Educator Frontend**: [http://localhost:3000](http://localhost:3000)
   - **Backend REST API**: [http://localhost:8000](http://localhost:8000)
   - **Swagger OpenAPI Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **System Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## Automated Test Suite

Run the full 61-test Pytest test suite covering all authentication, parser, OCR fallback, normalization, LLM provider, content analysis, accessibility profiles, transformation engine, validation/grounding, storage security, and end-to-end integration workflows:
```bash
python -m pytest backend/tests -v
```

Test Results: **61/61 Passed (100%)**.

---

## License
MIT License.

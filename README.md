# AccessLearn AI — AI Engine for Automatic Accessible Educational Content

**AccessLearn AI** is an enterprise-grade accessible learning platform designed to ingest educational materials across standard formats (PDF, Word DOCX, PowerPoint PPTX, Images, and Text) and transform them into normalized, structured, traceable, and WCAG 2.2 AA/AAA compliant learning formats.

---

## Status & Roadmap

| Phase | Description | Status |
|---|---|---|
| **Phase 1: Foundation** | FastAPI backend, PostgreSQL, Redis, Celery, JWT auth, secure storage, and Next.js frontend | **COMPLETED** |
| **Phase 2: Document Extraction & Normalization** | Multi-format parsers (PDF, DOCX, PPTX, Image, TXT), OCR fallback, common intermediate representation, normalization into Content JSON, asset persistence, and source preview | **COMPLETED** |
| **Phase 3: AI Core & Transformation Engine** | Managed LLM provider, pedagogical content analysis, learning objectives/concepts/vocabulary extraction, deterministic accessibility planner, Dyslexia/Cognitive/Visual profiles, grounding validation & numeric preservation, transformation caching, and Variant Studio | **COMPLETED** |
| **Phase 4: Multi-Modal Adaptation** | Timed audio narration generator, WebVTT subtitle synchronization, cognitive speech rate presets, and karaoke player | **COMPLETED** |
| **Phase 5: Educator Studio & Export** | WCAG 2.2 AA audit engine, Flesch-Kincaid readability scoring, block annotations & approval workflows, standalone offline HTML5 reader, and SCORM 1.2 LMS packages | **COMPLETED** |

---

## Key Market Features

1. **Automated WCAG 2.2 AA/AAA Audit Engine**: Automated verification of image alt text, heading landmarks, table structures, and reading grade bands with actionable remediation suggestions.
2. **Pedagogical Readability Calculator**: Multi-formula scoring (Flesch-Kincaid, Gunning Fog, SMOG, ARI) and CEFR level assessment.
3. **Synchronized Speech Narration & WebVTT Captions**: Block-level timestamp cue generation for synchronized karaoke text tracking.
4. **Assistive Reading Toolkit**: Built-in Bionic reading fixation engine, adjustable focus reading mask, and reading ruler.
5. **Smart Concept Flashcards**: Automatic glossary generation with memory cues and simplified definitions for neurodivergent learners.
6. **LMS & Standalone Distribution**: One-click export to SCORM 1.2 / 2004 for Canvas, Moodle, and Blackboard, plus zero-dependency offline HTML5 bundles.

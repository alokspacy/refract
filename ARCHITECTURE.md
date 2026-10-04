# AccessLearn AI — System Architecture

```text
Educational Inputs (PDF, DOCX, PPTX, Images, Math)
                     │
                     ▼
          [Multi-Format Parser Registry]
                     │
                     ▼
        [Normalized Content JSON v1.0]
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
 [AI Transformation Core]    [WCAG 2.2 Audit Engine]
  - Dyslexia Profile          - Contrast Verification
  - Cognitive Simplification  - Heading Landmarks
  - Visual Contrast           - Alt-Text Validation
        │
        ├─────────────────────────┬─────────────────────────┐
        ▼                         ▼                         ▼
[Audio & Narration]       [Braille & STEM Engine]   [Export & LMS Packaging]
 - WebVTT Subtitles        - UEB Grade 1 & 2         - SCORM 1.2 / 2004
 - Synchronized Karaoke    - ClearSpeak Math         - Standalone Offline HTML5
 - Calm Voice Presets      - Tactile Diagrams        - Self-Check Assessments
```

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
  - Dyscalculia Grouping      - Alt-Text Validation
  - Sensory Shield Mode       - PDF/UA Tag Inspector
        │
        ├─────────────────────────┬─────────────────────────┐
        ▼                         ▼                         ▼
[Audio & Narration]       [Braille & STEM Engine]   [Export & LMS Packaging]
 - WebVTT Subtitles        - UEB Grade 1 & 2         - SCORM 1.2 / 2004
 - Synchronized Karaoke    - ClearSpeak Math         - Standalone Offline HTML5
 - Calm Voice Presets      - Tactile Diagrams        - Accessible EPUB3
 - Waveform Visualizer     - Self-Check Assessments - Offline Service Worker
```

## Modular Components

1. **AI Transformation Core**: Multi-profile pedagogical adaptation covering dyslexia, cognitive load, dyscalculia, and visual contrast.
2. **WCAG 2.2 & PDF/UA Auditing**: Real-time rule evaluation, contrast checking, and document structure validation.
3. **Multi-Modal Adaptation**: Synchronized WebVTT audio, ClearSpeak STEM equations, and Unified English Braille (UEB).
4. **Distribution Formats**: LMS-ready SCORM 1.2/2004 packaging, accessible EPUB3, and zero-dependency offline HTML5 reader.

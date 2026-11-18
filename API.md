# AccessLearn AI - API Documentation

## AAC & Phonetic Pronunciation
- `POST /aac/board` - Generates core and fringe vocabulary AAC symbol communication boards.
- `POST /phonetics/guide` - Breaks academic terms into syllables and phonetic respellings.

## Table Linearization & Multimodal Reading Pace
- `POST /table-a11y/linearize` - Converts 2D tables into narrative sentences for screen readers.
- `POST /reading-pace/estimate` - Calculates completion times across visual, TTS, and Braille reading.

## Earcons, Vocabulary Tiers & Magnifier
- `GET /earcons/palette` - Returns acoustic landmark earcon frequencies and durations.
- `POST /vocab-tiers/analyze` - Classifies words into Tier 1, Tier 2, and Tier 3 academic vocabulary.
- `POST /magnifier/viewport` - Computes low-vision screen magnifier bounding geometry.

## Image Alt-Text, UDL Rubric & Gaze/Switch Control
- `POST /alt-text/audit` - Audits document images for missing alt attributes.
- `POST /rubric/evaluate` - Evaluates document scaffolding against UDL criteria.
- `POST /gaze/evaluate-dwell` - Evaluates eye-gaze dwell coordinates for hands-free activation.
- `POST /switch-access/metrics` - Computes scan cycle timing for motor accessibility.

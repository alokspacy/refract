# AccessLearn AI - API Documentation

## Image Accessibility & Alt-Text
- `POST /alt-text/audit` - Audits document images for missing alt attributes and synthesizes descriptions.

## UDL Comprehension Rubric
- `POST /rubric/evaluate` - Evaluates document scaffolding against Universal Design for Learning criteria.

## Assistive Eye-Gaze & Switch Control
- `POST /gaze/evaluate-dwell` - Evaluates eye-gaze dwell coordinates for hands-free activation.
- `POST /switch-access/metrics` - Computes scan cycle timing and scanning topology for motor accessibility.

## Closed Captions & Cognitive Load
- `POST /captions/webvtt` - Generates styled WebVTT closed caption tracks.
- `POST /cognitive-load/analyze` - Estimates intrinsic and extraneous cognitive load scores.

## Readability & Color Vision Deficiency
- `POST /assessment/evaluate-text` - Evaluates raw text for reading grade and Lexile score.
- `GET /colorblind/matrix/{deficiency}` - Generates 3x3 color deficiency simulation matrix.

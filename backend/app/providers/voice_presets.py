"""Voice presets for speech adaptation with clamped rates."""
VOICE_PRESETS = {
    "calm_student": {
        "voice_id": "alloy",
        "speaking_rate": max(0.5, min(1.5, 0.9)),
        "pitch": -0.1,
        "pause_between_blocks_ms": 600,
        "description": "Gentle, calm tone optimal for anxiety reduction and steady focus."
    },
    "slow_dyslexia": {
        "voice_id": "echo",
        "speaking_rate": max(0.5, min(1.5, 0.78)),
        "pitch": -0.3,
        "pause_between_blocks_ms": 900,
        "description": "Deliberate pacing with phoneme clarity for dyslexic learners."
    },
    "expressive_teacher": {
        "voice_id": "shimmer",
        "speaking_rate": max(0.5, min(1.5, 1.0)),
        "pitch": 0.3,
        "pause_between_blocks_ms": 500,
        "description": "Energetic, engaging classroom instruction style."
    },
    "screen_reader": {
        "voice_id": "fable",
        "speaking_rate": max(0.5, min(1.5, 1.25)),
        "pitch": 0.0,
        "pause_between_blocks_ms": 300,
        "description": "Fast, clear cadence for experienced assistive technology users."
    }
}

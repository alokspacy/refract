"""Voice presets for speech adaptation."""
VOICE_PRESETS = {
    "calm_student": {
        "voice_id": "alloy",
        "speaking_rate": 0.9,
        "pitch": 0.0,
        "pause_between_blocks_ms": 600,
        "description": "Gentle, calm tone optimal for anxiety reduction and steady focus."
    },
    "slow_dyslexia": {
        "voice_id": "echo",
        "speaking_rate": 0.78,
        "pitch": -0.5,
        "pause_between_blocks_ms": 900,
        "description": "Deliberate pacing with phoneme clarity for dyslexic learners."
    },
    "expressive_teacher": {
        "voice_id": "shimmer",
        "speaking_rate": 1.0,
        "pitch": 0.5,
        "pause_between_blocks_ms": 500,
        "description": "Energetic, engaging classroom instruction style."
    },
    "screen_reader": {
        "voice_id": "fable",
        "speaking_rate": 1.25,
        "pitch": 0.0,
        "pause_between_blocks_ms": 300,
        "description": "Fast, clear cadence for experienced assistive technology users."
    }
}

import pytest
from app.profiles.registry import get_profile_registry
from app.profiles.dyslexia import DyslexiaProfile, DyslexiaBlockOutput
from app.profiles.cognitive import CognitiveProfile, CognitiveBlockOutput
from app.profiles.visual import VisualBasicProfile, VisualBlockOutput


def test_profile_registry_discovery_and_precedence():
    registry = get_profile_registry()
    profiles = registry.list_profiles()
    assert len(profiles) >= 3
    
    profile_ids = [p.profile_id for p in profiles]
    assert "dyslexia" in profile_ids
    assert "cognitive" in profile_ids
    assert "visual_basic" in profile_ids

    # Precedence resolution
    ordered = registry.resolve_precedence(["visual_basic", "dyslexia", "cognitive"])
    assert ordered == ["cognitive", "dyslexia", "visual_basic"]


def test_dyslexia_profile_schema_validation():
    profile = DyslexiaProfile()
    valid_data = {
        "source_block_id": "blk_001",
        "title": "Plant Energy",
        "simplified_text": "Plants use light to make food.",
        "key_points": ["Uses sunlight", "Makes glucose"],
        "important_terms": [{"term": "Chlorophyll", "definition": "Green plant pigment"}],
        "example": "Like solar cells.",
        "omitted_information": [],
        "changed_information": []
    }
    validated = profile.validate_content(valid_data)
    assert isinstance(validated, DyslexiaBlockOutput)
    assert validated.title == "Plant Energy"


def test_cognitive_profile_schema_validation():
    profile = CognitiveProfile()
    valid_data = {
        "source_block_id": "blk_002",
        "concept_title": "Energy Conversion",
        "step_by_step": ["Step 1: Light absorption", "Step 2: Water splitting"],
        "explanation": "Plants make food from photons.",
        "example": "Solar panels on a roof.",
        "key_terms": [{"term": "Glucose", "definition": "Plant sugar"}],
        "recap": "Sunlight becomes plant food.",
        "comprehension_questions": [{"question": "What pigment absorbs light?", "answer_hint": "Chlorophyll"}]
    }
    validated = profile.validate_content(valid_data)
    assert isinstance(validated, CognitiveBlockOutput)
    assert len(validated.step_by_step) == 2


def test_visual_profile_schema_validation():
    profile = VisualBasicProfile()
    valid_data = {
        "source_block_id": "blk_003",
        "semantic_type": "heading",
        "heading_level": 2,
        "formatted_text": "Section 1: Cellular Biology",
        "items": [],
        "requires_description": False
    }
    validated = profile.validate_content(valid_data)
    assert isinstance(validated, VisualBlockOutput)
    assert validated.heading_level == 2

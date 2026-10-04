"""Unit tests for tactile graphics generator."""
from app.services.tactile_service import TactileService

def test_tactile_description_generation():
    svc = TactileService()
    desc = svc.describe_image("img-42", "Plant Cell", {"figure": "cell"})
    assert desc.asset_id == "img-42"
    assert "Plant Cell" in desc.title
    assert len(desc.layers) >= 2
    assert "clockwise" in desc.tactile_exploration_guide

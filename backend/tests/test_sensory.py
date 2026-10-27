"""Tests for sensory sensitivity evaluation service."""
from app.services.sensory_service import SensoryService
from app.schemas.sensory import SensoryProfile, MotionTolerance
from app.schemas.content import ContentDocument, Section, ContentBlock, BlockType

def test_sensory_flashing_hazard_detection():
    service = SensoryService()
    profile = SensoryProfile(motion=MotionTolerance.REDUCED, flash_suppression=True)
    doc = ContentDocument(
        title="Physics of Light",
        sections=[
            Section(
                title="Strobe Lights",
                blocks=[
                    ContentBlock(id="b1", type=BlockType.PARAGRAPH, source_text="A strobe effect creates flashing patterns.")
                ]
            )
        ]
    )
    result = service.inspect_content_hazards(doc, profile)
    assert not result["safe_for_viewing"]
    assert len(result["detected_hazards"]) == 1
    assert "prefers-reduced-motion" in result["accommodations_applied"][0]

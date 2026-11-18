"""Unit tests for earcon acoustic landmark service."""
from app.services.earcons_service import EarconsService

def test_default_earcon_palette():
    service = EarconsService()
    palette = service.get_default_palette()
    assert len(palette.cues) == 4
    assert palette.cues[0].event_type == "section_enter"
    assert palette.cues[0].frequency_hz == 523

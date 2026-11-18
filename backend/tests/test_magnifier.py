"""Unit tests for low-vision screen magnifier service."""
from app.services.magnifier_service import MagnifierService
from app.schemas.magnifier_config import MagnifierLensConfig

def test_magnifier_viewport_bounds():
    service = MagnifierService()
    cfg = MagnifierLensConfig(zoom_factor=3.0, lens_width_px=200, lens_height_px=100, invert_colors=True)
    bounds = service.compute_viewport_bounds(300, 250, cfg)
    assert bounds["left"] == 200
    assert bounds["top"] == 200
    assert bounds["scale"] == 3.0
    assert bounds["css_filter"] == "invert(100%)"

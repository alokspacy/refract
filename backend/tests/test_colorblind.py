"""Unit tests for color blindness simulation matrices and SVG filters."""
from app.services.colorblind_service import ColorBlindService
from app.schemas.colorblind import DeficiencyType

def test_colorblind_matrices_validity():
    service = ColorBlindService()
    for deficiency in DeficiencyType:
        cm = service.get_matrix(deficiency)
        assert len(cm.matrix) == 3
        for row in cm.matrix:
            assert len(row) == 3
            assert round(sum(row), 2) == 1.0

def test_svg_filter_generation():
    service = ColorBlindService()
    svg = service.generate_svg_filter(DeficiencyType.PROTANOPIA)
    assert '<filter id="cvd-protanopia">' in svg
    assert '<feColorMatrix type="matrix"' in svg

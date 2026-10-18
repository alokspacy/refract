"""Unit tests for DAISY service."""
from app.services.daisy_service import DaisyService
from app.schemas.content import ContentDocument, Section

def test_daisy_ncc_generation():
    svc = DaisyService()
    doc = ContentDocument(
        title="Cell Structure",
        sections=[Section(title="Nucleus"), Section(title="Cytoplasm")]
    )
    rep = svc.build_ncc(doc)
    assert len(rep.nav_points) == 2
    assert "DAISY 2.02" in rep.ncc_html
    assert "Nucleus" in rep.ncc_html

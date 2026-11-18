"""Unit tests for accessible table linearizer service."""
from app.services.table_a11y_service import TableAccessibilityService

def test_table_linearization():
    service = TableAccessibilityService()
    res = service.linearize_table(
        block_id="tbl-1",
        caption="Planet Gravity",
        headers=["Planet", "Gravity (m/s2)"],
        rows=[["Earth", "9.8"], ["Mars", "3.7"]]
    )
    assert len(res.row_narratives) == 2
    assert "Planet is Earth, Gravity (m/s2) is 9.8." in res.row_narratives[0].narrative_sentence
    assert "2 columns" in res.aria_summary

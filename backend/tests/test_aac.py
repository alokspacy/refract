"""Unit tests for AAC communication board generator service."""
from app.services.aac_service import AACService
from app.schemas.content import ContentDocument

def test_aac_board_generation():
    service = AACService()
    doc = ContentDocument(
        title="Solar System",
        glossary={"Orbit": "Curved path of a planet around a star"}
    )
    board = service.generate_board(doc, columns=4)
    assert board.grid_columns == 4
    assert len(board.cells) == 5
    assert any(c.label == "Orbit" for c in board.cells)

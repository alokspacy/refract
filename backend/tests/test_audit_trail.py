"""Unit tests for audit trail consistency."""
from app.schemas.annotation import AnnotationCreate

def test_annotation_create_schema():
    payload = AnnotationCreate(
        block_id="blk-999",
        status="approved",
        comment="Accurate simplification of biological processes.",
        suggested_content=None
    )
    assert payload.block_id == "blk-999"
    assert payload.status == "approved"
    assert "Accurate" in payload.comment

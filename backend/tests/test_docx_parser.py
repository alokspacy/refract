import pytest
from app.parsers.docx import DOCXParser
from tests.fixtures.generator import create_sample_docx


def test_docx_parser_headings_lists_and_tables():
    docx_bytes = create_sample_docx()
    parser = DOCXParser()
    assert parser.can_parse("application/vnd.openxmlformats-officedocument.wordprocessingml.document", "bio.docx") is True

    doc = parser.parse(docx_bytes, "bio.docx")
    assert doc.title == "Cellular Biology Overview"
    assert len(doc.sections) >= 1

    all_blocks = [b for sec in doc.sections for b in sec.blocks]
    assert len(all_blocks) > 0

    # Verify heading, paragraph, list, and table presence
    block_types = [b.type for b in all_blocks]
    assert "heading" in block_types
    assert "paragraph" in block_types
    assert "list" in block_types
    assert "table" in block_types

    # Verify table row extraction
    table_block = next(b for b in all_blocks if b.type == "table")
    assert table_block.metadata["row_count"] == 3
    assert table_block.metadata["col_count"] == 2
    assert "Cell Wall" in str(table_block.metadata["rows"])


def test_docx_parser_corrupted_file_handling():
    parser = DOCXParser()
    with pytest.raises(ValueError) as exc:
        parser.parse(b"Not a real docx zip archive", "fake.docx")
    assert "Corrupted or invalid DOCX" in str(exc.value)

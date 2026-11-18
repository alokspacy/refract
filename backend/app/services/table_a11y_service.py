"""Service converting 2D tables into screen-reader-friendly narrative sentences."""
from typing import List
from app.schemas.table_a11y import AccessibleTableSummary, LinearizedTableRow

class TableAccessibilityService:
    def linearize_table(
        self,
        block_id: str,
        caption: str,
        headers: List[str],
        rows: List[List[str]]
    ) -> AccessibleTableSummary:
        narratives: List[LinearizedTableRow] = []
        for r_idx, row in enumerate(rows, 1):
            pairs = []
            for c_idx, val in enumerate(row):
                col_name = headers[c_idx] if c_idx < len(headers) else f"Column {c_idx + 1}"
                pairs.append(f"{col_name} is {val}")
            sentence = f"Row {r_idx}: " + ", ".join(pairs) + "."
            narratives.append(LinearizedTableRow(row_index=r_idx, narrative_sentence=sentence))

        aria_summary = (
            f"Table titled '{caption}' with {len(headers)} columns ({', '.join(headers)}) "
            f"and {len(rows)} data rows."
        )
        return AccessibleTableSummary(
            block_id=block_id,
            caption=caption,
            headers=headers,
            row_narratives=narratives,
            aria_summary=aria_summary
        )

"""Dyscalculia accessibility transformation service."""
import re
from typing import List
from app.schemas.dyscalculia import NumberRepresentation, DyscalculiaBlockAdaptation

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

class DyscalculiaService:
    """Enhances numerical clarity through digit grouping and word spell-outs."""

    def format_digits(self, text: str) -> DyscalculiaBlockAdaptation:
        numbers_found: List[NumberRepresentation] = []

        def replace_num(match):
            val_str = match.group(0)
            chunked = " ".join([val_str[max(i - 3, 0):i] for i in range(len(val_str), 0, -3)][::-1])
            spelled = ONES[int(val_str)] if val_str.isdigit() and int(val_str) < 10 else f"{val_str} ({chunked})"
            rep = NumberRepresentation(
                raw_number=val_str,
                formatted_chunked=chunked,
                spelled_out_words=spelled,
                visual_dots_count=int(val_str) if val_str.isdigit() and int(val_str) <= 10 else None
            )
            numbers_found.append(rep)
            return f"[{val_str} • {spelled}]"

        adapted = re.sub(r'\b\d{2,}\b', replace_num, text)
        return DyscalculiaBlockAdaptation(
            block_id="auto",
            source_text=text,
            adapted_text=adapted,
            numbers_detected=numbers_found
        )

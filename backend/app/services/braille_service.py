"""Unified English Braille (UEB) translation service."""
import re
from typing import Dict, List
from app.schemas.braille import BrailleGrade, BrailleBlockTranslation, BrailleDocumentResponse
from app.schemas.content import ContentDocument

BRAILLE_MAP: Dict[str, str] = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
    'z': '⠵', ' ': ' ', ',': '⠂', ';': '⠆', ':': '⠒',
    '.': '⠲', '!': '⠖', '?': '⠦', '-': '⠤', "'": '⠄'
}

DIGIT_MAP: Dict[str, str] = {
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚'
}

UEB_CONTRACTIONS: Dict[str, str] = {
    'the': '⠮', 'and': '⠯', 'for': '⠿', 'of': '⠷',
    'with': '⠾', 'in': '⠔', 'to': '⠖', 'that': '⠹',
}

class BrailleService:
    """Translates text blocks into Grade 1 and Grade 2 Unified English Braille."""

    def to_braille_unicode(self, text: str, grade: BrailleGrade = BrailleGrade.GRADE_2) -> str:
        clean = text.lower()
        if grade == BrailleGrade.GRADE_2:
            for word, symbol in UEB_CONTRACTIONS.items():
                clean = re.sub(rf'\b{re.escape(word)}\b', symbol, clean)

        # Standard UEB Number Indicator ⠼ (dots 3-4-5-6)
        def replace_numbers(match):
            digits = match.group(0)
            return '⠼' + ''.join(DIGIT_MAP.get(d, d) for d in digits)

        clean = re.sub(r'\d+', replace_numbers, clean)
        clean = re.sub(r'\s+', ' ', clean)

        result = []
        for char in clean:
            result.append(BRAILLE_MAP.get(char, char))
        return "".join(result)

    def translate_document(self, doc: ContentDocument, grade: BrailleGrade = BrailleGrade.GRADE_2) -> BrailleDocumentResponse:
        blocks = []
        total_cells = 0
        brf_lines = [f"{doc.title.upper()} - BRAILLE EDITION", ""]

        for sec in doc.sections:
            if sec.title:
                b_title = self.to_braille_unicode(sec.title, grade)
                brf_lines.append(f",, {b_title}")

            for b in sec.blocks:
                txt = b.source_text or ""
                if not txt.strip():
                    continue
                b_trans = self.to_braille_unicode(txt, grade)
                total_cells += len(b_trans.replace(" ", ""))
                brf_lines.append(b_trans)
                blocks.append(BrailleBlockTranslation(
                    block_id=b.id,
                    source_text=txt,
                    braille_unicode=b_trans,
                    braille_ascii=txt.lower(),
                    character_count=len(b_trans)
                ))
            brf_lines.append("")

        return BrailleDocumentResponse(
            document_id=doc.id,
            grade=grade,
            total_braille_cells=total_cells,
            blocks=blocks,
            raw_brf_content="\n".join(brf_lines)
        )

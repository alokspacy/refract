"""Schemas for Unified English Braille (UEB) translation."""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class BrailleGrade(str, Enum):
    GRADE_1 = "grade_1"  # Uncontracted letter-for-letter
    GRADE_2 = "grade_2"  # Contracted Braille with standard abbreviations

class BrailleBlockTranslation(BaseModel):
    block_id: str
    source_text: str
    braille_unicode: str
    braille_ascii: str
    character_count: int

class BrailleDocumentResponse(BaseModel):
    document_id: str
    grade: BrailleGrade
    total_braille_cells: int
    blocks: List[BrailleBlockTranslation] = Field(default_factory=list)
    raw_brf_content: str = Field(..., description="Standard Braille Ready Format (.brf) text")

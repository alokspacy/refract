"""Schemas for phonetic respelling and syllable pronunciation guides."""
from typing import List
from pydantic import BaseModel

class PhoneticEntry(BaseModel):
    term: str
    syllables: List[str]
    phonetic_respelling: str
    stressed_index: int = 0

class PhoneticGuideResponse(BaseModel):
    total_terms: int
    entries: List[PhoneticEntry]

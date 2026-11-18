"""Schemas for classifying words into Tier 1 (basic), Tier 2 (academic), and Tier 3 (domain)."""
from typing import List
from pydantic import BaseModel

class TieredWord(BaseModel):
    word: str
    tier: int
    reason: str

class VocabularyTierReport(BaseModel):
    tier_1_count: int
    tier_2_count: int
    tier_3_count: int
    highlighted_terms: List[TieredWord]

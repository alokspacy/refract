"""Schemas for multilingual accessibility translations."""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class LanguageCode(str, Enum):
    ES = "es"  # Spanish
    FR = "fr"  # French
    AR = "ar"  # Arabic (RTL support)
    ZH = "zh"  # Chinese (Simplified)
    HI = "hi"  # Hindi
    DE = "de"  # German

class TranslationBlockResult(BaseModel):
    block_id: str
    target_language: LanguageCode
    translated_text: str
    is_rtl: bool = False

class TranslationDocumentResponse(BaseModel):
    document_id: str
    target_language: LanguageCode
    translated_title: str
    is_rtl: bool
    blocks: List[TranslationBlockResult] = Field(default_factory=list)

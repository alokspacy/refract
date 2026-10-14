"""Schemas for American Sign Language (ASL) grammatical glossing."""
from typing import List, Optional
from pydantic import BaseModel, Field

class ASLGlossToken(BaseModel):
    gloss: str = Field(..., description="Root ASL gloss representation, e.g., BOOK, TEACHER-AGENT")
    is_fingerspelled: bool = False
    facial_grammar: Optional[str] = None  # raised_eyebrows, furrowed_brows, head_nod

class ASLGlossSentence(BaseModel):
    source_english: str
    asl_gloss_sequence: str
    sentence_type: str = "declarative"  # wh_question, yes_no_question, topic_comment
    tokens: List[ASLGlossToken] = Field(default_factory=list)

class SignLanguageDocumentResponse(BaseModel):
    document_id: str
    sentences: List[ASLGlossSentence] = Field(default_factory=list)

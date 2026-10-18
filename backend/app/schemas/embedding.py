"""Schemas for educational text chunking and embeddings."""
from typing import List, Optional
from pydantic import BaseModel, Field

class TextChunk(BaseModel):
    chunk_id: str
    section_title: Optional[str] = None
    content: str
    token_count: int
    start_char_idx: int
    end_char_idx: int

class ChunkingResponse(BaseModel):
    document_id: str
    total_chunks: int
    chunks: List[TextChunk] = Field(default_factory=list)

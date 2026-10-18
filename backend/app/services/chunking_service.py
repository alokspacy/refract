"""Intelligent chunker preserving section and block boundaries."""
import uuid
import re
from typing import List
from app.schemas.content import ContentDocument, BlockType
from app.schemas.embedding import TextChunk, ChunkingResponse

class ChunkingService:
    """Splits ContentDocument into semantically coherent chunks for embeddings."""

    def chunk_document(self, doc: ContentDocument, max_words: int = 150) -> ChunkingResponse:
        chunks: List[TextChunk] = []
        char_offset = 0

        for sec in doc.sections:
            current_words: List[str] = []
            for b in sec.blocks:
                txt = b.source_text or ""
                if not txt.strip():
                    continue
                words = txt.split()
                if len(current_words) + len(words) > max_words and current_words:
                    chunk_text = " ".join(current_words)
                    chunks.append(TextChunk(
                        chunk_id=str(uuid.uuid4())[:8],
                        section_title=sec.title,
                        content=chunk_text,
                        token_count=len(current_words),
                        start_char_idx=char_offset,
                        end_char_idx=char_offset + len(chunk_text)
                    ))
                    char_offset += len(chunk_text) + 1
                    current_words = []
                current_words.extend(words)

            if current_words:
                chunk_text = " ".join(current_words)
                chunks.append(TextChunk(
                    chunk_id=str(uuid.uuid4())[:8],
                    section_title=sec.title,
                    content=chunk_text,
                    token_count=len(current_words),
                    start_char_idx=char_offset,
                    end_char_idx=char_offset + len(chunk_text)
                ))
                char_offset += len(chunk_text) + 1

        return ChunkingResponse(
            document_id=doc.id,
            total_chunks=len(chunks),
            chunks=chunks
        )

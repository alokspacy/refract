"""ASL grammatical gloss transformation service."""
import re
from typing import List
from app.schemas.sign_language import (
    ASLGlossSentence, ASLGlossToken, SignLanguageDocumentResponse
)
from app.schemas.content import ContentDocument, BlockType

QUESTION_WORDS = {"what", "where", "when", "why", "who", "how"}

class SignLanguageService:
    """Converts standard English sentences into ASL Topic-Comment grammatical glosses."""

    def to_asl_gloss(self, sentence: str) -> ASLGlossSentence:
        clean = sentence.strip().rstrip(".!?")
        words = clean.split()
        if not words:
            return ASLGlossSentence(source_english=sentence, asl_gloss_sequence="", tokens=[])

        is_question = sentence.strip().endswith("?")
        has_wh = any(w.lower() in QUESTION_WORDS for w in words)

        tokens: List[ASLGlossToken] = []
        gloss_words = []

        # ASL moves WH-question words to the end
        wh_found = None
        for w in words:
            lw = w.lower()
            if lw in QUESTION_WORDS:
                wh_found = lw.upper()
                continue
            token_gloss = lw.upper()
            is_fs = len(lw) <= 2 or re.match(r'^[A-Z0-9]+$', w) is not None
            tokens.append(ASLGlossToken(gloss=token_gloss, is_fingerspelled=is_fs))
            gloss_words.append(f"#{token_gloss}" if is_fs else token_gloss)

        if wh_found:
            tokens.append(ASLGlossToken(gloss=wh_found, facial_grammar="furrowed_brows"))
            gloss_words.append(wh_found)

        seq = " ".join(gloss_words)
        stype = "wh_question" if wh_found else ("yes_no_question" if is_question else "topic_comment")

        return ASLGlossSentence(
            source_english=sentence,
            asl_gloss_sequence=seq,
            sentence_type=stype,
            tokens=tokens
        )

    def convert_document(self, doc: ContentDocument) -> SignLanguageDocumentResponse:
        sentences: List[ASLGlossSentence] = []
        for sec in doc.sections:
            for b in sec.blocks:
                if b.type == BlockType.PARAGRAPH and b.source_text:
                    parts = re.split(r'[.!?]+', b.source_text)
                    for p in parts:
                        if p.strip():
                            sentences.append(self.to_asl_gloss(p.strip()))
        return SignLanguageDocumentResponse(document_id=doc.id, sentences=sentences)

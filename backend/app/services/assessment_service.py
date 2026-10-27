"""Service computing reading assessment and Lexile difficulty estimates."""
import re
from typing import List
from app.schemas.content import ContentDocument, BlockType
from app.schemas.assessment import ReadingAssessmentResponse, LexileEstimate, AssessmentMetrics

class AssessmentService:
    @staticmethod
    def _count_syllables(word: str) -> int:
        word = word.lower().strip()
        if len(word) <= 3:
            return 1
        word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
        word = re.sub(r'^y', '', word)
        matches = re.findall(r'[aeiouy]{1,2}', word)
        return max(1, len(matches))

    def evaluate_text(self, text: str, document_id: str = None) -> ReadingAssessmentResponse:
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        sentence_count = max(1, len(sentences))

        words = re.findall(r'\b[a-zA-Z]+\b', text)
        word_count = max(1, len(words))

        syllable_count = sum(self._count_syllables(w) for w in words)
        complex_words = [w for w in words if self._count_syllables(w) >= 3]
        complex_word_count = len(complex_words)

        asl = word_count / sentence_count
        asw = syllable_count / word_count
        fk_grade = round(0.39 * asl + 11.8 * asw - 15.59, 2)
        complex_pct = round((complex_word_count / word_count) * 100, 2)
        fog = round(0.4 * (asl + complex_pct), 2)

        lexile_score = max(200, int((fk_grade * 110) + 150))

        if fk_grade <= 3:
            grade_eq = "1st - 3rd Grade"
            band = "Beginner"
        elif fk_grade <= 6:
            grade_eq = "4th - 6th Grade"
            band = "Intermediate"
        elif fk_grade <= 9:
            grade_eq = "7th - 9th Grade"
            band = "Upper Intermediate"
        else:
            grade_eq = "10th - 12th+ Grade"
            band = "Advanced"

        recs = []
        if asl > 20:
            recs.append("Consider breaking down long sentences (> 20 words) for cognitive accessibility.")
        if complex_pct > 18:
            recs.append("High ratio of multi-syllabic vocabulary detected; provide glossary definitions.")

        return ReadingAssessmentResponse(
            document_id=document_id,
            lexile=LexileEstimate(
                score=lexile_score,
                grade_equivalent=grade_eq,
                difficulty_band=band
            ),
            metrics=AssessmentMetrics(
                word_count=word_count,
                sentence_count=sentence_count,
                syllable_count=syllable_count,
                flesch_kincaid_grade=fk_grade,
                gunning_fog_index=fog,
                average_sentence_length=round(asl, 2),
                complex_word_percentage=complex_pct
            ),
            recommendations=recs
        )

    def evaluate_document(self, doc: ContentDocument) -> ReadingAssessmentResponse:
        full_text = []
        for s in doc.sections:
            for b in s.blocks:
                if b.type in (BlockType.PARAGRAPH, BlockType.HEADING) and b.source_text:
                    full_text.append(b.source_text)
        text = " ".join(full_text) or doc.title or "Sample text"
        return self.evaluate_text(text, document_id=doc.id)

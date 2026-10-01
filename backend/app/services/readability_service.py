"""Readability calculator service."""
import re
import math
from app.schemas.readability import ReadabilityReport, ReadabilityScores, TextStatistics
from app.schemas.enums import ReadabilityGradeBand, CEFRLevel

class ReadabilityService:
    """Calculates standard readability metrics for educational content."""

    @staticmethod
    def count_syllables(word: str) -> int:
        word = word.lower().strip()
        if not word:
            return 0
        word = re.sub(r'[^a-z]', '', word)
        if len(word) <= 3:
            return 1
        # Remove trailing e
        word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
        word = re.sub(r'^y', '', word)
        matches = re.findall(r'[aeiouy]{1,2}', word)
        return max(len(matches), 1)

    def analyze_text(self, text: str) -> ReadabilityReport:
        clean = text.strip()
        if not clean:
            clean = "Empty text"

        raw_words = re.findall(r'\b[a-zA-Z0-9_-]+\b', clean)
        word_count = max(len(raw_words), 1)
        raw_sentences = [s for s in re.split(r'[.!?]+', clean) if s.strip()]
        sentence_count = max(len(raw_sentences), 1)
        paragraphs = [p for p in clean.split('\n\n') if p.strip()]
        paragraph_count = max(len(paragraphs), 1)

        syllable_counts = [self.count_syllables(w) for w in raw_words]
        total_syllables = sum(syllable_counts)
        complex_words = sum(1 for c in syllable_counts if c >= 3)

        avg_words_per_sent = word_count / sentence_count
        avg_syll_per_word = total_syllables / word_count

        # Flesch Reading Ease
        fre = 206.835 - (1.015 * avg_words_per_sent) - (84.6 * avg_syll_per_word)
        fre = round(max(0.0, min(100.0, fre)), 1)

        # Flesch-Kincaid Grade Level
        fkgl = (0.39 * avg_words_per_sent) + (11.8 * avg_syll_per_word) - 15.59
        fkgl = round(max(1.0, fkgl), 1)

        # Gunning Fog
        fog = 0.4 * (avg_words_per_sent + 100 * (complex_words / word_count))
        fog = round(max(1.0, fog), 1)

        # SMOG
        smog = 1.0430 * math.sqrt(complex_words * (30 / sentence_count)) + 3.1291 if sentence_count >= 3 else fkgl
        smog = round(max(1.0, smog), 1)

        # ARI
        chars = sum(len(w) for w in raw_words)
        ari = (4.71 * (chars / word_count)) + (0.5 * avg_words_per_sent) - 21.43
        ari = round(max(1.0, ari), 1)

        grade_band, cefr, label = self._map_grade(fkgl)
        recs = []
        if avg_words_per_sent > 20:
            recs.append("Shorten long sentences to support readers with dyslexia and ADHD.")
        if complex_words / word_count > 0.15:
            recs.append("Define or substitute complex multisyllabic terms.")

        return ReadabilityReport(
            text_sample_preview=clean[:120] + ("..." if len(clean) > 120 else ""),
            statistics=TextStatistics(
                character_count=len(clean),
                word_count=word_count,
                sentence_count=sentence_count,
                paragraph_count=paragraph_count,
                complex_word_count=complex_words,
                avg_words_per_sentence=round(avg_words_per_sent, 1),
                avg_syllables_per_word=round(avg_syll_per_word, 2),
            ),
            scores=ReadabilityScores(
                flesch_reading_ease=fre,
                flesch_kincaid_grade=fkgl,
                gunning_fog_index=fog,
                smog_index=smog,
                automated_readability_index=ari,
            ),
            grade_band=grade_band,
            cefr_level=cefr,
            cognitive_difficulty_label=label,
            recommendations=recs,
        )

    def _map_grade(self, fkgl: float):
        if fkgl <= 3.5:
            return ReadabilityGradeBand.EARLY_PRIMARY, CEFRLevel.A1, "Very Accessible"
        if fkgl <= 5.9:
            return ReadabilityGradeBand.UPPER_PRIMARY, CEFRLevel.A2, "Accessible"
        if fkgl <= 8.9:
            return ReadabilityGradeBand.MIDDLE_SCHOOL, CEFRLevel.B1, "Standard School"
        if fkgl <= 12.0:
            return ReadabilityGradeBand.HIGH_SCHOOL, CEFRLevel.B2, "Moderate Complexity"
        if fkgl <= 16.0:
            return ReadabilityGradeBand.COLLEGE, CEFRLevel.C1, "Advanced"
        return ReadabilityGradeBand.ACADEMIC_EXPERT, CEFRLevel.C2, "Scholarly / Dense"

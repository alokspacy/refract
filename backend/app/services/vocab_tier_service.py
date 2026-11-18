"""Service categorizing document words into Beck's Three-Tier Vocabulary model."""
import re
from typing import List
from app.schemas.content import ContentDocument
from app.schemas.vocab_tier import VocabularyTierReport, TieredWord

class VocabTierService:
    def analyze_document_tiers(self, doc: ContentDocument) -> VocabularyTierReport:
        glossary_lower = {k.lower() for k in doc.glossary.keys()}
        t1, t2, t3 = 0, 0, 0
        highlighted: List[TieredWord] = []
        seen = set()

        for sec in doc.sections:
            for b in sec.blocks:
                if not b.source_text:
                    continue
                for w in re.findall(r'\b[a-zA-Z]+\b', b.source_text):
                    wl = w.lower()
                    if wl in glossary_lower:
                        t3 += 1
                        if wl not in seen:
                            seen.add(wl)
                            highlighted.append(TieredWord(word=w, tier=3, reason="Domain-specific glossary concept"))
                    elif len(wl) >= 8:
                        t2 += 1
                        if wl not in seen and len(highlighted) < 25:
                            seen.add(wl)
                            highlighted.append(TieredWord(word=w, tier=2, reason="High-utility academic vocabulary"))
                    else:
                        t1 += 1

        return VocabularyTierReport(
            tier_1_count=t1,
            tier_2_count=t2,
            tier_3_count=t3,
            highlighted_terms=highlighted
        )

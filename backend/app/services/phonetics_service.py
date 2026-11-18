"""Service breaking academic vocabulary into syllable phonetic respellings."""
import re
from typing import List
from app.schemas.phonetics import PhoneticEntry, PhoneticGuideResponse

class PhoneticsService:
    @staticmethod
    def _split_syllables(word: str) -> List[str]:
        clean = re.sub(r'[^a-zA-Z]', '', word)
        if len(clean) <= 4:
            return [clean]
        chunks = re.findall(r'[^aeiouy]*[aeiouy]+(?:[^aeiouy]+(?=[^aeiouy][aeiouy])|[^aeiouy]*$)', clean, re.IGNORECASE)
        return chunks if chunks else [clean]

    def generate_guide(self, terms: List[str]) -> PhoneticGuideResponse:
        entries: List[PhoneticEntry] = []
        for raw_term in terms:
            t = raw_term.strip()
            if not t:
                continue
            syls = self._split_syllables(t)
            respelling_parts = [s.upper() if idx == 0 else s.lower() for idx, s in enumerate(syls)]
            entries.append(PhoneticEntry(
                term=t,
                syllables=syls,
                phonetic_respelling="-".join(respelling_parts),
                stressed_index=0
            ))

        return PhoneticGuideResponse(
            total_terms=len(entries),
            entries=entries
        )

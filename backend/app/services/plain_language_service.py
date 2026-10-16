"""Plain language rewriting and jargon replacement service."""
import re
from typing import List, Dict
from app.schemas.plain_language import JargonReplacement, PlainLanguageResponse

JARGON_MAP: Dict[str, str] = {
    "utilize": "use",
    "commence": "begin",
    "subsequently": "later",
    "elucidate": "explain",
    "homeostasis": "internal balance",
    "mitigate": "lessen",
    "demonstrate": "show",
    "facilitate": "help",
    "cognizant": "aware"
}

class PlainLanguageService:
    """Simplifies complex scholarly vocabulary into clear, accessible language."""

    def simplify_text(self, text: str) -> PlainLanguageResponse:
        replacements: List[JargonReplacement] = []
        simplified = text

        for word, plain in JARGON_MAP.items():
            pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE)
            matches = pattern.findall(simplified)
            if matches:
                replacements.append(JargonReplacement(
                    original_term=matches[0],
                    plain_alternative=plain,
                    context_note=f"Replaced scholarly '{matches[0]}' with clearer '{plain}'"
                ))
                simplified = pattern.sub(plain, simplified)

        return PlainLanguageResponse(
            source_text=text,
            simplified_text=simplified,
            replacements_made=replacements,
            reading_ease_improvement=round(len(replacements) * 4.2, 1)
        )

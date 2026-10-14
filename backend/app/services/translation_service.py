"""Multilingual translation service preserving block IDs and layout."""
from app.schemas.translation import (
    LanguageCode, TranslationBlockResult, TranslationDocumentResponse
)
from app.schemas.content import ContentDocument

RTL_LANGUAGES = {LanguageCode.AR}

# Mock linguistic dictionary for educational terms
TRANSLATIONS = {
    LanguageCode.ES: {
        "Photosynthesis Basics": "Conceptos básicos de fotosíntesis",
        "Plants convert light into chemical energy.": "Las plantas convierten la luz en energía química."
    },
    LanguageCode.FR: {
        "Photosynthesis Basics": "Notions de base de la photosynthèse",
        "Plants convert light into chemical energy.": "Les plantes transforment la lumière en énergie chimique."
    }
}

class TranslationService:
    """Translates content blocks while strictly preserving accessibility tags and bounding boxes."""

    def translate_document(self, doc: ContentDocument, lang: LanguageCode) -> TranslationDocumentResponse:
        dict_map = TRANSLATIONS.get(lang, {})
        is_rtl = lang in RTL_LANGUAGES

        blocks = []
        for sec in doc.sections:
            for b in sec.blocks:
                txt = b.source_text or ""
                translated = dict_map.get(txt, f"[{lang.value.upper()}] {txt}")
                blocks.append(TranslationBlockResult(
                    block_id=b.id,
                    target_language=lang,
                    translated_text=translated,
                    is_rtl=is_rtl
                ))

        return TranslationDocumentResponse(
            document_id=doc.id,
            target_language=lang,
            translated_title=dict_map.get(doc.title, f"[{lang.value.upper()}] {doc.title}"),
            is_rtl=is_rtl,
            blocks=blocks
        )

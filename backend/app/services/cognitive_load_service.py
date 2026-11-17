"""Service estimating cognitive load scores from concept density and block length."""
from app.schemas.content import ContentDocument
from app.schemas.cognitive_load import CognitiveLoadEstimate

class CognitiveLoadService:
    def analyze_load(self, doc: ContentDocument) -> CognitiveLoadEstimate:
        total_blocks = 0
        long_blocks = 0

        for sec in doc.sections:
            for b in sec.blocks:
                total_blocks += 1
                if b.source_text and len(b.source_text.split()) > 120:
                    long_blocks += 1

        glossary_count = len(doc.glossary)
        intrinsic = min(100.0, round(glossary_count * 6.5 + 25.0, 1))
        extraneous = min(100.0, round((long_blocks / max(1, total_blocks)) * 100.0 + 15.0, 1))
        avg_load = (intrinsic + extraneous) / 2.0

        band = "Low" if avg_load < 40 else ("Moderate" if avg_load < 70 else "High")
        bottlenecks = []
        if long_blocks > 0:
            bottlenecks.append(f"{long_blocks} dense text blocks exceed 120 words.")
        if glossary_count > 10:
            bottlenecks.append("High novel terminology density per section.")

        return CognitiveLoadEstimate(
            document_id=doc.id,
            intrinsic_load_score=intrinsic,
            extraneous_load_score=extraneous,
            overall_load_band=band,
            bottlenecks=bottlenecks
        )

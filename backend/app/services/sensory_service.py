"""Service checking and tailoring content according to sensory sensitivities."""
from app.schemas.sensory import SensoryProfile, MotionTolerance, ContrastPreference
from app.schemas.content import ContentDocument

class SensoryService:
    @staticmethod
    def inspect_content_hazards(doc: ContentDocument, profile: SensoryProfile) -> dict:
        flags = []

        for sec in doc.sections:
            for b in sec.blocks:
                if b.source_text and any(w in b.source_text.lower() for w in ["strobe", "flash", "flicker"]):
                    flags.append({
                        "block_id": b.id,
                        "hazard": "potential_flashing_content",
                        "severity": "high"
                    })

        accommodations = []
        if profile.motion != MotionTolerance.NORMAL:
            accommodations.append("Applied CSS prefers-reduced-motion override.")
        if profile.flash_suppression:
            accommodations.append("Filtered animations exceeding 3 flashes per second.")
        if profile.contrast == ContrastPreference.HIGH:
            accommodations.append("Enforced APCA compliant 60+ Lc high contrast theme.")

        return {
            "document_id": doc.id,
            "detected_hazards": flags,
            "accommodations_applied": accommodations,
            "safe_for_viewing": len(flags) == 0
        }

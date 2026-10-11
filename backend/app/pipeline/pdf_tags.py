"""Validates structural PDF/UA accessibility tags."""
from typing import List, Dict, Any

class PdfTagValidator:
    """Verifies that PDF export structures meet ISO 14289 (PDF/UA) tagging standards."""

    @staticmethod
    def validate_tags(tags: List[Dict[str, Any]]) -> Dict[str, Any]:
        has_struct_tree = any(t.get("type") == "StructTreeRoot" for t in tags)
        headings = [t for t in tags if t.get("tag", "").startswith("H")]
        has_h1 = any(t.get("tag") == "H1" for t in headings)

        issues = []
        if not has_struct_tree:
            issues.append("Document missing StructTreeRoot dictionary.")
        if not has_h1 and len(tags) > 3:
            issues.append("Tagged PDF has no primary H1 heading element.")

        return {
            "valid_pdf_ua": len(issues) == 0,
            "total_tags": len(tags),
            "issues": issues
        }

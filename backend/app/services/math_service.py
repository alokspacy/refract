"""Math accessibility conversion service."""
import re
from app.schemas.math_accessibility import MathAccessibleExpression

class MathService:
    """Translates LaTeX STEM equations into accessible MathML and ClearSpeak text."""

    def to_accessible_math(self, latex: str) -> MathAccessibleExpression:
        clean = latex.strip().replace("$", "")

        # Heuristic ClearSpeak speech translation
        spoken = clean
        spoken = re.sub(r'\frac\{([^}]+)\}\{([^}]+)\}', r'fraction  over , end fraction', spoken)
        spoken = re.sub(r'\^2', ' squared', spoken)
        spoken = re.sub(r'\^3', ' cubed', spoken)
        spoken = re.sub(r'\^\{([^}]+)\}', r' to the power of ', spoken)
        spoken = re.sub(r'\sqrt\{([^}]+)\}', r'square root of , end root', spoken)
        spoken = spoken.replace("+", " plus ").replace("-", " minus ").replace("=", " equals ")

        # Clean spaces
        spoken = re.sub(r'\s+', ' ', spoken).strip()

        mathml = (
            f'<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">'
            f'<mrow><mtext>{clean}</mtext></mrow>'
            f'</math>'
        )

        return MathAccessibleExpression(
            latex_source=clean,
            mathml=mathml,
            spoken_clearspeak=spoken,
            nemeth_braille=f"⠨⠹{clean}⠼",
            complexity_level="advanced" if "frac" in clean or "^" in clean else "elementary"
        )

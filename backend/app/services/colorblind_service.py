"""Service providing mathematically accurate color vision deficiency simulation matrices."""
from typing import Dict, List
from app.schemas.colorblind import DeficiencyType, ColorMatrix

MATRICES: Dict[DeficiencyType, List[List[float]]] = {
    DeficiencyType.PROTANOPIA: [
        [0.56667, 0.43333, 0.0],
        [0.55833, 0.44167, 0.0],
        [0.0,     0.24167, 0.75833]
    ],
    DeficiencyType.PROTANOMALY: [
        [0.81667, 0.18333, 0.0],
        [0.33333, 0.66667, 0.0],
        [0.0,     0.125,   0.875]
    ],
    DeficiencyType.DEUTERANOPIA: [
        [0.625,   0.375,   0.0],
        [0.70,    0.30,    0.0],
        [0.0,     0.30,    0.70]
    ],
    DeficiencyType.DEUTERANOMALY: [
        [0.80,    0.20,    0.0],
        [0.25833, 0.74167, 0.0],
        [0.0,     0.14167, 0.85833]
    ],
    DeficiencyType.TRITANOPIA: [
        [0.95,    0.05,    0.0],
        [0.0,     0.43333, 0.56667],
        [0.0,     0.475,   0.525]
    ],
    DeficiencyType.TRITANOMALY: [
        [0.96667, 0.03333, 0.0],
        [0.0,     0.73333, 0.26667],
        [0.0,     0.18333, 0.81667]
    ],
    DeficiencyType.ACHROMATOPSIA: [
        [0.299,   0.587,   0.114],
        [0.299,   0.587,   0.114],
        [0.299,   0.587,   0.114]
    ]
}

class ColorBlindService:
    def get_matrix(self, deficiency: DeficiencyType) -> ColorMatrix:
        matrix = MATRICES.get(deficiency, MATRICES[DeficiencyType.DEUTERANOPIA])
        return ColorMatrix(
            deficiency=deficiency,
            matrix=matrix,
            svg_filter_id=f"cvd-{deficiency.value}",
            description=f"Simulation filter for {deficiency.value.capitalize()}"
        )

    def generate_svg_filter(self, deficiency: DeficiencyType) -> str:
        m = self.get_matrix(deficiency).matrix
        vals = (
            f"{m[0][0]:.4f} {m[0][1]:.4f} {m[0][2]:.4f} 0 0 "
            f"{m[1][0]:.4f} {m[1][1]:.4f} {m[1][2]:.4f} 0 0 "
            f"{m[2][0]:.4f} {m[2][1]:.4f} {m[2][2]:.4f} 0 0 "
            "0 0 0 1 0"
        )
        return f'<filter id="cvd-{deficiency.value}"><feColorMatrix type="matrix" values="{vals}"/></filter>'

"""Tactile graphic and diagram description generator."""
import uuid
from typing import Dict, Any
from app.schemas.tactile import TactileGraphicDescription, TactileLayer

class TactileService:
    """Generates structured tactile diagrams and exploration scripts for blind learners."""

    def describe_image(self, asset_id: str, title: str, metadata: Dict[str, Any]) -> TactileGraphicDescription:
        fig_type = metadata.get("figure", "diagram")

        layers = [
            TactileLayer(
                layer_name="Main Boundary",
                raised_element_type="solid_raised_line",
                description="Outer boundary and primary shape contours.",
                braille_legend="OB"
            ),
            TactileLayer(
                layer_name="Focal Regions",
                raised_element_type="textured_dots",
                description="Key zones containing thematic structures or cellular bodies.",
                braille_legend="FZ"
            ),
            TactileLayer(
                layer_name="Braille Labels",
                raised_element_type="braille_label",
                description="UEB Grade 2 two-cell indicators for component identification.",
                braille_legend="A1..A4"
            )
        ]

        guide = (
            "Begin at the top left corner of the page. Move your right hand clockwise along the solid raised line. "
            "In the center, notice the textured dotted region representing internal components. "
            "Braille legend labels are located directly adjacent to each key feature."
        )

        return TactileGraphicDescription(
            asset_id=asset_id,
            title=title or "Tactile Science Graphic",
            visual_overview=f"Raised line diagram for pedagogical exploration of {title.lower()}.",
            tactile_exploration_guide=guide,
            layers=layers,
            key_findings=[
                "Main structure has clear spatial proportions.",
                "High tactile contrast separates primary and secondary features."
            ]
        )

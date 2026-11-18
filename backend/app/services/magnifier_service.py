"""Service computing bounding box and transform origin for low-vision screen magnification."""
from app.schemas.magnifier_config import MagnifierLensConfig

class MagnifierService:
    def compute_viewport_bounds(self, cursor_x: int, cursor_y: int, config: MagnifierLensConfig) -> dict:
        half_w = config.lens_width_px // 2
        half_h = config.lens_height_px // 2
        return {
            "left": max(0, cursor_x - half_w),
            "top": max(0, cursor_y - half_h),
            "width": config.lens_width_px,
            "height": config.lens_height_px,
            "scale": config.zoom_factor,
            "css_filter": "invert(100%)" if config.invert_colors else "none"
        }

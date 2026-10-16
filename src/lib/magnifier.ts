/**
 * Magnification calculations for low-vision learners.
 */
export interface MagnifierState {
  x: number;
  y: number;
  zoomLevel: number;
  active: boolean;
}

export function calculateMagnifiedOffset(
  mouseX: number,
  mouseY: number,
  lensRadius: number,
  zoom: number
): { offsetX: number; offsetY: number } {
  return {
    offsetX: -(mouseX * zoom - lensRadius),
    offsetY: -(mouseY * zoom - lensRadius),
  };
}

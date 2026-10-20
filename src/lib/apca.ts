/**
 * Accessible Perceptual Contrast Algorithm (APCA) lightness contrast approximation.
 */
export function sRGBtoY(r: number, g: number, b: number): number {
  const rs = Math.pow(r / 255.0, 2.4);
  const gs = Math.pow(g / 255.0, 2.4);
  const bs = Math.pow(b / 255.0, 2.4);
  return 0.2126729 * rs + 0.7151522 * gs + 0.0721750 * bs;
}

export function calculateLc(txtY: number, bgY: number): number {
  if (Math.abs(txtY - bgY) < 0.0005) return 0.0;
  // Perceptual polarity calculation
  if (bgY > txtY) {
    return (Math.pow(bgY, 0.56) - Math.pow(txtY, 0.57)) * 1.14 * 100;
  } else {
    return (Math.pow(bgY, 0.65) - Math.pow(txtY, 0.62)) * 1.14 * 100;
  }
}

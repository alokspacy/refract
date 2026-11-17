/**
 * High-visibility focus indicator helper for WCAG 2.4.11 Focus Appearance.
 */

export interface FocusRingOptions {
  color: string;
  widthPx: number;
  offsetPx: number;
}

export const HIGH_VISIBILITY_FOCUS: FocusRingOptions = {
  color: '#facc15',
  widthPx: 3,
  offsetPx: 3,
};

export function applyFocusRingVariables(options: FocusRingOptions = HIGH_VISIBILITY_FOCUS): void {
  if (typeof document === 'undefined') return;
  const root = document.documentElement;
  root.style.setProperty('--focus-ring-color', options.color);
  root.style.setProperty('--focus-ring-width', `${options.widthPx}px`);
  root.style.setProperty('--focus-ring-offset', `${options.offsetPx}px`);
}

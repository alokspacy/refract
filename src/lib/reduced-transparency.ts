/**
 * Helper enforcing solid opaque backgrounds for users with low vision or contrast sensitivity.
 */

export function setReducedTransparency(enabled: boolean): void {
  if (typeof document === 'undefined') return;
  const root = document.documentElement;
  if (enabled) {
    root.classList.add('reduce-transparency');
    root.style.setProperty('--backdrop-blur-amount', '0px');
    root.style.setProperty('--surface-opacity', '1');
  } else {
    root.classList.remove('reduce-transparency');
    root.style.setProperty('--backdrop-blur-amount', '8px');
    root.style.setProperty('--surface-opacity', '0.85');
  }
}

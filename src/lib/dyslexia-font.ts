/**
 * Dyslexia-friendly typography utility helper.
 * Handles OpenDyslexic / Lexend font classes and custom letter spacing.
 */

export interface TypographySettings {
  fontFamily: 'default' | 'opendyslexic' | 'lexend' | 'atkinson';
  fontSizeRatio: number;
  lineHeightRatio: number;
  letterSpacingPx: number;
}

export const DEFAULT_TYPOGRAPHY_SETTINGS: TypographySettings = {
  fontFamily: 'default',
  fontSizeRatio: 1.0,
  lineHeightRatio: 1.5,
  letterSpacingPx: 0.5,
};

export function applyTypographyStyles(settings: TypographySettings): void {
  if (typeof document === 'undefined') return;

  const root = document.documentElement;

  const fontMap: Record<string, string> = {
    opendyslexic: "'OpenDyslexic', sans-serif",
    lexend: "'Lexend', sans-serif",
    atkinson: "'Atkinson Hyperlegible', sans-serif",
    default: 'inherit',
  };

  root.style.setProperty('--user-font-family', fontMap[settings.fontFamily] || 'inherit');
  root.style.setProperty('--user-font-scale', `${settings.fontSizeRatio}`);
  root.style.setProperty('--user-line-height', `${settings.lineHeightRatio}`);
  root.style.setProperty('--user-letter-spacing', `${settings.letterSpacingPx}px`);
}

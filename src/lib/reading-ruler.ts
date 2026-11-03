/**
 * Assistive reading ruler utility state and CSS injection helper.
 * Keeps user focused on the active line of text to reduce cognitive strain.
 */

export interface ReadingRulerConfig {
  enabled: boolean;
  heightPx: number;
  opacity: number;
  tintColor: string;
}

export const DEFAULT_RULER_CONFIG: ReadingRulerConfig = {
  enabled: false,
  heightPx: 48,
  opacity: 0.15,
  tintColor: '#fef08a', // Pale yellow focus tint
};

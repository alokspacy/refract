/**
 * Curated accessible color palettes compliant with WCAG AAA (7.0+ contrast ratio).
 */
export interface ContrastPalette {
  id: string;
  name: string;
  bg: string;
  text: string;
  accent: string;
  border: string;
}

export const CONTRAST_PALETTES: ContrastPalette[] = [
  {
    id: "yellow-on-black",
    name: "Yellow on Black (Low Vision)",
    bg: "#000000",
    text: "#FFFF00",
    accent: "#00FFFF",
    border: "#FFFF00",
  },
  {
    id: "soft-cream",
    name: "Soft Cream & Amber (Dyslexia)",
    bg: "#FAF6EE",
    text: "#2C2621",
    accent: "#B85D19",
    border: "#E2D9CC",
  },
  {
    id: "ocean-calm",
    name: "Ocean Calm (ADHD Focus)",
    bg: "#0B1528",
    text: "#E2EDF8",
    accent: "#38BDF8",
    border: "#1E3A5F",
  },
];

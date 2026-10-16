/**
 * Local storage persistence helper for user contrast and font themes.
 */
export function getSavedTheme(): string {
  if (typeof window === "undefined") return "default";
  return localStorage.getItem("accesslearn_theme") || "default";
}

export function saveTheme(theme: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem("accesslearn_theme", theme);
}

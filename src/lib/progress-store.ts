/**
 * Local storage persistence helper for student reading progress.
 */
const KEY_PREFIX = "accesslearn_progress_";

export function saveReadingProgress(docId: string, percent: number): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(`${KEY_PREFIX}${docId}`, String(Math.round(percent)));
}

export function getReadingProgress(docId: string): number {
  if (typeof window === "undefined") return 0;
  const val = localStorage.getItem(`${KEY_PREFIX}${docId}`);
  return val ? parseInt(val, 10) : 0;
}

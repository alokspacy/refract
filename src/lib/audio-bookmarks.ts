/**
 * Local storage manager for narration audio bookmarks and playback checkpoints.
 */
export interface AudioBookmark {
  variantId: string;
  blockId: string;
  timestampSec: number;
  note?: string;
  savedAt: string;
}

const STORAGE_KEY = "accesslearn_audio_bookmarks";

export function saveAudioBookmark(bookmark: AudioBookmark): void {
  const all = getAudioBookmarks();
  const filtered = all.filter((b) => !(b.variantId === bookmark.variantId && b.blockId === bookmark.blockId));
  filtered.push(bookmark);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
}

export function getAudioBookmarks(): AudioBookmark[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

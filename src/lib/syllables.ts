/**
 * Splits English words into hyphenated phonetic syllable chunks for dyslexic reading support.
 */
export function hyphenateWord(word: string): string {
  if (word.length <= 4) return word;

  // Insert hyphen between double consonants or after common vowel patterns
  return word
    .replace(/([bcdfghjklmnpqrstvwxyz])([bcdfghjklmnpqrstvwxyz])/gi, "$1·$2")
    .replace(/(tion|sion|ment|ing|ed)$/gi, "·$1");
}

export function toSyllableChunkedText(text: string): string {
  return text
    .split(/(\s+)/)
    .map((w) => (/^\s+$/.test(w) ? w : hyphenateWord(w)))
    .join("");
}

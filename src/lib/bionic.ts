/**
 * Bionic Reading algorithm: highlights fixation points to guide saccadic eye movements.
 */
export function formatBionicWord(word: string): { bold: string; rest: string } {
  const clean = word.trim();
  if (clean.length === 0) return { bold: "", rest: "" };
  if (clean.length <= 3) return { bold: clean.slice(0, 1), rest: clean.slice(1) };
  if (clean.length <= 6) return { bold: clean.slice(0, 2), rest: clean.slice(2) };
  if (clean.length <= 9) return { bold: clean.slice(0, 3), rest: clean.slice(3) };
  return { bold: clean.slice(0, Math.ceil(clean.length * 0.4)), rest: clean.slice(Math.ceil(clean.length * 0.4)) };
}

export function toBionicHtml(text: string): string {
  if (!text) return "";
  const words = text.split(/(\s+)/);
  return words
    .map((w) => {
      if (/^\s+$/.test(w)) return w;
      const { bold, rest } = formatBionicWord(w);
      return `<b class="font-bold text-accent">${bold}</b>${rest}`;
    })
    .join("");
}

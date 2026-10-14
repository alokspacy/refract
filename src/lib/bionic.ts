/**
 * Bionic Reading algorithm: highlights fixation points to guide saccadic eye movements.
 * Preserves trailing punctuation and special characters.
 */
export function formatBionicWord(word: string): { bold: string; rest: string } {
  const match = word.match(/^([a-zA-Z0-9]+)([^a-zA-Z0-9]*)$/);
  if (!match) {
    return { bold: "", rest: word };
  }

  const core = match[1];
  const punct = match[2] || "";

  let boldLen = 1;
  if (core.length <= 3) boldLen = 1;
  else if (core.length <= 6) boldLen = 2;
  else if (core.length <= 9) boldLen = 3;
  else boldLen = Math.ceil(core.length * 0.4);

  return {
    bold: core.slice(0, boldLen),
    rest: core.slice(boldLen) + punct,
  };
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

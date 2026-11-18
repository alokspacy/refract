'use client';

import React, { useState } from 'react';

export interface SymbolItem {
  cell_id: string;
  label: string;
  speech_phrase: string;
  color_hex?: string;
}

const DEFAULT_SYMBOLS: SymbolItem[] = [
  { cell_id: '1', label: 'Explain', speech_phrase: 'Please explain this concept.', color_hex: '#fef08a' },
  { cell_id: '2', label: 'Slower', speech_phrase: 'Please read slower.', color_hex: '#bbf7d0' },
  { cell_id: '3', label: 'Example', speech_phrase: 'Can I see an example?', color_hex: '#bfdbfe' },
  { cell_id: '4', label: 'Break', speech_phrase: 'I need a short break.', color_hex: '#fecaca' },
];

export function AACBoard({ symbols = DEFAULT_SYMBOLS }: { symbols?: SymbolItem[] }) {
  const [sentenceStrip, setSentenceStrip] = useState<string>('');

  const speakPhrase = (phrase: string) => {
    setSentenceStrip(phrase);
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(phrase);
      window.speechSynthesis.speak(utterance);
    }
  };

  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-semibold uppercase tracking-wider text-muted-foreground">
          AAC Communication Board
        </span>
        {sentenceStrip && (
          <button
            type="button"
            onClick={() => setSentenceStrip('')}
            className="text-muted-foreground hover:text-foreground"
          >
            Clear
          </button>
        )}
      </div>

      <div className="p-2.5 min-h-[40px] rounded-lg bg-muted/60 border border-border text-xs font-medium flex items-center">
        {sentenceStrip || 'Tap a symbol cell to speak...'}
      </div>

      <div className="grid grid-cols-2 gap-2">
        {symbols.map((s) => (
          <button
            key={s.cell_id}
            type="button"
            onClick={() => speakPhrase(s.speech_phrase)}
            className="p-3 rounded-xl border border-black/10 text-black font-bold text-xs shadow-sm hover:opacity-90 transition"
            style={{ backgroundColor: s.color_hex || '#e2e8f0' }}
          >
            {s.label}
          </button>
        ))}
      </div>
    </div>
  );
}

"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

export interface Flashcard {
  id: string;
  term: string;
  definition: string;
  memory_cue: string;
  example: string;
}

export function FlashcardDeck({ cards }: { cards: Flashcard[] }) {
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);

  if (!cards || cards.length === 0) return null;
  const current = cards[index];

  return (
    <div className="flex flex-col items-center gap-4 w-full max-w-md mx-auto">
      <div
        onClick={() => setFlipped(!flipped)}
        className="w-full h-64 cursor-pointer perspective-1000"
      >
        <Glass
          strong
          className={`w-full h-full p-6 flex flex-col justify-center items-center text-center transition-all duration-300 border-2 ${
            flipped ? "border-accent/60 bg-accent/5" : "border-white/20"
          }`}
        >
          {!flipped ? (
            <div>
              <span className="text-xs uppercase tracking-widest text-accent mb-2 block">Vocabulary Term</span>
              <h3 className="text-2xl font-bold">{current.term}</h3>
              <p className="text-xs text-ink-muted mt-4">Click to reveal definition & mnemonic</p>
            </div>
          ) : (
            <div>
              <span className="text-xs uppercase tracking-widest text-ink-muted mb-2 block">Simplified Definition</span>
              <p className="text-sm font-medium mb-3">{current.definition}</p>
              <div className="p-2.5 bg-accent/10 rounded-lg border border-accent/20 text-xs text-accent">
                💡 <span className="font-semibold">Memory Cue:</span> {current.memory_cue}
              </div>
            </div>
          )}
        </Glass>
      </div>

      <div className="flex items-center gap-4 text-xs">
        <button
          onClick={() => { setFlipped(false); setIndex((prev) => Math.max(0, prev - 1)); }}
          disabled={index === 0}
          className="px-3 py-1.5 rounded-lg bg-white/10 disabled:opacity-30"
        >
          ← Prev
        </button>
        <span>{index + 1} / {cards.length}</span>
        <button
          onClick={() => { setFlipped(false); setIndex((prev) => Math.min(cards.length - 1, prev + 1)); }}
          disabled={index === cards.length - 1}
          className="px-3 py-1.5 rounded-lg bg-white/10 disabled:opacity-30"
        >
          Next →
        </button>
      </div>
    </div>
  );
}

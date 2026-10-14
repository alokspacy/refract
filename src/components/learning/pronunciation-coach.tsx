"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface CoachProps {
  term: string;
  phonetic: string;
  syllables: string[];
}

export function PronunciationCoach({ term, phonetic, syllables }: CoachProps) {
  const [activeSyllable, setActiveSyllable] = useState<number | null>(null);

  const speak = (text: string) => {
    window.speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(text);
    utt.rate = 0.8;
    window.speechSynthesis.speak(utt);
  };

  return (
    <Glass strong className="p-4 rounded-xl border border-white/10 space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-bold text-accent uppercase">Pronunciation Coach</span>
        <button
          onClick={() => speak(term)}
          className="px-2.5 py-1 bg-accent/20 text-accent rounded font-semibold text-xs"
        >
          🔊 Hear Whole Word
        </button>
      </div>

      <div className="text-center py-2">
        <h4 className="text-xl font-bold">{term}</h4>
        <p className="text-xs font-mono text-ink-muted">{phonetic}</p>
      </div>

      <div className="flex justify-center gap-2">
        {syllables.map((s, idx) => (
          <button
            key={idx}
            onClick={() => {
              setActiveSyllable(idx);
              speak(s);
            }}
            className={`px-3 py-1.5 rounded-lg border text-sm font-bold font-mono transition-colors ${
              activeSyllable === idx ? "bg-accent text-black border-accent" : "bg-white/5 border-white/10"
            }`}
          >
            {s}
          </button>
        ))}
      </div>
    </Glass>
  );
}

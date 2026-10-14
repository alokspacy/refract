"use client";

import React from "react";
import { Glass } from "@/components/ui/glass";

interface ASLToken {
  gloss: string;
  isFingerspelled?: boolean;
  facialGrammar?: string;
}

interface SignLanguageCardProps {
  englishText: string;
  aslSequence: string;
  tokens: ASLToken[];
}

export function SignLanguageCard({ englishText, aslSequence, tokens }: SignLanguageCardProps) {
  return (
    <Glass strong className="p-4 rounded-xl border border-white/10 space-y-3">
      <div className="flex items-center justify-between text-xs">
        <span className="font-bold text-accent uppercase tracking-wider">ASL Grammatical Gloss</span>
        <span className="px-2 py-0.5 bg-accent/20 text-accent rounded text-[0.65rem] font-bold">Topic-Comment</span>
      </div>

      <div className="flex flex-wrap gap-1.5 p-3 bg-black/40 rounded-lg border border-white/5">
        {tokens.map((t, idx) => (
          <span
            key={idx}
            className={`px-2 py-1 rounded text-xs font-mono font-bold ${
              t.isFingerspelled ? "bg-amber-500/20 text-amber-300 border border-amber-500/30" : "bg-accent/20 text-accent"
            }`}
          >
            {t.isFingerspelled ? `#${t.gloss}` : t.gloss}
          </span>
        ))}
      </div>

      <p className="text-[0.7rem] text-ink-muted">
        <span className="font-semibold text-ink">English:</span> {englishText}
      </p>
    </Glass>
  );
}

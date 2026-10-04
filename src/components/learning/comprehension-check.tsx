"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface Option {
  id: string;
  text: string;
  isCorrect: boolean;
  explanation: string;
}

interface ComprehensionCheckProps {
  prompt: string;
  options: Option[];
}

export function ComprehensionCheck({ prompt, options }: ComprehensionCheckProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const selected = options.find((o) => o.id === selectedId);

  return (
    <Glass strong className="p-5 rounded-2xl border border-white/15 space-y-4">
      <div className="flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-accent" />
        <h4 className="text-xs uppercase font-bold tracking-wider text-accent">Self-Check Question</h4>
      </div>

      <p className="text-sm font-semibold leading-snug">{prompt}</p>

      <div className="space-y-2">
        {options.map((opt) => (
          <button
            key={opt.id}
            onClick={() => setSelectedId(opt.id)}
            className={`w-full text-left p-3 rounded-xl border text-xs transition-all ${
              selectedId === opt.id
                ? opt.isCorrect
                  ? "border-emerald-500 bg-emerald-500/10 text-emerald-300"
                  : "border-rose-500 bg-rose-500/10 text-rose-300"
                : "border-white/10 hover:border-white/20 bg-white/5"
            }`}
          >
            {opt.text}
          </button>
        ))}
      </div>

      {selected && (
        <div
          className={`p-3 rounded-xl text-xs ${
            selected.isCorrect ? "bg-emerald-500/20 text-emerald-200" : "bg-rose-500/20 text-rose-200"
          }`}
        >
          <span className="font-bold">{selected.isCorrect ? "✓ Correct!" : "✗ Note:"}</span> {selected.explanation}
        </div>
      )}
    </Glass>
  );
}

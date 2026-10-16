"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

const LEVELS = [
  { id: "high_focus", label: "⚡ High Energy", desc: "Ready for deep reading & quizzes." },
  { id: "steady", label: "🌿 Steady Focus", desc: "Balanced pacing with reading guide." },
  { id: "overwhelmed", label: "🛡️ Overwhelmed", desc: "Enable sensory shield & plain language." },
  { id: "tired", label: "🌙 Low Energy", desc: "Audio narration with calm voice mode." },
];

export function EnergyCheckin({ onSelect }: { onSelect?: (level: string) => void }) {
  const [selected, setSelected] = useState("steady");

  return (
    <Glass strong className="p-5 rounded-2xl border border-white/10 space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-bold text-accent uppercase">Sensory & Energy Check-in</span>
        <span className="text-ink-muted">Customized Comfort</span>
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs">
        {LEVELS.map((lvl) => (
          <button
            key={lvl.id}
            onClick={() => {
              setSelected(lvl.id);
              onSelect?.(lvl.id);
            }}
            className={`p-3 rounded-xl border text-left transition-all ${
              selected === lvl.id
                ? "border-accent bg-accent/15 text-accent font-bold"
                : "border-white/10 bg-white/5 hover:border-white/20"
            }`}
          >
            <div>{lvl.label}</div>
            <div className="text-[0.65rem] text-ink-muted mt-0.5">{lvl.desc}</div>
          </button>
        ))}
      </div>
    </Glass>
  );
}

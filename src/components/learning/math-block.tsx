"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface MathBlockProps {
  latex: string;
  clearspeak: string;
}

export function MathBlock({ latex, clearspeak }: MathBlockProps) {
  const [speaking, setSpeaking] = useState(false);

  const speak = () => {
    window.speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(clearspeak);
    utt.rate = 0.85;
    utt.onend = () => setSpeaking(false);
    setSpeaking(true);
    window.speechSynthesis.speak(utt);
  };

  return (
    <Glass className="p-4 border border-accent/20 rounded-xl space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-[0.68rem] uppercase font-bold tracking-wider text-accent">Accessible Equation</span>
        <button
          onClick={speak}
          className="flex items-center gap-1.5 px-2.5 py-1 bg-accent/20 text-accent rounded-full text-xs font-semibold hover:bg-accent/30"
        >
          <span>{speaking ? "🔊 Speaking..." : "▶ Read Math Aloud"}</span>
        </button>
      </div>

      <div className="py-2 text-center text-lg font-mono font-bold text-ink">
        {latex}
      </div>

      <div className="p-2 bg-white/5 rounded text-xs text-ink-muted">
        <span className="font-semibold text-ink">ClearSpeak:</span> &ldquo;{clearspeak}&rdquo;
      </div>
    </Glass>
  );
}

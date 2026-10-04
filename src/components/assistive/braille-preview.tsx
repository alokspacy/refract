"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface BraillePreviewProps {
  brailleText: string;
  sourceText: string;
  grade?: "Grade 1" | "Grade 2";
}

export function BraillePreview({ brailleText, sourceText, grade = "Grade 2" }: BraillePreviewProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(brailleText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Glass strong className="p-4 rounded-xl border border-white/10 space-y-3">
      <div className="flex items-center justify-between text-xs">
        <span className="font-semibold text-accent uppercase tracking-wider">UEB {grade} Braille</span>
        <button
          onClick={handleCopy}
          className="px-2.5 py-1 bg-white/10 hover:bg-white/20 rounded text-[0.7rem] transition-colors"
        >
          {copied ? "✓ Copied" : "Copy Unicode"}
        </button>
      </div>

      <div className="p-3 bg-black/40 rounded-lg border border-white/5 font-mono text-xl tracking-widest text-emerald-400 select-all">
        {brailleText}
      </div>

      <p className="text-[0.7rem] text-ink-muted leading-relaxed">
        <span className="font-semibold text-ink">Source:</span> {sourceText}
      </p>
    </Glass>
  );
}

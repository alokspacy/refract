"use client";

import React from "react";
import { Glass } from "@/components/ui/glass";

interface BlockDiffProps {
  sourceText: string;
  adaptedText: string;
  sourceType: string;
  profileName: string;
}

export function BlockDiffViewer({ sourceText, adaptedText, sourceType, profileName }: BlockDiffProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
      {/* Original Source */}
      <Glass className="p-4 border border-white/10">
        <div className="flex justify-between items-center mb-2">
          <span className="text-[0.65rem] uppercase tracking-wider text-ink-muted">Original Document ({sourceType})</span>
          <span className="text-[0.65rem] bg-white/10 px-1.5 py-0.5 rounded">Source</span>
        </div>
        <p className="text-xs text-ink/80 leading-relaxed font-mono">{sourceText}</p>
      </Glass>

      {/* Adapted Accessible Variant */}
      <Glass strong className="p-4 border border-accent/30 bg-accent/5">
        <div className="flex justify-between items-center mb-2">
          <span className="text-[0.65rem] uppercase tracking-wider text-accent font-semibold">Accessible ({profileName})</span>
          <span className="text-[0.65rem] bg-accent/20 text-accent px-1.5 py-0.5 rounded font-bold">100% Grounded</span>
        </div>
        <p className="text-xs text-ink leading-relaxed font-sans">{adaptedText}</p>
      </Glass>
    </div>
  );
}

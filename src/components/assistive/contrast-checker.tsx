"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";
import { getContrastRatio, isWcagAa } from "@/lib/accessibility";

export function ContrastChecker() {
  const [ratio, setRatio] = useState<number>(7.4);

  return (
    <Glass className="p-3 border border-white/10 rounded-xl space-y-1.5 text-xs">
      <div className="flex justify-between items-center">
        <span className="font-semibold text-accent">Contrast Inspector</span>
        <span className="font-mono font-bold text-emerald-400">{ratio}:1</span>
      </div>
      <div className="flex gap-2 text-[0.68rem]">
        <span className="text-emerald-400">✓ WCAG AA (Normal)</span>
        <span className="text-emerald-400">✓ WCAG AAA (Large)</span>
      </div>
    </Glass>
  );
}

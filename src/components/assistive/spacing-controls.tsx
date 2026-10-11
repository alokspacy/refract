"use client";

import React from "react";
import { Glass } from "@/components/ui/glass";

interface SpacingControlsProps {
  letterSpacing: number;
  onLetterSpacingChange: (val: number) => void;
  lineHeight: number;
  onLineHeightChange: (val: number) => void;
}

export function SpacingControls({
  letterSpacing,
  onLetterSpacingChange,
  lineHeight,
  onLineHeightChange,
}: SpacingControlsProps) {
  return (
    <Glass className="p-3 border border-white/10 rounded-xl space-y-2 text-xs">
      <div className="flex justify-between items-center">
        <span>Letter Spacing (+{letterSpacing}px)</span>
        <div className="flex gap-1">
          <button onClick={() => onLetterSpacingChange(Math.max(0, letterSpacing - 1))} className="px-2 bg-white/10 rounded">-</button>
          <button onClick={() => onLetterSpacingChange(Math.min(6, letterSpacing + 1))} className="px-2 bg-white/10 rounded">+</button>
        </div>
      </div>
      <div className="flex justify-between items-center">
        <span>Line Height ({lineHeight.toFixed(1)}x)</span>
        <div className="flex gap-1">
          <button onClick={() => onLineHeightChange(Math.max(1.3, lineHeight - 0.2))} className="px-2 bg-white/10 rounded">-</button>
          <button onClick={() => onLineHeightChange(Math.min(2.5, lineHeight + 0.2))} className="px-2 bg-white/10 rounded">+</button>
        </div>
      </div>
    </Glass>
  );
}

"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

export function PitchSlider() {
  const [pitch, setPitch] = useState(1.0);

  return (
    <Glass className="p-3 border border-white/10 rounded-xl space-y-1 text-xs">
      <div className="flex justify-between items-center">
        <span>Voice Pitch</span>
        <span className="font-mono font-bold text-accent">{pitch.toFixed(1)}x</span>
      </div>
      <input
        type="range"
        min="0.5"
        max="1.5"
        step="0.1"
        value={pitch}
        onChange={(e) => setPitch(parseFloat(e.target.value))}
        className="w-full accent-accent"
      />
    </Glass>
  );
}

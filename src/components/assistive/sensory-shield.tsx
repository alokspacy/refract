"use client";

import React from "react";
import { Glass } from "@/components/ui/glass";

interface SensoryShieldProps {
  reducedMotion: boolean;
  onToggleMotion: () => void;
  muteAllAudio: boolean;
  onToggleAudio: () => void;
  calmPalette: boolean;
  onTogglePalette: () => void;
}

export function SensoryShield({
  reducedMotion,
  onToggleMotion,
  muteAllAudio,
  onToggleAudio,
  calmPalette,
  onTogglePalette,
}: SensoryShieldProps) {
  return (
    <Glass strong className="p-4 rounded-xl border border-white/10 space-y-3">
      <div className="flex items-center gap-2">
        <span className="text-base">🛡️</span>
        <h4 className="text-xs uppercase font-bold tracking-wider text-accent">Sensory Overload Shield</h4>
      </div>

      <div className="grid grid-cols-3 gap-2 text-xs">
        <button
          onClick={onToggleMotion}
          className={`p-2 rounded-lg border text-center font-semibold transition-colors ${
            reducedMotion ? "bg-accent/20 border-accent text-accent" : "bg-white/5 border-white/10"
          }`}
        >
          {reducedMotion ? "✓ Motion Off" : "Reduce Motion"}
        </button>

        <button
          onClick={onToggleAudio}
          className={`p-2 rounded-lg border text-center font-semibold transition-colors ${
            muteAllAudio ? "bg-accent/20 border-accent text-accent" : "bg-white/5 border-white/10"
          }`}
        >
          {muteAllAudio ? "✓ Sounds Muted" : "Mute Sounds"}
        </button>

        <button
          onClick={onTogglePalette}
          className={`p-2 rounded-lg border text-center font-semibold transition-colors ${
            calmPalette ? "bg-accent/20 border-accent text-accent" : "bg-white/5 border-white/10"
          }`}
        >
          {calmPalette ? "✓ Muted Colors" : "Calm Colors"}
        </button>
      </div>
    </Glass>
  );
}

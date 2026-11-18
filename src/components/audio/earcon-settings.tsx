'use client';

import React, { useState } from 'react';

export function EarconSettings() {
  const [enabled, setEnabled] = useState(true);

  const playTestTone = (freq: number) => {
    if (!enabled || typeof window === 'undefined') return;
    const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.frequency.value = freq;
    gain.gain.value = 0.1;
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.12);
  };

  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3 text-xs">
      <div className="flex justify-between items-center">
        <span className="font-semibold uppercase tracking-wider text-muted-foreground">
          Acoustic Landmark Earcons
        </span>
        <input
          type="checkbox"
          checked={enabled}
          onChange={(e) => setEnabled(e.target.checked)}
          className="accent-primary h-4 w-4"
          aria-label="Enable acoustic earcons"
        />
      </div>
      <div className="flex gap-2">
        <button
          type="button"
          onClick={() => playTestTone(523)}
          className="flex-1 py-1.5 px-2 rounded border border-border hover:bg-muted transition"
        >
          Test Section Cue
        </button>
        <button
          type="button"
          onClick={() => playTestTone(880)}
          className="flex-1 py-1.5 px-2 rounded border border-border hover:bg-muted transition"
        >
          Test Success Cue
        </button>
      </div>
    </div>
  );
}

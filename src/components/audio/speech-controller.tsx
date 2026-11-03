'use client';

import React, { useState } from 'react';

export function SpeechController() {
  const [rate, setRate] = useState<number>(1.0);
  const [pitch, setPitch] = useState<number>(1.0);

  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3">
      <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Speech Playback Dynamics
      </h4>

      <div className="space-y-1">
        <div className="flex justify-between text-xs">
          <span>Reading Rate</span>
          <span className="font-mono">{rate.toFixed(2)}x</span>
        </div>
        <input
          type="range"
          min="0.5"
          max="2.5"
          step="0.05"
          value={rate}
          onChange={(e) => setRate(parseFloat(e.target.value))}
          className="w-full accent-primary"
          aria-label="Speech rate slider"
        />
      </div>

      <div className="space-y-1">
        <div className="flex justify-between text-xs">
          <span>Voice Pitch</span>
          <span className="font-mono">{pitch.toFixed(2)}</span>
        </div>
        <input
          type="range"
          min="0.6"
          max="1.6"
          step="0.05"
          value={pitch}
          onChange={(e) => setPitch(parseFloat(e.target.value))}
          className="w-full accent-primary"
          aria-label="Voice pitch slider"
        />
      </div>

      <div className="flex gap-2 pt-1">
        <button
          type="button"
          onClick={() => { setRate(0.8); setPitch(1.0); }}
          className="text-xs py-1 px-2.5 rounded bg-muted hover:bg-muted/80 text-foreground transition"
        >
          Dyslexic (0.8x)
        </button>
        <button
          type="button"
          onClick={() => { setRate(1.0); setPitch(1.0); }}
          className="text-xs py-1 px-2.5 rounded bg-muted hover:bg-muted/80 text-foreground transition"
        >
          Standard (1.0x)
        </button>
        <button
          type="button"
          onClick={() => { setRate(1.4); setPitch(1.0); }}
          className="text-xs py-1 px-2.5 rounded bg-muted hover:bg-muted/80 text-foreground transition"
        >
          Speed (1.4x)
        </button>
      </div>
    </div>
  );
}

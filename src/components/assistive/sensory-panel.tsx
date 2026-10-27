'use client';

import React, { useState } from 'react';

export function SensoryPanel() {
  const [reduceMotion, setReduceMotion] = useState(false);
  const [suppressFlash, setSuppressFlash] = useState(true);
  const [audioNormalize, setAudioNormalize] = useState(true);

  return (
    <div className="p-4 rounded-xl border border-border bg-card space-y-4">
      <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
        Sensory & Neurodiversity Preferences
      </h3>

      <div className="space-y-3">
        <label className="flex items-center justify-between text-xs cursor-pointer">
          <span>Reduce Motion & Animations</span>
          <input
            type="checkbox"
            checked={reduceMotion}
            onChange={(e) => setReduceMotion(e.target.checked)}
            className="accent-primary h-4 w-4 rounded"
          />
        </label>

        <label className="flex items-center justify-between text-xs cursor-pointer">
          <span>Flash & Strobe Suppression</span>
          <input
            type="checkbox"
            checked={suppressFlash}
            onChange={(e) => setSuppressFlash(e.target.checked)}
            className="accent-primary h-4 w-4 rounded"
          />
        </label>

        <label className="flex items-center justify-between text-xs cursor-pointer">
          <span>Normalize Audio Volume Peaks</span>
          <input
            type="checkbox"
            checked={audioNormalize}
            onChange={(e) => setAudioNormalize(e.target.checked)}
            className="accent-primary h-4 w-4 rounded"
          />
        </label>
      </div>
    </div>
  );
}

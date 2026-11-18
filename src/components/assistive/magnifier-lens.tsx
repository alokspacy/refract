'use client';

import React, { useState } from 'react';

export function MagnifierLens() {
  const [zoom, setZoom] = useState(2.0);
  const [invert, setInvert] = useState(false);

  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3 text-xs">
      <div className="flex justify-between items-center">
        <span className="font-semibold uppercase tracking-wider text-muted-foreground">
          Low-Vision Magnifier Lens
        </span>
        <span className="font-mono font-bold text-primary">{zoom.toFixed(1)}x</span>
      </div>

      <input
        type="range"
        min="1.5"
        max="5.0"
        step="0.5"
        value={zoom}
        onChange={(e) => setZoom(parseFloat(e.target.value))}
        className="w-full accent-primary"
        aria-label="Magnification zoom factor"
      />

      <label className="flex items-center justify-between cursor-pointer">
        <span>Invert Lens Polarity</span>
        <input
          type="checkbox"
          checked={invert}
          onChange={(e) => setInvert(e.target.checked)}
          className="accent-primary h-4 w-4"
        />
      </label>
    </div>
  );
}

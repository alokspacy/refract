'use client';

import React, { useState } from 'react';

export function CaptionCustomizer() {
  const [textColor, setTextColor] = useState('#FFFFFF');
  const [bgColor, setBgColor] = useState('#000000');
  const [scale, setScale] = useState(100);

  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3">
      <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Closed Caption Appearance
      </h4>

      <div
        className="p-3 rounded-lg text-center font-medium transition-all"
        style={{
          backgroundColor: bgColor,
          color: textColor,
          fontSize: `${Math.round(14 * (scale / 100))}px`,
        }}
      >
        [Sample Synchronized Caption Track]
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs">
        <button
          type="button"
          onClick={() => { setTextColor('#FFFFFF'); setBgColor('#000000'); }}
          className="py-1.5 px-2 rounded border border-border hover:bg-muted"
        >
          White on Black
        </button>
        <button
          type="button"
          onClick={() => { setTextColor('#FFFF00'); setBgColor('#000000'); }}
          className="py-1.5 px-2 rounded border border-border hover:bg-muted"
        >
          Yellow on Black
        </button>
      </div>

      <div className="space-y-1">
        <div className="flex justify-between text-xs">
          <span>Caption Size</span>
          <span>{scale}%</span>
        </div>
        <input
          type="range"
          min="75"
          max="175"
          step="25"
          value={scale}
          onChange={(e) => setScale(parseInt(e.target.value))}
          className="w-full accent-primary"
        />
      </div>
    </div>
  );
}

'use client';

import React, { useState, useEffect } from 'react';
import { TypographySettings, DEFAULT_TYPOGRAPHY_SETTINGS, applyTypographyStyles } from '@/lib/dyslexia-font';

export function TypographyControls() {
  const [settings, setSettings] = useState<TypographySettings>(DEFAULT_TYPOGRAPHY_SETTINGS);

  useEffect(() => {
    applyTypographyStyles(settings);
  }, [settings]);

  const update = (partial: Partial<TypographySettings>) => {
    setSettings((prev) => ({ ...prev, ...partial }));
  };

  return (
    <section 
      aria-label="Typography Accessibility Controls" 
      className="p-4 bg-card text-card-foreground rounded-xl border border-border shadow-sm space-y-4"
    >
      <h3 className="text-sm font-semibold tracking-wide uppercase text-muted-foreground">
        Assistive Typography
      </h3>

      <div className="space-y-1">
        <label htmlFor="font-family-select" className="text-xs font-medium block">
          Font Family
        </label>
        <select
          id="font-family-select"
          value={settings.fontFamily}
          onChange={(e) => update({ fontFamily: e.target.value as TypographySettings['fontFamily'] })}
          className="w-full text-xs p-2 rounded-lg border border-input bg-background"
        >
          <option value="default">Standard System Font</option>
          <option value="opendyslexic">OpenDyslexic (Dyslexia-Optimized)</option>
          <option value="lexend">Lexend (Reading Fluency)</option>
          <option value="atkinson">Atkinson Hyperlegible (Low Vision)</option>
        </select>
      </div>

      <div className="space-y-1">
        <div className="flex justify-between text-xs">
          <span>Text Scale</span>
          <span>{Math.round(settings.fontSizeRatio * 100)}%</span>
        </div>
        <input
          type="range"
          min="0.8"
          max="1.6"
          step="0.05"
          value={settings.fontSizeRatio}
          onChange={(e) => update({ fontSizeRatio: parseFloat(e.target.value) })}
          className="w-full accent-primary"
          aria-label="Text scale slider"
        />
      </div>

      <div className="space-y-1">
        <div className="flex justify-between text-xs">
          <span>Line Spacing</span>
          <span>{settings.lineHeightRatio.toFixed(1)}x</span>
        </div>
        <input
          type="range"
          min="1.2"
          max="2.4"
          step="0.1"
          value={settings.lineHeightRatio}
          onChange={(e) => update({ lineHeightRatio: parseFloat(e.target.value) })}
          className="w-full accent-primary"
          aria-label="Line spacing slider"
        />
      </div>

      <button
        type="button"
        onClick={() => setSettings(DEFAULT_TYPOGRAPHY_SETTINGS)}
        className="w-full text-xs py-1.5 px-3 rounded-lg border border-border text-muted-foreground hover:text-foreground hover:bg-muted transition"
      >
        Reset Typography Defaults
      </button>
    </section>
  );
}

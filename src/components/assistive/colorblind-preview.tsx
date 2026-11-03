'use client';

import React, { useState } from 'react';

const CVD_FILTERS: Record<string, string> = {
  none: '',
  protanopia: 'url(#cvd-protanopia)',
  deuteranopia: 'url(#cvd-deuteranopia)',
  tritanopia: 'url(#cvd-tritanopia)',
  achromatopsia: 'grayscale(100%)',
};

export function ColorblindPreview() {
  const [filterMode, setFilterMode] = useState<string>('none');

  const applyFilter = (mode: string) => {
    setFilterMode(mode);
    if (typeof document !== 'undefined') {
      const target = document.getElementById('preview-content-root') || document.body;
      target.style.filter = CVD_FILTERS[mode] || '';
    }
  };

  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3">
      <div className="flex justify-between items-center">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Color Vision Deficiency Simulator
        </h4>
        <span className="text-[10px] px-2 py-0.5 rounded bg-muted text-muted-foreground font-mono">
          WCAG 1.4.1
        </span>
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs">
        <button
          type="button"
          onClick={() => applyFilter('none')}
          className={`py-1.5 px-3 rounded-lg border text-left transition ${
            filterMode === 'none' ? 'bg-primary text-primary-foreground border-primary' : 'border-border hover:bg-muted'
          }`}
        >
          Normal Vision
        </button>
        <button
          type="button"
          onClick={() => applyFilter('protanopia')}
          className={`py-1.5 px-3 rounded-lg border text-left transition ${
            filterMode === 'protanopia' ? 'bg-primary text-primary-foreground border-primary' : 'border-border hover:bg-muted'
          }`}
        >
          Protanopia (Red-Blind)
        </button>
        <button
          type="button"
          onClick={() => applyFilter('deuteranopia')}
          className={`py-1.5 px-3 rounded-lg border text-left transition ${
            filterMode === 'deuteranopia' ? 'bg-primary text-primary-foreground border-primary' : 'border-border hover:bg-muted'
          }`}
        >
          Deuteranopia (Green-Blind)
        </button>
        <button
          type="button"
          onClick={() => applyFilter('tritanopia')}
          className={`py-1.5 px-3 rounded-lg border text-left transition ${
            filterMode === 'tritanopia' ? 'bg-primary text-primary-foreground border-primary' : 'border-border hover:bg-muted'
          }`}
        >
          Tritanopia (Blue-Blind)
        </button>
        <button
          type="button"
          onClick={() => applyFilter('achromatopsia')}
          className={`col-span-2 py-1.5 px-3 rounded-lg border text-left transition ${
            filterMode === 'achromatopsia' ? 'bg-primary text-primary-foreground border-primary' : 'border-border hover:bg-muted'
          }`}
        >
          Achromatopsia (Monochrome)
        </button>
      </div>

      <svg className="hidden" aria-hidden="true">
        <defs>
          <filter id="cvd-protanopia">
            <feColorMatrix type="matrix" values="0.5667 0.4333 0 0 0 0.5583 0.4417 0 0 0 0 0.2417 0.7583 0 0 0 0 0 1 0" />
          </filter>
          <filter id="cvd-deuteranopia">
            <feColorMatrix type="matrix" values="0.625 0.375 0 0 0 0.7 0.3 0 0 0 0 0.3 0.7 0 0 0 0 0 1 0" />
          </filter>
          <filter id="cvd-tritanopia">
            <feColorMatrix type="matrix" values="0.95 0.05 0 0 0 0 0.4333 0.5667 0 0 0 0.475 0.525 0 0 0 0 0 1 0" />
          </filter>
        </defs>
      </svg>
    </div>
  );
}

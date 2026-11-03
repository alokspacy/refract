'use client';

import React, { useState, useEffect } from 'react';
import { ReadingRulerConfig, DEFAULT_RULER_CONFIG } from '@/lib/reading-ruler';

export function ReadingRuler() {
  const [config, setConfig] = useState<ReadingRulerConfig>(DEFAULT_RULER_CONFIG);
  const [posY, setPosY] = useState<number>(200);

  useEffect(() => {
    if (!config.enabled) return;
    const handleMouseMove = (e: MouseEvent) => {
      setPosY(e.clientY);
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [config.enabled]);

  return (
    <>
      <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3">
        <div className="flex justify-between items-center text-xs">
          <span className="font-semibold uppercase tracking-wider text-muted-foreground">
            Reading Guide Ruler
          </span>
          <button
            type="button"
            onClick={() => setConfig((c) => ({ ...c, enabled: !c.enabled }))}
            className={`px-3 py-1 rounded-full text-xs font-semibold transition ${
              config.enabled ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'
            }`}
          >
            {config.enabled ? 'Enabled' : 'Disabled'}
          </button>
        </div>

        {config.enabled && (
          <div className="space-y-1">
            <div className="flex justify-between text-xs">
              <span>Ruler Height</span>
              <span>{config.heightPx}px</span>
            </div>
            <input
              type="range"
              min="24"
              max="96"
              value={config.heightPx}
              onChange={(e) => setConfig((c) => ({ ...c, heightPx: parseInt(e.target.value) }))}
              className="w-full accent-primary"
            />
          </div>
        )}
      </div>

      {config.enabled && (
        <div
          aria-hidden="true"
          className="fixed left-0 right-0 pointer-events-none z-40 transition-[top] duration-75"
          style={{
            top: `${posY - config.heightPx / 2}px`,
            height: `${config.heightPx}px`,
            backgroundColor: config.tintColor,
            opacity: config.opacity,
            boxShadow: '0 0 0 9999px rgba(0, 0, 0, 0.25)',
          }}
        />
      )}
    </>
  );
}

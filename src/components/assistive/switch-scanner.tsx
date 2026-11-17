'use client';

import React, { useState, useEffect } from 'react';

const DEMO_TARGETS = ['Main Navigation', 'Document Reader', 'Audio Player', 'Quiz Section'];

export function SwitchScanner() {
  const [active, setActive] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (!active) return;
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % DEMO_TARGETS.length);
    }, 1200);
    return () => clearInterval(interval);
  }, [active]);

  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-semibold uppercase tracking-wider text-muted-foreground">
          Switch Access Auto-Scanner
        </span>
        <button
          type="button"
          onClick={() => setActive(!active)}
          className={`px-3 py-1 rounded-full font-semibold transition ${
            active ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'
          }`}
        >
          {active ? 'Scanning' : 'Off'}
        </button>
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs">
        {DEMO_TARGETS.map((target, idx) => (
          <div
            key={target}
            className={`p-2 rounded-lg border text-center font-medium transition ${
              active && currentIndex === idx
                ? 'border-2 border-primary bg-primary/10 text-primary'
                : 'border-border text-muted-foreground'
            }`}
          >
            {target}
          </div>
        ))}
      </div>
    </div>
  );
}

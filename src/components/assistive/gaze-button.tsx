'use client';

import React, { useState, useRef } from 'react';

interface GazeButtonProps {
  label: string;
  dwellMs?: number;
  onActivate?: () => void;
}

export function GazeButton({ label, dwellMs = 800, onActivate }: GazeButtonProps) {
  const [progress, setProgress] = useState(0);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const startDwell = () => {
    const stepMs = 40;
    let elapsed = 0;
    timerRef.current = setInterval(() => {
      elapsed += stepMs;
      const pct = Math.min(100, Math.round((elapsed / dwellMs) * 100));
      setProgress(pct);
      if (elapsed >= dwellMs) {
        if (timerRef.current) clearInterval(timerRef.current);
        onActivate?.();
      }
    }, stepMs);
  };

  const cancelDwell = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    setProgress(0);
  };

  return (
    <button
      type="button"
      onMouseEnter={startDwell}
      onMouseLeave={cancelDwell}
      onFocus={startDwell}
      onBlur={cancelDwell}
      onClick={onActivate}
      className="relative overflow-hidden py-3 px-5 rounded-xl border-2 border-primary font-semibold text-xs bg-card text-foreground shadow-sm transition"
    >
      <span
        aria-hidden="true"
        className="absolute inset-y-0 left-0 bg-primary/20 transition-all duration-75"
        style={{ width: `${progress}%` }}
      />
      <span className="relative z-10">{label}</span>
    </button>
  );
}

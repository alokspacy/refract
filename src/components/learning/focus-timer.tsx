'use client';

import React, { useState, useEffect, useRef } from 'react';

export function FocusTimer() {
  const [secondsLeft, setSecondsLeft] = useState(25 * 60);
  const [isActive, setIsActive] = useState(false);
  const [isBreak, setIsBreak] = useState(false);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (isActive) {
      timerRef.current = setInterval(() => {
        setSecondsLeft((prev) => {
          if (prev <= 1) {
            setIsBreak((b) => !b);
            return isBreak ? 25 * 60 : 5 * 60;
          }
          return prev - 1;
        });
      }, 1000);
    } else if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isActive, isBreak]);

  const toggle = () => setIsActive(!isActive);
  const reset = () => {
    setIsActive(false);
    setIsBreak(false);
    setSecondsLeft(25 * 60);
  };

  const minutes = Math.floor(secondsLeft / 60);
  const seconds = secondsLeft % 60;

  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3 text-center">
      <div className="flex justify-between items-center text-xs">
        <span className="font-semibold uppercase tracking-wider text-muted-foreground">
          {isBreak ? '☕ Rest Interval' : '🎯 Deep Focus'}
        </span>
        <span className="px-2 py-0.5 rounded bg-muted text-muted-foreground font-mono">
          Executive Aid
        </span>
      </div>

      <div className="text-3xl font-mono font-bold tracking-tight py-2">
        {String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}
      </div>

      <div className="flex justify-center gap-2">
        <button
          type="button"
          onClick={toggle}
          className={`py-1.5 px-4 rounded-lg font-medium text-xs transition ${
            isActive ? 'bg-amber-600 text-white' : 'bg-primary text-primary-foreground'
          }`}
        >
          {isActive ? 'Pause' : 'Start Focus'}
        </button>
        <button
          type="button"
          onClick={reset}
          className="py-1.5 px-3 rounded-lg border border-border text-xs text-muted-foreground hover:bg-muted transition"
        >
          Reset
        </button>
      </div>
    </div>
  );
}

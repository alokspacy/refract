"use client";

import React from "react";
import { Glass } from "@/components/ui/glass";
import { usePacingTimer } from "@/hooks/use-pacing-timer";

export function PacingTimer() {
  const { secondsLeft, isRunning, isBreak, toggle, reset } = usePacingTimer(25);

  const mins = Math.floor(secondsLeft / 60);
  const secs = secondsLeft % 60;
  const timeFormatted = `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;

  return (
    <Glass className="p-4 border border-white/10 rounded-xl space-y-2 text-center text-xs">
      <span className="font-bold text-accent uppercase tracking-wider">
        {isBreak ? "☕ Stretch & Rest Break" : "🎯 Focus Interval"}
      </span>
      <div className="text-3xl font-mono font-bold my-1 text-ink">{timeFormatted}</div>
      <div className="flex justify-center gap-2">
        <button onClick={toggle} className="px-3 py-1 bg-accent text-black rounded font-bold">
          {isRunning ? "Pause" : "Start"}
        </button>
        <button onClick={reset} className="px-3 py-1 bg-white/10 rounded">
          Reset
        </button>
      </div>
    </Glass>
  );
}

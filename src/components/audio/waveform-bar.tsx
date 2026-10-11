"use client";

import React from "react";

interface WaveformBarProps {
  isPlaying: boolean;
  barCount?: number;
}

export function WaveformBar({ isPlaying, barCount = 16 }: WaveformBarProps) {
  return (
    <div className="flex items-center gap-1 h-6 px-2">
      {Array.from({ length: barCount }).map((_, i) => (
        <span
          key={i}
          className="w-1 bg-accent rounded-full transition-all duration-150"
          style={{
            height: isPlaying ? `${Math.max(20, Math.sin((i + 1) * 0.8) * 100)}%` : "20%",
            opacity: isPlaying ? 0.9 : 0.3,
          }}
        />
      ))}
    </div>
  );
}

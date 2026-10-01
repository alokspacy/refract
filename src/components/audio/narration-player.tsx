"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface NarrationPlayerProps {
  onCueChange?: (blockId: string | null) => void;
  title?: string;
}

export function NarrationPlayer({ onCueChange, title = "Audio Narration" }: NarrationPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState<number>(0.9);
  const [progress, setProgress] = useState<number>(25);

  const togglePlay = () => setIsPlaying(!isPlaying);

  return (
    <Glass strong className="p-3.5 flex items-center gap-4 border border-white/15 rounded-2xl shadow-xl">
      <button
        onClick={togglePlay}
        className="w-10 h-10 rounded-full bg-accent text-black flex items-center justify-center font-bold text-sm shadow hover:scale-105 transition-transform"
      >
        {isPlaying ? "❚❚" : "▶"}
      </button>

      <div className="flex-1">
        <div className="flex justify-between text-xs mb-1">
          <span className="font-semibold">{title}</span>
          <span className="text-ink-muted">01:14 / 04:30</span>
        </div>
        <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
          <div className="h-full bg-accent transition-all duration-200" style={{ width: `${progress}%` }} />
        </div>
      </div>

      <div className="flex items-center gap-2">
        <select
          value={speed}
          onChange={(e) => setSpeed(parseFloat(e.target.value))}
          className="bg-black/30 border border-white/10 rounded px-2 py-1 text-xs text-ink"
        >
          <option value="0.75">0.75x (Dyslexia)</option>
          <option value="0.9">0.9x (Calm)</option>
          <option value="1.0">1.0x (Normal)</option>
          <option value="1.25">1.25x (Fast)</option>
        </select>
      </div>
    </Glass>
  );
}

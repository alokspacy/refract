"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface Cue {
  cue_id: number;
  start_sec: number;
  end_sec: number;
  speaker_label?: string;
  text: string;
}

interface InteractiveTranscriptProps {
  cues: Cue[];
  currentTime?: number;
  onSeek?: (sec: number) => void;
}

export function InteractiveTranscript({ cues, currentTime = 0, onSeek }: InteractiveTranscriptProps) {
  return (
    <Glass strong className="p-4 rounded-xl border border-white/10 space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-bold text-accent uppercase">Accessible Media Transcript</span>
        <span className="text-[0.65rem] text-ink-muted">Click any line to seek</span>
      </div>

      <div className="max-h-64 overflow-y-auto space-y-2 pr-1">
        {cues.map((c) => {
          const isActive = currentTime >= c.start_sec && currentTime <= c.end_sec;
          return (
            <div
              key={c.cue_id}
              onClick={() => onSeek?.(c.start_sec)}
              className={`p-2.5 rounded-lg text-xs cursor-pointer transition-colors ${
                isActive ? "bg-accent/20 border border-accent/40 text-accent font-semibold" : "bg-white/5 hover:bg-white/10 text-ink/90"
              }`}
            >
              <div className="flex items-center justify-between text-[0.65rem] text-ink-muted mb-1 font-mono">
                <span>{c.speaker_label ? `[${c.speaker_label}]` : "Speaker"}</span>
                <span>{Math.floor(c.start_sec / 60)}:{String(Math.floor(c.start_sec % 60)).padStart(2, "0")}</span>
              </div>
              <p>{c.text}</p>
            </div>
          );
        })}
      </div>
    </Glass>
  );
}

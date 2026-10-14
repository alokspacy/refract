"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";
import { ambientSound } from "@/lib/ambient-sound";

export function SoundGenerator() {
  const [playing, setPlaying] = useState(false);
  const [soundType, setSoundType] = useState<"brown" | "pink" | "white">("brown");

  const toggle = () => {
    if (playing) {
      ambientSound.stop();
      setPlaying(false);
    } else {
      ambientSound.start(soundType, 0.15);
      setPlaying(true);
    }
  };

  return (
    <Glass className="p-3 border border-white/10 rounded-xl space-y-2 text-xs">
      <div className="flex justify-between items-center">
        <span className="font-semibold text-accent">Ambient Focus Sound</span>
        <button
          onClick={toggle}
          className={`px-2.5 py-1 rounded text-xs font-bold ${
            playing ? "bg-rose-500 text-white" : "bg-accent text-black"
          }`}
        >
          {playing ? "⏹ Stop Sound" : "▶ Brown Noise"}
        </button>
      </div>
    </Glass>
  );
}

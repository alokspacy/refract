"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface AssistiveToolbarProps {
  bionicActive: boolean;
  onToggleBionic: () => void;
  maskActive: boolean;
  onToggleMask: () => void;
  rulerActive: boolean;
  onToggleRuler: () => void;
  fontSize: number;
  onFontSizeChange: (size: number) => void;
}

export function AssistiveToolbar({
  bionicActive,
  onToggleBionic,
  maskActive,
  onToggleMask,
  rulerActive,
  onToggleRuler,
  fontSize,
  onFontSizeChange,
}: AssistiveToolbarProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {open ? (
        <Glass strong className="p-4 flex flex-col gap-3 w-72 shadow-2xl border border-white/20">
          <div className="flex items-center justify-between border-b border-white/10 pb-2">
            <span className="text-xs uppercase font-bold tracking-wider text-accent">Assistive Studio</span>
            <button onClick={() => setOpen(false)} className="text-xs opacity-60 hover:opacity-100">✕ Close</button>
          </div>

          <div className="space-y-2 text-xs">
            <div className="flex items-center justify-between">
              <span>Bionic Reading</span>
              <button
                onClick={onToggleBionic}
                className={`px-2.5 py-1 rounded-md text-xs font-semibold ${bionicActive ? "bg-accent text-black" : "bg-white/10"}`}
              >
                {bionicActive ? "ON" : "OFF"}
              </button>
            </div>

            <div className="flex items-center justify-between">
              <span>Focus Reading Mask</span>
              <button
                onClick={onToggleMask}
                className={`px-2.5 py-1 rounded-md text-xs font-semibold ${maskActive ? "bg-accent text-black" : "bg-white/10"}`}
              >
                {maskActive ? "ON" : "OFF"}
              </button>
            </div>

            <div className="flex items-center justify-between">
              <span>Reading Ruler</span>
              <button
                onClick={onToggleRuler}
                className={`px-2.5 py-1 rounded-md text-xs font-semibold ${rulerActive ? "bg-accent text-black" : "bg-white/10"}`}
              >
                {rulerActive ? "ON" : "OFF"}
              </button>
            </div>

            <div className="flex items-center justify-between pt-1">
              <span>Font Scale ({fontSize}px)</span>
              <div className="flex gap-1">
                <button onClick={() => onFontSizeChange(Math.max(14, fontSize - 2))} className="px-2 py-0.5 bg-white/10 rounded">-</button>
                <button onClick={() => onFontSizeChange(Math.min(26, fontSize + 2))} className="px-2 py-0.5 bg-white/10 rounded">+</button>
              </div>
            </div>
          </div>
        </Glass>
      ) : (
        <button
          onClick={() => setOpen(true)}
          className="bg-accent text-black font-semibold px-4 py-2.5 rounded-full shadow-lg hover:scale-105 transition-all text-xs flex items-center gap-2"
        >
          <span>👁 Assistive Tools</span>
        </button>
      )}
    </div>
  );
}

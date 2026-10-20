"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

export function PaletteGenerator() {
  const [bg, setBg] = useState("#0a0f1d");
  const [text, setText] = useState("#f8fafc");
  const [accent, setAccent] = useState("#14b8a6");

  return (
    <Glass strong className="p-5 rounded-2xl border border-white/10 space-y-3 text-xs">
      <div className="flex justify-between items-center">
        <span className="font-bold text-accent uppercase">Custom Accessibility Palette</span>
        <span className="text-emerald-400 font-bold">✓ High Legibility</span>
      </div>

      <div className="grid grid-cols-3 gap-2">
        <div>
          <label className="block text-[0.68rem] text-ink-muted mb-1">Background</label>
          <input
            type="color"
            value={bg}
            onChange={(e) => setBg(e.target.value)}
            className="w-full h-8 rounded border border-white/10 cursor-pointer bg-transparent"
          />
        </div>
        <div>
          <label className="block text-[0.68rem] text-ink-muted mb-1">Text Color</label>
          <input
            type="color"
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="w-full h-8 rounded border border-white/10 cursor-pointer bg-transparent"
          />
        </div>
        <div>
          <label className="block text-[0.68rem] text-ink-muted mb-1">Accent</label>
          <input
            type="color"
            value={accent}
            onChange={(e) => setAccent(e.target.value)}
            className="w-full h-8 rounded border border-white/10 cursor-pointer bg-transparent"
          />
        </div>
      </div>

      <div
        className="p-3 rounded-lg border text-center font-semibold"
        style={{ backgroundColor: bg, color: text, borderColor: accent }}
      >
        Live Preview: AccessLearn AI Reading Mode
      </div>
    </Glass>
  );
}

"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface ZoomableDiagramProps {
  src: string;
  alt: string;
  caption?: string;
}

export function ZoomableDiagram({ src, alt, caption }: ZoomableDiagramProps) {
  const [scale, setScale] = useState(1);

  return (
    <Glass className="p-4 border border-white/10 rounded-xl space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-semibold text-accent">Interactive Visual Explorer</span>
        <div className="flex items-center gap-1.5">
          <button onClick={() => setScale(Math.max(1, scale - 0.25))} className="px-2 py-0.5 bg-white/10 rounded">-</button>
          <span>{Math.round(scale * 100)}%</span>
          <button onClick={() => setScale(Math.min(3, scale + 0.25))} className="px-2 py-0.5 bg-white/10 rounded">+</button>
          <button onClick={() => setScale(1)} className="px-2 py-0.5 bg-white/10 rounded ml-1">Reset</button>
        </div>
      </div>

      <div className="overflow-hidden border border-white/5 rounded-lg flex justify-center items-center min-h-48 bg-black/30">
        <div style={{ transform: `scale(${scale})`, transition: "transform 0.2s ease" }}>
          {/* Visual SVG diagram or placeholder */}
          <div className="w-64 h-40 bg-accent/10 border border-accent/30 rounded flex items-center justify-center text-xs text-accent">
            {alt}
          </div>
        </div>
      </div>

      {caption && <p className="text-xs text-ink-muted text-center italic">{caption}</p>}
    </Glass>
  );
}

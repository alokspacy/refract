"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface MagnifierLensProps {
  zoom?: number;
  active?: boolean;
}

export function MagnifierLens({ zoom = 2, active = false }: MagnifierLensProps) {
  const [zoomLevel, setZoomLevel] = useState(zoom);

  if (!active) return null;

  return (
    <Glass strong className="fixed bottom-20 left-6 z-40 p-3 rounded-2xl border border-white/20 text-xs space-y-2">
      <div className="flex justify-between items-center gap-3">
        <span className="font-bold text-accent uppercase">Screen Lens</span>
        <div className="flex items-center gap-1 font-mono">
          <button onClick={() => setZoomLevel(Math.max(1.5, zoomLevel - 0.5))} className="px-2 bg-white/10 rounded">-</button>
          <span>{zoomLevel.toFixed(1)}x</span>
          <button onClick={() => setZoomLevel(Math.min(4, zoomLevel + 0.5))} className="px-2 bg-white/10 rounded">+</button>
        </div>
      </div>
    </Glass>
  );
}

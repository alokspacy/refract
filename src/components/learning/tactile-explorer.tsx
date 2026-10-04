"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface Layer {
  name: string;
  type: string;
  desc: string;
}

export function TactileExplorer({
  title = "Leaf Cross-Section",
  guide = "Move hands clockwise along the raised edge to locate stomata.",
  layers = [
    { name: "Epidermis Boundary", type: "Raised Line", desc: "Top protective cellular layer." },
    { name: "Chloroplast Zone", type: "Textured Fill", desc: "Region with dense photosynthetic activity." }
  ]
}: {
  title?: string;
  guide?: string;
  layers?: Layer[];
}) {
  const [activeLayer, setActiveLayer] = useState<number>(0);

  return (
    <Glass strong className="p-5 border border-white/10 rounded-2xl space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <span className="text-[0.68rem] uppercase font-bold text-accent">Tactile Graphic Companion</span>
          <h3 className="text-base font-bold">{title}</h3>
        </div>
        <span className="px-2.5 py-1 bg-white/10 text-xs rounded-full">Tactile Ready</span>
      </div>

      <div className="p-3 bg-black/40 rounded-xl text-xs border border-white/5 space-y-1">
        <span className="font-semibold text-accent">Exploration Guide:</span>
        <p className="text-ink-muted">{guide}</p>
      </div>

      <div className="space-y-2">
        <span className="text-xs font-semibold">Diagram Layers:</span>
        <div className="grid grid-cols-2 gap-2">
          {layers.map((l, i) => (
            <button
              key={l.name}
              onClick={() => setActiveLayer(i)}
              className={`p-2.5 text-left rounded-lg border text-xs transition-colors ${
                activeLayer === i ? "border-accent bg-accent/10" : "border-white/10 bg-white/5"
              }`}
            >
              <div className="font-bold">{l.name}</div>
              <div className="text-[0.65rem] text-ink-muted">{l.type}</div>
            </button>
          ))}
        </div>
      </div>
    </Glass>
  );
}

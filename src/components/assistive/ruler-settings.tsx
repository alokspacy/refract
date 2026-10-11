"use client";

import React from "react";
import { Glass } from "@/components/ui/glass";

interface RulerSettingsProps {
  color: string;
  onColorChange: (color: string) => void;
  height: number;
  onHeightChange: (height: number) => void;
}

const RULER_COLORS = ["#14b8a6", "#f59e0b", "#ec4899", "#8b5cf6", "#3b82f6"];

export function RulerSettings({ color, onColorChange, height, onHeightChange }: RulerSettingsProps) {
  return (
    <Glass className="p-3 border border-white/10 rounded-xl space-y-2 text-xs">
      <span className="font-semibold text-accent">Ruler Guide Customization</span>
      <div className="flex items-center gap-2">
        <span>Color:</span>
        <div className="flex gap-1.5">
          {RULER_COLORS.map((c) => (
            <button
              key={c}
              onClick={() => onColorChange(c)}
              className={`w-5 h-5 rounded-full border-2 ${color === c ? "border-white scale-110" : "border-transparent"}`}
              style={{ backgroundColor: c }}
            />
          ))}
        </div>
      </div>
    </Glass>
  );
}

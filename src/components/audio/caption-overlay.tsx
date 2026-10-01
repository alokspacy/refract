"use client";

import React from "react";

interface CaptionOverlayProps {
  currentCueText: string | null;
  visible?: boolean;
}

export function CaptionOverlay({ currentCueText, visible = true }: CaptionOverlayProps) {
  if (!visible || !currentCueText) return null;

  return (
    <div className="fixed bottom-24 inset-x-0 flex justify-center pointer-events-none z-30 px-4">
      <div className="bg-black/85 text-yellow-300 px-6 py-2.5 rounded-xl border border-yellow-300/40 text-sm md:text-base font-semibold max-w-2xl text-center shadow-2xl backdrop-blur-sm">
        {currentCueText}
      </div>
    </div>
  );
}

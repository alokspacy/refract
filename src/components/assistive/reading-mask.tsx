"use client";

import React, { useEffect, useState } from "react";

interface ReadingMaskProps {
  enabled: boolean;
  windowHeight?: number;
}

export function ReadingMask({ enabled, windowHeight = 120 }: ReadingMaskProps) {
  const [mouseY, setMouseY] = useState<number>(300);

  useEffect(() => {
    if (!enabled) return;
    const handleMove = (e: MouseEvent) => {
      setMouseY(e.clientY);
    };
    window.addEventListener("mousemove", handleMove);
    return () => window.removeEventListener("mousemove", handleMove);
  }, [enabled]);

  if (!enabled) return null;

  const topMaskHeight = Math.max(0, mouseY - windowHeight / 2);
  const bottomMaskTop = mouseY + windowHeight / 2;

  return (
    <div className="pointer-events-none fixed inset-0 z-40 transition-opacity duration-150">
      {/* Top overlay */}
      <div
        className="absolute inset-x-0 top-0 bg-black/65 backdrop-blur-[1px]"
        style={{ height: `${topMaskHeight}px` }}
      />
      {/* Bottom overlay */}
      <div
        className="absolute inset-x-0 bottom-0 bg-black/65 backdrop-blur-[1px]"
        style={{ top: `${bottomMaskTop}px` }}
      />
      {/* Clear focus guide lines */}
      <div
        className="absolute inset-x-0 border-y-2 border-accent/80 shadow-[0_0_15px_rgba(20,184,166,0.3)]"
        style={{ top: `${topMaskHeight}px`, height: `${windowHeight}px` }}
      />
    </div>
  );
}

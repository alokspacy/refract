"use client";

import React, { useEffect, useState } from "react";

interface FocusRulerProps {
  enabled: boolean;
  color?: string;
  height?: number;
}

export function FocusRuler({ enabled, color = "#14b8a6", height = 4 }: FocusRulerProps) {
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

  return (
    <div
      className="pointer-events-none fixed inset-x-0 z-50 transition-all duration-75 shadow-lg"
      style={{
        top: `${mouseY}px`,
        height: `${height}px`,
        backgroundColor: color,
        boxShadow: `0 0 12px ${color}`,
      }}
    />
  );
}

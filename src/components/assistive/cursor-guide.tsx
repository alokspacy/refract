"use client";

import React, { useEffect, useState } from "react";

export function CursorGuide({ enabled = true }: { enabled?: boolean }) {
  const [pos, setPos] = useState({ x: -100, y: -100 });

  useEffect(() => {
    if (!enabled) return;
    const handleMove = (e: MouseEvent) => {
      setPos({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", handleMove);
    return () => window.removeEventListener("mousemove", handleMove);
  }, [enabled]);

  if (!enabled) return null;

  return (
    <div
      className="pointer-events-none fixed z-50 transition-all duration-75"
      style={{
        left: `${pos.x}px`,
        top: `${pos.y}px`,
        transform: "translate(-50%, -50%)",
      }}
    >
      <div className="w-10 h-10 rounded-full border-2 border-accent shadow-[0_0_15px_rgba(20,184,166,0.6)] animate-pulse" />
      <div className="w-1.5 h-1.5 rounded-full bg-accent absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
    </div>
  );
}

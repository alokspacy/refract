"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface ReaderShellProps {
  title: string;
  children: React.ReactNode;
}

export function ReaderShell({ title, children }: ReaderShellProps) {
  const [fullscreen, setFullscreen] = useState(false);

  return (
    <div className={`min-h-screen transition-colors ${fullscreen ? "bg-black text-yellow-300" : "bg-surface"}`}>
      <header className="sticky top-0 z-30 flex items-center justify-between px-6 py-3 border-b border-white/10 bg-surface/80 backdrop-blur-md">
        <h1 className="text-sm font-bold truncate max-w-md">{title}</h1>
        <div className="flex items-center gap-2 text-xs">
          <button
            onClick={() => setFullscreen(!fullscreen)}
            className="px-3 py-1 bg-white/10 hover:bg-white/20 rounded font-semibold"
          >
            {fullscreen ? "Exit Focus Mode" : "Focus Mode"}
          </button>
        </div>
      </header>

      <main className="max-w-2xl mx-auto py-10 px-4 leading-relaxed">
        {children}
      </main>
    </div>
  );
}

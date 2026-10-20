"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

export function SettingsDrawer() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="fixed top-20 right-4 z-40 bg-accent text-black font-bold p-2 rounded-full shadow-lg text-xs"
        aria-label="Open Accessibility Settings Panel"
      >
        ⚙️
      </button>

      {open && (
        <div className="fixed inset-y-0 right-0 z-50 w-80 bg-surface border-l border-white/20 p-6 shadow-2xl flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-sm font-bold text-accent">Accessibility Preferences</h2>
              <button onClick={() => setOpen(false)} className="text-xs opacity-60">✕</button>
            </div>
            <p className="text-xs text-ink-muted">Fine-tune reading rulers, contrast, font scaling, and voice narration.</p>
          </div>
          <button onClick={() => setOpen(false)} className="w-full py-2 bg-accent text-black font-bold rounded-lg text-xs">
            Save Preferences
          </button>
        </div>
      )}
    </>
  );
}

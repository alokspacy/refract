"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

const SHORTCUTS = [
  { key: "Alt + S", desc: "Toggle Read Aloud Speech" },
  { key: "Alt + B", desc: "Toggle Bionic Reading Mode" },
  { key: "Alt + M", desc: "Toggle Reading Focus Mask" },
  { key: "Alt + +", desc: "Increase Font Size" },
  { key: "Alt + -", desc: "Decrease Font Size" },
  { key: "Space", desc: "Flip Vocabulary Flashcard" },
];

export function KeyboardHelpDialog() {
  const [open, setOpen] = useState(false);

  return (
    <div>
      <button
        onClick={() => setOpen(true)}
        className="px-2.5 py-1 rounded bg-white/5 border border-white/10 hover:bg-white/10 text-xs text-ink-muted"
        aria-label="Open Keyboard Shortcuts Guide"
      >
        ⌨ Shortcuts Guide
      </button>

      {open && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4 backdrop-blur-sm">
          <Glass strong className="p-6 rounded-2xl max-w-sm w-full space-y-4 border border-white/20">
            <div className="flex justify-between items-center">
              <h3 className="text-sm font-bold text-accent">Accessibility Shortcuts</h3>
              <button onClick={() => setOpen(false)} className="text-xs opacity-60 hover:opacity-100">✕</button>
            </div>
            <div className="space-y-2 text-xs">
              {SHORTCUTS.map((s) => (
                <div key={s.key} className="flex justify-between items-center py-1 border-b border-white/5">
                  <span className="text-ink-muted">{s.desc}</span>
                  <kbd className="px-2 py-0.5 bg-white/10 rounded font-mono font-bold text-accent">{s.key}</kbd>
                </div>
              ))}
            </div>
          </Glass>
        </div>
      )}
    </div>
  );
}

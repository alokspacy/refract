'use client';

import React, { useState, useEffect } from 'react';

const SHORTCUTS = [
  { key: '?', desc: 'Toggle keyboard shortcuts guide' },
  { key: 'Space', desc: 'Play / Pause audio reader & flip cards' },
  { key: 'Alt + T', desc: 'Toggle Assistive Typography menu' },
  { key: 'Alt + S', desc: 'Open Sensory Accommodations panel' },
  { key: 'Esc', desc: 'Close dialogs, drawers, and menus' },
  { key: 'Tab / Shift+Tab', desc: 'Navigate interactive page elements' },
];

export function ShortcutGuide() {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === '?' && !['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement)?.tagName)) {
        e.preventDefault();
        setOpen((prev) => !prev);
      } else if (e.key === 'Escape' && open) {
        setOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [open]);

  if (!open) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="shortcuts-dialog-title"
      className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4"
    >
      <div className="bg-card text-card-foreground border border-border rounded-2xl max-w-md w-full p-6 shadow-xl space-y-4">
        <div className="flex justify-between items-center">
          <h2 id="shortcuts-dialog-title" className="text-lg font-bold">
            Keyboard Shortcuts
          </h2>
          <button
            type="button"
            onClick={() => setOpen(false)}
            aria-label="Close shortcuts guide"
            className="text-muted-foreground hover:text-foreground text-sm font-semibold"
          >
            ✕
          </button>
        </div>

        <div className="divide-y divide-border">
          {SHORTCUTS.map((item) => (
            <div key={item.key} className="py-2.5 flex justify-between items-center text-xs">
              <span className="text-muted-foreground">{item.desc}</span>
              <kbd className="px-2 py-1 rounded bg-muted border border-border font-mono font-medium">
                {item.key}
              </kbd>
            </div>
          ))}
        </div>

        <p className="text-[11px] text-muted-foreground text-center">
          Press <kbd className="px-1 rounded bg-muted">Esc</kbd> anytime to dismiss this guide.
        </p>
      </div>
    </div>
  );
}

'use client';

import React, { useState } from 'react';

export interface AltItem {
  block_id: string;
  short_alt: string;
  long_description?: string;
  is_decorative?: boolean;
}

export function AltTextInspector({ items = [] }: { items?: AltItem[] }) {
  const [selectedId, setSelectedId] = useState<string | null>(items[0]?.block_id || null);

  if (items.length === 0) {
    return (
      <div className="p-4 rounded-xl border border-dashed border-border text-xs text-muted-foreground text-center">
        No figures or images found in document.
      </div>
    );
  }

  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3">
      <div className="flex justify-between items-center">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Alt-Text & Figure Inspector
        </h4>
        <span className="text-[10px] px-2 py-0.5 rounded bg-muted font-mono">
          WCAG 1.1.1
        </span>
      </div>

      <div className="space-y-2">
        {items.map((item) => (
          <div
            key={item.block_id}
            onClick={() => setSelectedId(item.block_id)}
            className={`p-2.5 rounded-lg border text-xs cursor-pointer transition ${
              selectedId === item.block_id ? 'border-primary bg-primary/5' : 'border-border hover:bg-muted'
            }`}
          >
            <div className="font-semibold text-foreground">{item.short_alt}</div>
            {selectedId === item.block_id && item.long_description && (
              <p className="mt-1 text-muted-foreground text-[11px]">{item.long_description}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

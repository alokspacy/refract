'use client';

import React from 'react';

export interface OutlineHeading {
  block_id: string;
  level: number;
  title: string;
}

interface OutlineNavigatorProps {
  headings: OutlineHeading[];
  onSelect?: (blockId: string) => void;
}

export function OutlineNavigator({ headings, onSelect }: OutlineNavigatorProps) {
  if (!headings || headings.length === 0) {
    return (
      <div className="p-3 text-xs text-muted-foreground border border-dashed rounded-lg">
        No headings detected in current document.
      </div>
    );
  }

  return (
    <nav aria-label="Table of Contents & Headings" className="p-3 rounded-xl border border-border bg-card space-y-2">
      <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Document Structure (H1-H6)
      </h4>
      <ul className="space-y-1 text-xs max-h-60 overflow-y-auto">
        {headings.map((h) => (
          <li key={h.block_id} style={{ paddingLeft: `${Math.max(0, (h.level - 1) * 12)}px` }}>
            <button
              type="button"
              onClick={() => onSelect?.(h.block_id)}
              className="w-full text-left py-1 px-2 rounded hover:bg-muted text-foreground/90 transition truncate block"
            >
              <span className="text-muted-foreground font-mono text-[10px] mr-1.5">
                H{h.level}
              </span>
              {h.title}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}

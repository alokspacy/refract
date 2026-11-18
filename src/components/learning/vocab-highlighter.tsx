'use client';

import React from 'react';

export interface TierItem {
  word: string;
  tier: number;
  reason: string;
}

export function VocabHighlighter({ items = [] }: { items?: TierItem[] }) {
  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3 text-xs">
      <h4 className="font-semibold uppercase tracking-wider text-muted-foreground">
        Academic Vocabulary Tiers
      </h4>
      <div className="flex flex-wrap gap-1.5">
        {items.map((item) => (
          <span
            key={item.word}
            title={item.reason}
            className={`px-2.5 py-1 rounded-full font-medium ${
              item.tier === 3
                ? 'bg-purple-500/15 text-purple-600 dark:text-purple-300 border border-purple-500/30'
                : 'bg-blue-500/15 text-blue-600 dark:text-blue-300 border border-blue-500/30'
            }`}
          >
            {item.word} (T{item.tier})
          </span>
        ))}
      </div>
    </div>
  );
}

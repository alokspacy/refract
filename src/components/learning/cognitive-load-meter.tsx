'use client';

import React from 'react';

interface CognitiveLoadMeterProps {
  intrinsic?: number;
  extraneous?: number;
  band?: string;
}

export function CognitiveLoadMeter({
  intrinsic = 42,
  extraneous = 28,
  band = 'Low',
}: CognitiveLoadMeterProps) {
  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-semibold uppercase tracking-wider text-muted-foreground">
          Cognitive Load Index
        </span>
        <span className="px-2 py-0.5 rounded bg-primary/10 text-primary font-semibold">
          {band} Load
        </span>
      </div>

      <div className="space-y-2 text-xs">
        <div>
          <div className="flex justify-between mb-1">
            <span>Intrinsic Complexity</span>
            <span className="font-mono">{intrinsic}%</span>
          </div>
          <div className="h-2 rounded-full bg-muted overflow-hidden">
            <div className="h-full bg-primary" style={{ width: `${intrinsic}%` }} />
          </div>
        </div>

        <div>
          <div className="flex justify-between mb-1">
            <span>Extraneous Friction</span>
            <span className="font-mono">{extraneous}%</span>
          </div>
          <div className="h-2 rounded-full bg-muted overflow-hidden">
            <div className="h-full bg-amber-500" style={{ width: `${extraneous}%` }} />
          </div>
        </div>
      </div>
    </div>
  );
}

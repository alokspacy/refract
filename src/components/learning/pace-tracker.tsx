'use client';

import React from 'react';

interface PaceTrackerProps {
  visualMins?: number;
  audioMins?: number;
  brailleMins?: number;
}

export function PaceTracker({
  visualMins = 4.5,
  audioMins = 5.2,
  brailleMins = 8.0,
}: PaceTrackerProps) {
  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-2 text-xs">
      <h4 className="font-semibold uppercase tracking-wider text-muted-foreground">
        Estimated Study Time
      </h4>
      <div className="grid grid-cols-3 gap-2 text-center pt-1">
        <div className="p-2 rounded-lg bg-muted/50">
          <div className="text-muted-foreground text-[11px]">Visual</div>
          <div className="font-mono font-bold text-sm">{visualMins}m</div>
        </div>
        <div className="p-2 rounded-lg bg-muted/50">
          <div className="text-muted-foreground text-[11px]">Audio TTS</div>
          <div className="font-mono font-bold text-sm">{audioMins}m</div>
        </div>
        <div className="p-2 rounded-lg bg-muted/50">
          <div className="text-muted-foreground text-[11px]">Braille</div>
          <div className="font-mono font-bold text-sm">{brailleMins}m</div>
        </div>
      </div>
    </div>
  );
}

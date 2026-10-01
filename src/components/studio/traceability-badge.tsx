"use client";

import React from "react";

interface TraceabilityBadgeProps {
  pageOrSlide?: number;
  bbox?: number[];
  model?: string;
  promptVersion?: string;
}

export function TraceabilityBadge({ pageOrSlide, bbox, model = "gpt-4o", promptVersion = "v1.0" }: TraceabilityBadgeProps) {
  return (
    <div className="inline-flex items-center gap-1.5 text-[0.65rem] bg-white/5 border border-white/10 px-2 py-0.5 rounded-full text-ink-muted">
      {pageOrSlide !== undefined && <span>Page {pageOrSlide}</span>}
      <span>•</span>
      <span>{model}</span>
      <span>•</span>
      <span className="text-accent">{promptVersion}</span>
    </div>
  );
}

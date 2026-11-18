'use client';

import React, { useState } from 'react';

interface PhoneticTooltipProps {
  term: string;
  respelling: string;
  definition?: string;
}

export function PhoneticTooltip({ term, respelling, definition }: PhoneticTooltipProps) {
  const [open, setOpen] = useState(false);

  return (
    <span className="relative inline-block">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        onBlur={() => setOpen(false)}
        className="underline decoration-dotted decoration-primary underline-offset-4 font-medium text-primary hover:bg-primary/10 px-1 rounded transition"
      >
        {term}
      </button>
      {open && (
        <span
          role="tooltip"
          className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1.5 z-30 w-48 p-2.5 rounded-xl bg-popover text-popover-foreground border border-border shadow-lg text-xs block"
        >
          <span className="font-mono font-bold text-primary block">/{respelling}/</span>
          {definition && <span className="text-muted-foreground mt-1 block">{definition}</span>}
        </span>
      )}
    </span>
  );
}

"use client";

import React, { useState } from "react";

interface JargonTooltipProps {
  term: string;
  definition: string;
  children: React.ReactNode;
}

export function JargonTooltip({ term, definition, children }: JargonTooltipProps) {
  const [show, setShow] = useState(false);

  return (
    <span
      className="relative inline-block cursor-help border-b border-dotted border-accent"
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
      onFocus={() => setShow(true)}
      onBlur={() => setShow(false)}
      tabIndex={0}
      role="button"
      aria-label={`${term}: ${definition}`}
    >
      {children}
      {show && (
        <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 p-2 bg-black/90 text-yellow-300 text-[0.68rem] rounded-lg border border-yellow-300/40 shadow-xl z-50 pointer-events-none">
          <strong className="block font-bold">{term}</strong>
          {definition}
        </span>
      )}
    </span>
  );
}

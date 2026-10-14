"use client";

import React from "react";

export function AccessibilityLogo({ className = "w-7 h-7" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      role="img"
      aria-label="AccessLearn AI Accessible Learning Engine Logo"
    >
      <circle cx="16" cy="16" r="14" stroke="currentColor" strokeWidth="2.5" className="text-accent" />
      <circle cx="16" cy="10" r="2.5" fill="currentColor" className="text-accent" />
      <path
        d="M9 15h14M16 15v10M12 25l4-3 4 3"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="text-ink"
      />
    </svg>
  );
}

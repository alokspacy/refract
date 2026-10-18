"use client";

import React from "react";

export function SkipLinks() {
  return (
    <a
      href="#main-content"
      className="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:px-4 focus:py-2 focus:bg-accent focus:text-black focus:font-bold focus:rounded-lg focus:shadow-2xl focus:outline-none"
    >
      Skip to main learning content
    </a>
  );
}

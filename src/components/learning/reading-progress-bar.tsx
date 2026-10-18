"use client";

import React, { useEffect, useState } from "react";

export function ReadingProgressBar() {
  const [percent, setPercent] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const el = document.documentElement;
      const total = el.scrollHeight - el.clientHeight;
      if (total > 0) {
        setPercent(Math.min(100, Math.round((el.scrollTop / total) * 100)));
      }
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="fixed top-0 inset-x-0 h-1 bg-transparent z-50 pointer-events-none">
      <div
        className="h-full bg-accent transition-all duration-150 shadow-[0_0_8px_rgba(20,184,166,0.8)]"
        style={{ width: `${percent}%` }}
      />
    </div>
  );
}

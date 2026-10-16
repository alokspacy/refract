"use client";

import React from "react";

interface KaraokeProps {
  text: string;
  activeSentenceIndex: number;
}

export function KaraokeHighlighter({ text, activeSentenceIndex }: KaraokeProps) {
  const sentences = text.split(/(?<=[.!?])\s+/);

  return (
    <p className="leading-relaxed text-sm md:text-base">
      {sentences.map((sentence, idx) => (
        <span
          key={idx}
          className={`transition-all duration-200 rounded px-1 ${
            idx === activeSentenceIndex
              ? "bg-accent/30 text-accent font-semibold shadow-[0_0_8px_rgba(20,184,166,0.4)]"
              : "text-ink/80"
          }`}
        >
          {sentence}{" "}
        </span>
      ))}
    </p>
  );
}

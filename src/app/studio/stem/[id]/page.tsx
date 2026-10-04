"use client";

import React from "react";
import { Glass, Kicker } from "@/components/ui/glass";
import { MathBlock } from "@/components/learning/math-block";
import { TactileExplorer } from "@/components/learning/tactile-explorer";
import { BraillePreview } from "@/components/assistive/braille-preview";

export default function StemAccessibilityStudio({ params }: { params: { id: string } }) {
  return (
    <div className="max-w-4xl mx-auto py-10 px-4 space-y-6">
      <div>
        <Kicker>Multi-Modal STEM Adaptation</Kicker>
        <h1 className="text-3xl font-bold mt-1">STEM & Braille Accessibility Hub</h1>
        <p className="text-sm text-ink-muted">
          Real-time ClearSpeak mathematical speech, tactile diagrams, and Unified English Braille (UEB).
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <MathBlock
          latex="E = m c^2"
          clearspeak="E equals m times c squared"
        />
        <BraillePreview
          sourceText="Energy equals mass times the speed of light squared."
          brailleText="⠑⠝⠑⠗⠛⠽ ⠑⠟⠥⠁⠇⠎ ⠍⠁⠎⠎ ⠮ ⠎⠏⠑⠑⠙ ⠷ ⠇⠊⠛⠓⠞"
          grade="Grade 2"
        />
      </div>

      <TactileExplorer />
    </div>
  );
}

"use client";

import React from "react";
import { Glass, Kicker } from "@/components/ui/glass";
import { ComprehensionCheck } from "@/components/learning/comprehension-check";

export default function StudySessionPage({ params }: { params: { id: string } }) {
  return (
    <div className="max-w-3xl mx-auto py-10 px-4 space-y-6">
      <div>
        <Kicker>Learner Assistive Mode</Kicker>
        <h1 className="text-3xl font-bold mt-1">Comprehension Self-Check</h1>
        <p className="text-sm text-ink-muted">
          Paced interactive check-ins generated automatically from transformed lesson concepts.
        </p>
      </div>

      <ComprehensionCheck
        prompt="Why is chlorophyll essential for plant photosynthesis?"
        options={[
          {
            id: "1",
            text: "It absorbs sunlight energy to convert water and carbon dioxide into sugars.",
            isCorrect: true,
            explanation: "Spot on! Chlorophyll traps solar photons to drive chemical synthesis."
          },
          {
            id: "2",
            text: "It prevents water from evaporating through the roots.",
            isCorrect: false,
            explanation: "Incorrect; root cuticle and stomata regulate transpiration."
          }
        ]}
      />
    </div>
  );
}

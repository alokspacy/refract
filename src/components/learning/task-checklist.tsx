"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface Step {
  step_number: number;
  title: string;
  description: string;
  estimated_minutes: number;
}

export function TaskChecklist({ steps }: { steps: Step[] }) {
  const [completed, setCompleted] = useState<Record<number, boolean>>({});

  const toggle = (num: number) => {
    setCompleted((prev) => ({ ...prev, [num]: !prev[num] }));
  };

  return (
    <Glass strong className="p-5 rounded-2xl border border-white/10 space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-bold text-accent uppercase tracking-wider">Step-by-Step Task Breakdown</span>
        <span className="text-ink-muted">Executive Function Guide</span>
      </div>

      <div className="space-y-2">
        {steps.map((s) => (
          <div
            key={s.step_number}
            onClick={() => toggle(s.step_number)}
            className={`p-3 rounded-xl border cursor-pointer transition-all ${
              completed[s.step_number]
                ? "bg-emerald-500/10 border-emerald-500/30 opacity-70"
                : "bg-white/5 border-white/10 hover:border-white/20"
            }`}
          >
            <div className="flex items-center justify-between text-xs font-semibold">
              <span className={completed[s.step_number] ? "line-through text-emerald-300" : "text-ink"}>
                {s.step_number}. {s.title}
              </span>
              <span className="text-[0.65rem] px-2 py-0.5 rounded bg-white/10 text-ink-muted">
                ⏱ {s.estimated_minutes} min
              </span>
            </div>
            <p className="text-[0.7rem] text-ink-muted mt-1">{s.description}</p>
          </div>
        ))}
      </div>
    </Glass>
  );
}

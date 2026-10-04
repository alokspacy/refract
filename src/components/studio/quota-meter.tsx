"use client";

import React from "react";
import { Glass } from "@/components/ui/glass";

interface QuotaMeterProps {
  institutionName: string;
  tier: string;
  pagesUsed: number;
  pageLimit: number;
}

export function QuotaMeter({ institutionName, tier, pagesUsed, pageLimit }: QuotaMeterProps) {
  const percent = Math.min(100, Math.round((pagesUsed / Math.max(pageLimit, 1)) * 100));

  return (
    <Glass className="p-4 border border-white/10 rounded-xl flex items-center justify-between gap-4">
      <div>
        <div className="flex items-center gap-2">
          <span className="font-bold text-xs">{institutionName}</span>
          <span className="text-[0.65rem] uppercase font-bold px-1.5 py-0.5 bg-accent/20 text-accent rounded">
            {tier}
          </span>
        </div>
        <p className="text-[0.7rem] text-ink-muted mt-0.5">
          {pagesUsed.toLocaleString()} of {pageLimit.toLocaleString()} monthly pages used
        </p>
      </div>

      <div className="flex items-center gap-3">
        <div className="w-32 h-2 bg-white/10 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all duration-300 ${percent > 90 ? "bg-rose-500" : "bg-accent"}`}
            style={{ width: `${percent}%` }}
          />
        </div>
        <span className="text-xs font-mono font-bold">{percent}%</span>
      </div>
    </Glass>
  );
}

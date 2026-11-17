'use client';

import React from 'react';

export interface CriterionItem {
  criterion_id: string;
  title: string;
  score: number;
  feedback: string;
}

interface RubricScorecardProps {
  overallScore?: number;
  masteryLevel?: string;
  criteria?: CriterionItem[];
}

export function RubricScorecard({
  overallScore = 3.8,
  masteryLevel = 'Exemplary',
  criteria = [],
}: RubricScorecardProps) {
  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3">
      <div className="flex justify-between items-center">
        <div>
          <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            UDL Scaffolding Rubric
          </h4>
          <p className="text-sm font-bold text-foreground">{masteryLevel}</p>
        </div>
        <div className="text-lg font-mono font-bold px-3 py-1 rounded-lg bg-primary/10 text-primary">
          {overallScore.toFixed(1)} / 4.0
        </div>
      </div>

      <div className="space-y-2">
        {criteria.map((c) => (
          <div key={c.criterion_id} className="p-2 rounded-lg bg-muted/50 text-xs space-y-1">
            <div className="flex justify-between font-medium">
              <span>{c.title}</span>
              <span className="font-mono">{c.score}/4</span>
            </div>
            <p className="text-[11px] text-muted-foreground">{c.feedback}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

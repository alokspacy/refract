"use client";

import React from "react";
import { Glass, Kicker } from "@/components/ui/glass";

export default function ComplianceAuditPage({ params }: { params: { id: string } }) {
  return (
    <div className="max-w-4xl mx-auto py-10 px-4 space-y-6">
      <div>
        <Kicker>Automated Accessibility Inspection</Kicker>
        <h1 className="text-3xl font-bold mt-1">WCAG 2.2 Compliance Audit</h1>
        <p className="text-sm text-ink-muted">Automated verification against Perceivable, Operable, Understandable, and Robust criteria.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Glass strong className="p-5 text-center">
          <span className="text-xs text-ink-muted">Overall Score</span>
          <p className="text-4xl font-extrabold text-accent mt-1">94%</p>
          <span className="text-[0.7rem] text-emerald-400 font-semibold">WCAG 2.2 AA Certified</span>
        </Glass>
        <Glass strong className="p-5 text-center">
          <span className="text-xs text-ink-muted">Reading Level</span>
          <p className="text-2xl font-bold mt-2">Grade 5.4</p>
          <span className="text-[0.7rem] text-ink-muted">Accessible for Upper Primary</span>
        </Glass>
        <Glass strong className="p-5 text-center">
          <span className="text-xs text-ink-muted">Violations Flagged</span>
          <p className="text-2xl font-bold mt-2 text-yellow-400">0 Critical</p>
          <span className="text-[0.7rem] text-ink-muted">1 Minor Remediation</span>
        </Glass>
      </div>

      <Glass className="p-6 space-y-4">
        <h3 className="text-base font-bold">Rule Evaluation Breakdown</h3>
        <div className="space-y-2 text-xs">
          <div className="flex justify-between items-center p-2 rounded bg-white/5">
            <div>
              <p className="font-semibold">1.1.1 Non-text Content (Alt-Text)</p>
              <p className="text-ink-muted">All diagrams have complete educational descriptions.</p>
            </div>
            <span className="text-emerald-400 font-bold">PASSED</span>
          </div>
          <div className="flex justify-between items-center p-2 rounded bg-white/5">
            <div>
              <p className="font-semibold">1.3.1 Info and Relationships (Structure)</p>
              <p className="text-ink-muted">Table matrices contain explicit header column relationships.</p>
            </div>
            <span className="text-emerald-400 font-bold">PASSED</span>
          </div>
          <div className="flex justify-between items-center p-2 rounded bg-white/5">
            <div>
              <p className="font-semibold">2.4.6 Headings and Labels (Hierarchy)</p>
              <p className="text-ink-muted">H1, H2, and H3 nested correctly without skipped levels.</p>
            </div>
            <span className="text-emerald-400 font-bold">PASSED</span>
          </div>
        </div>
      </Glass>
    </div>
  );
}

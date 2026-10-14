"use client";

import React from "react";

export type ExportStatus = "queued" | "compiling" | "ready" | "failed";

export function ExportStatusBadge({ status }: { status: ExportStatus }) {
  const configs = {
    queued: { label: "Queued", color: "bg-white/10 text-ink-muted" },
    compiling: { label: "Compiling Package...", color: "bg-accent/20 text-accent animate-pulse" },
    ready: { label: "✓ Ready for Download", color: "bg-emerald-500/20 text-emerald-300" },
    failed: { label: "Failed", color: "bg-rose-500/20 text-rose-300" },
  };

  const current = configs[status] || configs.queued;

  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-[0.68rem] font-bold ${current.color}`}>
      {current.label}
    </span>
  );
}

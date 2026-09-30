import React from "react";
import { CheckCircle2, Clock, AlertCircle, Loader2 } from "lucide-react";

interface StatusBadgeProps {
  status: "UPLOADED" | "QUEUED" | "PROCESSING" | "COMPLETED" | "FAILED" | string;
  stage?: string;
  progress?: number;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, stage, progress }) => {
  const normStatus = status.toUpperCase();

  switch (normStatus) {
    case "COMPLETED":
      return (
        <span
          className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800"
          role="status"
          aria-label="Status: Completed"
        >
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" aria-hidden="true" />
          <span>Ready</span>
        </span>
      );
    case "PROCESSING":
      return (
        <span
          className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 dark:bg-blue-950/60 dark:text-blue-300 border border-blue-200 dark:border-blue-800"
          role="status"
          aria-label={`Status: Processing ${stage ? `stage ${stage}` : ""}`}
        >
          <Loader2 className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400 animate-spin" aria-hidden="true" />
          <span>
            {stage ? `Processing (${stage})` : "Processing"}
            {typeof progress === "number" && progress > 0 ? ` ${Math.round(progress)}%` : ""}
          </span>
        </span>
      );
    case "QUEUED":
    case "UPLOADED":
      return (
        <span
          className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-900 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-200 dark:border-amber-800"
          role="status"
          aria-label="Status: Queued for processing"
        >
          <Clock className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" aria-hidden="true" />
          <span>Queued</span>
        </span>
      );
    case "FAILED":
      return (
        <span
          className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300 border border-rose-200 dark:border-rose-800"
          role="status"
          aria-label="Status: Processing failed"
        >
          <AlertCircle className="w-3.5 h-3.5 text-rose-600 dark:text-rose-400" aria-hidden="true" />
          <span>Failed</span>
        </span>
      );
    default:
      return (
        <span
          className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700"
          role="status"
          aria-label={`Status: ${status}`}
        >
          <span>{status}</span>
        </span>
      );
  }
};

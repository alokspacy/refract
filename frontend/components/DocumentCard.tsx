"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Document } from "@/types/document";
import { ProcessingJob } from "@/types/job";
import { StatusBadge } from "./StatusBadge";
import { api } from "@/lib/api";
import { FileText, Music, Video, Image, File, Calendar, HardDrive, RefreshCw, Eye, AlertTriangle } from "lucide-react";

interface DocumentCardProps {
  document: Document;
  onRefresh?: () => void;
}

export const DocumentCard: React.FC<DocumentCardProps> = ({ document, onRefresh }) => {
  const [job, setJob] = useState<ProcessingJob | null>(null);
  const [loadingJob, setLoadingJob] = useState(false);

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    const fetchJob = async () => {
      if (!document.latest_job_id) return;
      try {
        const jobData = await api.jobs.get(document.latest_job_id);
        setJob(jobData);

        // If job completed or failed, clear interval and trigger refresh
        if (jobData.status === "COMPLETED" || jobData.status === "FAILED") {
          if (interval) clearInterval(interval);
          if (onRefresh) onRefresh();
        }
      } catch {
        // Silently fail if job polling has issues
      }
    };

    if (document.latest_job_id && (document.status === "PROCESSING" || document.status === "UPLOADED" || document.extraction_status === "PROCESSING")) {
      fetchJob();
      interval = setInterval(fetchJob, 2000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [document.latest_job_id, document.status, document.extraction_status, onRefresh]);

  const handleManualPoll = async () => {
    if (!document.latest_job_id) return;
    setLoadingJob(true);
    try {
      const jobData = await api.jobs.get(document.latest_job_id);
      setJob(jobData);
      if (onRefresh) onRefresh();
    } catch {
      // Ignored
    } finally {
      setLoadingJob(false);
    }
  };

  const getFileIcon = (fileName: string) => {
    const ext = fileName.split(".").pop()?.toLowerCase();
    if (["mp3", "wav"].includes(ext || "")) return <Music className="w-5 h-5 text-amber-500" aria-hidden="true" />;
    if (["mp4"].includes(ext || "")) return <Video className="w-5 h-5 text-purple-500" aria-hidden="true" />;
    if (["png", "jpg", "jpeg"].includes(ext || "")) return <Image className="w-5 h-5 text-emerald-500" aria-hidden="true" />;
    if (["pdf", "docx", "pptx", "txt"].includes(ext || "")) return <FileText className="w-5 h-5 text-indigo-500" aria-hidden="true" />;
    return <File className="w-5 h-5 text-slate-500" aria-hidden="true" />;
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  const formatDate = (isoString: string): string => {
    try {
      const date = new Date(isoString);
      return date.toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return isoString;
    }
  };

  const currentStatus = job?.status || (document.extraction_status === "COMPLETED" ? "COMPLETED" : document.status);
  const currentStage = job?.current_stage || (document.extraction_status === "COMPLETED" ? "COMPLETED" : undefined);
  const currentProgress = job?.progress || (document.extraction_status === "COMPLETED" ? 100 : undefined);
  const isReady = document.extraction_status === "COMPLETED" || document.status === "READY" || document.status === "COMPLETED";

  return (
    <article className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-5 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3 min-w-0">
          <div className="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-700/60 flex items-center justify-center shrink-0 mt-0.5">
            {getFileIcon(document.original_filename)}
          </div>
          <div className="min-w-0">
            <h4 className="text-base font-bold text-slate-900 dark:text-white truncate" title={document.original_filename}>
              {document.original_filename}
            </h4>
            <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-1 text-xs text-slate-700 dark:text-slate-200">
              <span className="flex items-center gap-1">
                <HardDrive className="w-3.5 h-3.5" aria-hidden="true" />
                {formatFileSize(document.file_size)}
              </span>
              <span className="flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5" aria-hidden="true" />
                {formatDate(document.created_at)}
              </span>
            </div>
          </div>
        </div>

        {/* Status Badge */}
        <div className="shrink-0 flex items-center gap-2">
          <StatusBadge status={currentStatus} stage={currentStage} progress={currentProgress} />
          {document.latest_job_id && (
            <button
              onClick={handleManualPoll}
              disabled={loadingJob}
              className="p-1.5 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 focus-visible:ring-2 focus-visible:ring-indigo-500"
              title="Refresh job status"
              aria-label="Refresh job status"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loadingJob ? "animate-spin text-indigo-600" : ""}`} aria-hidden="true" />
            </button>
          )}
        </div>
      </div>

      {/* Processing Progress Bar (if processing) */}
      {currentStatus === "PROCESSING" && (
        <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-700/50">
          <div className="flex items-center justify-between text-xs text-slate-700 dark:text-slate-200 mb-1.5">
            <span>Stage: <strong className="font-semibold text-indigo-600 dark:text-indigo-400">{currentStage || "EXTRACTING"}</strong></span>
            <span>{Math.round(currentProgress || 0)}%</span>
          </div>
          <div className="w-full bg-slate-100 dark:bg-slate-700 rounded-full h-2 overflow-hidden">
            <div
              className="bg-indigo-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${currentProgress || 10}%` }}
              role="progressbar"
              aria-valuenow={currentProgress || 10}
              aria-valuemin={0}
              aria-valuemax={100}
            />
          </div>
        </div>
      )}

      {/* Extraction Warnings Pill */}
      {document.extraction_warnings && document.extraction_warnings.length > 0 && (
        <div className="mt-3 flex items-center gap-1.5 text-xs text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-950/40 px-2.5 py-1.5 rounded-lg">
          <AlertTriangle className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
          <span>{document.extraction_warnings.length} non-fatal extraction warning(s)</span>
        </div>
      )}

      {/* Error Message display */}
      {job?.error_message && (
        <div className="mt-3 p-2.5 rounded-lg bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-300 text-xs">
          <strong>Error:</strong> {job.error_message}
        </div>
      )}

      {/* Actions Footer */}
      {isReady && (
        <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-700/50 flex flex-wrap items-center justify-between gap-2">
          <Link
            href={`/documents/${document.id}`}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-800 dark:text-slate-200 text-xs font-semibold focus-visible:ring-2 focus-visible:ring-indigo-500 transition-colors"
          >
            <Eye className="w-3.5 h-3.5" aria-hidden="true" />
            Source Preview
          </Link>
          <Link
            href={`/documents/${document.id}/generate`}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-sm focus-visible:ring-2 focus-visible:ring-indigo-500 transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" aria-hidden="true" />
            Generate Accessible Version
          </Link>
        </div>
      )}
    </article>
  );
};

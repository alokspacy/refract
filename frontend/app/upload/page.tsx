"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { isAuthenticated } from "@/lib/auth";
import { Document } from "@/types/document";
import { FileUpload } from "@/components/FileUpload";
import { DocumentCard } from "@/components/DocumentCard";
import { ArrowLeft, Sparkles, CheckCircle2, ShieldCheck } from "lucide-react";

export default function UploadPage() {
  const router = useRouter();
  const [recentUpload, setRecentUpload] = useState<Document | null>(null);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace("/login");
    }
  }, [router]);

  const handleUploadSuccess = (doc: Document) => {
    setRecentUpload(doc);
  };

  return (
    <div className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header & Back Link */}
      <div>
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-700 hover:text-indigo-600 dark:text-slate-200 dark:hover:text-indigo-400 mb-3 focus-visible:ring-2 focus-visible:ring-indigo-500 rounded p-1"
        >
          <ArrowLeft className="w-4 h-4" aria-hidden="true" />
          <span>Back to Library Dashboard</span>
        </Link>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          New Accessible Material Ingestion
        </h1>
        <p className="text-sm text-slate-700 dark:text-slate-200 mt-1">
          Upload educational documents to initiate secure validation, persistent storage, and background processing.
        </p>
      </div>

      {/* Upload Component */}
      <div className="bg-white dark:bg-slate-800 rounded-3xl border border-slate-200 dark:border-slate-700 p-6 sm:p-8 shadow-sm">
        <FileUpload onUploadSuccess={handleUploadSuccess} />
      </div>

      {/* Recent Upload Status */}
      {recentUpload && (
        <section aria-labelledby="active-upload-heading" className="space-y-3">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400" aria-hidden="true" />
            <h2 id="active-upload-heading" className="text-base font-bold text-slate-900 dark:text-white">
              Active Ingestion Job
            </h2>
          </div>
          <DocumentCard document={recentUpload} />
          <div className="flex justify-end">
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-xl text-xs font-bold shadow-sm transition-all focus-visible:ring-2 focus-visible:ring-indigo-600"
            >
              <span>View All in Dashboard</span>
            </Link>
          </div>
        </section>
      )}

      {/* Phase 2 Technical Context Callout */}
      <aside aria-label="Pipeline Architecture Information" className="p-5 rounded-2xl bg-indigo-50/50 dark:bg-indigo-950/30 border border-indigo-200/80 dark:border-indigo-900/60 text-xs text-slate-700 dark:text-slate-200 space-y-2">
        <div className="flex items-center gap-2 font-bold text-indigo-950 dark:text-indigo-200">
          <ShieldCheck className="w-4 h-4 text-indigo-600 dark:text-indigo-400" aria-hidden="true" />
          <span>Phase 2 Extraction & Normalization Pipeline Active</span>
        </div>
        <p className="leading-relaxed">
          Files uploaded here undergo automated format detection (PDF via PyMuPDF, Word via python-docx, PowerPoint via python-pptx, Images via Pillow/OCR, and Plain Text). The asynchronous Celery worker executes: <code className="font-mono bg-indigo-100 dark:bg-indigo-900/60 px-1 py-0.5 rounded">EXTRACTING (25%)</code> → <code className="font-mono bg-indigo-100 dark:bg-indigo-900/60 px-1 py-0.5 rounded">OCR (50% if needed)</code> → <code className="font-mono bg-indigo-100 dark:bg-indigo-900/60 px-1 py-0.5 rounded">NORMALIZING (75%)</code> → <code className="font-mono bg-indigo-100 dark:bg-indigo-900/60 px-1 py-0.5 rounded">COMPLETED (100%)</code> into strict traceable Content JSON.
        </p>
      </aside>
    </div>
  );
}

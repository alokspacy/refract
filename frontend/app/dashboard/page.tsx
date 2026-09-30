"use client";

import React, { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api, ApiError } from "@/lib/api";
import { getCurrentUser, isAuthenticated } from "@/lib/auth";
import { User } from "@/types/auth";
import { Document } from "@/types/document";
import { DocumentCard } from "@/components/DocumentCard";
import { LoadingState } from "@/components/LoadingState";
import {
  FileText,
  PlusCircle,
  Clock,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  Sparkles,
  Inbox,
} from "lucide-react";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchDocuments = useCallback(async (isRefresh = false) => {
    if (isRefresh) setRefreshing(true);
    setError(null);
    try {
      const data = await api.documents.list();
      setDocuments(data.items);
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.status === 401) {
          router.replace("/login");
          return;
        }
        setError(err.message);
      } else {
        setError("Failed to load documents. Please check backend connection.");
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [router]);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace("/login");
      return;
    }

    const currentUser = getCurrentUser();
    setUser(currentUser);
    fetchDocuments();
  }, [router, fetchDocuments]);

  const totalDocs = documents.length;
  const processingDocs = documents.filter((d) => d.status === "PROCESSING" || d.status === "UPLOADED" || (d.status as string) === "QUEUED").length;
  const completedDocs = documents.filter((d) => d.status === "COMPLETED").length;

  return (
    <div className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Welcome Banner */}
      <section
        aria-labelledby="welcome-heading"
        className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-indigo-900 via-indigo-800 to-slate-900 text-white p-6 sm:p-8 shadow-lg border border-indigo-700/50"
      >
        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/30 border border-indigo-400/30 text-indigo-200 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5" aria-hidden="true" />
              <span>AccessLearn AI — Educator Portal</span>
            </div>
            <h1 id="welcome-heading" className="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Welcome back, {user?.name || "Educator"}
            </h1>
            <p className="text-sm text-indigo-100/90 leading-relaxed">
              Upload educational course materials to begin secure foundation ingestion. In later phases, your documents will automatically convert to multi-modal accessible formats.
            </p>
          </div>

          <div className="shrink-0 flex items-center gap-3">
            <Link
              href="/upload"
              className="inline-flex items-center gap-2 bg-white text-indigo-900 hover:bg-indigo-50 px-5 py-2.5 rounded-xl font-bold text-sm shadow-md transition-all focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-white"
            >
              <PlusCircle className="w-4 h-4" aria-hidden="true" />
              <span>New Conversion</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Metric Cards */}
      <section aria-label="Course Material Metrics" className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Total */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-bold text-slate-700 dark:text-slate-200 uppercase tracking-wider">
                Total Documents
              </p>
              <p className="text-3xl font-black text-slate-900 dark:text-white mt-1">
                {totalDocs}
              </p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center">
              <FileText className="w-6 h-6" aria-hidden="true" />
            </div>
          </div>
        </div>

        {/* Processing */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-bold text-slate-700 dark:text-slate-200 uppercase tracking-wider">
                In Pipeline
              </p>
              <p className="text-3xl font-black text-blue-600 dark:text-blue-400 mt-1">
                {processingDocs}
              </p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 flex items-center justify-center">
              <Clock className="w-6 h-6" aria-hidden="true" />
            </div>
          </div>
        </div>

        {/* Ready */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-bold text-slate-700 dark:text-slate-200 uppercase tracking-wider">
                Ready / Foundation Completed
              </p>
              <p className="text-3xl font-black text-emerald-600 dark:text-emerald-400 mt-1">
                {completedDocs}
              </p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
              <CheckCircle2 className="w-6 h-6" aria-hidden="true" />
            </div>
          </div>
        </div>
      </section>

      {/* Documents Section */}
      <section aria-labelledby="documents-heading" className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 id="documents-heading" className="text-xl font-bold text-slate-900 dark:text-white">
              Course Material Library
            </h2>
            <p className="text-xs text-slate-700 dark:text-slate-200">
              Your uploaded syllabus, slides, worksheets, and lecture media
            </p>
          </div>

          <button
            onClick={() => fetchDocuments(true)}
            disabled={refreshing || loading}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors focus-visible:ring-2 focus-visible:ring-indigo-500"
            aria-label="Refresh documents list"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? "animate-spin text-indigo-600" : ""}`} aria-hidden="true" />
            <span>Refresh</span>
          </button>
        </div>

        {/* Error Alert */}
        {error && (
          <div
            role="alert"
            className="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-200 flex items-start gap-3 text-sm"
          >
            <AlertCircle className="w-5 h-5 text-rose-600 dark:text-rose-400 shrink-0 mt-0.5" aria-hidden="true" />
            <div>
              <p className="font-semibold">Library Error</p>
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* Content */}
        {loading ? (
          <LoadingState message="Loading your educational documents..." />
        ) : documents.length === 0 ? (
          <div className="rounded-2xl border-2 border-dashed border-slate-300 dark:border-slate-700 p-12 text-center bg-white/50 dark:bg-slate-800/30">
            <div className="w-14 h-14 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-400 flex items-center justify-center mx-auto mb-4">
              <Inbox className="w-7 h-7" aria-hidden="true" />
            </div>
            <h3 className="text-base font-bold text-slate-800 dark:text-slate-200">
              No educational documents uploaded yet
            </h3>
            <p className="text-xs text-slate-700 dark:text-slate-200 mt-1 max-w-sm mx-auto">
              Upload your first syllabus, textbook PDF, slides, or lecture recording to initialize the foundation pipeline.
            </p>
            <div className="mt-5">
              <Link
                href="/upload"
                className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-xl font-semibold text-sm shadow-sm transition-all focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-indigo-600"
              >
                <PlusCircle className="w-4 h-4" aria-hidden="true" />
                <span>Upload First Document</span>
              </Link>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {documents.map((doc) => (
              <DocumentCard
                key={doc.id}
                document={doc}
                onRefresh={() => fetchDocuments(false)}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

"use client";

import React, { useEffect, useState, use } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api, ApiError } from "@/lib/api";
import { getAccessToken } from "@/lib/auth";
import { DocumentPreview, Section, ContentBlock } from "@/types/document";
import { LoadingState } from "@/components/LoadingState";
import {
  ArrowLeft,
  FileText,
  AlertTriangle,
  Layers,
  Code,
  Info,
  Calendar,
  CheckCircle2,
  Table as TableIcon,
  Image as ImageIcon,
  Copy,
  Check
} from "lucide-react";

export default function DocumentPreviewPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const documentId = resolvedParams.id;
  const router = useRouter();

  const [preview, setPreview] = useState<DocumentPreview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showTraceability, setShowTraceability] = useState(false);
  const [showRawJson, setShowRawJson] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const token = getAccessToken();
    if (!token) {
      router.push("/login");
      return;
    }

    const fetchPreview = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await api.documents.getPreview(documentId);
        setPreview(data);
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message);
        } else {
          setError("Failed to load document source preview.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchPreview();
  }, [documentId, router]);

  const handleCopyJson = () => {
    if (!preview) return;
    navigator.clipboard.writeText(JSON.stringify(preview, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const renderBlock = (block: ContentBlock) => {
    const { type, source_text, metadata } = block;

    return (
      <div
        key={block.id}
        className={`group relative p-4 rounded-xl transition-colors ${
          showTraceability
            ? "border border-indigo-200 dark:border-indigo-900/60 bg-indigo-50/30 dark:bg-indigo-950/20 my-2"
            : "hover:bg-slate-50/80 dark:hover:bg-slate-800/40 my-1"
        }`}
      >
        {/* Traceability Badge */}
        {showTraceability && (
          <div className="flex flex-wrap items-center gap-2 mb-2 text-[11px] font-mono text-indigo-700 dark:text-indigo-300">
            <span className="px-2 py-0.5 rounded bg-indigo-100 dark:bg-indigo-900/60 font-semibold">
              ID: {block.id.slice(0, 8)}...
            </span>
            <span className="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
              Type: {type}
            </span>
            {block.page_or_slide && (
              <span className="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                Page/Slide: {block.page_or_slide}
              </span>
            )}
            {metadata?.bbox && (
              <span className="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                BBox: [{metadata.bbox.join(", ")}]
              </span>
            )}
            {metadata?.ocr_confidence && (
              <span className="px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300">
                OCR: {Math.round(metadata.ocr_confidence * 100)}%
              </span>
            )}
          </div>
        )}

        {/* Block Content Rendering */}
        {type === "heading" && (
          <div className="text-slate-900 dark:text-white font-bold">
            {metadata?.heading_level === 1 ? (
              <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-indigo-950 dark:text-indigo-200">
                {source_text}
              </h2>
            ) : metadata?.heading_level === 2 ? (
              <h3 className="text-lg sm:text-xl font-bold text-slate-800 dark:text-slate-100">
                {source_text}
              </h3>
            ) : (
              <h4 className="text-base sm:text-lg font-semibold text-slate-800 dark:text-slate-200">
                {source_text}
              </h4>
            )}
          </div>
        )}

        {type === "paragraph" && (
          <p className="text-sm sm:text-base text-slate-700 dark:text-slate-300 leading-relaxed">
            {source_text}
          </p>
        )}

        {type === "list" && (
          <div className="flex items-start gap-2 text-sm sm:text-base text-slate-700 dark:text-slate-300">
            <span className="text-indigo-600 dark:text-indigo-400 font-bold shrink-0">•</span>
            <span className="leading-relaxed">{source_text}</span>
          </div>
        )}

        {type === "table" && (
          <div className="my-3 overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-700">
            <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-700 text-sm">
              {metadata?.headers && metadata.headers.length > 0 && (
                <thead className="bg-slate-50 dark:bg-slate-800/80">
                  <tr>
                    {metadata.headers.map((h: string, idx: number) => (
                      <th
                        key={idx}
                        scope="col"
                        className="px-4 py-3 text-left text-xs font-semibold text-slate-700 dark:text-slate-200 uppercase tracking-wider"
                      >
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
              )}
              <tbody className="divide-y divide-slate-200 dark:divide-slate-700 bg-white dark:bg-slate-900">
                {metadata?.rows?.map((row: string[], rIdx: number) => (
                  <tr key={rIdx} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40">
                    {row.map((cell: string, cIdx: number) => (
                      <td key={cIdx} className="px-4 py-2.5 text-slate-700 dark:text-slate-300">
                        {cell}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {type === "image" && (
          <div className="my-3 p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-dashed border-slate-300 dark:border-slate-600 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-indigo-100 dark:bg-indigo-950/80 flex items-center justify-center text-indigo-600 dark:text-indigo-400 shrink-0">
              <ImageIcon className="w-5 h-5" aria-hidden="true" />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-800 dark:text-slate-200">
                {block.source_asset_id ? `Extracted Asset (${metadata?.asset_filename || "Image"})` : source_text}
              </p>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Dimensions: {metadata?.width ? `${metadata.width}x${metadata.height}px` : "Preserved"} • Format: {metadata?.format || "PNG"}
              </p>
            </div>
          </div>
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-50 dark:bg-slate-900 py-10">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <LoadingState message="Loading normalized source preview..." />
        </div>
      </main>
    );
  }

  if (error || !preview) {
    return (
      <main className="min-h-screen bg-slate-50 dark:bg-slate-900 py-10">
        <div className="max-w-4xl mx-auto px-4 sm:px-6">
          <div className="bg-white dark:bg-slate-800 rounded-2xl border border-rose-200 dark:border-rose-900/60 p-8 text-center shadow-sm">
            <AlertTriangle className="w-12 h-12 text-rose-600 mx-auto mb-4" aria-hidden="true" />
            <h1 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
              Preview Unavailable
            </h1>
            <p className="text-slate-600 dark:text-slate-400 mb-6 text-sm">
              {error || "Could not retrieve document preview."}
            </p>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold transition-colors focus-visible:ring-2 focus-visible:ring-indigo-500"
            >
              <ArrowLeft className="w-4 h-4" aria-hidden="true" />
              Return to Dashboard
            </Link>
          </div>
        </div>
      </main>
    );
  }

  const totalBlocks = preview.sections.reduce((acc, sec) => acc + (sec.blocks?.length || 0), 0);

  return (
    <main className="min-h-screen bg-slate-50 dark:bg-slate-900 py-8">
      <div className="max-w-5xl mx-auto px-4 sm:px-6">
        
        {/* Navigation & Actions */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 text-sm font-semibold text-slate-600 dark:text-slate-300 hover:text-indigo-600 dark:hover:text-indigo-400 focus-visible:ring-2 focus-visible:ring-indigo-500 rounded-lg p-1 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" aria-hidden="true" />
            Back to Library
          </Link>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowTraceability(!showTraceability)}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-colors focus-visible:ring-2 focus-visible:ring-indigo-500 ${
                showTraceability
                  ? "bg-indigo-600 text-white border-indigo-600"
                  : "bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-700"
              }`}
            >
              <Layers className="w-3.5 h-3.5" aria-hidden="true" />
              {showTraceability ? "Hide Traceability" : "Show Traceability"}
            </button>

            <button
              onClick={() => setShowRawJson(!showRawJson)}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-colors focus-visible:ring-2 focus-visible:ring-indigo-500 ${
                showRawJson
                  ? "bg-slate-900 text-white border-slate-900 dark:bg-white dark:text-slate-900"
                  : "bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-700"
              }`}
            >
              <Code className="w-3.5 h-3.5" aria-hidden="true" />
              {showRawJson ? "View Rendered" : "View Raw JSON"}
            </button>
          </div>
        </div>

        {/* Document Header Card */}
        <header className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6 shadow-sm mb-6">
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="px-2.5 py-0.5 rounded-md bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 text-xs font-bold uppercase tracking-wider">
                  {preview.mime_type.split("/")[1]?.toUpperCase() || "DOCUMENT"}
                </span>
                <span className="px-2.5 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 text-xs font-semibold flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3" aria-hidden="true" />
                  Normalized v{preview.schema_version}
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">
                {preview.title}
              </h1>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                File: {preview.original_filename}
              </p>
            </div>

            <div className="text-right shrink-0 text-xs text-slate-500 dark:text-slate-400">
              <p><strong>{preview.sections.length}</strong> Sections</p>
              <p><strong>{totalBlocks}</strong> Content Blocks</p>
            </div>
          </div>

          {/* Warnings Banner if any */}
          {preview.extraction_warnings && preview.extraction_warnings.length > 0 && (
            <div className="mt-4 p-3.5 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900/60 text-amber-800 dark:text-amber-200 text-xs">
              <div className="flex items-center gap-2 font-semibold mb-1">
                <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" aria-hidden="true" />
                Extraction Notes & Non-Fatal Warnings ({preview.extraction_warnings.length})
              </div>
              <ul className="list-disc list-inside space-y-0.5 pl-1">
                {preview.extraction_warnings.map((w, idx) => (
                  <li key={idx}>{w}</li>
                ))}
              </ul>
            </div>
          )}
        </header>

        {/* Main Content Area: Rendered Blocks vs Raw JSON */}
        {showRawJson ? (
          <section className="bg-slate-900 text-slate-100 rounded-2xl p-6 font-mono text-xs overflow-x-auto relative shadow-sm">
            <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800">
              <span className="text-slate-400">ContentDocument JSON Representation</span>
              <button
                onClick={handleCopyJson}
                className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs transition-colors focus-visible:ring-2 focus-visible:ring-indigo-500"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? "Copied" : "Copy JSON"}
              </button>
            </div>
            <pre className="text-slate-300">{JSON.stringify(preview, null, 2)}</pre>
          </section>
        ) : (
          <div className="space-y-6">
            {preview.sections.map((section: Section, sIdx: number) => (
              <section
                key={section.id || sIdx}
                className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6 sm:p-8 shadow-sm"
              >
                {/* Section Header */}
                <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-100 dark:border-slate-700/60">
                  <h2 className="text-lg font-bold text-indigo-900 dark:text-indigo-300">
                    {section.title || `Section ${sIdx + 1}`}
                  </h2>
                  <span className="text-xs px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 font-medium">
                    {section.blocks.length} blocks
                  </span>
                </div>

                {/* Section Blocks */}
                <div className="space-y-1">
                  {section.blocks.map((block) => renderBlock(block))}
                </div>
              </section>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}

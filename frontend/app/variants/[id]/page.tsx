"use client";

import { useEffect, useState, use } from "react";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { api } from "@/lib/api";
import { GeneratedVariant, GeneratedBlock, ValidationResult } from "@/types/variant";

export default function VariantPreviewPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const variantId = resolvedParams.id;

  const [variant, setVariant] = useState<GeneratedVariant | null>(null);
  const [blocks, setBlocks] = useState<GeneratedBlock[]>([]);
  const [validation, setValidation] = useState<ValidationResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showTraceability, setShowTraceability] = useState(false);

  useEffect(() => {
    async function fetchVariantData() {
      try {
        setIsLoading(true);
        const [variantData, blocksData] = await Promise.all([
          api.variants.get(variantId),
          api.variants.getBlocks(variantId),
        ]);
        setVariant(variantData);
        setBlocks(blocksData);

        try {
          const valData = await api.variants.getValidation(variantId);
          setValidation(valData);
        } catch {
          // Validation may be pending or not generated
        }
      } catch (err: any) {
        setError(err.message || "Failed to load generated variant");
      } finally {
        setIsLoading(false);
      }
    }
    fetchVariantData();
  }, [variantId]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
        <Navbar />
        <main className="flex-1 max-w-6xl w-full mx-auto px-4 py-12">
          <div className="animate-pulse space-y-6">
            <div className="h-8 bg-slate-800 rounded w-1/3"></div>
            <div className="h-48 bg-slate-900 border border-slate-800 rounded-xl"></div>
            <div className="h-64 bg-slate-900 border border-slate-800 rounded-xl"></div>
          </div>
        </main>
      </div>
    );
  }

  if (error || !variant) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
        <Navbar />
        <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-16 text-center">
          <div className="p-8 bg-rose-950/40 border border-rose-800 rounded-2xl max-w-lg mx-auto">
            <h1 className="text-xl font-bold text-rose-200 mb-2">Variant Not Available</h1>
            <p className="text-slate-400 text-sm mb-6">{error || "Unable to find the requested accessible variant."}</p>
            <Link
              href="/dashboard"
              className="inline-flex items-center px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-sm transition"
            >
              Return to Dashboard
            </Link>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar />

      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-8">
        {/* Navigation Breadcrumb */}
        <div className="mb-6 flex items-center gap-2 text-sm text-slate-400">
          <Link href="/dashboard" className="hover:text-cyan-400 focus:outline-none focus:underline">
            Dashboard
          </Link>
          <span>/</span>
          <Link href={`/documents/${variant.document_id}`} className="hover:text-cyan-400 focus:outline-none focus:underline">
            Document
          </Link>
          <span>/</span>
          <span className="text-slate-200">Generated Variant</span>
        </div>

        {/* Header Summary */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 mb-8 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-3 mb-1">
                <h1 className="text-2xl font-bold text-white">{variant.name}</h1>
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider ${
                  variant.status === "COMPLETED"
                    ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                    : variant.status === "FAILED"
                    ? "bg-rose-950 text-rose-300 border border-rose-800"
                    : "bg-amber-950 text-amber-300 border border-amber-800"
                }`}>
                  {variant.status}
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Created: {new Date(variant.created_at).toLocaleString()} • {blocks.length} Generated Blocks
              </p>
            </div>

            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => setShowTraceability(!showTraceability)}
                className={`px-3 py-1.5 text-xs font-medium rounded-lg border transition ${
                  showTraceability
                    ? "bg-cyan-950/70 border-cyan-500/80 text-cyan-300"
                    : "bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700"
                }`}
              >
                {showTraceability ? "Hide Traceability Metadata" : "Show Traceability Metadata"}
              </button>

              <Link
                href={`/documents/${variant.document_id}`}
                className="px-3 py-1.5 text-xs font-medium bg-slate-800 border border-slate-700 hover:bg-slate-700 text-slate-300 rounded-lg transition"
              >
                Source Document
              </Link>
            </div>
          </div>

          {/* Validation & Grounding Status Banner */}
          {validation && (
            <div className="mt-6 pt-4 border-t border-slate-800 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
              <div className="flex items-center gap-2">
                <span className="text-slate-400">Grounding Integrity:</span>
                <span className={`font-semibold ${validation.grounded ? "text-emerald-400" : "text-amber-400"}`}>
                  {validation.grounded ? "100% Grounded in Source" : "Potential Unverified Claims"}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-slate-400">Schema Validation:</span>
                <span className={`font-semibold ${validation.is_valid ? "text-emerald-400" : "text-rose-400"}`}>
                  {validation.is_valid ? "Strictly Valid" : "Validation Flagged"}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-slate-400">Validation Warnings:</span>
                <span className="font-semibold text-slate-200">
                  {validation.warnings.length} Recorded
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Validation Warnings List if present */}
        {validation && validation.warnings.length > 0 && (
          <div className="mb-6 p-4 bg-amber-950/40 border border-amber-800/80 rounded-xl text-amber-200 text-xs space-y-1">
            <p className="font-semibold text-amber-100 mb-1">Non-Fatal Verification Notes:</p>
            {validation.warnings.map((w, idx) => (
              <p key={idx} className="leading-relaxed">• {w}</p>
            ))}
          </div>
        )}

        {/* Generated Blocks Presentation */}
        <div className="space-y-6">
          {blocks.map((block, idx) => {
            const content = block.content || {};
            const isDyslexia = block.profile_id === "dyslexia";
            const isCognitive = block.profile_id === "cognitive";

            return (
              <section
                key={block.id}
                aria-labelledby={`block-heading-${block.id}`}
                className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-sm hover:border-slate-700 transition"
              >
                {/* Block Header */}
                <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800/80 text-xs">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-cyan-400 uppercase tracking-wider">
                      Block {idx + 1}
                    </span>
                    <span className="text-slate-500">•</span>
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">
                      {block.profile_id}
                    </span>
                  </div>

                  <span className="text-slate-400 font-mono text-[11px]">
                    Source: {block.source_block_id}
                  </span>
                </div>

                {/* Dyslexia Profile Layout */}
                {isDyslexia && (
                  <div className="space-y-4">
                    {content.title && (
                      <h2 id={`block-heading-${block.id}`} className="text-lg font-bold text-white">
                        {content.title}
                      </h2>
                    )}

                    {content.simplified_text && (
                      <p className="text-slate-200 text-sm leading-relaxed font-normal bg-slate-950/40 p-4 rounded-xl border border-slate-800/80">
                        {content.simplified_text}
                      </p>
                    )}

                    {content.key_points && content.key_points.length > 0 && (
                      <div>
                        <h3 className="text-xs font-semibold uppercase tracking-wider text-cyan-400 mb-2">
                          Key Points
                        </h3>
                        <ul className="space-y-1.5 text-xs text-slate-300 list-disc list-inside">
                          {content.key_points.map((kp: string, kpIdx: number) => (
                            <li key={kpIdx} className="leading-relaxed">{kp}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {content.important_terms && content.important_terms.length > 0 && (
                      <div className="pt-2">
                        <h3 className="text-xs font-semibold uppercase tracking-wider text-teal-400 mb-2">
                          Important Terms & Definitions
                        </h3>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                          {content.important_terms.map((item: any, tIdx: number) => (
                            <div key={tIdx} className="p-2.5 bg-teal-950/20 border border-teal-900/40 rounded-lg">
                              <span className="font-bold text-teal-300">{item.term}:</span>{" "}
                              <span className="text-slate-300">{item.definition}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {content.example && (
                      <div className="p-3 bg-indigo-950/20 border border-indigo-900/40 rounded-xl text-xs text-slate-300">
                        <span className="font-bold text-indigo-300">Example:</span> {content.example}
                      </div>
                    )}
                  </div>
                )}

                {/* Cognitive Profile Layout */}
                {isCognitive && (
                  <div className="space-y-4">
                    {content.concept_title && (
                      <h2 id={`block-heading-${block.id}`} className="text-lg font-bold text-white">
                        {content.concept_title}
                      </h2>
                    )}

                    {content.explanation && (
                      <p className="text-slate-200 text-sm leading-relaxed bg-slate-950/40 p-4 rounded-xl border border-slate-800/80">
                        {content.explanation}
                      </p>
                    )}

                    {content.step_by_step && content.step_by_step.length > 0 && (
                      <div>
                        <h3 className="text-xs font-semibold uppercase tracking-wider text-cyan-400 mb-2">
                          Step-by-Step Breakdown
                        </h3>
                        <div className="space-y-2 text-xs text-slate-300">
                          {content.step_by_step.map((step: string, sIdx: number) => (
                            <div key={sIdx} className="flex items-start gap-2 p-2 bg-slate-950/30 rounded-lg border border-slate-800/60">
                              <span className="px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-400 font-mono font-bold text-[10px]">
                                {sIdx + 1}
                              </span>
                              <span className="leading-relaxed">{step}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {content.recap && (
                      <div className="p-3 bg-cyan-950/20 border border-cyan-900/40 rounded-xl text-xs text-slate-300">
                        <span className="font-bold text-cyan-300">Takeaway Recap:</span> {content.recap}
                      </div>
                    )}

                    {content.comprehension_questions && content.comprehension_questions.length > 0 && (
                      <div className="pt-2">
                        <h3 className="text-xs font-semibold uppercase tracking-wider text-amber-400 mb-2">
                          Comprehension Check
                        </h3>
                        <div className="space-y-2 text-xs">
                          {content.comprehension_questions.map((q: any, qIdx: number) => (
                            <div key={qIdx} className="p-3 bg-amber-950/10 border border-amber-900/30 rounded-xl">
                              <p className="font-semibold text-slate-200 mb-1">{q.question}</p>
                              {q.answer_hint && (
                                <p className="text-slate-400 italic text-[11px]">Hint: {q.answer_hint}</p>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Generic / Visual Profile Layout fallback */}
                {!isDyslexia && !isCognitive && (
                  <div className="space-y-2 text-xs text-slate-300">
                    <p className="text-sm text-slate-100">{content.formatted_text || JSON.stringify(content)}</p>
                  </div>
                )}

                {/* Optional Traceability Inspector */}
                {showTraceability && (
                  <div className="mt-4 pt-3 border-t border-slate-800/60 text-[11px] font-mono text-slate-400 grid grid-cols-2 sm:grid-cols-4 gap-2 bg-slate-950/60 p-3 rounded-lg">
                    <div>Block UUID: <span className="text-slate-300">{block.id.slice(0, 8)}...</span></div>
                    <div>Source ID: <span className="text-slate-300">{block.source_block_id}</span></div>
                    <div>Prompt: <span className="text-slate-300">v{block.prompt_version}</span></div>
                    <div>Model: <span className="text-slate-300">{block.model}</span></div>
                  </div>
                )}
              </section>
            );
          })}
        </div>
      </main>
    </div>
  );
}

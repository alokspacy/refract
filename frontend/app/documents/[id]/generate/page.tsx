"use client";

import { useEffect, useState, use } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { api, ApiError } from "@/lib/api";
import { Document } from "@/types/document";
import { ProfileInfo, ContentAnalysis } from "@/types/variant";
import { ProcessingJob } from "@/types/job";

export default function GenerateVariantPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const documentId = resolvedParams.id;
  const router = useRouter();

  const [document, setDocument] = useState<Document | null>(null);
  const [profiles, setProfiles] = useState<ProfileInfo[]>([]);
  const [analysis, setAnalysis] = useState<ContentAnalysis | null>(null);
  const [selectedProfiles, setSelectedProfiles] = useState<string[]>(["dyslexia"]);
  const [subjectOverride, setSubjectOverride] = useState<string>("");
  const [gradeOverride, setGradeOverride] = useState<string>("");

  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [activeJob, setActiveJob] = useState<ProcessingJob | null>(null);
  const [createdVariantId, setCreatedVariantId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Load Document, Available Profiles, and Content Analysis
  useEffect(() => {
    async function loadData() {
      try {
        setIsLoading(true);
        const [docData, profileList] = await Promise.all([
          api.documents.get(documentId),
          api.profiles.list(),
        ]);
        setDocument(docData);
        setProfiles(profileList);

        // Try to fetch analysis if already generated
        try {
          const analysisData = await api.documents.getAnalysis(documentId);
          setAnalysis(analysisData);
          if (analysisData.subject) setSubjectOverride(analysisData.subject);
          if (analysisData.grade_hint) setGradeOverride(analysisData.grade_hint);
        } catch {
          // Analysis not yet run, will run during pipeline
        }
      } catch (err: any) {
        setError(err.message || "Failed to load document or profile data");
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, [documentId]);

  // Poll Active Job Progress
  useEffect(() => {
    if (!activeJob || activeJob.status === "COMPLETED" || activeJob.status === "FAILED") {
      return;
    }

    const interval = setInterval(async () => {
      try {
        const updated = await api.jobs.get(activeJob.id);
        setActiveJob(updated);
        if (updated.status === "COMPLETED" && createdVariantId) {
          setIsGenerating(false);
          // Redirect to Variant Preview after short delay
          setTimeout(() => {
            router.push(`/variants/${createdVariantId}`);
          }, 1200);
        } else if (updated.status === "FAILED") {
          setIsGenerating(false);
          setError(updated.error_message || "Generation pipeline failed");
        }
      } catch (pollErr: any) {
        console.error("Job poll error:", pollErr);
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [activeJob, createdVariantId, router]);

  const toggleProfile = (id: string) => {
    if (selectedProfiles.includes(id)) {
      if (selectedProfiles.length > 1) {
        setSelectedProfiles(selectedProfiles.filter((p) => p !== id));
      }
    } else {
      setSelectedProfiles([...selectedProfiles, id]);
    }
  };

  const handleStartGeneration = async () => {
    if (selectedProfiles.length === 0) {
      setError("Please select at least one accessibility profile");
      return;
    }

    try {
      setIsGenerating(true);
      setError(null);

      const overrides: Record<string, any> = {};
      if (subjectOverride.trim()) overrides.subject = subjectOverride.trim();
      if (gradeOverride.trim()) overrides.grade_hint = gradeOverride.trim();

      const res = await api.documents.createVariant(documentId, {
        profile_ids: selectedProfiles,
        metadata_overrides: overrides,
      });

      setCreatedVariantId(res.variant_id);
      const initialJob = await api.jobs.get(res.job_id);
      setActiveJob(initialJob);
    } catch (err: any) {
      setIsGenerating(false);
      setError(err.message || "Failed to start accessible transformation");
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
        <Navbar />
        <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-12">
          <div className="animate-pulse space-y-6">
            <div className="h-8 bg-slate-800 rounded w-1/3"></div>
            <div className="h-32 bg-slate-900 border border-slate-800 rounded-xl"></div>
            <div className="h-64 bg-slate-900 border border-slate-800 rounded-xl"></div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-8">
        {/* Navigation Breadcrumb */}
        <div className="mb-6 flex items-center gap-2 text-sm text-slate-400">
          <Link href="/dashboard" className="hover:text-cyan-400 focus:outline-none focus:underline">
            Dashboard
          </Link>
          <span>/</span>
          <Link href={`/documents/${documentId}`} className="hover:text-cyan-400 focus:outline-none focus:underline">
            {document?.original_filename || "Document"}
          </Link>
          <span>/</span>
          <span className="text-slate-200">AI Transformation Studio</span>
        </div>

        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight text-white mb-2">
            Generate Accessible Learning Variant
          </h1>
          <p className="text-slate-400 leading-relaxed">
            Select pedagogical accessibility profiles to generate structured, source-grounded learning representations.
          </p>
        </div>

        {error && (
          <div
            role="alert"
            className="mb-6 p-4 bg-rose-950/80 border border-rose-800/80 rounded-xl text-rose-200 text-sm flex items-start gap-3 shadow-lg"
          >
            <svg className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p className="font-semibold text-rose-100">Generation Notice</p>
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* Progress Tracker when Generating */}
        {isGenerating && activeJob && (
          <div
            aria-live="polite"
            className="mb-8 p-6 bg-slate-900/90 border border-cyan-500/40 rounded-2xl shadow-xl shadow-cyan-950/20 backdrop-blur"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 rounded-full border-2 border-cyan-400 border-t-transparent animate-spin" />
                <span className="font-semibold text-cyan-300">
                  Transformation in Progress: {activeJob.current_stage}
                </span>
              </div>
              <span className="text-sm font-mono text-cyan-400 font-bold">
                {Math.round(activeJob.progress)}%
              </span>
            </div>

            {/* Accessible Progress Bar */}
            <div
              role="progressbar"
              aria-valuenow={Math.round(activeJob.progress)}
              aria-valuemin={0}
              aria-valuemax={100}
              className="w-full h-3 bg-slate-800 rounded-full overflow-hidden p-0.5 border border-slate-700"
            >
              <div
                className="h-full bg-gradient-to-r from-cyan-500 via-teal-400 to-indigo-500 rounded-full transition-all duration-500 ease-out"
                style={{ width: `${Math.max(activeJob.progress, 5)}%` }}
              />
            </div>

            {/* Stages Stepper */}
            <div className="grid grid-cols-4 gap-2 mt-4 text-xs font-medium text-center text-slate-400">
              <div className={activeJob.progress >= 20 ? "text-cyan-300 font-bold" : ""}>
                1. Analyzing (20%)
              </div>
              <div className={activeJob.progress >= 35 ? "text-cyan-300 font-bold" : ""}>
                2. Planning (35%)
              </div>
              <div className={activeJob.progress >= 70 ? "text-cyan-300 font-bold" : ""}>
                3. Transforming (70%)
              </div>
              <div className={activeJob.progress >= 90 ? "text-cyan-300 font-bold" : ""}>
                4. Validating (100%)
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Main Column: Profile Selection */}
          <div className="md:col-span-2 space-y-6">
            <section className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-sm">
              <h2 className="text-lg font-semibold text-white mb-1">
                Select Accessibility Profiles
              </h2>
              <p className="text-xs text-slate-400 mb-6">
                Choose one or more compatible accessibility profiles. Multiple selections apply deterministic transformation precedence.
              </p>

              <div className="space-y-4">
                {profiles.map((prof) => {
                  const isSelected = selectedProfiles.includes(prof.id);
                  return (
                    <label
                      key={prof.id}
                      className={`relative flex items-start gap-4 p-4 rounded-xl border transition-all cursor-pointer select-none ${
                        isSelected
                          ? "bg-cyan-950/30 border-cyan-500/60 shadow-md shadow-cyan-950/20"
                          : "bg-slate-950/40 border-slate-800 hover:border-slate-700"
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => toggleProfile(prof.id)}
                        disabled={isGenerating}
                        className="mt-1 w-5 h-5 rounded border-slate-700 text-cyan-500 focus:ring-cyan-400 focus:ring-offset-slate-900"
                      />
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <span className="font-semibold text-slate-100">{prof.name}</span>
                          <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                            v{prof.version}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                          {prof.description}
                        </p>
                      </div>
                    </label>
                  );
                })}
              </div>
            </section>
          </div>

          {/* Right Column: Educational Metadata & Actions */}
          <div className="space-y-6">
            <section className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-sm">
              <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 mb-4">
                Content Parameters
              </h2>

              <div className="space-y-4 text-sm">
                <div>
                  <label htmlFor="subject-input" className="block text-xs text-slate-400 mb-1">
                    Subject / Discipline
                  </label>
                  <input
                    id="subject-input"
                    type="text"
                    value={subjectOverride}
                    onChange={(e) => setSubjectOverride(e.target.value)}
                    disabled={isGenerating}
                    placeholder="e.g. Biology, History, Math"
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-slate-100 text-sm focus:outline-none focus:ring-1 focus:ring-cyan-500"
                  />
                </div>

                <div>
                  <label htmlFor="grade-input" className="block text-xs text-slate-400 mb-1">
                    Grade Level / Complexity
                  </label>
                  <input
                    id="grade-input"
                    type="text"
                    value={gradeOverride}
                    onChange={(e) => setGradeOverride(e.target.value)}
                    disabled={isGenerating}
                    placeholder="e.g. Grade 9-10, Intermediate"
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-slate-100 text-sm focus:outline-none focus:ring-1 focus:ring-cyan-500"
                  />
                </div>

                {analysis && (
                  <div className="pt-2 border-t border-slate-800/80 text-xs text-slate-400 space-y-1">
                    <p>Detected Objectives: <span className="font-semibold text-slate-200">{analysis.learning_objectives.length}</span></p>
                    <p>Detected Concepts: <span className="font-semibold text-slate-200">{analysis.concepts.length}</span></p>
                    <p>Detected Terms: <span className="font-semibold text-slate-200">{analysis.vocabulary.length}</span></p>
                  </div>
                )}
              </div>

              <div className="mt-6 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={handleStartGeneration}
                  disabled={isGenerating || selectedProfiles.length === 0}
                  className="w-full py-3 px-4 bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-semibold rounded-xl shadow-lg shadow-cyan-950/40 transition-all focus:outline-none focus:ring-2 focus:ring-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {isGenerating ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Transforming...
                    </>
                  ) : (
                    <>
                      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                      Start AI Transformation
                    </>
                  )}
                </button>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}

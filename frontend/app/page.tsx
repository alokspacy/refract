"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/lib/auth";
import Link from "next/link";
import { BookOpen, Sparkles, ShieldCheck, ArrowRight } from "lucide-react";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated()) {
      router.replace("/dashboard");
    }
  }, [router]);

  return (
    <div className="flex-1 flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8 py-12">
      <div className="max-w-3xl w-full text-center space-y-8">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 text-indigo-700 dark:text-indigo-300 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5" aria-hidden="true" />
          <span>AccessLearn AI Foundation — Phase 1</span>
        </div>

        {/* Title */}
        <h1 className="text-4xl sm:text-5xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-tight">
          AI Engine for Automatic Accessible Educational Content
        </h1>

        {/* Description */}
        <p className="text-lg text-slate-700 dark:text-slate-200 max-w-2xl mx-auto">
          Empowering educators to upload and manage accessible course materials, syllabi, slides, and lectures with secure document pipelines and future multi-modal accessibility adaptations.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <Link
            href="/login"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-7 py-3 rounded-xl font-semibold shadow-md transition-all focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-indigo-600"
          >
            <span>Teacher Portal Login</span>
            <ArrowRight className="w-4 h-4" aria-hidden="true" />
          </Link>
          <Link
            href="/register"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-800 dark:text-white border border-slate-300 dark:border-slate-700 px-7 py-3 rounded-xl font-semibold shadow-sm transition-all focus-visible:ring-2 focus-visible:ring-slate-400"
          >
            <span>Create Account</span>
          </Link>
        </div>

        {/* Value Props */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-12 text-left">
          <div className="p-5 rounded-2xl bg-white dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 shadow-sm">
            <div className="w-9 h-9 rounded-lg bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 flex items-center justify-center mb-3">
              <BookOpen className="w-5 h-5" aria-hidden="true" />
            </div>
            <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-1">Teacher Dashboard</h2>
            <p className="text-xs text-slate-700 dark:text-slate-200">
              Manage learning materials and track ingestion pipeline statuses seamlessly.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 shadow-sm">
            <div className="w-9 h-9 rounded-lg bg-emerald-100 dark:bg-emerald-900/50 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mb-3">
              <ShieldCheck className="w-5 h-5" aria-hidden="true" />
            </div>
            <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-1">Strict File Security</h2>
            <p className="text-xs text-slate-700 dark:text-slate-200">
              MIME validation, isolated storage, and JWT-authenticated ownership protection.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 shadow-sm">
            <div className="w-9 h-9 rounded-lg bg-purple-100 dark:bg-purple-900/50 text-purple-600 dark:text-purple-400 flex items-center justify-center mb-3">
              <Sparkles className="w-5 h-5" aria-hidden="true" />
            </div>
            <h2 className="text-sm font-bold text-slate-900 dark:text-white mb-1">Phase 1 Foundation</h2>
            <p className="text-xs text-slate-700 dark:text-slate-200">
              Modular architecture ready for OCR, LLM transformations, and multi-modal accessibility.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

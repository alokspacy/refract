"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect } from "react";
import { Glass, Kicker } from "@/components/ui/glass";
import { useStudio } from "@/hooks/use-studio";
import { PIPELINE_STAGES, PROFILE_MAP } from "@/lib/profiles";
import { cn } from "@/lib/utils";

export default function JobPage() {
  const router = useRouter();
  const params = useParams<{ id: string }>();
  const { jobs, documents, ready } = useStudio();
  const job = jobs.find((j) => j.id === params.id);
  const doc = documents.find((d) => d.id === job?.document_id);

  useEffect(() => {
    if (job?.status === "ready" && doc) {
      const t = window.setTimeout(() => {
        router.push(`/studio/review/${doc.id}`);
      }, 800);
      return () => window.clearTimeout(t);
    }
  }, [job?.status, doc, router]);

  if (!ready) {
    return (
      <main id="main" className="px-5 py-10 text-sm text-ink-muted">
        Loading job…
      </main>
    );
  }

  if (!job || !doc) {
    return (
      <main id="main" className="px-5 py-10">
        <p>That job is not on this device.</p>
        <Link href="/studio" className="mt-3 inline-block text-sm underline">
          Back to library
        </Link>
      </main>
    );
  }

  const stageIndex = PIPELINE_STAGES.findIndex((s) => s.id === job.stage);

  return (
    <main id="main" className="mx-auto w-full max-w-3xl flex-1 px-5 py-12">
      <Kicker>Job {job.id.slice(-6)}</Kicker>
      <h1 className="font-display mt-2 text-4xl tracking-tight">{doc.title}</h1>
      <p className="mt-2 text-sm text-ink-muted" aria-live="polite">
        {job.status === "ready" ? "Ready for review." : `${job.stage} · ${job.progress}%`}
      </p>

      <Glass className="mt-8 p-6">
        <div className="h-1 overflow-hidden rounded-full bg-paper-2" role="progressbar" aria-valuenow={job.progress} aria-valuemin={0} aria-valuemax={100}>
          <div className="hairline h-full" style={{ width: `${job.progress}%` }} />
        </div>
        <ol className="mt-6 space-y-3">
          {PIPELINE_STAGES.map((stage, i) => {
            const done = job.status === "ready" || i <= stageIndex;
            const current = job.stage === stage.id;
            return (
              <li key={stage.id} className="flex gap-3">
                <span
                  className={cn(
                    "mt-1 h-2 w-2 rounded-full",
                    done ? "bg-ink" : "border border-stroke",
                    current && "ring-4 ring-ink/10",
                  )}
                />
                <div>
                  <p className={cn("text-sm", current && "font-medium")}>{stage.label}</p>
                  <p className="text-xs text-ink-muted">{stage.detail}</p>
                </div>
              </li>
            );
          })}
        </ol>
      </Glass>

      <p className="mt-6 text-sm text-ink-muted">
        Profiles: {job.profile_ids.map((id) => PROFILE_MAP[id].short).join(" · ")}
      </p>

      {job.events[0] ? (
        <p className="mt-2 text-xs text-ink-muted" aria-live="polite">
          {job.events[0].message}
        </p>
      ) : null}

      {job.status === "ready" ? (
        <Link href={`/studio/review/${doc.id}`} className="mt-8 inline-flex rounded-full bg-ink px-5 py-2.5 text-sm text-paper">
          Open review workspace
        </Link>
      ) : null}
    </main>
  );
}

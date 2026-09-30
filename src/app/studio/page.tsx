"use client";

import Link from "next/link";
import { ArrowUpRight, Plus } from "lucide-react";
import { ButtonLink } from "@/components/ui/button-link";
import { Glass, Kicker } from "@/components/ui/glass";
import { useStudio } from "@/hooks/use-studio";
import { PROFILE_MAP } from "@/lib/profiles";
import { formatWhen } from "@/lib/utils";

export default function StudioHomePage() {
  const { documents, jobs, ready } = useStudio();

  return (
    <main id="main" className="mx-auto w-full max-w-5xl flex-1 px-5 py-10">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <Kicker>Studio</Kicker>
          <h1 className="font-display mt-2 text-4xl tracking-tight">Library</h1>
          <p className="mt-2 max-w-xl text-sm text-ink-muted">
            Conversions stay on this device for the pilot. Approve before anything is treated as classroom-ready.
          </p>
        </div>
        <ButtonLink href="/studio/new" className="gap-2">
          <Plus className="h-4 w-4" />
          New conversion
        </ButtonLink>
      </div>

      {!ready ? (
        <p className="mt-12 text-sm text-ink-muted">Loading library…</p>
      ) : documents.length === 0 ? (
        <Glass className="mt-12 p-10 text-center">
          <p className="font-display text-3xl">A quiet shelf.</p>
          <p className="mx-auto mt-3 max-w-md text-sm text-ink-muted">
            Upload a lesson, or start with the photosynthesis sample to see structure, descriptions, captions, and review in one pass.
          </p>
          <div className="mt-6 flex justify-center gap-3">
            <ButtonLink href="/studio/new">Upload</ButtonLink>
            <ButtonLink href="/studio/new?sample=photosynthesis" variant="ghost">
              Sample lesson
            </ButtonLink>
          </div>
        </Glass>
      ) : (
        <ul className="mt-10 space-y-3">
          {documents.map((doc) => {
            const job = jobs.find((j) => j.document_id === doc.id);
            return (
              <li key={doc.id}>
                <Glass className="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <p className="font-display text-2xl leading-tight">{doc.title}</p>
                    <p className="mt-1 text-sm text-ink-muted">
                      {doc.subject ?? doc.input_kind.toUpperCase()}
                      {doc.grade_hint ? ` · ${doc.grade_hint}` : ""}
                      {job ? ` · ${job.status === "ready" ? "Ready for review" : job.stage}` : ""}
                      {" · "}
                      {formatWhen(doc.created_at)}
                    </p>
                    {job ? (
                      <p className="mt-2 flex flex-wrap gap-1.5">
                        {job.profile_ids.map((id) => (
                          <span
                            key={id}
                            className="rounded-full border border-stroke px-2 py-0.5 text-[0.68rem] uppercase tracking-[0.14em]"
                          >
                            {PROFILE_MAP[id].short}
                          </span>
                        ))}
                      </p>
                    ) : null}
                  </div>
                  <Link
                    href={
                      job?.status === "ready"
                        ? `/studio/review/${doc.id}`
                        : job
                          ? `/studio/jobs/${job.id}`
                          : "/studio/new"
                    }
                    className="inline-flex items-center gap-1 text-sm"
                  >
                    Open
                    <ArrowUpRight className="h-4 w-4" />
                  </Link>
                </Glass>
              </li>
            );
          })}
        </ul>
      )}
    </main>
  );
}

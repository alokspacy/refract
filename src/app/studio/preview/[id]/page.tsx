"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useState } from "react";
import { useStudio } from "@/hooks/use-studio";
import { PROFILE_MAP } from "@/lib/profiles";
import { cn } from "@/lib/utils";

export default function PreviewPage() {
  const params = useParams<{ id: string }>();
  const { variants, documents, ready } = useStudio();
  const variant = variants.find((item) => item.id === params.id);
  const doc = documents.find((item) => item.id === variant?.document_id);
  const [step, setStep] = useState(0);

  if (!ready) {
    return (
      <main id="main" className="px-5 py-10 text-sm text-ink-muted">
        Opening preview…
      </main>
    );
  }

  if (!variant || !doc) {
    return (
      <main id="main" className="px-5 py-10">
        <p>Preview is not on this device.</p>
        <Link href="/studio" className="underline">
          Library
        </Link>
      </main>
    );
  }

  const meta = PROFILE_MAP[variant.profile_id];
  const theme = meta.previewTheme;
  const chunks = variant.blocks.flatMap((b) => b.chunks ?? []);
  const showStepper = variant.profile_id === "cognitive" && chunks.length > 0;
  const current = chunks[step];

  return (
    <main
      id="main"
      className={cn("min-h-full px-5 py-10", variant.profile_id === "dyslexia" && "dyslexia-target")}
      style={{
        background: theme.bg,
        color: theme.fg,
        fontSize: variant.profile_id === "low-vision" ? "1.25rem" : undefined,
      }}
    >
      <div className="mx-auto" style={{ maxWidth: theme.measure, lineHeight: theme.spacing }}>
        <p className="text-[0.65rem] uppercase tracking-[0.18em] opacity-70">
          Learner preview · {meta.short} · not a diagnosis
        </p>
        <h1 className="font-display mt-3 text-4xl tracking-tight">{doc.title}</h1>
        <p className="mt-3 text-sm opacity-80">{meta.promise}</p>

        <Link
          href={`/studio/review/${doc.id}`}
          className="mt-4 inline-flex min-h-11 items-center rounded-full border px-4 py-2 text-sm"
          style={{ borderColor: "currentColor" }}
        >
          Back to review
        </Link>

        {showStepper && current ? (
          <section className="mt-10">
            <p className="text-xs opacity-70">
              Concept {step + 1} of {chunks.length}
            </p>
            <h2 className="font-display mt-2 text-3xl">{current.title}</h2>
            <p className="mt-4 text-lg">{current.explanation}</p>
            {current.example ? (
              <p className="mt-4">
                <strong>Example.</strong> {current.example}
              </p>
            ) : null}
            {current.recap ? (
              <p className="mt-4">
                <strong>Recap.</strong> {current.recap}
              </p>
            ) : null}
            <div className="mt-8 flex gap-3">
              <button
                type="button"
                className="min-h-12 min-w-28 rounded-full border px-5"
                style={{ borderColor: "currentColor" }}
                onClick={() => setStep((s) => Math.max(0, s - 1))}
                disabled={step === 0}
              >
                Previous
              </button>
              <button
                type="button"
                className="min-h-12 min-w-28 rounded-full px-5"
                style={{ background: theme.fg, color: theme.bg }}
                onClick={() => setStep((s) => Math.min(chunks.length - 1, s + 1))}
                disabled={step === chunks.length - 1}
              >
                Next
              </button>
            </div>
          </section>
        ) : (
          <article className="mt-10 space-y-5">
            {variant.blocks.map((block) => (
              <section key={block.id}>
                {block.type === "heading" ? (
                  <h2 className="font-display text-2xl">{block.text}</h2>
                ) : (
                  <p className="whitespace-pre-wrap">{block.text}</p>
                )}
                {block.aac_choices?.length ? (
                  <div className="mt-3 grid gap-2">
                    {block.aac_choices.map((choice) => (
                      <button
                        key={choice}
                        type="button"
                        className="min-h-12 rounded-2xl border px-4 py-3 text-left"
                        style={{ borderColor: "currentColor" }}
                      >
                        {choice}
                      </button>
                    ))}
                  </div>
                ) : null}
              </section>
            ))}
            {variant.glossary.length ? (
              <section>
                <h2 className="font-display text-2xl">Glossary</h2>
                <dl className="mt-3 space-y-2">
                  {variant.glossary.map((g) => (
                    <div key={g.term}>
                      <dt className="font-medium">{g.term}</dt>
                      <dd className="opacity-80">{g.definition}</dd>
                    </div>
                  ))}
                </dl>
              </section>
            ) : null}
          </article>
        )}
      </div>
    </main>
  );
}

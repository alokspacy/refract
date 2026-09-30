import type { Metadata } from "next";
import { SiteFooter, SiteHeader } from "@/components/site/chrome";
import { Glass, Kicker } from "@/components/ui/glass";
import { PIPELINE_STAGES } from "@/lib/profiles";

export const metadata: Metadata = { title: "How it works" };

const layers = [
  {
    title: "Ingest",
    body: "PDF, DOCX, PPTX, images, pasted text, audio, and video. Native text first; OCR only when the page is silent.",
  },
  {
    title: "Normalize",
    body: "Everything becomes one Content JSON: document → sections → blocks, with page or slide pointers.",
  },
  {
    title: "Plan",
    body: "Selected accessibility profiles become a machine-readable transformation plan. Multiple profiles compose; conflicts follow precedence.",
  },
  {
    title: "Transform",
    body: "Plain language, chunking, alt text, transcripts, quizzes, AAC choices — each with structured output and a prompt version.",
  },
  {
    title: "Validate",
    body: "Schema, coverage, number/name checks, alt-text and caption completeness. Failed blocks stay visible and retryable.",
  },
  {
    title: "Approve & export",
    body: "A teacher edits, regenerates, and freezes a version. Exporters render deterministic HTML, captions, audio scripts, and JSON — never arbitrary model markup.",
  },
];

export default function HowItWorksPage() {
  return (
    <div className="flex min-h-full flex-col">
      <SiteHeader />
      <main id="main" className="mx-auto w-full max-w-6xl flex-1 px-5 py-16">
        <Kicker>Architecture</Kicker>
        <h1 className="font-display mt-4 max-w-3xl text-4xl tracking-tight md:text-6xl">
          Heterogeneous in. Traceable out.
        </h1>
        <p className="mt-5 max-w-2xl text-lg text-ink-muted">
          Refract is an orchestration layer. Foundation models, OCR, and speech APIs are interchangeable
          providers behind a vendor-neutral schema.
        </p>
        <ol className="mt-12 grid gap-3 md:grid-cols-2">
          {layers.map((layer, i) => (
            <li key={layer.title}>
              <Glass className="h-full p-6">
                <span className="font-mono text-xs text-ink-muted">0{i + 1}</span>
                <h2 className="mt-3 font-display text-2xl">{layer.title}</h2>
                <p className="mt-2 text-sm leading-relaxed text-ink-muted">{layer.body}</p>
              </Glass>
            </li>
          ))}
        </ol>
        <div className="mt-12">
          <h2 className="font-display text-2xl">Live pipeline stages</h2>
          <ul className="mt-4 flex flex-col gap-2">
            {PIPELINE_STAGES.map((stage) => (
              <li key={stage.id} className="flex items-baseline justify-between gap-4 border-b border-stroke py-3">
                <span>{stage.label}</span>
                <span className="text-sm text-ink-muted">{stage.detail}</span>
              </li>
            ))}
          </ul>
        </div>
      </main>
      <SiteFooter />
    </div>
  );
}

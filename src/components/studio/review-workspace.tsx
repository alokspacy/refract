"use client";

import Link from "next/link";
import { useState } from "react";
import { Check, Pause, Pencil, RefreshCw, Volume2 } from "lucide-react";
import { CycleFigure, LeafFigure } from "@/components/brand/mark";
import { Button } from "@/components/ui/button";
import { Glass } from "@/components/ui/glass";
import { useStudio } from "@/hooks/use-studio";
import { regenerateBlock, renderAccessibleHtml } from "@/lib/engine";
import { PROFILE_MAP } from "@/lib/profiles";
import { patchVariant } from "@/lib/store";
import { downloadBlob, speak, stopSpeaking, cn } from "@/lib/utils";
import type { GeneratedBlock, GeneratedVariant, ProfileId, SourceBlock } from "@/lib/types";

function Figure({ figure }: { figure?: string }) {
  if (figure === "leaf") return <LeafFigure className="max-h-48" />;
  if (figure === "cycle") return <CycleFigure className="max-h-48" />;
  return null;
}

function SourceCard({ block }: { block: SourceBlock }) {
  return (
    <article className="rounded-[1.2rem] border border-stroke bg-paper/50 p-4">
      <p className="text-[0.65rem] uppercase tracking-[0.16em] text-ink-muted">
        {block.type}
        {block.page_or_slide ? ` · p.${block.page_or_slide}` : ""}
      </p>
      {block.metadata?.figure ? (
        <div className="mt-3">
          <Figure figure={block.metadata.figure} />
        </div>
      ) : null}
      {block.type === "list" && block.metadata?.items ? (
        <ul className="mt-3 list-disc space-y-1 pl-5 text-sm">
          {block.metadata.items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : block.type === "table" && block.metadata?.headers && block.metadata.rows ? (
        <div className="mt-3 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr>
                {block.metadata.headers.map((h) => (
                  <th key={h} className="border-b border-stroke py-1 pr-3 font-medium">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {block.metadata.rows.map((row, i) => (
                <tr key={i}>
                  {row.map((cell, j) => (
                    <td key={j} className="border-b border-stroke py-1 pr-3">
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className={cn("mt-2 text-sm leading-relaxed", block.type === "heading" && "font-display text-xl")}>
          {block.source_text}
        </p>
      )}
    </article>
  );
}

function OutputCard({
  block,
  onEdit,
  onRegenerate,
}: {
  block: GeneratedBlock;
  onEdit: (text: string) => void;
  onRegenerate: (instruction: string) => void;
}) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(block.text);
  const [instruction, setInstruction] = useState("");

  return (
    <article className="rounded-[1.2rem] border border-stroke bg-paper/80 p-4">
      <div className="flex items-center justify-between gap-2">
        <p className="text-[0.65rem] uppercase tracking-[0.16em] text-ink-muted">
          {block.type}
          {block.teacher_edited ? " · edited" : ""}
          {block.status !== "ok" ? ` · ${block.status}` : ""}
        </p>
        <div className="flex gap-1">
          <button
            type="button"
            className="rounded-full p-2 text-ink-muted hover:text-ink"
            onClick={() => setEditing((v) => !v)}
            aria-label="Edit block"
          >
            <Pencil className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
      {block.chunks?.length ? (
        <div className="mt-3 space-y-3">
          {block.chunks.map((chunk) => (
            <div key={chunk.title}>
              <p className="font-display text-lg">{chunk.title}</p>
              <p className="mt-1 text-sm leading-relaxed">{chunk.explanation}</p>
              {chunk.example ? (
                <p className="mt-1 text-sm text-ink-muted">Example. {chunk.example}</p>
              ) : null}
              {chunk.recap ? <p className="mt-1 text-sm">Recap. {chunk.recap}</p> : null}
            </div>
          ))}
        </div>
      ) : editing ? (
        <textarea
          className="mt-3 min-h-28 w-full rounded-xl border border-stroke bg-transparent p-2 text-sm"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
        />
      ) : (
        <p className="mt-3 whitespace-pre-wrap text-sm leading-relaxed">{block.text}</p>
      )}
      {block.alt_text && block.alt_text !== block.text ? (
        <p className="mt-2 text-xs text-ink-muted">Alt: {block.alt_text}</p>
      ) : null}
      {block.aac_choices?.length ? (
        <div className="mt-3 flex flex-wrap gap-2" role="group" aria-label="AAC choices">
          {block.aac_choices.map((choice) => (
            <span key={choice} className="rounded-full border border-stroke px-3 py-2 text-sm">
              {choice}
            </span>
          ))}
        </div>
      ) : null}
      {editing ? (
        <div className="mt-3 flex gap-2">
          <Button
            onClick={() => {
              onEdit(draft);
              setEditing(false);
            }}
          >
            Save
          </Button>
          <Button variant="ghost" onClick={() => setEditing(false)}>
            Cancel
          </Button>
        </div>
      ) : null}
      <form
        className="mt-3 flex gap-2"
        onSubmit={(e) => {
          e.preventDefault();
          if (!instruction.trim()) return;
          onRegenerate(instruction);
          setInstruction("");
        }}
      >
        <input
          className="min-w-0 flex-1 rounded-full border border-stroke bg-transparent px-3 py-2 text-xs"
          placeholder="Regenerate with a note — e.g. shorter, simpler, more detail"
          value={instruction}
          onChange={(e) => setInstruction(e.target.value)}
        />
        <Button type="submit" variant="ghost" icon={<RefreshCw className="h-3.5 w-3.5" />}>
          Retry
        </Button>
      </form>
    </article>
  );
}

export function ReviewWorkspace({ documentId }: { documentId: string }) {
  const { documents, variants: allVariants, ready } = useStudio();
  const doc = documents.find((item) => item.id === documentId);
  const variants = allVariants.filter((item) => item.document_id === documentId);
  const [profile, setProfile] = useState<ProfileId | null>(null);
  const [speaking, setSpeaking] = useState(false);

  const variant = variants.find((v) => v.profile_id === (profile ?? variants[0]?.profile_id));
  const sourceBlocks = doc?.sections.flatMap((s) => s.blocks) ?? [];

  function saveVariant(next: GeneratedVariant) {
    patchVariant(next);
  }

  if (!ready) {
    return (
      <main id="main" className="px-5 py-10 text-sm text-ink-muted">
        Opening review…
      </main>
    );
  }

  if (!doc || !variant) {
    return (
      <main id="main" className="px-5 py-10">
        <p>No reviewed document on this device.</p>
        <Link href="/studio" className="mt-3 inline-block text-sm underline">
          Library
        </Link>
      </main>
    );
  }

  const profileMeta = PROFILE_MAP[variant.profile_id];

  return (
    <main id="main" className="flex min-h-0 flex-1 flex-col">
      <header className="border-b border-stroke px-5 py-4">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-[0.65rem] uppercase tracking-[0.18em] text-ink-muted">Review workspace</p>
            <h1 className="font-display mt-1 text-3xl tracking-tight">{doc.title}</h1>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button
              variant="ghost"
              icon={speaking ? <Pause className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
              onClick={() => {
                if (speaking) {
                  stopSpeaking();
                  setSpeaking(false);
                } else if (variant.narration_text) {
                  speak(variant.narration_text);
                  setSpeaking(true);
                }
              }}
            >
              {speaking ? "Stop" : "Narrate"}
            </Button>
            <Button
              variant="ghost"
              onClick={() =>
                downloadBlob(
                  `${doc.title}-${variant.profile_id}.html`,
                  renderAccessibleHtml(doc, variant),
                  "text/html",
                )
              }
            >
              Export HTML
            </Button>
            {variant.captions_vtt ? (
              <Button
                variant="ghost"
                onClick={() => downloadBlob(`${doc.title}.vtt`, variant.captions_vtt!, "text/vtt")}
              >
                Captions
              </Button>
            ) : null}
            <Button
              variant="ghost"
              onClick={() =>
                downloadBlob(
                  `${doc.title}-${variant.profile_id}.json`,
                  JSON.stringify({ document: doc, variant }, null, 2),
                  "application/json",
                )
              }
            >
              JSON
            </Button>
            <Link
              href={`/studio/preview/${variant.id}`}
              className="inline-flex items-center rounded-full border border-stroke px-4 py-2.5 text-sm"
            >
              Learner preview
            </Link>
            <Button
              icon={<Check className="h-4 w-4" />}
              onClick={() =>
                saveVariant({
                  ...variant,
                  status: "approved",
                  approved_at: new Date().toISOString(),
                })
              }
            >
              {variant.status === "approved" ? "Approved" : "Approve"}
            </Button>
          </div>
        </div>
        <div className="mt-4 flex flex-wrap gap-2" role="tablist" aria-label="Accessibility profiles">
          {variants.map((item) => {
            const meta = PROFILE_MAP[item.profile_id];
            const selected = item.id === variant.id;
            return (
              <button
                key={item.id}
                type="button"
                role="tab"
                aria-selected={selected}
                onClick={() => setProfile(item.profile_id)}
                className={cn(
                  "rounded-full border px-3 py-1.5 text-sm",
                  selected ? "border-ink bg-ink text-paper" : "border-stroke",
                )}
              >
                <span className="mr-2 inline-block h-1.5 w-1.5 rounded-full" style={{ background: selected ? "currentColor" : meta.hex }} />
                {meta.short}
              </button>
            );
          })}
        </div>
      </header>

      <p className="border-b border-stroke px-5 py-2 text-xs text-ink-muted">
        {profileMeta.promise} Coverage {variant.validation.coverage.mapped}/{variant.validation.coverage.total}
        {variant.validation.issues.length ? ` · ${variant.validation.issues.length} checks to review` : " · checks passed"}
        {variant.status === "approved" ? " · frozen" : ""}
      </p>

      <div className="grid flex-1 gap-0 lg:grid-cols-2">
        <section className="min-h-0 space-y-3 overflow-y-auto border-b border-stroke p-5 lg:border-b-0 lg:border-r" aria-label="Source">
          <h2 className="text-[0.65rem] uppercase tracking-[0.18em] text-ink-muted">Source</h2>
          {sourceBlocks.map((block) => (
            <SourceCard key={block.id} block={block} />
          ))}
        </section>
        <section className="min-h-0 space-y-3 overflow-y-auto p-5" aria-label={`${profileMeta.short} output`}>
          <h2 className="text-[0.65rem] uppercase tracking-[0.18em] text-ink-muted">{profileMeta.short} output</h2>
          {variant.blocks.map((block) => (
            <OutputCard
              key={block.id}
              block={block}
              onEdit={(text) =>
                saveVariant({
                  ...variant,
                  blocks: variant.blocks.map((b) =>
                    b.id === block.id ? { ...b, text, teacher_edited: true } : b,
                  ),
                })
              }
              onRegenerate={(instruction) => saveVariant(regenerateBlock(variant, block.id, instruction, doc))}
            />
          ))}
          {variant.glossary.length ? (
            <Glass className="p-4">
              <h3 className="font-display text-xl">Glossary</h3>
              <dl className="mt-3 space-y-2 text-sm">
                {variant.glossary.map((entry) => (
                  <div key={entry.term}>
                    <dt className="font-medium">{entry.term}</dt>
                    <dd className="text-ink-muted">{entry.definition}</dd>
                  </div>
                ))}
              </dl>
            </Glass>
          ) : null}
          {variant.quiz.length ? (
            <Glass className="p-4">
              <h3 className="font-display text-xl">Comprehension</h3>
              <ol className="mt-3 space-y-3 text-sm">
                {variant.quiz.map((item, i) => (
                  <li key={item.id}>
                    <p>
                      {i + 1}. {item.prompt}
                    </p>
                    {item.choices ? (
                      <ul className="mt-1 list-disc pl-5 text-ink-muted">
                        {item.choices.map((c) => (
                          <li key={c}>{c}</li>
                        ))}
                      </ul>
                    ) : null}
                  </li>
                ))}
              </ol>
            </Glass>
          ) : null}
          {variant.validation.issues.length ? (
            <Glass className="p-4">
              <h3 className="font-display text-xl">Validator</h3>
              <ul className="mt-3 space-y-2 text-sm text-ink-muted">
                {variant.validation.issues.map((issue) => (
                  <li key={issue.code + issue.message}>
                    {issue.severity}: {issue.message}
                  </li>
                ))}
              </ul>
            </Glass>
          ) : null}
        </section>
      </div>
    </main>
  );
}

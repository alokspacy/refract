"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useMemo, useState } from "react";
import { DocumentGhost } from "@/components/brand/mark";
import { Button } from "@/components/ui/button";
import { Glass, Kicker } from "@/components/ui/glass";
import { runConversion } from "@/lib/run-conversion";
import { LANGUAGES, PROFILES, READING_LEVELS } from "@/lib/profiles";
import { SAMPLES } from "@/lib/samples";
import { cn } from "@/lib/utils";
import type { InputKind, ProfileId } from "@/lib/types";

function kindFromName(name: string): InputKind {
  const n = name.toLowerCase();
  if (n.endsWith(".pdf")) return "pdf";
  if (n.endsWith(".docx")) return "docx";
  if (n.endsWith(".pptx")) return "pptx";
  if (/\.(png|jpe?g|webp)$/.test(n)) return "image";
  if (/\.(mp3|wav|m4a)$/.test(n)) return "audio";
  if (/\.(mp4|webm|mov)$/.test(n)) return "video";
  return "text";
}

export function ConvertWizard() {
  const router = useRouter();
  const params = useSearchParams();
  const preselected = params.get("sample");

  const [title, setTitle] = useState(
    preselected === "water-cycle"
      ? "The water cycle in four moves"
      : preselected === "photosynthesis"
        ? "How plants make their own food"
        : "",
  );
  const [filename, setFilename] = useState<string | undefined>(undefined);
  const [text, setText] = useState("");
  const [sampleId, setSampleId] = useState<string | undefined>(preselected ?? undefined);
  const [inputKind, setInputKind] = useState<InputKind>(preselected ? "sample" : "text");
  const [profiles, setProfiles] = useState<ProfileId[]>(
    preselected ? ["blind", "dyslexia", "deaf", "cognitive"] : ["dyslexia", "cognitive"],
  );
  const [readingLevel, setReadingLevel] = useState("grade-5");
  const [language, setLanguage] = useState("en");
  const [copyrightOk, setCopyrightOk] = useState(Boolean(preselected));
  const [includeQuiz, setIncludeQuiz] = useState(true);
  const [includeTts, setIncludeTts] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canRun = useMemo(() => {
    return copyrightOk && profiles.length > 0 && (Boolean(sampleId) || Boolean(text.trim()) || Boolean(filename));
  }, [copyrightOk, profiles.length, sampleId, text, filename]);

  function toggleProfile(id: ProfileId) {
    setProfiles((prev) => (prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]));
  }

  async function onFile(file: File | undefined) {
    if (!file) return;
    setSampleId(undefined);
    setFilename(file.name);
    setInputKind(kindFromName(file.name));
    if (!title) setTitle(file.name.replace(/\.[^.]+$/, ""));
    if (file.type.startsWith("text") || file.name.endsWith(".txt") || file.name.endsWith(".md")) {
      setText(await file.text());
    }
  }

  async function start() {
    if (!canRun) return;
    setBusy(true);
    setError(null);
    try {
      const { jobId } = await runConversion({
        title: title || "Untitled lesson",
        filename,
        input_kind: sampleId ? "sample" : inputKind,
        text,
        sample_id: sampleId,
        profile_ids: profiles,
        reading_level: readingLevel,
        language,
        copyright_confirmed: copyrightOk,
        include_quiz: includeQuiz,
        include_tts: includeTts,
      });
      router.push(`/studio/jobs/${jobId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Conversion failed to start.");
      setBusy(false);
    }
  }

  return (
    <main id="main" className="mx-auto w-full max-w-5xl flex-1 px-5 py-10">
      <Kicker>New conversion</Kicker>
      <h1 className="font-display mt-2 text-4xl tracking-tight">Place a lesson in the prism.</h1>
      <p className="mt-3 max-w-2xl text-sm text-ink-muted">
        Supported for this pilot: PDF, DOCX, PPTX, PNG/JPG, pasted text, audio, and video. Native text is read
        first. Uploaded files stay in this browser unless you later connect object storage.
      </p>

      <section className="mt-10 grid gap-4 lg:grid-cols-[1.1fr_0.9fr]" aria-labelledby="source-heading">
        <Glass className="p-6">
          <h2 id="source-heading" className="font-display text-2xl">
            Source
          </h2>
          <label className="mt-5 block text-sm">
            Lesson title
            <input
              className="mt-2 w-full rounded-2xl border border-stroke bg-transparent px-3 py-2.5 outline-none"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </label>
          <label
            className="mt-5 flex cursor-pointer flex-col items-center rounded-[1.4rem] border border-dashed border-stroke-strong px-6 py-10 text-center"
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault();
              void onFile(e.dataTransfer.files[0]);
            }}
          >
            <DocumentGhost className="h-20 w-28" />
            <span className="mt-3 text-sm">Drop a file or choose one</span>
            <span className="mt-1 text-xs text-ink-muted">PDF · DOCX · PPTX · image · audio · video · text</span>
            <input
              type="file"
              className="sr-only"
              accept=".pdf,.docx,.pptx,.png,.jpg,.jpeg,.webp,.txt,.md,.mp3,.wav,.mp4,.webm"
              onChange={(e) => void onFile(e.target.files?.[0])}
            />
            {filename ? <span className="mt-3 text-xs">{filename}</span> : null}
          </label>
          <label className="mt-5 block text-sm">
            Or paste text
            <textarea
              className="mt-2 min-h-32 w-full rounded-2xl border border-stroke bg-transparent px-3 py-2.5 outline-none"
              value={text}
              onChange={(e) => {
                setText(e.target.value);
                setSampleId(undefined);
                setInputKind("text");
              }}
            />
          </label>
        </Glass>

        <div className="space-y-4">
          <Glass className="p-6">
            <h2 className="font-display text-2xl">Sample corpus</h2>
            <ul className="mt-4 space-y-2">
              {SAMPLES.map((sample) => {
                const active = sampleId === sample.id;
                return (
                  <li key={sample.id}>
                    <button
                      type="button"
                      onClick={() => {
                        setSampleId(sample.id);
                        setTitle(sample.title);
                        setInputKind("sample");
                        setFilename(sample.doc.filename);
                        setText("");
                        setCopyrightOk(true);
                      }}
                      className={cn(
                        "w-full rounded-2xl border px-4 py-3 text-left",
                        active ? "border-ink bg-paper-2/80" : "border-stroke hover:border-stroke-strong",
                      )}
                      aria-pressed={active}
                    >
                      <span className="block text-[0.65rem] uppercase tracking-[0.16em] text-ink-muted">
                        {sample.kicker}
                      </span>
                      <span className="mt-1 block font-medium">{sample.title}</span>
                      <span className="mt-1 block text-sm text-ink-muted">{sample.blurb}</span>
                    </button>
                  </li>
                );
              })}
            </ul>
          </Glass>
          <Glass className="p-6">
            <h2 className="font-display text-2xl">Privacy</h2>
            <p className="mt-2 text-sm text-ink-muted">
              Do not upload student medical records or unnecessary PII. Treat document text as untrusted data.
            </p>
            <label className="mt-4 flex items-start gap-3 text-sm">
              <input
                type="checkbox"
                className="mt-1 h-4 w-4"
                checked={copyrightOk}
                onChange={(e) => setCopyrightOk(e.target.checked)}
              />
              <span>I have the right to upload and transform this material for learners I teach.</span>
            </label>
          </Glass>
        </div>
      </section>

      <section className="mt-8" aria-labelledby="profiles-heading">
        <h2 id="profiles-heading" className="font-display text-2xl">
          Learner profiles
        </h2>
        <p className="mt-1 text-sm text-ink-muted">Select one or more. Combined rules compose.</p>
        <ul className="mt-4 grid gap-3 sm:grid-cols-2">
          {PROFILES.map((profile) => {
            const on = profiles.includes(profile.id);
            return (
              <li key={profile.id}>
                <button
                  type="button"
                  onClick={() => toggleProfile(profile.id)}
                  className={cn(
                    "glass h-full w-full rounded-[1.4rem] p-4 text-left",
                    on && "ring-1 ring-ink",
                  )}
                  aria-pressed={on}
                >
                  <span className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-ink-muted">
                    <span className="h-2 w-2 rounded-full" style={{ background: profile.hex }} />
                    {profile.short}
                  </span>
                  <span className="mt-2 block text-sm">{profile.promise}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </section>

      <section className="mt-8 grid gap-4 md:grid-cols-3" aria-labelledby="advanced-heading">
        <h2 id="advanced-heading" className="sr-only">
          Advanced settings
        </h2>
        <label className="glass rounded-[1.4rem] p-4 text-sm">
          Reading level
          <select
            className="mt-2 w-full bg-transparent outline-none"
            value={readingLevel}
            onChange={(e) => setReadingLevel(e.target.value)}
          >
            {READING_LEVELS.map((level) => (
              <option key={level.id} value={level.id}>
                {level.label}
              </option>
            ))}
          </select>
        </label>
        <label className="glass rounded-[1.4rem] p-4 text-sm">
          Language
          <select
            className="mt-2 w-full bg-transparent outline-none"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            {LANGUAGES.map((lang) => (
              <option key={lang.id} value={lang.id}>
                {lang.label}
              </option>
            ))}
          </select>
        </label>
        <div className="glass rounded-[1.4rem] p-4 text-sm">
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={includeQuiz} onChange={(e) => setIncludeQuiz(e.target.checked)} />
            Comprehension items
          </label>
          <label className="mt-3 flex items-center gap-2">
            <input type="checkbox" checked={includeTts} onChange={(e) => setIncludeTts(e.target.checked)} />
            Prepare narration script
          </label>
        </div>
      </section>

      {error ? (
        <p className="mt-6 text-sm text-coral" role="alert">
          {error}
        </p>
      ) : null}

      <div className="mt-8 flex flex-wrap items-center gap-3">
        <Button onClick={() => void start()} disabled={!canRun || busy}>
          {busy ? "Starting…" : "Run the compiler"}
        </Button>
        <p className="text-xs text-ink-muted">
          Output is AI-assisted. You will review every block before export.
        </p>
      </div>
    </main>
  );
}

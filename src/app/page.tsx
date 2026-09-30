import { ArrowUpRight } from "lucide-react";
import { PrismHero, SpectrumHairline } from "@/components/brand/mark";
import { SiteFooter, SiteHeader } from "@/components/site/chrome";
import { ButtonLink } from "@/components/ui/button-link";
import { Glass, Kicker } from "@/components/ui/glass";
import { PIPELINE_STAGES, PROFILES } from "@/lib/profiles";

export default function HomePage() {
  return (
    <div className="flex min-h-full flex-col">
      <SiteHeader />
      <main id="main" className="flex-1">
        <section className="mx-auto grid max-w-6xl items-center gap-10 px-5 pb-8 pt-10 lg:grid-cols-[1.05fr_0.95fr] lg:pt-16">
          <div>
            <Kicker>Accessibility compiler · not a new model</Kicker>
            <h1 className="font-display mt-5 max-w-xl text-[clamp(2.6rem,6vw,5.4rem)] leading-[0.95] tracking-tight text-ink">
              One lesson.
              <br />
              A spectrum of ways to learn.
            </h1>
            <p className="mt-6 max-w-lg text-lg leading-relaxed text-ink-muted">
              Refract takes a worksheet, slide deck, or lecture and refracts it into reviewable versions for
              blind, low-vision, deaf, dyslexic, cognitive, motor, and AAC learners — without changing the
              facts.
            </p>
            <div className="mt-8 flex flex-wrap items-center gap-3">
              <ButtonLink href="/studio/new">Start a conversion</ButtonLink>
              <ButtonLink href="/studio/new?sample=photosynthesis" variant="ghost">
                Try a sample lesson
              </ButtonLink>
            </div>
            <p className="mt-6 max-w-md text-sm text-ink-muted">
              Teachers stay in the loop. Nothing is classroom-ready until a human approves it.
            </p>
          </div>
          <Glass className="relative overflow-hidden p-4 md:p-6">
            <PrismHero className="text-ink" />
          </Glass>
        </section>

        <section className="mx-auto max-w-6xl px-5 py-16" aria-labelledby="profiles-title">
          <div className="flex items-end justify-between gap-6">
            <div>
              <Kicker>Seven recipes, one engine</Kicker>
              <h2 id="profiles-title" className="font-display mt-3 text-3xl tracking-tight md:text-4xl">
                Profiles, not diagnoses.
              </h2>
            </div>
            <ButtonLink href="/profiles" variant="ghost" className="hidden sm:inline-flex">
              All profiles
              <ArrowUpRight className="h-4 w-4" />
            </ButtonLink>
          </div>
          <ul className="mt-8 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            {PROFILES.map((profile) => (
              <li key={profile.id}>
                <Glass className="h-full p-5">
                    <span className="flex items-center gap-2 text-xs uppercase tracking-[0.18em] text-ink-muted">
                    <span className="h-2 w-2 rounded-full" style={{ background: profile.hex }} />
                    {profile.short}
                  </span>
                  <p className="mt-4 text-[1.05rem] leading-snug text-ink">{profile.promise}</p>
                </Glass>
              </li>
            ))}
          </ul>
        </section>

        <section className="mx-auto max-w-6xl px-5 py-8" aria-labelledby="pipeline-title">
          <Kicker>Predictable orchestration</Kicker>
          <h2 id="pipeline-title" className="font-display mt-3 text-3xl tracking-tight md:text-4xl">
            A compiler, not an agent.
          </h2>
          <p className="mt-4 max-w-2xl text-ink-muted">
            Native text is extracted first. OCR, vision, speech, and language models are called only when a
            recipe needs them. Every block keeps a pointer back to the source.
          </p>
          <ol className="mt-10 grid gap-3 md:grid-cols-5">
            {PIPELINE_STAGES.map((stage, i) => (
              <li key={stage.id} className="glass rounded-[1.4rem] p-4">
                <span className="font-mono text-xs text-ink-muted">0{i + 1}</span>
                <p className="mt-3 font-medium">{stage.label}</p>
                <p className="mt-1 text-sm text-ink-muted">{stage.detail}</p>
              </li>
            ))}
          </ol>
        </section>

        <section className="mx-auto max-w-6xl px-5 py-16" aria-labelledby="review-title">
          <div className="grid items-center gap-8 lg:grid-cols-2">
            <div>
              <Kicker>Human in the loop</Kicker>
              <h2 id="review-title" className="font-display mt-3 text-3xl tracking-tight md:text-4xl">
                Source on the left.
                <br />
                Accessible on the right.
              </h2>
              <p className="mt-4 text-ink-muted">
                Edit a block, regenerate it with a note, or flag an issue. Approve only when the meaning still
                holds. Export semantic HTML, captions, narration, and structured JSON.
              </p>
            </div>
            <Glass className="p-3">
              <div className="grid gap-3 sm:grid-cols-2">
                <div className="rounded-[1.2rem] border border-stroke bg-paper/40 p-4">
                  <p className="text-[0.65rem] uppercase tracking-[0.18em] text-ink-muted">Source · p.2</p>
                  <p className="mt-3 font-display text-xl leading-tight">6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂</p>
                </div>
                <div className="rounded-[1.2rem] border border-stroke bg-paper/70 p-4">
                  <p className="text-[0.65rem] uppercase tracking-[0.18em] text-ink-muted">Blind profile</p>
                  <p className="mt-3 text-sm leading-relaxed">
                    Six carbon dioxide plus six water, in the presence of light, yields glucose plus six oxygen.
                  </p>
                </div>
              </div>
              <SpectrumHairline className="my-3" />
              <p className="px-2 pb-2 text-xs text-ink-muted">Coverage 18/18 · numbers preserved · teacher review required</p>
            </Glass>
          </div>
        </section>

        <section className="mx-auto max-w-6xl px-5 pb-20" aria-labelledby="ethics-title">
          <Glass className="grid gap-8 p-8 md:grid-cols-[1fr_1fr]">
            <div>
              <Kicker>What Refract will not do</Kicker>
              <h2 id="ethics-title" className="font-display mt-3 text-3xl tracking-tight">
                No diagnosis. No silent publish.
              </h2>
            </div>
            <ul className="space-y-3 text-sm leading-relaxed text-ink-muted">
              <li>It does not infer a disability from student behavior.</li>
              <li>It does not claim “certified accessible” by AI alone.</li>
              <li>It does not follow instructions hidden inside uploaded files.</li>
              <li>It does not send student medical records to model providers.</li>
            </ul>
          </Glass>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}

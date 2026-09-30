import type { Metadata } from "next";
import { SiteFooter, SiteHeader } from "@/components/site/chrome";
import { Glass, Kicker } from "@/components/ui/glass";

export const metadata: Metadata = { title: "Accessibility" };

export default function AccessibilityPage() {
  return (
    <div className="flex min-h-full flex-col">
      <SiteHeader />
      <main id="main" className="mx-auto w-full max-w-3xl flex-1 px-5 py-16">
        <Kicker>Conformance posture</Kicker>
        <h1 className="font-display mt-4 text-4xl tracking-tight md:text-6xl">
          Built to be used with a keyboard, a reader, and a careful teacher.
        </h1>
        <div className="mt-10 space-y-4 text-ink-muted leading-relaxed">
          <p>
            Refract targets <a className="underline decoration-stroke-strong underline-offset-4" href="https://www.w3.org/TR/WCAG22/">WCAG 2.2</a> as the
            baseline for both this application and generated web content. Cognitive design draws on{" "}
            <a className="underline decoration-stroke-strong underline-offset-4" href="https://www.w3.org/WAI/cognitive/">W3C cognitive accessibility guidance</a>.
          </p>
          <p>
            Standards are not achieved by asking a model to “make it accessible.” Templates, focus, labels,
            contrast, and reflow are engineered. Generated lessons are labeled AI-assisted and remain
            teacher-reviewable.
          </p>
        </div>
        <Glass className="mt-10 p-6">
          <h2 className="font-display text-2xl">In this product</h2>
          <ul className="mt-4 space-y-2 text-sm text-ink-muted">
            <li>Skip link, visible focus, semantic headings and landmarks</li>
            <li>No color-only meaning — profiles also use names and structure</li>
            <li>Preferences: contrast, type size, dyslexia-friendly font, reduced motion</li>
            <li>Large targets in the motor and AAC previews; no timed tasks</li>
            <li>Status announced in the conversion pipeline</li>
          </ul>
        </Glass>
      </main>
      <SiteFooter />
    </div>
  );
}

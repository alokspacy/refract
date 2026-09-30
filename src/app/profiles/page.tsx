import type { Metadata } from "next";
import { SiteFooter, SiteHeader } from "@/components/site/chrome";
import { Glass, Kicker } from "@/components/ui/glass";
import { PROFILES } from "@/lib/profiles";

export const metadata: Metadata = { title: "Profiles" };

export default function ProfilesPage() {
  return (
    <div className="flex min-h-full flex-col">
      <SiteHeader />
      <main id="main" className="mx-auto w-full max-w-6xl flex-1 px-5 py-16">
        <Kicker>Configurable recipes</Kicker>
        <h1 className="font-display mt-4 max-w-3xl text-4xl tracking-tight md:text-6xl">
          A profile is a set of rules — not a person.
        </h1>
        <p className="mt-5 max-w-2xl text-lg text-ink-muted">
          Teachers select one or more profiles for the same lesson. Combined needs compose; for example, blind
          + dyslexia yields structure, descriptions, plain language, and narration.
        </p>
        <ul className="mt-12 space-y-4">
          {PROFILES.map((profile) => (
            <li key={profile.id}>
              <Glass className="p-6 md:p-8">
                <div className="flex flex-wrap items-center gap-3">
                  <span className="h-2.5 w-2.5 rounded-full" style={{ background: profile.hex }} />
                  <h2 className="font-display text-2xl md:text-3xl">{profile.name}</h2>
                </div>
                <p className="mt-3 text-ink-muted">{profile.promise}</p>
                <ul className="mt-5 grid gap-2 text-sm md:grid-cols-2">
                  {profile.transformations.map((item) => (
                    <li key={item} className="border-t border-stroke pt-2">
                      {item}
                    </li>
                  ))}
                </ul>
                <p className="mt-5 text-sm text-ink-muted">{profile.note}</p>
              </Glass>
            </li>
          ))}
        </ul>
      </main>
      <SiteFooter />
    </div>
  );
}

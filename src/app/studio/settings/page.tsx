"use client";

import { Button } from "@/components/ui/button";
import { Glass, Kicker } from "@/components/ui/glass";
import { usePrefs } from "@/hooks/use-prefs";
import { emptyState, saveStudio } from "@/lib/store";

export default function SettingsPage() {
  const { prefs, setPrefs } = usePrefs();

  return (
    <main id="main" className="mx-auto w-full max-w-3xl flex-1 px-5 py-10">
      <Kicker>Studio</Kicker>
      <h1 className="font-display mt-2 text-4xl tracking-tight">Settings</h1>
      <p className="mt-2 text-sm text-ink-muted">
        These preferences change the authoring interface. Learner previews follow the selected accessibility profile.
      </p>

      <Glass className="mt-8 space-y-6 p-6">
        <fieldset>
          <legend className="text-sm font-medium">Theme</legend>
          <div className="mt-3 flex flex-wrap gap-2">
            {(["light", "dark", "system"] as const).map((theme) => (
              <Button
                key={theme}
                variant={prefs.theme === theme ? "primary" : "ghost"}
                onClick={() => setPrefs({ theme })}
              >
                {theme}
              </Button>
            ))}
          </div>
        </fieldset>
        <fieldset>
          <legend className="text-sm font-medium">Contrast</legend>
          <div className="mt-3 flex gap-2">
            <Button variant={prefs.contrast === "normal" ? "primary" : "ghost"} onClick={() => setPrefs({ contrast: "normal" })}>
              Standard
            </Button>
            <Button variant={prefs.contrast === "high" ? "primary" : "ghost"} onClick={() => setPrefs({ contrast: "high" })}>
              High contrast
            </Button>
          </div>
        </fieldset>
        <fieldset>
          <legend className="text-sm font-medium">Type</legend>
          <div className="mt-3 flex flex-wrap gap-2">
            <Button variant={prefs.typeScale === "regular" ? "primary" : "ghost"} onClick={() => setPrefs({ typeScale: "regular" })}>
              Regular
            </Button>
            <Button variant={prefs.typeScale === "large" ? "primary" : "ghost"} onClick={() => setPrefs({ typeScale: "large" })}>
              Larger
            </Button>
            <Button
              variant={prefs.dyslexiaFont ? "primary" : "ghost"}
              onClick={() => setPrefs({ dyslexiaFont: !prefs.dyslexiaFont })}
            >
              Atkinson Hyperlegible
            </Button>
          </div>
        </fieldset>
        <label className="flex items-center gap-3 text-sm">
          <input
            type="checkbox"
            checked={prefs.reduceMotion}
            onChange={(e) => setPrefs({ reduceMotion: e.target.checked })}
          />
          Reduce motion
        </label>
      </Glass>

      <Glass className="mt-4 p-6">
        <h2 className="font-display text-2xl">This device</h2>
        <p className="mt-2 text-sm text-ink-muted">
          The pilot store is localStorage. Clearing it does not call a remote deletion API yet.
        </p>
        <Button
          className="mt-4"
          variant="danger"
          onClick={() => {
            saveStudio(emptyState());
          }}
        >
          Clear library
        </Button>
      </Glass>
    </main>
  );
}

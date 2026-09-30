"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useSyncExternalStore,
  type ReactNode,
} from "react";

export type ThemeChoice = "light" | "dark" | "system";

export interface Prefs {
  theme: ThemeChoice;
  contrast: "normal" | "high";
  typeScale: "regular" | "large";
  dyslexiaFont: boolean;
  reduceMotion: boolean;
}

const DEFAULTS: Prefs = {
  theme: "light",
  contrast: "normal",
  typeScale: "regular",
  dyslexiaFont: false,
  reduceMotion: false,
};

const KEY = "refract.prefs.v1";
const EVENT = "refract:prefs";

function readPrefs(): Prefs {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? { ...DEFAULTS, ...(JSON.parse(raw) as Prefs) } : DEFAULTS;
  } catch {
    return DEFAULTS;
  }
}

// Snapshots are compared by reference, so cache the parsed value against the
// raw string to keep useSyncExternalStore from looping.
let cachedRaw: string | null | undefined;
let cachedPrefs: Prefs = DEFAULTS;

function getSnapshot(): Prefs {
  const raw = localStorage.getItem(KEY);
  if (raw === cachedRaw) return cachedPrefs;
  cachedRaw = raw;
  cachedPrefs = readPrefs();
  return cachedPrefs;
}

function getServerSnapshot(): Prefs {
  return DEFAULTS;
}

function apply(prefs: Prefs) {
  const root = document.documentElement;
  const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const theme = prefs.theme === "system" ? (systemDark ? "dark" : "light") : prefs.theme;
  root.dataset.theme = theme;
  root.dataset.contrast = prefs.contrast;
  root.dataset.type = prefs.typeScale;
  root.dataset.dyslexia = prefs.dyslexiaFont ? "on" : "off";
  root.dataset.motion = prefs.reduceMotion ? "reduce" : "full";
}

function subscribe(onStoreChange: () => void) {
  window.addEventListener("storage", onStoreChange);
  window.addEventListener(EVENT, onStoreChange);
  return () => {
    window.removeEventListener("storage", onStoreChange);
    window.removeEventListener(EVENT, onStoreChange);
  };
}

const Ctx = createContext<{
  prefs: Prefs;
  setPrefs: (patch: Partial<Prefs>) => void;
} | null>(null);

export function PreferencesProvider({ children }: { children: ReactNode }) {
  const prefs = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);

  useEffect(() => {
    apply(prefs);
  }, [prefs]);

  const setPrefs = useCallback((patch: Partial<Prefs>) => {
    const next = { ...readPrefs(), ...patch };
    localStorage.setItem(KEY, JSON.stringify(next));
    apply(next);
    window.dispatchEvent(new Event(EVENT));
  }, []);

  const value = useMemo(() => ({ prefs, setPrefs }), [prefs, setPrefs]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function usePrefs() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("usePrefs must be used within PreferencesProvider");
  return ctx;
}

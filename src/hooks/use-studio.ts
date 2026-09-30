"use client";

import { useSyncExternalStore } from "react";
import { STUDIO_KEY, loadStudio } from "@/lib/store";
import type { StudioState } from "@/lib/types";

const EMPTY: StudioState = { documents: [], jobs: [], variants: [] };

// useSyncExternalStore compares snapshots by reference, so the parsed state is
// memoized against the raw localStorage string to avoid an infinite render loop.
let cachedRaw: string | null | undefined;
let cachedState: StudioState = EMPTY;

function getSnapshot(): StudioState {
  const raw = window.localStorage.getItem(STUDIO_KEY);
  if (raw === cachedRaw) return cachedState;
  cachedRaw = raw;
  cachedState = loadStudio();
  return cachedState;
}

function getServerSnapshot(): StudioState {
  return EMPTY;
}

function subscribe(onStoreChange: () => void) {
  window.addEventListener("refract:studio", onStoreChange);
  window.addEventListener("storage", onStoreChange);
  return () => {
    window.removeEventListener("refract:studio", onStoreChange);
    window.removeEventListener("storage", onStoreChange);
  };
}

const noopSubscribe = () => () => {};
const onClient = () => true;
const onServer = () => false;

export function useStudio(): StudioState & { ready: boolean } {
  const ready = useSyncExternalStore(noopSubscribe, onClient, onServer);
  const state = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
  return { ...state, ready };
}

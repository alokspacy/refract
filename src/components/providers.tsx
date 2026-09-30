"use client";

import { PreferencesProvider } from "@/hooks/use-prefs";

export function Providers({ children }: { children: React.ReactNode }) {
  return <PreferencesProvider>{children}</PreferencesProvider>;
}

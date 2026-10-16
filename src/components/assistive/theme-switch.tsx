"use client";

import React, { useState, useEffect } from "react";
import { getSavedTheme, saveTheme } from "@/lib/theme-store";

export function ThemeSwitch() {
  const [theme, setThemeState] = useState("default");

  useEffect(() => {
    setThemeState(getSavedTheme());
  }, []);

  const change = (newTheme: string) => {
    setThemeState(newTheme);
    saveTheme(newTheme);
    document.documentElement.dataset.theme = newTheme;
  };

  return (
    <div className="inline-flex rounded-lg bg-white/5 p-1 border border-white/10 text-xs">
      <button
        onClick={() => change("default")}
        className={`px-2.5 py-1 rounded ${theme === "default" ? "bg-accent text-black font-bold" : "text-ink-muted"}`}
      >
        Default
      </button>
      <button
        onClick={() => change("high-contrast")}
        className={`px-2.5 py-1 rounded ${theme === "high-contrast" ? "bg-accent text-black font-bold" : "text-ink-muted"}`}
      >
        High Contrast
      </button>
    </div>
  );
}

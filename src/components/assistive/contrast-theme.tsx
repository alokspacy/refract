"use client";

import React, { useState, useEffect } from "react";

export type ContrastMode = "default" | "high-contrast" | "sepia" | "dyslexia-blue" | "dark-oled";

export function useContrastTheme() {
  const [theme, setTheme] = useState<ContrastMode>("default");

  useEffect(() => {
    document.documentElement.dataset.assistiveTheme = theme;
  }, [theme]);

  return { theme, setTheme };
}

"use client";

import { useEffect } from "react";

interface ShortcutHandlers {
  onToggleSpeech?: () => void;
  onToggleBionic?: () => void;
  onToggleMask?: () => void;
  onIncreaseFont?: () => void;
  onDecreaseFont?: () => void;
}

export function useAccessibilityShortcuts(handlers: ShortcutHandlers) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Modifiers: Alt + Key for assistive actions
      if (e.altKey) {
        if (e.key === "s" || e.key === "S") {
          e.preventDefault();
          handlers.onToggleSpeech?.();
        } else if (e.key === "b" || e.key === "B") {
          e.preventDefault();
          handlers.onToggleBionic?.();
        } else if (e.key === "m" || e.key === "M") {
          e.preventDefault();
          handlers.onToggleMask?.();
        } else if (e.key === "+" || e.key === "=") {
          e.preventDefault();
          handlers.onIncreaseFont?.();
        } else if (e.key === "-") {
          e.preventDefault();
          handlers.onDecreaseFont?.();
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handlers]);
}

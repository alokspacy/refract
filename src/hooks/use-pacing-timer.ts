"use client";

import { useState, useEffect } from "react";

export function usePacingTimer(initialMinutes: number = 20) {
  const [secondsLeft, setSecondsLeft] = useState(initialMinutes * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [isBreak, setIsBreak] = useState(false);

  useEffect(() => {
    if (!isRunning) return;
    const interval = setInterval(() => {
      setSecondsLeft((prev) => {
        if (prev <= 1) {
          setIsBreak((b) => !b);
          return isBreak ? initialMinutes * 60 : 5 * 60; // 5 min break
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [isRunning, isBreak, initialMinutes]);

  const toggle = () => setIsRunning(!isRunning);
  const reset = () => {
    setIsRunning(false);
    setIsBreak(false);
    setSecondsLeft(initialMinutes * 60);
  };

  return { secondsLeft, isRunning, isBreak, toggle, reset };
}

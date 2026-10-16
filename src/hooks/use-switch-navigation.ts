"use client";

import { useState, useEffect } from "react";

export function useSwitchNavigation(totalItems: number, scanSpeedMs: number = 2000) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isScanning, setIsScanning] = useState(false);

  useEffect(() => {
    if (!isScanning || totalItems === 0) return;
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % totalItems);
    }, scanSpeedMs);
    return () => clearInterval(interval);
  }, [isScanning, totalItems, scanSpeedMs]);

  const toggleScan = () => setIsScanning((s) => !s);

  return { currentIndex, isScanning, toggleScan };
}

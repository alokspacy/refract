"use client";

import React from "react";
import { Glass } from "@/components/ui/glass";

interface SwitchToolbarProps {
  isScanning: boolean;
  onToggleScan: () => void;
  currentIndex: number;
}

export function SwitchToolbar({ isScanning, onToggleScan, currentIndex }: SwitchToolbarProps) {
  return (
    <Glass className="p-3 border border-white/10 rounded-xl space-y-1 text-xs">
      <div className="flex justify-between items-center">
        <span className="font-bold text-accent">Switch Scanning (Motor)</span>
        <button
          onClick={onToggleScan}
          className={`px-2.5 py-1 rounded text-xs font-bold ${
            isScanning ? "bg-accent text-black" : "bg-white/10"
          }`}
        >
          {isScanning ? "Auto-Scanning Active" : "Start Switch Scan"}
        </button>
      </div>
    </Glass>
  );
}

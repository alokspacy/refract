"use client";

import React from "react";
import { Glass } from "@/components/ui/glass";

interface UploadProgressProps {
  filename: string;
  percent: number;
}

export function UploadProgress({ filename, percent }: UploadProgressProps) {
  return (
    <Glass strong className="p-4 border border-white/10 rounded-xl space-y-2">
      <div className="flex justify-between items-center text-xs">
        <span className="font-bold truncate max-w-xs">{filename}</span>
        <span className="font-mono font-bold text-accent">{percent}%</span>
      </div>
      <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
        <div
          className="h-full bg-accent transition-all duration-300"
          style={{ width: `${percent}%` }}
        />
      </div>
    </Glass>
  );
}

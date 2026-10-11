"use client";

import React from "react";
import { Glass } from "@/components/ui/glass";

interface AccessibleTableProps {
  caption: string;
  headers: string[];
  rows: string[][];
}

export function AccessibleTable({ caption, headers, rows }: AccessibleTableProps) {
  return (
    <Glass strong className="p-4 rounded-xl overflow-x-auto border border-white/10 my-4">
      <table className="w-full text-left text-xs border-collapse" role="table">
        <caption className="text-left font-bold text-accent mb-2">{caption}</caption>
        <thead>
          <tr className="border-b border-white/20">
            {headers.map((h, i) => (
              <th key={i} scope="col" className="p-2 font-semibold text-ink">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, ri) => (
            <tr key={ri} className="border-b border-white/5 hover:bg-white/5">
              {r.map((cell, ci) => (
                <td key={ci} className="p-2 text-ink-muted">
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </Glass>
  );
}

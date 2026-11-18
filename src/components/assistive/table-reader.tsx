'use client';

import React, { useState } from 'react';

interface TableReaderProps {
  caption: string;
  headers: string[];
  rows: string[][];
}

export function TableReader({ caption, headers, rows }: TableReaderProps) {
  const [linearMode, setLinearMode] = useState(false);

  return (
    <div className="p-4 rounded-xl border border-border bg-card shadow-sm space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-semibold text-foreground">{caption}</span>
        <button
          type="button"
          onClick={() => setLinearMode(!linearMode)}
          className="px-2.5 py-1 rounded-lg border border-border hover:bg-muted font-medium"
        >
          {linearMode ? 'Grid View' : 'Linear Screen-Reader View'}
        </button>
      </div>

      {linearMode ? (
        <ul className="space-y-2 text-xs">
          {rows.map((r, rIdx) => (
            <li key={rIdx} className="p-2.5 rounded-lg bg-muted/50 border border-border">
              <span className="font-bold mr-1">Row {rIdx + 1}:</span>
              {r.map((cell, cIdx) => `${headers[cIdx] || 'Col'}: ${cell}`).join(' • ')}
            </li>
          ))}
        </ul>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-xs border-collapse">
            <thead>
              <tr className="border-b border-border bg-muted/40">
                {headers.map((h) => (
                  <th key={h} scope="col" className="p-2 text-left font-semibold">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {rows.map((r, rIdx) => (
                <tr key={rIdx}>
                  {r.map((cell, cIdx) => (
                    <td key={cIdx} className="p-2">
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

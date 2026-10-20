"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

interface Node {
  node_id: string;
  label: string;
  node_type: string;
  children?: Node[];
}

export function MindMapExplorer({ rootNode }: { rootNode: Node }) {
  const [expanded, setExpanded] = useState<Record<string, boolean>>({ [rootNode.node_id]: true });

  const toggle = (id: string) => {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const renderTree = (node: Node, depth = 0) => {
    const isExp = expanded[node.node_id] !== false;
    return (
      <div key={node.node_id} style={{ marginLeft: `${depth * 20}px` }} className="my-1 text-xs">
        <div
          onClick={() => toggle(node.node_id)}
          className={`p-2 rounded-lg border inline-flex items-center gap-2 cursor-pointer transition-all ${
            depth === 0
              ? "bg-accent/20 border-accent text-accent font-bold text-sm"
              : "bg-white/5 border-white/10 hover:border-white/20 text-ink"
          }`}
        >
          <span>{node.children && node.children.length > 0 ? (isExp ? "▼" : "▶") : "•"}</span>
          <span>{node.label}</span>
        </div>
        {isExp && node.children && node.children.map((c) => renderTree(c, depth + 1))}
      </div>
    );
  };

  return (
    <Glass strong className="p-5 rounded-2xl border border-white/10 space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-bold text-accent uppercase">Concept Mind Map</span>
        <span className="text-[0.68rem] text-ink-muted">Visual Hierarchy</span>
      </div>
      <div className="overflow-x-auto py-2">
        {renderTree(rootNode)}
      </div>
    </Glass>
  );
}

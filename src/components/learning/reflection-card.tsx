"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";

export function ReflectionCard() {
  const [rating, setRating] = useState(4);
  const [text, setText] = useState("");
  const [saved, setSaved] = useState(false);

  const save = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <Glass strong className="p-5 border border-white/10 rounded-2xl space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-bold text-accent uppercase">Lesson Reflection</span>
        <div className="flex gap-1 text-sm cursor-pointer">
          {[1, 2, 3, 4, 5].map((star) => (
            <span
              key={star}
              onClick={() => setRating(star)}
              className={star <= rating ? "text-amber-400" : "text-white/20"}
            >
              ★
            </span>
          ))}
        </div>
      </div>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="What was the most important idea you learned?"
        className="w-full bg-black/30 border border-white/10 rounded-xl p-2.5 text-xs text-ink focus:outline-none focus:border-accent"
        rows={3}
      />

      <div className="flex justify-end">
        <button onClick={save} className="px-3 py-1 bg-accent text-black font-bold rounded-lg text-xs">
          {saved ? "✓ Saved" : "Save Reflection"}
        </button>
      </div>
    </Glass>
  );
}

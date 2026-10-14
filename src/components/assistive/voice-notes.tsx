"use client";

import React, { useState } from "react";
import { Glass } from "@/components/ui/glass";
import { useSpeechRecognition } from "@/hooks/use-speech-recognition";

export function VoiceNotes() {
  const { transcript, isListening, toggle } = useSpeechRecognition();
  const [notes, setNotes] = useState<string[]>([]);

  const saveNote = () => {
    if (transcript.trim()) {
      setNotes((prev) => [...prev, transcript]);
    }
  };

  return (
    <Glass strong className="p-4 rounded-xl border border-white/10 space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-bold text-accent uppercase">Voice Dictation Notes</span>
        <button
          onClick={toggle}
          className={`px-3 py-1 rounded text-xs font-bold ${
            isListening ? "bg-rose-500 animate-pulse text-white" : "bg-accent text-black"
          }`}
        >
          {isListening ? "🎙 Recording..." : "🎙 Dictate"}
        </button>
      </div>

      <div className="p-2.5 bg-black/30 rounded-lg min-h-16 text-xs text-ink-muted">
        {transcript || "Speak to record notes..."}
      </div>

      {transcript && (
        <button onClick={saveNote} className="px-3 py-1 bg-white/10 rounded text-xs">
          Save Note
        </button>
      )}
    </Glass>
  );
}

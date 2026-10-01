"use client";

import React from "react";
import { FlashcardDeck, Flashcard } from "./flashcard-deck";

export function StudyModal({
  isOpen,
  onClose,
  cards
}: {
  isOpen: boolean;
  onClose: () => void;
  cards: Flashcard[];
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4 backdrop-blur-sm">
      <div className="bg-surface border border-white/20 rounded-2xl w-full max-w-lg p-6 relative shadow-2xl">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-lg font-bold">Concept Flashcards</h2>
          <button onClick={onClose} className="text-sm opacity-60 hover:opacity-100">✕</button>
        </div>
        <FlashcardDeck cards={cards} />
      </div>
    </div>
  );
}

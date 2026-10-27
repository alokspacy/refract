'use client';

import React, { useState } from 'react';

export interface Card {
  id: string;
  front: string;
  back: string;
  category?: string;
}

interface FlashcardDeckProps {
  title?: string;
  cards: Card[];
}

export function FlashcardDeck({ title = 'Study Deck', cards }: FlashcardDeckProps) {
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);

  if (!cards || cards.length === 0) {
    return (
      <div className="p-8 text-center text-muted-foreground border border-dashed rounded-xl">
        No flashcards available in this deck.
      </div>
    );
  }

  const current = cards[index];

  const handleNext = () => {
    setFlipped(false);
    setIndex((prev) => (prev + 1) % cards.length);
  };

  const handlePrev = () => {
    setFlipped(false);
    setIndex((prev) => (prev - 1 + cards.length) % cards.length);
  };

  return (
    <div className="space-y-4 max-w-lg mx-auto">
      <div className="flex justify-between items-center text-sm font-medium">
        <span>{title}</span>
        <span className="text-muted-foreground">
          {index + 1} of {cards.length}
        </span>
      </div>

      <div
        role="button"
        tabIndex={0}
        aria-label={`Flashcard: ${flipped ? 'Answer' : 'Question'}. Press Enter to flip.`}
        onClick={() => setFlipped(!flipped)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            setFlipped(!flipped);
          }
        }}
        className="min-h-[220px] p-8 rounded-2xl border border-border bg-card shadow-md flex flex-col justify-between items-center text-center cursor-pointer transition-all hover:border-primary focus:outline-none focus:ring-2 focus:ring-primary"
      >
        <span className="text-xs uppercase tracking-wider text-primary font-semibold">
          {current.category || (flipped ? 'Answer' : 'Prompt')}
        </span>

        <p className="text-lg font-medium my-auto">
          {flipped ? current.back : current.front}
        </p>

        <span className="text-xs text-muted-foreground">
          Click or press Space to {flipped ? 'see question' : 'reveal answer'}
        </span>
      </div>

      <div className="flex justify-between gap-3">
        <button
          type="button"
          onClick={handlePrev}
          className="flex-1 py-2 px-4 rounded-xl border border-border hover:bg-muted font-medium text-sm transition"
        >
          Previous
        </button>
        <button
          type="button"
          onClick={handleNext}
          className="flex-1 py-2 px-4 rounded-xl bg-primary text-primary-foreground font-medium text-sm shadow hover:opacity-90 transition"
        >
          Next Card
        </button>
      </div>
    </div>
  );
}

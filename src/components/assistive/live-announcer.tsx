"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";

interface AnnouncerContextType {
  announce: (message: string, priority?: "polite" | "assertive") => void;
}

const AnnouncerContext = createContext<AnnouncerContextType>({
  announce: () => {},
});

export function AnnouncerProvider({ children }: { children: ReactNode }) {
  const [politeMessage, setPoliteMessage] = useState("");
  const [assertiveMessage, setAssertiveMessage] = useState("");

  const announce = (message: string, priority: "polite" | "assertive" = "polite") => {
    if (priority === "assertive") {
      setAssertiveMessage(message);
    } else {
      setPoliteMessage(message);
    }
  };

  return (
    <AnnouncerContext.Provider value={{ announce }}>
      {children}
      <div className="sr-only" aria-live="polite" aria-atomic="true">
        {politeMessage}
      </div>
      <div className="sr-only" aria-live="assertive" aria-atomic="true">
        {assertiveMessage}
      </div>
    </AnnouncerContext.Provider>
  );
}

export const useAnnounce = () => useContext(AnnouncerContext);

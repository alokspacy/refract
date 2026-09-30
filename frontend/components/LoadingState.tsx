import React from "react";
import { Loader2 } from "lucide-react";

interface LoadingStateProps {
  message?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({ message = "Loading educational resources..." }) => {
  return (
    <div
      className="flex flex-col items-center justify-center p-12 text-center"
      role="status"
      aria-live="polite"
      aria-busy="true"
    >
      <Loader2 className="w-8 h-8 text-indigo-600 dark:text-indigo-400 animate-spin mb-4" aria-hidden="true" />
      <p className="text-sm font-medium text-slate-700 dark:text-slate-300">{message}</p>
      <span className="sr-only">Loading, please wait.</span>
    </div>
  );
};

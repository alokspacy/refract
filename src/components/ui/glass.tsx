import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "react";

export function Glass({
  className,
  strong,
  ...props
}: HTMLAttributes<HTMLDivElement> & { strong?: boolean }) {
  return <div className={cn(strong ? "glass-strong" : "glass", "rounded-[1.6rem]", className)} {...props} />;
}

export function Kicker({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <p className={cn("text-[0.68rem] uppercase tracking-[0.22em] text-ink-muted", className)}>
      {children}
    </p>
  );
}

import { cn } from "@/lib/utils";
import type { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "primary" | "ghost" | "quiet" | "danger";

export function Button({
  className,
  variant = "primary",
  icon,
  children,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: Variant;
  icon?: ReactNode;
}) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-full px-4 py-2.5 text-sm tracking-tight transition-colors disabled:cursor-not-allowed disabled:opacity-40",
        variant === "primary" && "bg-ink text-paper hover:opacity-90",
        variant === "ghost" && "glass text-ink hover:bg-glass-strong",
        variant === "quiet" && "text-ink-muted hover:text-ink",
        variant === "danger" && "bg-coral/15 text-coral hover:bg-coral/25",
        className,
      )}
      {...props}
    >
      {icon}
      {children}
    </button>
  );
}

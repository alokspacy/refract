import Link from "next/link";
import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

export function ButtonLink({
  href,
  children,
  className,
  variant = "primary",
}: {
  href: string;
  children: ReactNode;
  className?: string;
  variant?: "primary" | "ghost";
}) {
  return (
    <Link
      href={href}
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-full px-5 py-2.5 text-sm tracking-tight transition-colors",
        variant === "primary" && "bg-ink text-paper hover:opacity-90",
        variant === "ghost" && "glass text-ink hover:bg-glass-strong",
        className,
      )}
    >
      {children}
    </Link>
  );
}

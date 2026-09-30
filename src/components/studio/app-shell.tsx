"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  FileStack,
  Settings2,
  Sparkles,
  SunMedium,
} from "lucide-react";
import { Logo } from "@/components/brand/mark";
import { cn } from "@/lib/utils";
import { usePrefs } from "@/hooks/use-prefs";

const nav = [
  { href: "/studio", label: "Library", icon: FileStack },
  { href: "/studio/new", label: "New conversion", icon: Sparkles },
  { href: "/studio/settings", label: "Settings", icon: Settings2 },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { prefs, setPrefs } = usePrefs();

  return (
    <div className="flex min-h-svh flex-col md:h-svh md:flex-row">
      <a href="#main" className="skip-link">
        Skip to content
      </a>
      <aside className="glass-strong sticky top-0 z-30 flex items-center justify-between gap-3 border-b border-stroke px-4 py-3 md:h-svh md:w-56 md:flex-col md:items-stretch md:border-b-0 md:border-r md:py-6">
        <Logo href="/" />
        <nav aria-label="Studio" className="flex gap-1 md:mt-8 md:flex-col">
          {nav.map((item) => {
            const active =
              item.href === "/studio"
                ? pathname === "/studio"
                : pathname.startsWith(item.href);
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-2 rounded-full px-3 py-2 text-sm",
                  active ? "bg-ink text-paper" : "text-ink-muted hover:text-ink",
                )}
                aria-current={active ? "page" : undefined}
              >
                <Icon className="h-4 w-4" aria-hidden />
                <span className="hidden md:inline">{item.label}</span>
                <span className="sr-only md:hidden">{item.label}</span>
              </Link>
            );
          })}
        </nav>
        <button
          type="button"
          className="mt-auto hidden rounded-full px-3 py-2 text-left text-sm text-ink-muted hover:text-ink md:block"
          onClick={() =>
            setPrefs({ theme: prefs.theme === "dark" ? "light" : "dark" })
          }
        >
          <span className="inline-flex items-center gap-2">
            <SunMedium className="h-4 w-4" />
            {prefs.theme === "dark" ? "Light paper" : "Dark paper"}
          </span>
        </button>
      </aside>
      <div className="flex min-h-0 min-w-0 flex-1 flex-col overflow-auto">{children}</div>
    </div>
  );
}

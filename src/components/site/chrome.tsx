import { Logo } from "@/components/brand/mark";
import { ButtonLink } from "@/components/ui/button-link";
import { SpectrumHairline } from "@/components/brand/mark";

const links = [
  { href: "/how-it-works", label: "How it works" },
  { href: "/profiles", label: "Profiles" },
  { href: "/accessibility", label: "Accessibility" },
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-40">
      <a href="#main" className="skip-link">
        Skip to content
      </a>
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-6 px-5 py-4">
        <Logo />
        <nav aria-label="Primary" className="glass hidden items-center gap-1 rounded-full px-2 py-1 md:flex">
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="rounded-full px-3 py-1.5 text-sm text-ink-muted transition-colors hover:text-ink"
            >
              {link.label}
            </a>
          ))}
        </nav>
        <ButtonLink href="/studio">Open studio</ButtonLink>
      </div>
      <SpectrumHairline />
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="mt-24 border-t border-stroke">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-5 py-10 md:flex-row md:items-end md:justify-between">
        <div>
          <Logo href="/" />
          <p className="mt-3 max-w-sm text-sm text-ink-muted">
            An accessibility compiler for educational content. AI-assisted, teacher-approved — never a medical device, never a silent publish.
          </p>
        </div>
        <p className="text-xs text-ink-muted">
          WCAG 2.2 as a baseline · No diagnosis · Source meaning preserved
        </p>
      </div>
    </footer>
  );
}

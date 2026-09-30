"use client";

import Link from "next/link";
import { cn } from "@/lib/utils";

export function PrismMark({ className, title }: { className?: string; title?: string }) {
  return (
    <svg
      viewBox="0 0 48 48"
      className={cn("overflow-visible", className)}
      role={title ? "img" : "presentation"}
      aria-hidden={title ? undefined : true}
      aria-label={title}
    >
      <title>{title}</title>
      <defs>
        <linearGradient id="refract-beam" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stopColor="currentColor" stopOpacity="0" />
          <stop offset="1" stopColor="currentColor" stopOpacity="0.55" />
        </linearGradient>
      </defs>
      <path d="M2 24 H16" stroke="url(#refract-beam)" strokeWidth="1.15" fill="none" />
      <path
        d="M16.5 9.5 L39.5 24 L16.5 38.5 Z"
        fill="currentColor"
        fillOpacity="0.06"
        stroke="currentColor"
        strokeWidth="1.15"
        strokeLinejoin="round"
      />
      <path d="M22 22.5 L28.5 24 L22 25.5 Z" fill="currentColor" fillOpacity="0.12" />
      <path d="M39.5 24 L47 13" stroke="#5b4fff" strokeWidth="1.2" strokeLinecap="round" />
      <path d="M39.5 24 L47 18" stroke="#2f7ef0" strokeWidth="1.2" strokeLinecap="round" />
      <path d="M39.5 24 L47 22" stroke="#1aa89a" strokeWidth="1.2" strokeLinecap="round" />
      <path d="M39.5 24 L47 26.5" stroke="#d59a12" strokeWidth="1.2" strokeLinecap="round" />
      <path d="M39.5 24 L47 31" stroke="#e05a3c" strokeWidth="1.2" strokeLinecap="round" />
      <path d="M39.5 24 L46.2 36" stroke="#c44d8a" strokeWidth="1.2" strokeLinecap="round" />
    </svg>
  );
}

export function Logo({
  className,
  href = "/",
  wordmark = true,
}: {
  className?: string;
  href?: string;
  wordmark?: boolean;
}) {
  const inner = (
    <span className={cn("inline-flex items-center gap-2 text-ink", className)}>
      <PrismMark className="h-8 w-8" />
      {wordmark ? (
        <span className="font-display text-[1.35rem] leading-none tracking-tight">refract</span>
      ) : (
        <span className="sr-only">Refract</span>
      )}
    </span>
  );
  if (!href) return inner;
  return (
    <Link href={href} className="rounded-full">
      {inner}
    </Link>
  );
}

export function SpectrumHairline({ className }: { className?: string }) {
  return <div className={cn("hairline h-px w-full", className)} aria-hidden />;
}

export function PrismHero({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 720 420"
      className={cn("w-full overflow-visible", className)}
      role="img"
      aria-labelledby="prism-hero-title prism-hero-desc"
    >
      <title id="prism-hero-title">A glass prism splitting one lesson into a spectrum of accessible versions</title>
      <desc id="prism-hero-desc">
        A faint incoming beam enters a transparent triangular prism and fans into seven colored rays, each standing for an accessibility profile.
      </desc>
      <defs>
        <linearGradient id="hero-in" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stopColor="currentColor" stopOpacity="0" />
          <stop offset="0.7" stopColor="currentColor" stopOpacity="0.3" />
          <stop offset="1" stopColor="currentColor" stopOpacity="0.5" />
        </linearGradient>
        <linearGradient id="hero-glass" x1="0" y1="0" x2="0.7" y2="1">
          <stop offset="0" stopColor="currentColor" stopOpacity="0.09" />
          <stop offset="0.5" stopColor="currentColor" stopOpacity="0.03" />
          <stop offset="1" stopColor="currentColor" stopOpacity="0.08" />
        </linearGradient>
      </defs>

      <g opacity="0.45" stroke="currentColor" strokeWidth="0.6" fill="none">
        <rect x="40" y="150" width="86" height="112" rx="6" />
        <path d="M52 190 H114 M52 206 H104 M52 222 H110 M52 238 H96" opacity="0.5" />
        <text x="56" y="176" fontSize="9" fill="currentColor" stroke="none" opacity="0.8">
          lesson.pdf
        </text>
      </g>

      <path d="M126 210 H296" stroke="url(#hero-in)" strokeWidth="1.4" fill="none" />
      <circle cx="126" cy="210" r="2.2" fill="currentColor" opacity="0.35" />

      <path
        d="M300 62 L500 210 L300 358 Z"
        fill="url(#hero-glass)"
        stroke="currentColor"
        strokeOpacity="0.5"
        strokeWidth="1.1"
        strokeLinejoin="round"
      />
      <path d="M300 62 L344 210 L300 358" fill="none" stroke="currentColor" strokeOpacity="0.14" strokeWidth="0.8" />

      <g strokeWidth="1.3" strokeLinecap="round" fill="none">
        <path d="M500 210 L592 92" stroke="#5b4fff" />
        <path d="M500 210 L592 134" stroke="#2f7ef0" />
        <path d="M500 210 L592 174" stroke="#1aa89a" />
        <path d="M500 210 H592" stroke="#d59a12" />
        <path d="M500 210 L592 250" stroke="#e05a3c" />
        <path d="M500 210 L592 292" stroke="#c44d8a" />
        <path d="M500 210 L592 334" stroke="#8a7d6c" />
      </g>

      <g fontSize="12" fill="currentColor" opacity="0.75">
        <text x="604" y="96">Blind</text>
        <text x="604" y="138">Low vision</text>
        <text x="604" y="178">Deaf / HoH</text>
        <text x="604" y="214">Dyslexia</text>
        <text x="604" y="254">Cognitive</text>
        <text x="604" y="296">Speech / AAC</text>
        <text x="604" y="338">Motor</text>
      </g>
    </svg>
  );
}

export function DocumentGhost({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 160 120" className={cn("text-ink", className)} aria-hidden>
      <rect x="38" y="16" width="84" height="92" rx="8" fill="currentColor" fillOpacity="0.04" stroke="currentColor" strokeWidth="1" />
      <path d="M54 40 H106 M54 54 H98 M54 68 H102 M54 82 H88" stroke="currentColor" strokeOpacity="0.35" strokeWidth="1.1" />
      <circle cx="118" cy="28" r="16" fill="none" stroke="currentColor" strokeOpacity="0.35" />
      <path d="M118 20 V28 H126" stroke="currentColor" strokeOpacity="0.5" strokeWidth="1.1" fill="none" />
    </svg>
  );
}

export function LeafFigure({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 360 220" className={cn("w-full text-ink", className)} role="img" aria-label="Leaf diagram of photosynthesis inputs and outputs">
      <path d="M40 40 L70 28" stroke="#d59a12" strokeWidth="1.2" fill="none" />
      <circle cx="40" cy="40" r="16" fill="#d59a12" fillOpacity="0.12" stroke="#d59a12" />
      <text x="40" y="44" textAnchor="middle" fontSize="9" fill="currentColor">sun</text>
      <path
        d="M180 30 C250 50 280 120 180 190 C80 120 110 50 180 30 Z"
        fill="#1aa89a"
        fillOpacity="0.1"
        stroke="#1aa89a"
        strokeWidth="1.2"
      />
      <path d="M180 40 V190" stroke="#1aa89a" strokeOpacity="0.4" />
      <path d="M70 170 H150" stroke="#2f7ef0" strokeWidth="1.2" markerEnd="url(#arr)" />
      <text x="70" y="164" fontSize="10" fill="currentColor">water</text>
      <path d="M70 120 H130" stroke="#8a7d6c" strokeWidth="1.2" />
      <text x="70" y="114" fontSize="10" fill="currentColor">CO₂</text>
      <path d="M230 70 H310" stroke="#5b4fff" strokeWidth="1.2" />
      <text x="236" y="64" fontSize="10" fill="currentColor">glucose</text>
      <path d="M240 150 H310" stroke="#1aa89a" strokeWidth="1.2" />
      <text x="246" y="144" fontSize="10" fill="currentColor">oxygen</text>
    </svg>
  );
}

export function CycleFigure({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 280 220" className={cn("w-full text-ink", className)} role="img" aria-label="Water cycle in four stages">
      <circle cx="140" cy="110" r="72" fill="currentColor" fillOpacity="0.04" stroke="currentColor" strokeWidth="1" />
      <text x="140" y="42" textAnchor="middle" fontSize="11" fill="currentColor">condensation</text>
      <text x="140" y="196" textAnchor="middle" fontSize="11" fill="currentColor">collection</text>
      <text x="34" y="114" fontSize="11" fill="currentColor">evaporation</text>
      <text x="188" y="114" fontSize="11" fill="currentColor">precipitation</text>
      <path d="M140 58 A52 52 0 1 1 139.9 58" fill="none" stroke="#2f7ef0" strokeWidth="1.2" strokeDasharray="4 6" />
    </svg>
  );
}

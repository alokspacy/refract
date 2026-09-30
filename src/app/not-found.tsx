import { Logo } from "@/components/brand/mark";
import { ButtonLink } from "@/components/ui/button-link";

export default function NotFound() {
  return (
    <main className="flex min-h-svh flex-col items-center justify-center px-5 text-center">
      <Logo />
      <h1 className="font-display mt-8 text-4xl">This page did not survive refraction.</h1>
      <p className="mt-3 max-w-md text-sm text-ink-muted">
        The path you asked for is not in the spectrum. Head back to the lesson or the studio.
      </p>
      <div className="mt-8 flex gap-3">
        <ButtonLink href="/">Home</ButtonLink>
        <ButtonLink href="/studio" variant="ghost">
          Studio
        </ButtonLink>
      </div>
    </main>
  );
}

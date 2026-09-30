import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/Navbar";

export const metadata: Metadata = {
  title: "AccessLearn AI — Accessible Educational Content Engine",
  description: "AI Engine for Automatic Accessible Educational Content Conversion for Teachers and Students",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      <body className="h-full flex flex-col antialiased">
        {/* Skip Navigation Link for Accessibility */}
        <a href="#main-content" className="skip-to-content-link">
          Skip to main content
        </a>

        {/* Global Header / Navbar */}
        <Navbar />

        {/* Main Content Landmark */}
        <main id="main-content" className="flex-1 flex flex-col" tabIndex={-1}>
          {children}
        </main>

        {/* Accessible Footer */}
        <footer className="border-t border-slate-200 dark:border-slate-800 py-6 px-4 text-center text-xs text-slate-700 dark:text-slate-200 bg-white/50 dark:bg-slate-900/50">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
            <p>© {new Date().getFullYear()} AccessLearn AI — Phase 1 Foundation</p>
            <p className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block" aria-hidden="true" />
              <span>WCAG 2.1 AA Compliant Interface</span>
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}

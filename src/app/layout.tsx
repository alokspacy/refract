import type { Metadata } from "next";
import { Atkinson_Hyperlegible, Fraunces, Geist, Geist_Mono } from "next/font/google";
import { Providers } from "@/components/providers";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const fraunces = Fraunces({
  variable: "--font-fraunces",
  subsets: ["latin"],
});

const atkinson = Atkinson_Hyperlegible({
  variable: "--font-atkinson",
  subsets: ["latin"],
  weight: ["400", "700"],
});

export const metadata: Metadata = {
  title: {
    default: "Refract — one lesson, every learner",
    template: "%s · Refract",
  },
  description:
    "An accessibility compiler for teachers. Upload a lesson and review structured, simplified, described, captioned, and AAC-ready versions before anything reaches a classroom.",
  icons: { icon: "/favicon.svg" },
  openGraph: {
    title: "Refract — one lesson, every learner",
    description: "Accessibility compiler for educational content. AI-assisted. Teacher-approved.",
    type: "website",
  },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable} ${fraunces.variable} ${atkinson.variable} h-full antialiased`}
    >
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{var p=JSON.parse(localStorage.getItem("refract.prefs.v1")||"{}");var t=p.theme||"light";if(t==="system")t=matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";var r=document.documentElement;r.dataset.theme=t;if(p.contrast)r.dataset.contrast=p.contrast;if(p.typeScale)r.dataset.type=p.typeScale;r.dataset.dyslexia=p.dyslexiaFont?"on":"off";r.dataset.motion=p.reduceMotion?"reduce":"full";}catch(e){}})();`,
          }}
        />
      </head>
      <body className="min-h-full flex flex-col">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

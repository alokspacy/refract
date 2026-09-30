import { AppShell } from "@/components/studio/app-shell";
import type { Metadata } from "next";

export const metadata: Metadata = { title: "Studio" };

export default function StudioLayout({ children }: LayoutProps<"/studio">) {
  return <AppShell>{children}</AppShell>;
}

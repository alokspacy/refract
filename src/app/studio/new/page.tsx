import { Suspense } from "react";
import { ConvertWizard } from "@/components/studio/convert-wizard";

export default function NewConversionPage() {
  return (
    <Suspense fallback={<main className="px-5 py-10 text-sm text-ink-muted">Loading converter…</main>}>
      <ConvertWizard />
    </Suspense>
  );
}

"use client";

import { useParams } from "next/navigation";
import { ReviewWorkspace } from "@/components/studio/review-workspace";

export default function ReviewPage() {
  const params = useParams<{ id: string }>();
  return <ReviewWorkspace documentId={params.id} />;
}

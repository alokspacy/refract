import { generateVariant, normalizeRequest } from "@/lib/engine";
import type { ConversionRequest } from "@/lib/types";

export async function POST(request: Request) {
  const body = (await request.json()) as ConversionRequest;
  if (!body?.profile_ids?.length) {
    return Response.json({ error: "Select at least one accessibility profile." }, { status: 400 });
  }
  if (!body.copyright_confirmed) {
    return Response.json({ error: "Copyright confirmation is required." }, { status: 400 });
  }

  const document = normalizeRequest(body);
  const variants = body.profile_ids.map((profile) =>
    generateVariant(document, profile, body.reading_level || "grade-5"),
  );

  return Response.json({
    document,
    variants,
    prompt_version: variants[0]?.prompt_version,
    notice: "AI-assisted. Teacher review required before classroom use.",
  });
}

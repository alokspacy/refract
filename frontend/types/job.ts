export interface ProcessingJob {
  id: string;
  document_id: string;
  status: "QUEUED" | "PROCESSING" | "COMPLETED" | "FAILED";
  current_stage: string;
  progress: number;
  error_message?: string | null;
  created_at: string;
  updated_at: string;
}

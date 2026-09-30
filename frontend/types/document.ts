export interface Document {
  id: string;
  owner_id: string;
  original_filename: string;
  stored_filename: string;
  mime_type: string;
  file_size: number;
  storage_key: string;
  status: "UPLOADED" | "PROCESSING" | "COMPLETED" | "READY" | "FAILED";
  extraction_status: "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED";
  extraction_warnings?: string[] | null;
  extracted_at?: string | null;
  created_at: string;
  updated_at: string;
  latest_job_id?: string | null;
}

export interface DocumentListResponse {
  items: Document[];
  total: number;
}

export interface ContentBlock {
  id: string;
  type: "heading" | "paragraph" | "list" | "table" | "image" | "equation" | "media";
  source_text?: string | null;
  source_asset_id?: string | null;
  page_or_slide?: number | null;
  metadata: {
    heading_level?: number;
    bbox?: number[];
    order?: number;
    headers?: string[];
    rows?: string[][];
    row_count?: number;
    col_count?: number;
    asset_filename?: string;
    width?: number;
    height?: number;
    is_ocr?: boolean;
    ocr_confidence?: number;
    source_type?: string;
    [key: string]: any;
  };
  accessibility_annotations: Record<string, any>;
}

export interface Section {
  id: string;
  title?: string | null;
  blocks: ContentBlock[];
}

export interface ContentDocument {
  schema_version: string;
  id: string;
  title: string;
  source_language: string;
  subject?: string | null;
  grade_hint?: string | null;
  learning_objectives: string[];
  glossary: Record<string, string>;
  sections: Section[];
}

export interface DocumentPreview {
  document_id: string;
  title: string;
  original_filename: string;
  mime_type: string;
  extraction_status: string;
  extraction_warnings: string[];
  extracted_at?: string | null;
  sections: Section[];
  schema_version: string;
}

export interface LearningObjectiveItem {
  id: string;
  text: string;
  inferred: boolean;
}

export interface ConceptItem {
  id: string;
  name: string;
  description: string;
  source_block_ids: string[];
}

export interface VocabularyItem {
  term: string;
  definition: string;
  example?: string | null;
  source_block_ids: string[];
}

export interface ContentAnalysis {
  id: string;
  document_id: string;
  language: string;
  subject?: string | null;
  grade_hint?: string | null;
  complexity: string;
  learning_objectives: LearningObjectiveItem[];
  concepts: ConceptItem[];
  vocabulary: VocabularyItem[];
  extra_metadata?: Record<string, any> | null;
  created_at: string;
  updated_at: string;
}

export interface ProfileInfo {
  id: string;
  name: string;
  description: string;
  version: string;
}

export interface GeneratedBlock {
  id: string;
  variant_id: string;
  source_block_id: string;
  profile_id: string;
  content: Record<string, any>;
  status: string;
  prompt_version: string;
  model: string;
  provider: string;
  error_message?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ValidationResult {
  id: string;
  variant_id: string;
  block_id?: string | null;
  is_valid: boolean;
  grounded: boolean;
  unsupported_claims: string[];
  warnings: string[];
  errors: string[];
  created_at: string;
}

export interface GeneratedVariant {
  id: string;
  document_id: string;
  name: string;
  status: "PENDING" | "PROCESSING" | "COMPLETED" | "PARTIAL" | "FAILED";
  profile_ids: string[];
  profile_versions: Record<string, string>;
  metadata_overrides?: Record<string, any> | null;
  created_at: string;
  updated_at: string;
  blocks_count?: number;
}

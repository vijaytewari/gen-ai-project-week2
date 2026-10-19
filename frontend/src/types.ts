export type Evidence = { page: number; box: number[] };
export type Field = {
  id: string; locator: number; group: string; label: string; row: string;
  value: string; original: string; status: string; evidence: Evidence | null;
  confidence: number | null; source: string; reviewed: boolean;
  requires_review?: boolean; ocr_warning?: string;
  money_normalization?: string;
};
export type Group = { id: string; label: string; locators: number[] };
export type Sample = { id: number; name: string; variant: string; patient: string };
export type LibraryRecord = { id: string; filename: string; revision: number;
  form_type: string; field_count: number; edit_count: number; status: string };
export type Claim = {
  id: string; revision: number; filename: string; mode: string; sample: number | null;
  fields: Field[]; reviewed: string[]; acknowledgments: Record<string, string>;
  pages: { width: number; height: number; rotation: number }[];
  issues: { field_id: string; group: string; message: string }[];
  job: { status: string; error: string };
  form_type?: string; groups?: Group[];
  saved_json?: boolean;
  schema_generation?: { source: string; status: string; message: string };
  schema_validation?: { valid: boolean; errors: { field_id: string; message: string }[] };
  extraction?: { status: string; engine?: string; error?: string; warnings: string[];
    mapped_fields?: number; elapsed_ms?: number;
    pages?: { page: number; orientation: number; deskew_degrees: number; text: string }[] };
};
export type Citation = {
  field_id: string; label: string; value: string; group: string;
  evidence: Evidence | null; source: string;
};
export type Answer = {
  answer: string; abstained: boolean; mode: string; citations: Citation[];
  revision: number; backend: string; reranker: string;
  timings: Record<string, number>; chunks: Record<string, unknown>[];
};
export type Change = { field_id: string; value: string; status: string };
export type Metric = {
  name: string; strategy: string; rerank: boolean; recall: number; mrr: number;
  ndcg: number; answer_accuracy: number; latency_ms: number; recall_budget: number;
  abstention_accuracy: number; context_tokens: number;
};
export type Report = { run_id: string; backend: string; embedding: string;
  reranker: string; query_count: number; cases: number; configs: Metric[] };

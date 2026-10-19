import type { Claim, LibraryRecord, Group, Change, Answer, Report } from './types';

const BASE = import.meta.env.VITE_API_BASE_URL || '';
export const url = (path: string) => `${BASE}/api${path}`;

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url(path), options);
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(typeof error.detail === 'string' ? error.detail : `Request failed (${response.status})`);
  }
  return response.json();
}
const json = (body: unknown, method = 'POST') => ({
  method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
});
export const api = {
  library: () => request<{ records: LibraryRecord[]; groups: Group[] }>('/library'),
  open: (id: number) => request<Claim>(`/samples/${id}`, { method: 'POST' }),
  claim: (id: string) => request<Claim>(`/claims/${id}`),
  export: (id: string) => request<Claim & { audit: unknown[] }>(`/claims/${id}/export`),
  savedJSON: (id: string) => request<Claim & { audit: unknown[] }>(`/library/${id}`),
  upload: (file: File) => {
    const form = new FormData(); form.append('file', file);
    return request<Claim>('/documents', { method: 'POST', body: form });
  },
  save: (claim: Claim, changes: Change[]) => request<Claim>(`/claims/${claim.id}/fields`,
    json({ revision: claim.revision, changes }, 'PUT')),
  review: (claim: Claim, group: string, reason: string) =>
    request<Claim>(`/claims/${claim.id}/review`, json({ revision: claim.revision, group, reason })),
  index: (id: string) => request(`/claims/${id}/index`, { method: 'POST' }),
  ocr: (claim: Claim) => request<Claim>(`/claims/${claim.id}/analyze`, json({ revision: claim.revision })),
  addLine: (claim: Claim) => request<Claim>(`/claims/${claim.id}/service-lines`,
    json({ revision: claim.revision })),
  ask: (claim: Claim, query: string, strategy: string, rerank: boolean) =>
    request<Answer>(`/claims/${claim.id}/questions`, json({ query, strategy, rerank,
      revision: claim.revision })),
  reports: () => request<{ reports: Report[]; running: boolean; error: string }>('/reports'),
  benchmark: () => request('/reports/run', { method: 'POST' }),
  health: () => request<Record<string, string>>('/health'),
};

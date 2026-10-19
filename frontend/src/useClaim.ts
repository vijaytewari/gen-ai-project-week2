import { useEffect, useRef, useState } from 'react';
import { api } from './api';
import type { Claim, Change } from './types';

export function useClaim() {
  const [claim, setClaim] = useState<Claim | null>(null);
  const [changes, setChanges] = useState<Record<string, Change>>({});
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const dirty = Object.keys(changes).length > 0;
  const dirtyRef = useRef(false);
  useEffect(() => { dirtyRef.current = dirty; }, [dirty]);
  async function run<T>(action: () => Promise<T>): Promise<T | undefined> {
    setError(''); setBusy(true);
    try { return await action(); }
    catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  }
  function accept(next: Claim) {
    setClaim(next); setChanges({});
    localStorage.setItem('claimlens:last', next.id);
  }
  async function open(id: string) {
    if (dirty && !confirm('Discard unsaved field changes?')) return;
    const next = await run(() => api.claim(id)); if (next) accept(next);
  }
  async function upload(file: File) {
    if (dirty && !confirm('Discard unsaved field changes?')) return;
    const next = await run(() => api.upload(file)); if (next) accept(next);
  }
  async function save() {
    if (!claim) return;
    const next = await run(() => api.save(claim, Object.values(changes)));
    if (next) accept(next);
    return next;
  }
  async function review(group: string, reason: string) {
    if (!claim) return;
    await run(async () => {
      const current = dirty ? await api.save(claim, Object.values(changes)) : claim;
      if (dirty) accept(current);
      const next = await api.review(current, group, reason);
      accept(next);
    });
  }
  function edit(id: string, value: string, status = value ? 'present' : 'blank') {
    setChanges(previous => ({ ...previous, [id]: { field_id: id, value, status } }));
  }
  async function addLine() {
    if (!claim) return;
    await run(async () => {
      const current = dirty ? await api.save(claim, Object.values(changes)) : claim;
      if (dirty) accept(current);
      accept(await api.addLine(current));
    });
  }
  async function ocr() {
    if (!claim || dirty) { setError('Save changes before rerunning OCR.'); return; }
    const next = await run(() => api.ocr(claim)); if (next) accept(next);
  }
  useEffect(() => {
    const id = localStorage.getItem('claimlens:last');
    if (id) api.claim(id).then(accept).catch(() => localStorage.removeItem('claimlens:last'));
  }, []);
  useEffect(() => {
    if (!claim) return;
    const timer = setInterval(() => api.claim(claim.id).then(next => {
      setClaim(current => current?.id === next.id && next.revision >= current.revision
        && (!dirtyRef.current || next.revision === current.revision) ? next : current);
    }).catch(() => {}), 2500);
    return () => clearInterval(timer);
  }, [claim?.id]);
  useEffect(() => {
    const warn = (event: BeforeUnloadEvent) => { if (dirty) { event.preventDefault(); event.returnValue = ''; } };
    window.addEventListener('beforeunload', warn);
    return () => window.removeEventListener('beforeunload', warn);
  }, [dirty]);
  return { claim, changes, error, busy, dirty, run, open, upload, save, review, edit, addLine, ocr,
    reload: async () => { if (claim) { const next = await run(() => api.claim(claim.id)); if (next) accept(next); } } };
}
export type ClaimController = ReturnType<typeof useClaim>;

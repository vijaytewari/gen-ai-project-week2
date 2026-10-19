import { useEffect, useRef, useState } from 'react';
import { Download, Braces, X } from 'lucide-react';
import { api } from '../api';
import type { Claim } from '../types';

type Props = { claim: Pick<Claim, 'id'>; dirty: boolean; busy: boolean;
  save: () => Promise<Claim | undefined>; saved?: boolean };
type Snapshot = Claim & { audit: unknown[] };

function download(snapshot: Snapshot) {
  const blob = new Blob([JSON.stringify(snapshot, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `claim-${snapshot.id}-r${snapshot.revision}.json`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export function ClaimJSON({ claim, dirty, busy, save, saved = false }: Props) {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const dialog = useRef<HTMLDialogElement>(null);
  useEffect(() => { if (snapshot) dialog.current?.showModal(); }, [snapshot]);
  async function open(asDownload: boolean) {
    setLoading(true); setError('');
    try {
      const persisted = dirty ? await save() : claim;
      if (!persisted) return;
      const exported = await (saved ? api.savedJSON(persisted.id) : api.export(persisted.id));
      if (asDownload) download(exported);
      else setSnapshot(exported);
    } catch (e) { setError((e as Error).message); }
    finally { setLoading(false); }
  }
  return <>
    <button disabled={busy || loading} onClick={() => open(false)}
      title={dirty ? 'Save changes and view JSON' : 'View saved JSON'}>
      <Braces size={16} />{dirty ? 'Save & view JSON' : 'View JSON'}</button>
    <button disabled={busy || loading} onClick={() => open(true)}
      title={dirty ? 'Save changes and download JSON' : 'Download saved JSON'}>
      <Download size={16} />{dirty ? 'Save & download JSON' : 'Download JSON'}</button>
    {error && <span role="alert">{error}</span>}
    {snapshot && <dialog ref={dialog} className="json-dialog" aria-labelledby="json-title"
      onClose={() => setSnapshot(null)}>
      <header><div><h2 id="json-title">Saved claim JSON</h2>
        <p>Revision {snapshot.revision} · Field values, source evidence and audit history</p></div>
        <button aria-label="Close JSON" onClick={() => dialog.current?.close()}><X size={18} /></button></header>
      <pre tabIndex={0}>{JSON.stringify(snapshot, null, 2)}</pre>
      <footer><button onClick={() => download(snapshot)}><Download size={16} />Download JSON</button>
        <button onClick={() => dialog.current?.close()}>Close</button></footer>
    </dialog>}
  </>;
}

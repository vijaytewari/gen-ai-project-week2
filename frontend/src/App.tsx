import { useEffect, useState } from 'react';
import { AlertCircle, ArrowRight, RefreshCw } from 'lucide-react';
import { api } from './api';
import type { Group, LibraryRecord } from './types';
import { useClaim } from './useClaim';
import { Shell } from './components/Shell';
import { Library } from './components/Library';
import { Review } from './components/Review';
import { Reports } from './components/Reports';

export default function App() {
  const control = useClaim();
  const [tab, setTab] = useState('library');
  const [records, setRecords] = useState<LibraryRecord[]>([]);
  const [groups, setGroups] = useState<Group[]>([]);
  const [connection, setConnection] = useState('Connecting');
  useEffect(() => {
    api.library().then(data => { setRecords(data.records); setGroups(data.groups); })
      .catch(() => setConnection('Backend unavailable'));
    api.health().then(data => setConnection(`${data.backend} · ${data.embedding}`))
      .catch(() => setConnection('Backend unavailable'));
  }, []);
  useEffect(() => {
    if (tab !== 'library') return;
    const refresh = () => api.library().then(data => setRecords(data.records)).catch(() => {});
    refresh();
    const timer = setInterval(refresh, 4000);
    return () => clearInterval(timer);
  }, [tab, control.claim?.revision]);
  const open = async (id: string) => { await control.open(id); setTab('review'); };
  const upload = async (file: File) => { await control.upload(file); setTab('review'); };
  return <Shell tab={tab} navigate={setTab} connection={connection}>
    {control.error && <div className="error-banner" role="alert">
      <AlertCircle size={18} />{control.error}
      {control.claim && <button onClick={control.reload}><RefreshCw size={14} />Reload claim</button>}
    </div>}
    {tab === 'library' && <Library records={records} open={open} upload={upload} busy={control.busy} />}
    {tab === 'review' && (control.claim
      ? <Review control={control} groups={groups} />
      : <div className="empty-page"><h1>A clearer view of every claim.</h1>
          <p>Open a saved claim or upload a form to start reviewing.</p>
          <button className="primary" onClick={() => setTab('library')}>Open document library <ArrowRight size={16} /></button>
        </div>)}
    {tab === 'reports' && <Reports />}
  </Shell>;
}

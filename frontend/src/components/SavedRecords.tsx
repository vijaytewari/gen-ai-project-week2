import { useState } from 'react';
import { FileJson, Search } from 'lucide-react';
import type { LibraryRecord } from '../types';
import { ClaimJSON } from './ClaimJSON';

type Props = { records: LibraryRecord[]; open: (id: string) => void; busy: boolean };
export function SavedRecords({ records, open, busy }: Props) {
  const [search, setSearch] = useState('');
  const matches = records.filter(record => `${record.filename} ${record.form_type} ${record.id}`
    .toLowerCase().includes(search.toLowerCase()));
  return <section className="saved-library" aria-label="Saved claim JSON library">
    <div className="section-heading"><div><h2>Saved claim JSON <span>{records.length}</span></h2>
      <p>Reopen a claim to continue editing, or inspect and download its saved JSON.</p></div>
      <label className="search"><Search size={16} /><input aria-label="Find a saved claim"
        placeholder="Find a saved claim…" value={search} onChange={e => setSearch(e.target.value)} /></label></div>
    <div className="saved-records">{matches.map(record => <article className="saved-record" key={record.id}>
      <div className="record-info"><FileJson size={24} /><div><h3>{record.filename}</h3>
        <p>{record.form_type} · Revision {record.revision} · {record.field_count} fields · {record.edit_count} field edits</p>
        <small>{record.id} · {record.status === 'pending' ? 'OCR in progress' : 'Saved JSON'}</small></div></div>
      <div className="record-actions"><button className="primary" disabled={busy}
        onClick={() => open(record.id)} aria-label={`Open ${record.filename}`}>Open claim</button>
        <ClaimJSON claim={record} dirty={false} busy={busy} saved save={async () => undefined} /></div>
    </article>)}
    {!matches.length && <p className="table-empty">{records.length ? 'No saved claims match your search.'
      : 'No saved claims yet. Upload a form above, then save your edits to build your JSON library.'}</p>}</div>
  </section>;
}

import { useRef, useState } from 'react';
import { ArrowDownToLine, ArrowRight, Layers3, ScanLine, UploadCloud } from 'lucide-react';
import type { LibraryRecord } from '../types';
import { SavedRecords } from './SavedRecords';

type Props = { records: LibraryRecord[]; open: (id: string) => void;
  upload: (file: File) => void; busy: boolean };
export function Library({ records, open, upload, busy }: Props) {
  const input = useRef<HTMLInputElement>(null);
  const [drag, setDrag] = useState(false);
  return <div className="library page-enter">
    <div className="eyebrow"><span /> HUMAN IN THE LOOP CLAIM REVIEW</div>
    <div className="page-heading"><div><h1>Review by HITL</h1>
      <p>Upload a claim, press Analyzer, review the fields, then save JSON to your library.</p></div>
      <span className="pill"><span className="status-dot" />CMS-1450 + CMS-1500</span>
    </div>
    <section className={`upload-card ${drag ? 'dragging' : ''}`} onDragOver={event => {
      event.preventDefault(); setDrag(true);
    }} onDragLeave={() => setDrag(false)} onDrop={event => {
      event.preventDefault(); setDrag(false);
      if (!busy && event.dataTransfer.files[0]) upload(event.dataTransfer.files[0]);
    }}>
      <div className="upload-illustration"><div className="paper-back" /><div className="paper-front">
        <span /><i /><i /><i /><div /><i /><i /></div><span className="scan-badge"><ScanLine size={22} /></span></div>
      <div className="upload-copy"><span className="eyebrow">YOUR REVIEW STARTS HERE</span>
        <h2>Upload a claim for review</h2><p>Keep the source in view while you correct each section.<br />Saved edits appear in the JSON library below.</p>
        <button className="primary" disabled={busy} onClick={() => input.current?.click()}>
          <UploadCloud size={17} />{busy ? 'Opening document…' : 'Upload a claim'}<ArrowRight size={16} /></button>
        <small>PDF, PNG or JPG · Up to 20 MB · 9 pages · OCR runs only with Analyzer</small>
        <input ref={input} type="file" accept=".pdf,.png,.jpg,.jpeg" hidden aria-label="Upload claim"
          onChange={event => { const file = event.target.files?.[0]; if (file) upload(file); event.target.value = ''; }} />
      </div>
      <div className="upload-tag"><Layers3 size={14} />ORIGINAL + STRUCTURED VIEW</div>
    </section>
    <SavedRecords records={records} open={open} busy={busy} />
    <p className="library-footnote"><ArrowDownToLine size={14} />JSON includes all defined fields, original values, saved revisions and the edit history.</p>
  </div>;
}

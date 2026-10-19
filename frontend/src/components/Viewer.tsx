import { useEffect, useState } from 'react';
import { ChevronLeft, ChevronRight, ExternalLink, Minus, Plus, RotateCw } from 'lucide-react';
import type { Claim, Field } from '../types';
import { url } from '../api';
import { PdfCanvas } from './PdfCanvas';

function transform(box: number[], rotation: number) {
  const [x, y, w, h] = box;
  if (rotation === 90) return [1 - y - h, x, h, w];
  if (rotation === 180) return [1 - x - w, 1 - y - h, w, h];
  if (rotation === 270) return [y, 1 - x - w, h, w];
  return box;
}
export function Viewer({ claim, selected, focus }: { claim: Claim; selected?: Field; focus: (id: string) => void }) {
  const [page, setPage] = useState(0);
  const [zoom, setZoom] = useState(100);
  const [rotation, setRotation] = useState(0);
  useEffect(() => {
    if (selected?.evidence) setPage(selected.evidence.page);
  }, [selected?.id, claim.id]);
  const totalRotation = ((claim.pages[page]?.rotation || 0) + rotation) % 360;
  return <>
    <div className="pane-toolbar"><span className="eyebrow">SOURCE DOCUMENT</span>
      <a href={url(`/claims/${claim.id}/original`)} target="_blank" rel="noreferrer" title="Open original"><ExternalLink size={15} /></a>
    </div>
    <div className="viewer-controls"><button aria-label="Previous page" disabled={page === 0} onClick={() => setPage(page - 1)}><ChevronLeft size={16} /></button>
      <span>Page <strong>{page + 1}</strong> / {claim.pages.length}</span>
      <button aria-label="Next page" disabled={page === claim.pages.length - 1} onClick={() => setPage(page + 1)}><ChevronRight size={16} /></button>
      <div className="control-spacer" /><button aria-label="Zoom out" onClick={() => setZoom(Math.max(60, zoom - 20))}><Minus size={16} /></button>
      <span>{zoom}%</span><button aria-label="Zoom in" onClick={() => setZoom(Math.min(200, zoom + 20))}><Plus size={16} /></button>
      <button aria-label="Rotate page" onClick={() => setRotation((rotation + 90) % 360)}><RotateCw size={16} /></button>
    </div>
    <div className="document-scroll"><div className="document-paper" style={{ width: `${zoom}%` }}>
      <PdfCanvas claim={claim} page={page} rotation={rotation} />
      <div className="evidence-overlay">{claim.fields.filter(f => f.evidence?.page === page).map(field => {
        const [x, y, w, h] = transform(field.evidence!.box, totalRotation);
        return <button key={field.id} title={`FL ${field.id}: ${field.label}`} aria-label={`Source FL ${field.id}`}
          className={selected?.id === field.id ? 'evidence-region selected' : 'evidence-region'}
          onClick={() => focus(field.id)} style={{ left: `${x * 100}%`, top: `${y * 100}%`, width: `${w * 100}%`, height: `${h * 100}%` }} />;
      })}</div>
    </div></div>
    <div className="viewer-caption"><span className="highlight-key" />Select any highlighted field to inspect its structured value.</div>
  </>;
}

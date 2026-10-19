import { useEffect, useState } from 'react';
import { Check, FileText, LoaderCircle, Save, Sparkles } from 'lucide-react';
import { api } from '../api';
import type { ClaimController } from '../useClaim';
import type { Group } from '../types';
import { Viewer } from './Viewer';
import { GroupEditor } from './GroupEditor';
import { Assistant } from './Assistant';
import { SplitHandle } from './SplitHandle';
import { OCRStatus } from './OCRStatus';
import { ClaimJSON } from './ClaimJSON';

export function Review({ control, groups: defaults }: { control: ClaimController; groups: Group[] }) {
  const { claim, changes, dirty, busy, edit, save, review, run } = control;
  const [selected, setSelected] = useState('1');
  const [group, setGroup] = useState('identity');
  const [assistant, setAssistant] = useState(false);
  const [pane, setPane] = useState('fields');
  const [width, setWidth] = useState(50);
  const groups = claim?.groups || defaults;
  const extracting = claim?.extraction?.status === 'pending';
  useEffect(() => {
    if (claim && !claim.fields.some(field => field.id === selected)) {
      const first = claim.fields.find(field => field.value) || claim.fields[0];
      setSelected(first.id); setGroup(first.group);
    }
  }, [claim?.form_type, claim?.id]);
  if (!claim) return null;
  const field = claim.fields.find(f => f.id === selected);
  const focus = (id: string) => {
    setSelected(id); setGroup(claim.fields.find(f => f.id === id)?.group || 'identity');
  };
  const indexing = ['queued', 'indexing'].includes(claim.job.status);
  const ready = claim.job.status === `ready:${claim.revision}`;
  return <div className="review-page page-enter" key={claim.id}>
    <div className="review-heading"><div><span className="eyebrow">CLAIM WORKSPACE</span>
      <h1><FileText size={25} />{claim.filename}<span className="pill">Revision {claim.revision}</span></h1>
      <p>{claim.mode === 'curated' ? 'Curated extraction · synthetic layout · not for billing'
        : claim.mode === 'ocr' ? `Local OCR · ${claim.form_type} · review required` : 'Uploaded document · press Analyzer to read fields'}
        <span> · {claim.reviewed.length}/{groups.length} groups reviewed</span></p></div>
      <div className="review-actions">
        <button className="primary" disabled={busy || dirty || !!extracting || claim.mode === 'curated'}
          onClick={control.ocr}><Sparkles size={16} />{extracting ? 'Analyzing…' : 'Analyzer'}</button>
        <ClaimJSON claim={claim} dirty={dirty} busy={busy || !!extracting} save={save} />
        <button className="primary" disabled={(!dirty && !!claim.saved_json) || busy || extracting} onClick={save}>
          <Save size={16} />{busy ? 'Saving…' : dirty ? 'Save changes' : claim.saved_json ? 'Saved' : 'Save JSON'}</button></div>
    </div>
    <OCRStatus claim={claim} />
    <div className="review-status"><span><span className="status-dot" />{dirty ? 'Unsaved changes' : 'Original source preserved'}</span>
      <span>{claim.issues.length} validation issues</span>
      <button disabled={busy || indexing || dirty || extracting} onClick={() => run(() => api.index(claim.id))}>
        {indexing ? <LoaderCircle size={14} className="spin" /> : ready ? <Check size={14} /> : <Sparkles size={14} />}
        {ready ? 'Reindex revision' : indexing ? 'Indexing…' : 'Index current draft'}</button>
      <button className={assistant ? 'assistant-toggle enabled' : 'assistant-toggle'} onClick={() => setAssistant(!assistant)}><Sparkles size={14} />Ask this claim</button>
    </div>
    {claim.job.error && <div role="alert" className="error-banner">Indexing failed: {claim.job.error}</div>}
    <div className="mobile-tabs"><button onClick={() => setPane('source')}>Source document</button><button onClick={() => setPane('fields')}>Editable fields</button></div>
    <div className="review-split" style={{ gridTemplateColumns: `${width}% 6px minmax(0, 1fr)` }}>
      <div className={`source-pane ${pane === 'source' ? 'mobile-active' : ''}`}>
        <Viewer claim={claim} selected={field} focus={focus} /></div>
      <SplitHandle width={width} resize={setWidth} />
      <div className={`fields-pane ${pane === 'fields' ? 'mobile-active' : ''}`}>
        <GroupEditor claim={claim} groups={groups} group={group} setGroup={setGroup}
          changes={changes} selected={selected} focus={focus} edit={edit} review={review}
          busy={busy || !!extracting} dirty={dirty} save={save} addLine={control.addLine} />
      </div>
    </div>
    {assistant && <Assistant claim={claim} ready={ready && !dirty} close={() => setAssistant(false)} focus={focus} />}
  </div>;
}

import { useEffect, useState } from 'react';
import { Check, ChevronRight, CircleCheck, Layers3 } from 'lucide-react';
import type { Change, Claim, Group } from '../types';
import { FieldInput } from './FieldInput';
import { ServiceTable } from './ServiceTable';

type Props = {
  claim: Claim; groups: Group[]; group: string; setGroup: (id: string) => void;
  changes: Record<string, Change>; selected: string; focus: (id: string) => void;
  edit: (id: string, value: string, status?: string) => void;
  review: (group: string, reason: string) => void; busy: boolean;
  addLine: () => void;
  dirty: boolean; save: () => void;
};
export function GroupEditor(props: Props) {
  const { claim, groups, group, setGroup, changes, selected, focus, edit, review, busy } = props;
  const [menu, setMenu] = useState(false);
  const [reason, setReason] = useState('');
  const current = groups.find(g => g.id === group);
  const fields = claim.fields.filter(f => f.group === group);
  const issues = claim.issues.filter(i => i.group === group);
  const reviewed = claim.reviewed.includes(group);
  const grid = group === 'services' && claim.form_type !== 'CMS-1500';
  useEffect(() => { setReason(''); }, [group, claim.id]);
  useEffect(() => {
    if (document.activeElement?.closest('.service-section')) return;
    document.getElementById(`field-${selected}`)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }, [selected]);
  return <>
    <div className="pane-toolbar"><span className="eyebrow">STRUCTURED FIELDS</span><span className="tiny-pill">EDITABLE</span></div>
    <div className="group-select"><button onClick={() => setMenu(!menu)} aria-expanded={menu}>
      <Layers3 size={18} /><strong>{current?.label}</strong><span>{groups.findIndex(g => g.id === group) + 1} / {groups.length}</span><ChevronRight size={16} /></button>
      {menu && <div className="group-menu">{groups.map(g => <button key={g.id} onClick={() => { setGroup(g.id); setMenu(false); }}>
        {g.label}{claim.reviewed.includes(g.id) && <CircleCheck size={15} />}</button>)}</div>}
    </div>
    <div className="group-intro"><p>{fields.filter(f => f.value).length} populated fields · {issues.length} checks to review</p>
      <span>Select an FL number to locate the field on the source.</span>
      <div className="group-navigation">{['Previous', 'Next'].map((text, direction) => {
        const index = groups.findIndex(g => g.id === group) + (direction ? 1 : -1);
        return <button key={text} disabled={index < 0 || index >= groups.length}
          onClick={() => setGroup(groups[index].id)}>{text} section</button>;
      })}</div></div>
    <div className="field-scroll">
      <fieldset className="ocr-fields" disabled={busy || claim.extraction?.status === 'pending'}>
      {grid && <ServiceTable fields={fields} changes={changes} focus={focus}
        edit={edit} addLine={props.addLine} busy={busy} />}
      {grid && <h3 className="detail-title">Selected line details & claim total</h3>}
      {fields.filter(field => !grid || field.row === fields.find(f => f.id === selected)?.row || field.row === 'total').map(field => <FieldInput key={field.id} field={field} change={changes[field.id]}
        selected={selected === field.id} select={() => focus(field.id)} edit={edit}
        issue={issues.find(i => i.field_id === field.id)?.message} />)}
      {issues.length > 0 && <label className="acknowledge">Review acknowledgment
        <textarea placeholder="Explain any unresolved issues before marking reviewed…" value={reason} onChange={e => setReason(e.target.value)} />
      </label>}
      </fieldset>
    </div>
    <div className="review-group-footer"><span>{reviewed ? <><CircleCheck size={16} />Group reviewed</> : <>{fields.length} fields · {issues.length} issues</>}</span>
      <div className="footer-actions"><button disabled={busy || (!props.dirty && !!claim.saved_json)} onClick={props.save}>Save fields</button>
      <button disabled={busy || (reviewed && !props.dirty)} className="primary" onClick={() => review(group, reason)}>
        <Check size={15} />{props.dirty ? 'Save & mark reviewed' : 'Mark reviewed'}</button></div></div>
  </>;
}

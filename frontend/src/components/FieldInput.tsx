import { AlertCircle, CornerUpLeft, LocateFixed, Pencil } from 'lucide-react';
import type { Field, Change } from '../types';
import { isMoney, MoneyInput } from './MoneyInput';

type Props = { field: Field; change?: Change; selected: boolean; select: () => void;
  edit: (id: string, value: string, status?: string) => void; issue?: string };
export function FieldInput({ field, change, selected, select, edit, issue }: Props) {
  const value = change?.value ?? field.value;
  const status = change?.status ?? field.status;
  return <div id={`field-${field.id}`} className={`field-card ${selected ? 'focused' : ''} ${issue ? 'has-issue' : ''}`}>
    <div className="field-label"><label htmlFor={`value-${field.id}`}>{field.label}</label>
      <button onClick={select} title="Locate source" aria-label={`Locate FL ${field.id}`}><LocateFixed size={14} />FL {field.id}</button></div>
    {isMoney(field) ? <MoneyInput id={`value-${field.id}`} label={field.label} value={value}
      focus={select} update={next => edit(field.id, next)} /> :
    <div className="field-value"><input id={`value-${field.id}`} value={value} placeholder={status === 'unreadable' ? 'Unreadable — review source' : 'Not provided'}
      onFocus={select} onChange={event => edit(field.id, event.target.value)} /><Pencil size={13} /></div>}
    <div className="field-meta"><select aria-label={`Status FL ${field.id}`} value={status}
      onChange={event => edit(field.id, event.target.value === 'present' ? value : '', event.target.value)}>
      {['present', 'blank', 'missing', 'unreadable', 'not_applicable'].map(s => <option key={s} value={s}>{s.replace('_', ' ')}</option>)}</select>
      <span>{field.source === 'reviewer' ? 'Reviewer correction' : field.confidence === null ? 'Manual entry'
        : `${field.source === 'ocr' ? 'OCR score' : 'Simulated score'} ${field.confidence.toFixed(2)}`}</span>
      {field.evidence ? <button onClick={select}>Page {field.evidence.page + 1}</button> : <span>No source location</span>}
    </div>
    {(change || field.source === 'reviewer' || field.money_normalization) && <div className="original-value"><CornerUpLeft size={11} />Original: {field.original || '(empty)'}</div>}
    {issue && <p className="field-issue" title={issue}><AlertCircle size={12} />{selected || field.money_normalization ? issue : 'Verify against source'}</p>}
  </div>;
}

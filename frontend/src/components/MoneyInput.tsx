import type { Field } from '../types';
import { useState } from 'react';

export function isMoney(field: Field) {
  if (field.id.startsWith('1500.')) return ['1500.28', '1500.29'].includes(field.id)
    || field.id.endsWith('.charges');
  return [47, 48, 54, 55].includes(field.locator)
    || ([39, 40, 41].includes(field.locator) && field.id.endsWith('.amount'));
}

type Props = { id: string; label: string; value: string; focus: () => void;
  update: (value: string) => void };
export function MoneyInput({ id, label, value, focus, update }: Props) {
  const [dollars, fraction = '00'] = value.replace(/[$,]/g, '').split('.');
  const cents = value ? fraction : '';
  const [centDraft, setCentDraft] = useState<string | null>(null);
  function change(whole: string, part: string) {
    update(whole || part ? `${whole || '0'}.${part.padStart(2, '0')}` : '');
  }
  return <div className="money-input">
    <span aria-hidden="true">$</span>
    <label>Dollars<input id={id} aria-label={`${label} dollars`} inputMode="numeric"
      value={dollars} onFocus={focus}
      onChange={e => { if (/^\d*$/.test(e.target.value)) change(e.target.value, cents); }} /></label>
    <span>.</span>
    <label>Cents<input aria-label={`${label} cents`} inputMode="numeric" maxLength={2}
      value={centDraft ?? cents} onFocus={e => { focus(); setCentDraft(cents); e.target.select(); }}
      onBlur={() => setCentDraft(null)}
      onChange={e => { if (/^\d{0,2}$/.test(e.target.value)) {
        setCentDraft(e.target.value); change(dollars, e.target.value);
      } }} /></label>
  </div>;
}

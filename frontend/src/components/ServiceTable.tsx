import { useState } from 'react';
import { Plus } from 'lucide-react';
import type { Change, Field } from '../types';
import { MoneyInput } from './MoneyInput';

type Props = { fields: Field[]; changes: Record<string, Change>; focus: (id: string) => void;
  edit: (id: string, value: string, status?: string) => void; addLine: () => void; busy: boolean };
export function ServiceTable({ fields, changes, focus, edit, addLine, busy }: Props) {
  const [showEmpty, setShowEmpty] = useState(false);
  const all = [...new Set(fields.filter(f => f.row !== 'total' && f.status !== 'not_applicable').map(f => f.row))];
  const value = (id: string) => changes[id]?.value ?? fields.find(f => f.id === id)?.value ?? '';
  const rows = all.filter(row => showEmpty || fields.some(f => f.row === row && value(f.id)));
  return <section className="service-section">
    <div className="service-heading"><strong>Service charges</strong><span>{rows.length} lines · USD</span></div>
    <p className="service-help">Select a line to review its procedure, date and noncovered charges.</p>
    <div className="service-table-scroll"><table className="service-table">
      <thead><tr><th>Line / code</th><th>Service / units</th><th>Charge (USD)</th></tr></thead>
      <tbody>{rows.map(row => <tr key={row}>
        <td><button onClick={() => focus(`42.${row}`)}>Line {row}</button>
          <input aria-label={`Service row ${row} Code`} value={value(`42.${row}`)}
            onFocus={() => focus(`42.${row}`)} onChange={e => edit(`42.${row}`, e.target.value)} /></td>
        <td><input aria-label={`Service row ${row} Description`} value={value(`43.${row}`)}
          onFocus={() => focus(`43.${row}`)} onChange={e => edit(`43.${row}`, e.target.value)} />
          <label className="service-units">Units<input aria-label={`Service row ${row} Units`}
            value={value(`46.${row}`)} onFocus={() => focus(`46.${row}`)}
            onChange={e => edit(`46.${row}`, e.target.value)} /></label></td>
        <td><MoneyInput id={`charge-${row}`} label={`Service row ${row} Charges`}
          value={value(`47.${row}`)} focus={() => focus(`47.${row}`)}
          update={next => edit(`47.${row}`, next)} /></td>
      </tr>)}</tbody>
    </table></div>
    <div className="service-actions"><label><input type="checkbox" checked={showEmpty}
      onChange={e => setShowEmpty(e.target.checked)} />Show empty lines</label>
      <button disabled={busy} onClick={addLine}><Plus size={13} />Add service row</button></div>
  </section>;
}

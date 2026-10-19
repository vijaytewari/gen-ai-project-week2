import { useState } from 'react';
import { ArrowUpRight, LoaderCircle, Send, Sparkles, X } from 'lucide-react';
import { api } from '../api';
import type { Answer, Claim } from '../types';

type Props = { claim: Claim; ready: boolean; close: () => void; focus: (id: string) => void };
export function Assistant({ claim, ready, close, focus }: Props) {
  const [query, setQuery] = useState('');
  const [strategy, setStrategy] = useState('semantic');
  const [rerank, setRerank] = useState(true);
  const [answer, setAnswer] = useState<Answer | null>(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  async function ask(text = query) {
    if (!text.trim()) return;
    setQuery(text); setError(''); setAnswer(null); setBusy(true);
    try { setAnswer(await api.ask(claim, text, strategy, rerank)); }
    catch (error) { setError((error as Error).message); }
    finally { setBusy(false); }
  }
  return <aside className="assistant-drawer" aria-label="Claim assistant">
    <div className="assistant-heading"><span><Sparkles size={20} />Ask this claim<small>Answers connected to evidence</small></span>
      <button onClick={close} aria-label="Close assistant"><X size={18} /></button></div>
    <div className="assistant-options"><label>Chunking<select value={strategy} onChange={e => setStrategy(e.target.value)}>
      <option value="semantic">Logical semantic</option><option value="fixed">Fixed size</option></select></label>
      <label className="checkbox"><input type="checkbox" checked={rerank} onChange={e => setRerank(e.target.checked)} />Rerank</label></div>
    <div className="assistant-content">
      {!ready && <p className="inline-note">Save changes, then select “Index current draft” to ask about this revision.</p>}
      {!answer && <><div className="assistant-orb"><Sparkles size={29} /></div><h3>Start with a question.</h3>
        <p>Explore the facts in this claim, with a clear path back to the source.</p>
        {['What is the patient name?', 'What are the total charges?', 'What is the statement period?'].map(text =>
          <button className="suggestion" key={text} disabled={!ready || busy} onClick={() => ask(text)}>{text}<ArrowUpRight size={14} /></button>)}</>}
      {error && <p role="alert" className="error-banner">{error}</p>}
      {answer && <div className="answer"><span className="eyebrow">{answer.mode === 'lookup' ? 'EVIDENCE LOOKUP' : 'GROUNDED ANSWER'} · R{answer.revision}</span>
        <p>{answer.answer}</p><div className="answer-sources">{answer.citations.map(citation =>
          <button key={citation.field_id} onClick={() => focus(citation.field_id)}><span>FL {citation.field_id}</span>
            {citation.label}<small>{citation.source === 'reviewer' ? 'Reviewer value' : 'Source evidence'}</small><ArrowUpRight size={14} /></button>)}</div>
        <small>{answer.backend} · {answer.reranker} · {Object.values(answer.timings).reduce((a, b) => a + b, 0).toFixed(0)} ms</small>
        <details><summary>Inspect retrieved chunks ({answer.chunks.length})</summary><pre>{JSON.stringify(answer.chunks, null, 2)}</pre></details>
        {answer.revision !== claim.revision && <p className="inline-note">Historical answer. Ask again for the current revision.</p>}</div>}
    </div>
    <form className="ask-form" onSubmit={event => { event.preventDefault(); void ask(); }}>
      <input aria-label="Ask a question" placeholder="Ask about this claim…" value={query} onChange={e => setQuery(e.target.value)} />
      <button className="primary" disabled={!ready || busy || !query.trim()} aria-label="Send question">{busy ? <LoaderCircle className="spin" size={17} /> : <Send size={17} />}</button></form>
    <div className="assistant-disclaimer">Verify the evidence. This prototype does not determine coverage.</div>
  </aside>;
}

import { useEffect, useState } from 'react';
import { ArrowUpRight, ChartNoAxesCombined, FlaskConical, LoaderCircle, Play } from 'lucide-react';
import { api, url } from '../api';
import type { Report } from '../types';

export function Reports() {
  const [reports, setReports] = useState<Report[]>([]);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const refresh = () => api.reports().then(data => {
    setReports(data.reports); setRunning(data.running); setError(data.error);
  }).catch(error => setError(error.message));
  useEffect(() => { void refresh(); const timer = setInterval(refresh, 3000); return () => clearInterval(timer); }, []);
  async function run() {
    setError(''); setRunning(true);
    try { await api.benchmark(); }
    catch (error) { setError((error as Error).message); setRunning(false); }
  }
  const report = reports[0];
  return <div className="reports-page page-enter"><div className="eyebrow"><FlaskConical size={15} />THE RETRIEVAL LAB</div>
    <div className="page-heading"><div><h1>Evidence, measured.</h1><p>Same questions. Different boundaries. A clearer picture of retrieval.</p></div>
      <button className="primary" disabled={running} onClick={run}>{running ? <LoaderCircle size={16} className="spin" /> : <Play size={16} />}{running ? 'Running experiment…' : 'Run comparison'}</button></div>
    <div className="experiment-note"><FlaskConical size={21} /><div><strong>Four configurations. One controlled comparison.</strong>
      <p>Fixed vs. logical semantic chunks, each with and without reranking. 45 held-out questions across 9 synthetic claims.</p></div><span className="pill">SYNTHETIC BENCHMARK</span></div>
    {error && <p className="error-banner" role="alert">{error}</p>}
    {!report ? <div className="report-empty"><ChartNoAxesCombined size={45} /><h2>Let the results speak.</h2>
      <p>Run the comparison to generate measured results.<br />No placeholder scores, no assumed improvements.</p></div>
      : <><div className="report-meta"><span>RUN {report.run_id}</span><span>{report.backend} · {report.embedding} · {report.reranker}</span></div>
        <div className="metric-grid">{report.configs.map(config => <section className="metric-card" key={config.name}>
          <span className="eyebrow">{config.strategy === 'fixed' ? 'FIXED SIZE' : 'LOGICAL SEMANTIC'}</span>
          <span className="rerank-label">{config.rerank ? '+ Reranking' : 'Baseline retrieval'}</span>
          <strong>{(config.recall * 100).toFixed(1)}<small>%</small></strong><span>Evidence recall @ 5</span>
          <div className="metric-track"><span style={{ width: `${config.recall * 100}%` }} /></div>
          <dl><div><dt>MRR @ 5</dt><dd>{config.mrr.toFixed(3)}</dd></div><div><dt>nDCG @ 5</dt><dd>{config.ndcg.toFixed(3)}</dd></div>
            <div><dt>800-token recall</dt><dd>{config.recall_budget.toFixed(3)}</dd></div>
            <div><dt>Lookup accuracy</dt><dd>{(config.answer_accuracy * 100).toFixed(1)}%</dd></div>
            <div><dt>Latency</dt><dd>{config.latency_ms.toFixed(1)} ms</dd></div></dl>
        </section>)}</div>
        <div className="report-downloads">{['CHUNKING_COMPARISON.md', 'RERANKING_IMPACT.md', 'manifest.json'].map(name =>
          <a key={name} href={url(`/reports/${report.run_id}/${name}`)} target="_blank" rel="noreferrer">{name.replaceAll('_', ' ')}<ArrowUpRight size={16} /></a>)}</div>
        <p className="inline-note">Provisional, template-authored labels. Small synthetic results do not establish production accuracy. {report.reranker === 'lexical' && 'This run uses heuristic reranking; neural cross-encoder results must be measured separately.'}</p>
      </>}
  </div>;
}

import { ReactNode } from 'react';
import { Activity, ArrowUpRight, ChartNoAxesCombined, Files, Layers3, ScanLine, ShieldCheck } from 'lucide-react';

type Props = { tab: string; navigate: (tab: string) => void; connection: string; children: ReactNode };
export function Shell({ tab, navigate, connection, children }: Props) {
  const links = [
    { id: 'library', label: 'Document library', icon: Files },
    { id: 'review', label: 'Claim workspace', icon: ScanLine },
    { id: 'reports', label: 'Retrieval insights', icon: ChartNoAxesCombined },
  ];
  return <div className="app-shell">
    <aside className="sidebar">
      <a className="brand" href="#" onClick={() => navigate('library')}>
        <span className="brand-icon"><Layers3 size={23} /></span>Claims Processor
      </a>
      <div className="workspace-label">WORKSPACE <span>HITL</span></div>
      <nav aria-label="Main navigation">{links.map(({ id, label, icon: Icon }) =>
        <button key={id} className={tab === id ? 'nav-link active' : 'nav-link'} onClick={() => navigate(id)}>
          <Icon size={19} />{label}{tab === id && <span className="active-dot" />}
        </button>)}</nav>
      <div className="sidebar-note"><ShieldCheck size={22} /><h3>Built for careful review.</h3>
        <p>Every field connected to its source. Every correction preserved.</p>
        <span>SYNTHETIC DATA ONLY <ArrowUpRight size={13} /></span>
      </div>
      <div className="profile"><span className="avatar">HR</span><div>HITL reviewer<small>Institutional claims</small></div></div>
    </aside>
    <div className="main-area">
      <header className="topbar"><span>Institutional claims <span className="slash">/</span>
        <strong>{links.find(link => link.id === tab)?.label}</strong></span>
        <span className="connection"><Activity size={13} />{connection}</span>
      </header>
      <main>{children}</main>
      <footer>CLAIMS PROCESSOR <span>Human judgment. Traceable evidence.</span><span>CMS-1450 review prototype · Not for billing</span></footer>
    </div>
  </div>;
}

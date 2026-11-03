import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Building2, Lock, Plus, FolderOpen, RefreshCw } from 'lucide-react';
import { listCompanies, loginToCompany } from '../services/companies';
import './CompanySelect.css';

// ============================================================================
// Select Company for Operation
// The first screen of ARTHA: every company on this PC is listed (one folder
// each, data/COMP0001, data/COMP0002 ...). Pick one and press Enter / double
// click / "Open Company" to log in to it, or start a new company with
// "Setup New Company" (that opens the same setup wizard every company uses).
// A company protected by a PIN asks for it here.
// ============================================================================

const fmtDate = (iso) => {
  if (!iso) return '—';
  const d = new Date(iso);
  return Number.isNaN(d.getTime()) ? '—' : d.toLocaleDateString('en-IN', { day: '2-digit', month: '2-digit', year: 'numeric' });
};

export default function CompanySelect({ onOpened, onNewCompany, notice = '', suspended = false }) {
  const [state, setState] = useState({ loading: true, error: '', companies: [], dataDirectory: '' });
  const [query, setQuery] = useState('');
  const [selectedId, setSelectedId] = useState('');
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [pinFor, setPinFor] = useState(null); // { company, length } while a PIN is being asked
  const [pin, setPin] = useState('');
  const searchRef = useRef(null);
  const pinRef = useRef(null);

  const load = useCallback(async () => {
    setState((s) => ({ ...s, loading: true, error: '' }));
    try {
      const { companies, dataDirectory } = await listCompanies();
      setState({ loading: false, error: '', companies, dataDirectory });
      // Open the one used last, or the first.
      setSelectedId((cur) => (companies.some((c) => c.id === cur) ? cur : (
        [...companies].sort((a, b) => String(b.lastOpenedAt || '').localeCompare(String(a.lastOpenedAt || '')))[0]?.id || ''
      )));
    } catch {
      setState({ loading: false, error: 'Cannot reach the ARTHA server. Make sure ARTHA is running, then try again.', companies: [], dataDirectory: '' });
    }
  }, []);

  useEffect(() => { load(); }, [load]);
  useEffect(() => { searchRef.current?.focus(); }, [state.loading]);
  useEffect(() => { if (pinFor) pinRef.current?.focus(); }, [pinFor]);

  // While the "Setup New Company" wizard sits on top, this page is INERT: its
  // window-level shortcuts must not react at all. Before this, pressing Enter
  // in the wizard's company-name box also fired openSelected() and logged the
  // user straight into whichever company was highlighted underneath. When the
  // wizard closes, the search box takes focus back so Enter/arrows still work.
  useEffect(() => {
    if (!suspended) searchRef.current?.focus();
  }, [suspended]);

  const shown = useMemo(() => {
    const q = query.trim().toLowerCase();
    const all = [...state.companies].sort((a, b) => a.id.localeCompare(b.id));
    return q ? all.filter((c) => c.name.toLowerCase().includes(q) || c.id.toLowerCase().includes(q)) : all;
  }, [state.companies, query]);

  // Keep the highlighted row inside the filtered list.
  useEffect(() => {
    if (shown.length && !shown.some((c) => c.id === selectedId)) setSelectedId(shown[0].id);
  }, [shown, selectedId]);

  const selected = shown.find((c) => c.id === selectedId) || null;

  const attemptLogin = useCallback(async (company, pinValue) => {
    if (busy) return;
    setBusy(true);
    setMessage('');
    try {
      await loginToCompany(company.id, pinValue);
      await onOpened(company);
    } catch (err) {
      if (err.status === 401 && err.body?.error === 'pin-required') {
        setPinFor({ company, length: err.body.length === 8 ? 8 : 6 });
        setPin('');
      } else if (err.status === 401 && err.body?.error === 'wrong-pin') {
        setPin('');
        setMessage('Wrong PIN. Try again.');
        setTimeout(() => pinRef.current?.focus(), 0);
      } else if (err.status === 429) {
        setPin('');
        setMessage(`Too many wrong tries. Wait ${err.body?.wait || 30} seconds and try again.`);
      } else {
        setMessage('Could not open this company. Is ARTHA still running?');
      }
    } finally {
      setBusy(false);
    }
  }, [busy, onOpened]);

  const openSelected = useCallback(() => { if (selected && !pinFor) attemptLogin(selected); }, [selected, pinFor, attemptLogin]);

  // Keyboard: Up / Down move, Enter opens, Esc clears the search (or the PIN box).
  // Suspended while the Setup New Company wizard is open — otherwise a keystroke
  // meant for the wizard would open (log in to) the highlighted company.
  useEffect(() => {
    if (suspended) return undefined;
    const onKey = (e) => {
      if (e.defaultPrevented) return; // the wizard already claimed this key
      if (e.key === 'Escape') {
        if (pinFor) { setPinFor(null); setPin(''); setMessage(''); } else setQuery('');
        return;
      }
      if (pinFor || !shown.length) return;
      const i = shown.findIndex((c) => c.id === selectedId);
      if (e.key === 'ArrowDown') { e.preventDefault(); setSelectedId(shown[Math.min(shown.length - 1, i + 1)].id); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setSelectedId(shown[Math.max(0, i - 1)].id); }
      else if (e.key === 'Enter' && !(e.target instanceof HTMLButtonElement)) { e.preventDefault(); openSelected(); }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [suspended, shown, selectedId, pinFor, openSelected]);

  const onPinChange = (e) => {
    const v = e.target.value.replace(/\D/g, '').slice(0, pinFor.length);
    setPin(v);
    setMessage('');
    if (v.length === pinFor.length) attemptLogin(pinFor.company, v);
  };

  return (
    <div className="cs-page" inert={suspended || undefined}>
      <div className="cs-title">Select Company for Operation</div>
      <div className="cs-datadir">( Data Directory : {state.dataDirectory || '…'} )</div>

      <label className="cs-search">
        <span>Search Company</span>
        <input ref={searchRef} type="text" value={query} onChange={(e) => setQuery(e.target.value)}
          placeholder="Type a company name or code" aria-label="Search company" autoComplete="off" />
      </label>

      {notice && <div className="cs-notice" role="status">{notice}</div>}

      <div className="cs-table-wrap">
        <table className="cs-table">
          <thead>
            <tr>
              <th>Company Name</th>
              <th>Code</th>
              <th className="cs-hide-sm">Created</th>
              <th className="cs-hide-sm">Last Opened</th>
              <th className="cs-num">Size (MB)</th>
            </tr>
          </thead>
          <tbody>
            {shown.map((c) => (
              <tr key={c.id} className={c.id === selectedId ? 'cs-selected' : ''} aria-selected={c.id === selectedId}
                onClick={() => setSelectedId(c.id)} onDoubleClick={() => attemptLogin(c)}>
                <td>{c.name}{c.locked && <Lock size={13} className="cs-lock" aria-label="PIN protected" />}</td>
                <td>{c.id}</td>
                <td className="cs-hide-sm">{fmtDate(c.createdAt)}</td>
                <td className="cs-hide-sm">{fmtDate(c.lastOpenedAt)}</td>
                <td className="cs-num">{c.sizeMB}</td>
              </tr>
            ))}
            {Array.from({ length: Math.max(0, 8 - shown.length) }).map((_, i) => (
              <tr key={`blank-${i}`} className="cs-blank" aria-hidden="true"><td colSpan={5}>&nbsp;</td></tr>
            ))}
          </tbody>
        </table>
        {!state.loading && !state.error && !state.companies.length && (
          <div className="cs-empty">
            <Building2 size={28} />
            <p>No company yet.</p>
            <p>Click <strong>Setup New Company</strong> to create your first one.</p>
          </div>
        )}
        {!state.loading && !state.error && state.companies.length > 0 && !shown.length && (
          <div className="cs-empty"><p>No company matches “{query}”.</p></div>
        )}
        {state.error && <div className="cs-empty cs-error" role="alert"><p>{state.error}</p></div>}
      </div>

      {pinFor && (
        <form className="cs-pin" onSubmit={(e) => { e.preventDefault(); if (pin.length === pinFor.length) attemptLogin(pinFor.company, pin); }}>
          <Lock size={16} />
          <span><strong>{pinFor.company.name}</strong> is protected. Enter its {pinFor.length}-digit PIN:</span>
          <input ref={pinRef} type="password" inputMode="numeric" autoComplete="off" value={pin} onChange={onPinChange}
            maxLength={pinFor.length} placeholder={'•'.repeat(pinFor.length)} disabled={busy} aria-label={`${pinFor.length} digit PIN`} />
          <button type="button" className="cs-btn" onClick={() => { setPinFor(null); setPin(''); setMessage(''); }}>Cancel</button>
        </form>
      )}
      {message && <div className="cs-message" role="alert">{message}</div>}

      <div className="cs-actions">
        <button type="button" className="cs-btn cs-btn-primary" onClick={openSelected} disabled={!selected || busy || !!pinFor}>
          <FolderOpen size={16} /> Open Company <kbd>Enter</kbd>
        </button>
        <button type="button" className="cs-btn cs-btn-new" onClick={() => onNewCompany(state.companies)} disabled={busy || state.loading || !!state.error}>
          <Plus size={16} /> Setup New Company
        </button>
        <button type="button" className="cs-btn" onClick={load} disabled={busy} title="Reload the list">
          <RefreshCw size={16} /> Refresh
        </button>
      </div>
      <div className="cs-hint">↑ ↓ to choose · Enter or double-click to open · each company keeps its own data in its own folder</div>
    </div>
  );
}

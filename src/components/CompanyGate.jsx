import { useCallback, useEffect, useState } from 'react';
import CompanySelect from './CompanySelect';
import SetupWizard, { applyWizardChoices } from './SetupWizard';
import { getPrintSettings, savePrintSettings } from '../utils/printSettings';
import { pushAllMirroredNow } from '../utils/prefsMirror';
import {
  AUTH_REQUIRED_EVENT, getSession, createCompanyOnServer, enterCompany,
  clearCompanyScopedStorage, nextCompanyCode,
} from '../services/companies';

// ============================================================================
// Sits in front of the whole app (main.jsx):
//   no company open  -> "Select Company for Operation" page
//   Setup New Company -> the setup wizard (with a company-name step)
//   company open      -> the app, exactly as before
// Opening or creating a company ends in a page reload, so the app always
// starts clean for the company that was chosen.
// ============================================================================
export default function CompanyGate({ children }) {
  const [view, setView] = useState('loading'); // loading | select | wizard | app | error
  const [companies, setCompanies] = useState([]);
  const [notice, setNotice] = useState('');
  const [wizardError, setWizardError] = useState('');

  const check = useCallback(async () => {
    try {
      const s = await getSession();
      setView(s.authenticated ? 'app' : 'select');
    } catch {
      setView('error');
    }
  }, []);

  useEffect(() => { check(); }, [check]);

  // The server forgot this browser (ARTHA was restarted, or the company was
  // closed in another tab): back to the list.
  useEffect(() => {
    const onLost = () => {
      setNotice('Your session ended (ARTHA was restarted or the company was closed). Please open a company again.');
      setView((v) => (v === 'app' ? 'select' : v));
    };
    window.addEventListener(AUTH_REQUIRED_EVENT, onLost);
    return () => window.removeEventListener(AUTH_REQUIRED_EVENT, onLost);
  }, []);

  // Wizard finished: create the company (this also opens it), give it its first
  // settings, send them to its folder, then start the app on it.
  const createCompany = useCallback(async (name, choices) => {
    setWizardError('');
    try {
      // Nothing of a previously opened company may carry over into the new one.
      clearCompanyScopedStorage();
      const { company } = await createCompanyOnServer(name);
      if (choices) await applyWizardChoices(choices);
      else savePrintSettings({ ...getPrintSettings(), onboardingComplete: true, onboardingSkipped: false });
      await pushAllMirroredNow();
      await enterCompany(company.id, { keepStorage: true });
    } catch (err) {
      setWizardError(err?.body?.error || 'Could not create the company. Is ARTHA still running?');
    }
  }, []);

  if (view === 'loading') return null;
  if (view === 'app') return children;

  if (view === 'error') {
    return (
      <div style={{ padding: '3rem 1.5rem', textAlign: 'center', fontFamily: 'system-ui, sans-serif' }}>
        <h2>Cannot reach the ARTHA server</h2>
        <p>Make sure ARTHA is running, then try again.</p>
        <button type="button" className="btn btn-primary" onClick={() => { setView('loading'); check(); }}>Try again</button>
      </div>
    );
  }

  return (
    <>
      <CompanySelect
        notice={notice}
        suspended={view === 'wizard'}
        onOpened={(company) => enterCompany(company.id)}
        onNewCompany={(list) => { setCompanies(list); setWizardError(''); setView('wizard'); }}
      />
      {view === 'wizard' && (
        <>
          <SetupWizard mode="new-company" defaultCode={nextCompanyCode(companies)}
            onCreate={createCompany} onCancel={() => setView('select')} />
          {wizardError && (
            <div role="alert" style={{ position: 'fixed', left: '50%', bottom: 24, transform: 'translateX(-50%)', zIndex: 10000,
              background: 'var(--destructive-surface)', border: '1px solid var(--destructive-surface-border)', color: 'var(--destructive)', padding: '0.6rem 1rem', borderRadius: 8, fontSize: '0.9rem' }}>
              {wizardError}
            </div>
          )}
        </>
      )}
    </>
  );
}

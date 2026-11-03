import { useEffect, useState } from 'react';
import { LogOut } from 'lucide-react';
import { getSession, logoutAndReload } from '../services/companies';
import { confirmAction } from './ConfirmModal';
import { cn } from '@/lib/utils';
import { NAV_BTN } from './navStyles';

// Sidebar button: shows which company is open and logs out of it. Logging out
// returns to the Select Company page (to switch to another company, or to
// leave ARTHA closed). The company's data stays in its own folder.
//
// Ported to Tailwind: the label/code block used an inline flex style and a
// second line at 0.68rem with 0.75 opacity. Both are classes now, reading the
// sidebar tokens so the two lines keep their contrast in either theme.
export default function CompanySwitcher({ className = NAV_BTN }) {
  const [company, setCompany] = useState(null);
  useEffect(() => {
    let alive = true;
    getSession().then((s) => { if (alive && s.authenticated) setCompany(s.company); }).catch(() => {});
    return () => { alive = false; };
  }, []);

  const logout = async () => {
    const ok = await confirmAction({
      title: 'Close this company?',
      message: `${company ? `${company.name} (${company.id}) will be closed` : 'This company will be closed'} and you return to the company list. Anything you have typed but not saved is lost. Your saved data stays in its folder.`,
      confirmLabel: 'Log out',
      cancelLabel: 'Stay',
    });
    if (ok) logoutAndReload();
  };

  return (
    <button
      type="button"
      className={cn(NAV_BTN, className)}
      onClick={logout}
      title={company ? `Open company: ${company.name} (${company.id}). Click to log out or switch company.` : 'Log out / switch company'}
    >
      <LogOut size={18} className="shrink-0" />
      <span className="flex min-w-0 flex-col items-start leading-[1.15]">
        <span>Switch / Logout</span>
        {company && (
          <span className="max-w-[150px] truncate text-[0.68rem] opacity-75">
            {company.id} · {company.name}
          </span>
        )}
      </span>
    </button>
  );
}

import { createBrowserRouter, Navigate, Link, useLocation } from 'react-router-dom';
import App from '../App';
import { useAuth, useTheme } from './providers';
import LoginPage from '../features/auth/LoginPage';
import SetupPage from '../features/auth/SetupPage';
import PinChangePage from '../features/auth/PinChangePage';
import UnitsPage from '../features/master/UnitsPage';
import ItemsPage from '../features/master/ItemsPage';
import PartiesPage from '../features/master/PartiesPage';
import InvoiceBuilderPage from '../features/invoices/InvoiceBuilderPage';
import InvoiceListPage from '../features/invoices/InvoiceListPage';
import OrderListPage from '../features/orders/OrderListPage';
import OrderBuilderPage from '../features/orders/OrderBuilderPage';
import ReturnListPage from '../features/returns/ReturnListPage';
import ReturnBuilderPage from '../features/returns/ReturnBuilderPage';
import QuotationListPage from '../features/quotations/QuotationListPage';
import QuotationBuilderPage from '../features/quotations/QuotationBuilderPage';
import BOQListPage from '../features/boqs/BOQListPage';
import EstimateListPage from '../features/estimates/EstimateListPage';
import AdjustmentNoteListPage from '../features/adjustmentNotes/AdjustmentNoteListPage';
import AdjustmentNoteBuilderPage from '../features/adjustmentNotes/AdjustmentNoteBuilderPage';

// ── Guards ────────────────────────────────────────────────────────────────────
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" />;
  return <>{children}</>;
};

// ── Theme toggle button ───────────────────────────────────────────────────────
function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const icons = { light: '☀️', dark: '🌙', system: '💻' };
  const next: Record<string, 'dark' | 'system' | 'light'> = { light: 'dark', dark: 'system', system: 'light' };
  return (
    <button
      onClick={() => setTheme(next[theme])}
      title={`Theme: ${theme} — click to change`}
      className="text-xs px-2 py-1 rounded-md bg-muted text-muted-foreground hover:bg-accent transition-colors border border"
    >
      {icons[theme]}
    </button>
  );
}

// ── Nav link ──────────────────────────────────────────────────────────────────
function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  const loc = useLocation();
  const active = loc.pathname === to || (to !== '/' && loc.pathname.startsWith(to));
  return (
    <Link
      to={to}
      className={`block px-3 py-2 rounded-md text-sm transition-colors ${
        active ? 'bg-sidebar-accent text-sidebar-accent-foreground font-medium' : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
      }`}
    >
      {children}
    </Link>
  );
}

// ── Dashboard Shell ───────────────────────────────────────────────────────────
const DashboardShell = ({ children }: { children: React.ReactNode }) => {
  const { logout } = useAuth();

  return (
    <div className="min-h-screen flex bg-background">
      {/* Sidebar */}
      <aside className="w-64 bg-sidebar border-r border-sidebar-border hidden md:flex flex-col">
        {/* Logo */}
        <div className="h-16 flex items-center justify-between px-5 border-b border-sidebar-border flex-shrink-0">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-slate-900 dark:bg-white flex items-center justify-center">
              <span className="text-white dark:text-slate-900 text-xs font-black">A</span>
            </div>
            <span className="font-black tracking-widest text-foreground text-sm uppercase">ARTHA</span>
          </Link>
          <ThemeToggle />
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-3 space-y-0.5">
          <NavLink to="/">Dashboard</NavLink>

          <div className="pt-3 pb-1">
            <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Sales</p>
          </div>
          <NavLink to="/invoices/new">+ Create Invoice</NavLink>
          <NavLink to="/invoices">Sales Invoices</NavLink>

          <div className="pt-3 pb-1">
            <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Purchases</p>
          </div>
          <NavLink to="/purchase-bills">Purchase Bills</NavLink>

          <div className="pt-3 pb-1">
            <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Supply</p>
          </div>
          <NavLink to="/supply-in">Supply In</NavLink>
          <NavLink to="/supply-in/quotations">↳ Quotations</NavLink>
          <NavLink to="/supply-in/returns">↳ Returns</NavLink>
          <NavLink to="/supply-out">Supply Out</NavLink>
          <NavLink to="/supply-out/quotations">↳ Quotations</NavLink>
          <NavLink to="/supply-out/returns">↳ Returns</NavLink>

          <div className="pt-3 pb-1">
            <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Documents</p>
          </div>
          <NavLink to="/boqs">BOQ</NavLink>
          <NavLink to="/estimates">Estimates</NavLink>

          <div className="pt-3 pb-1">
            <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Accounting</p>
          </div>
          <NavLink to="/credit-notes">Credit Notes</NavLink>
          <NavLink to="/debit-notes">Debit Notes</NavLink>

          <div className="pt-3 pb-1">
            <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Master</p>
          </div>
          <NavLink to="/parties">Customers & Vendors</NavLink>
          <NavLink to="/items">Items & Products</NavLink>
          <NavLink to="/units">Units</NavLink>
        </nav>

        {/* Footer */}
        <div className="p-3 border-t border-sidebar-border space-y-1 flex-shrink-0">
          <NavLink to="/pin-change">🔐 Security PIN</NavLink>
          <button
            onClick={logout}
            className="w-full text-left block px-3 py-2 rounded-md text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
          >
            ← Logout
          </button>
        </div>
      </aside>

      {/* Main area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile header */}
        <header className="h-14 bg-sidebar border-b border-sidebar-border flex items-center justify-between px-4 md:hidden">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-slate-900 dark:bg-white flex items-center justify-center">
              <span className="text-white dark:text-slate-900 text-xs font-black">A</span>
            </div>
            <span className="font-black tracking-widest text-foreground text-sm uppercase">ARTHA</span>
          </Link>
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <button
              onClick={logout}
              className="text-sm text-red-500 font-medium px-3 py-1.5 rounded-md hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
            >
              Logout
            </button>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 p-4 md:p-6 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

// ── Helpers for themed page elements ─────────────────────────────────────────
// Re-exported for use in page components
export { DashboardShell };

// ── Router ────────────────────────────────────────────────────────────────────
const wrap = (element: React.ReactNode) => (
  <ProtectedRoute>
    <DashboardShell>{element}</DashboardShell>
  </ProtectedRoute>
);

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: wrap(
          <div className="bg-card rounded-xl shadow-sm border border p-6">
            <h1 className="text-2xl font-bold text-foreground mb-2">Welcome to ARTHA</h1>
            <p className="text-muted-foreground mb-6">Your secure GST billing dashboard. Choose a module from the sidebar.</p>
            <div className="flex flex-wrap gap-3">
              <Link to="/invoices/new" className="px-4 py-2 bg-slate-900 dark:bg-white text-white dark:text-slate-900 rounded-lg font-medium text-sm hover:opacity-90 transition-opacity">
                Create Invoice
              </Link>
              <Link to="/invoices" className="px-4 py-2 bg-muted text-foreground rounded-lg font-medium text-sm border border hover:bg-accent transition-colors">
                View Invoices
              </Link>
            </div>
          </div>
        ),
      },
      { path: 'invoices/new',              element: wrap(<InvoiceBuilderPage />) },
      { path: 'invoices',                  element: wrap(<InvoiceListPage />) },
      { path: 'purchase-bills',            element: wrap(<InvoiceListPage />) },
      { path: 'supply-in',                 element: wrap(<OrderListPage />) },
      { path: 'supply-in/quotations',      element: wrap(<QuotationListPage />) },
      { path: 'supply-in/quotations/new',  element: wrap(<QuotationBuilderPage />) },
      { path: 'supply-in/returns',         element: wrap(<ReturnListPage />) },
      { path: 'supply-in/returns/new',     element: wrap(<ReturnBuilderPage />) },
      { path: 'supply-in/new',             element: wrap(<OrderBuilderPage />) },
      { path: 'supply-out',                element: wrap(<OrderListPage />) },
      { path: 'supply-out/quotations',     element: wrap(<QuotationListPage />) },
      { path: 'supply-out/quotations/new', element: wrap(<QuotationBuilderPage />) },
      { path: 'supply-out/returns',        element: wrap(<ReturnListPage />) },
      { path: 'supply-out/returns/new',    element: wrap(<ReturnBuilderPage />) },
      { path: 'supply-out/new',            element: wrap(<OrderBuilderPage />) },
      { path: 'boqs',                      element: wrap(<BOQListPage />) },
      { path: 'estimates',                 element: wrap(<EstimateListPage />) },
      { path: 'credit-notes',              element: wrap(<AdjustmentNoteListPage noteType="CREDIT_NOTE" />) },
      { path: 'credit-notes/new',          element: wrap(<AdjustmentNoteBuilderPage noteType="CREDIT_NOTE" />) },
      { path: 'debit-notes',               element: wrap(<AdjustmentNoteListPage noteType="DEBIT_NOTE" />) },
      { path: 'debit-notes/new',           element: wrap(<AdjustmentNoteBuilderPage noteType="DEBIT_NOTE" />) },
      { path: 'parties',                   element: wrap(<PartiesPage />) },
      { path: 'items',                     element: wrap(<ItemsPage />) },
      { path: 'units',                     element: wrap(<UnitsPage />) },
      { path: 'pin-change',                element: wrap(<PinChangePage />) },
      { path: 'login',                     element: <LoginPage /> },
      { path: 'setup',                     element: <SetupPage /> },
    ],
  },
]);

import { createBrowserRouter, Navigate, Link } from 'react-router-dom';
import App from '../App';
import { useAuth } from './providers';
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

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  if (!isAuthenticated) return <Navigate to="/login" />;
  
  return <>{children}</>;
};

const DashboardShell = ({ children }: { children: React.ReactNode }) => {
  const { logout } = useAuth();
  return (
    <div className="min-h-screen flex bg-gray-50">
      <div className="w-64 bg-white border-r hidden md:block">
        <div className="h-16 flex items-center px-6 font-bold text-xl text-primary-600 border-b">
          Artha Billing
        </div>
        <nav className="p-4 space-y-2">
          <Link to="/" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">Dashboard</Link>
          <Link to="/invoices/new" className="block px-4 py-2 text-blue-700 hover:bg-blue-50 font-medium rounded-md bg-blue-50">+ Create Invoice</Link>
          <Link to="/invoices" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">Sales Invoices</Link>
          <Link to="/purchase-bills" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">Purchase Bills</Link>
          <Link to="/supply-in" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">Supply In</Link>
          <Link to="/supply-in/quotations" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md pl-8">↳ Quotations</Link>
          <Link to="/supply-in/returns" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md pl-8">↳ Returns</Link>
          <Link to="/supply-out" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">Supply Out</Link>
          <Link to="/supply-out/quotations" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md pl-8">↳ Quotations</Link>
          <Link to="/supply-out/returns" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md pl-8">↳ Returns</Link>
          <Link to="/boqs" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">BOQ</Link>
          <Link to="/estimates" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">Estimates</Link>
          <Link to="/parties" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">Customers & Vendors</Link>
          <Link to="/items" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">Items & Products</Link>
          <Link to="/units" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">Units</Link>
          <Link to="/pin-change" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">Security PIN</Link>
          <button onClick={logout} className="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50 rounded-md">Logout</button>
        </nav>
      </div>
      <div className="flex-1">
        <header className="h-16 bg-white border-b flex items-center px-6 md:hidden justify-between">
          <span className="font-bold text-xl text-primary-600">Artha</span>
          <button onClick={logout} className="text-sm text-red-600 font-medium">Logout</button>
        </header>
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                <h1 className="text-2xl font-bold mb-4">Welcome to Artha</h1>
                <p className="text-gray-600 mb-6">This is your secure billing dashboard. Choose a module from the sidebar to begin.</p>
                <div className="flex space-x-4">
                  <Link to="/invoices/new" className="px-4 py-2 bg-primary-600 text-white rounded-md font-medium">Create Invoice</Link>
                  <Link to="/invoices" className="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md font-medium hover:bg-gray-50">View Invoices</Link>
                </div>
              </div>
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'invoices/new',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <InvoiceBuilderPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'invoices',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <InvoiceListPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'purchase-bills',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <InvoiceListPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'supply-in',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <OrderListPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'supply-in/quotations',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <QuotationListPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'supply-in/quotations/new',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <QuotationBuilderPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'supply-in/returns',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <ReturnListPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'supply-in/returns/new',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <ReturnBuilderPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'supply-in/new',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <OrderBuilderPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'supply-out',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <OrderListPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'supply-out/quotations',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <QuotationListPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'supply-out/quotations/new',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <QuotationBuilderPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'supply-out/returns',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <ReturnListPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'supply-out/returns/new',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <ReturnBuilderPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'boqs',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <BOQListPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'estimates',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <EstimateListPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'supply-out/new',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <OrderBuilderPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'parties',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <PartiesPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'items',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <ItemsPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'units',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <UnitsPage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'pin-change',
        element: (
          <ProtectedRoute>
            <DashboardShell>
              <PinChangePage />
            </DashboardShell>
          </ProtectedRoute>
        ),
      },
      {
        path: 'login',
        element: <LoginPage />,
      },
      {
        path: 'setup',
        element: <SetupPage />,
      }
    ],
  },
]);

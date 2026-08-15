import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { invoicesApi } from '../../api/invoices';
import { Button } from '../../components/ui/button';

export default function InvoiceDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [activeTab, setActiveTab] = useState('overview');

  const { data: invoice, isLoading } = useQuery({
    queryKey: ['invoice', id],
    queryFn: async () => {
      // Replace with a dedicated GET endpoint for a single invoice in the future.
      const res = await invoicesApi.getAll('SALES');
      return res.items.find((i: any) => i.id === id) || null;
    }
  });

  if (isLoading) return <div>Loading...</div>;
  if (!invoice) return <div>Invoice not found.</div>;

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'items', label: 'Items' },
    { id: 'payments', label: 'Payments' },
    { id: 'returns', label: 'Returns' },
    { id: 'credit_notes', label: 'Credit Notes' },
    { id: 'debit_notes', label: 'Debit Notes' },
    { id: 'documents', label: 'Documents' },
    { id: 'timeline', label: 'Timeline' },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-6 mt-4">
      <div className="flex justify-between items-start">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold">{invoice.invoice_number}</h1>
            <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-bold">
              {invoice.invoice_status}
            </span>
          </div>
          <p className="text-muted-foreground mt-1">{invoice.customer_name_snapshot} • {invoice.invoice_date}</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Payment</Button>
          <Button variant="outline">Credit Note</Button>
          <Button variant="outline" onClick={() => invoicesApi.getPdf(invoice.id)}>Download PDF</Button>
        </div>
      </div>

      <div className="border-b">
        <nav className="flex space-x-8 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap transition-colors
                ${activeTab === tab.id 
                  ? 'border-primary text-primary' 
                  : 'border-transparent text-muted-foreground hover:text-foreground hover:border-muted'
                }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      <div className="pt-4">
        {activeTab === 'overview' && (
          <div className="grid grid-cols-3 gap-6">
            <div className="bg-card border p-4 rounded-lg">
              <p className="text-sm text-muted-foreground mb-1">Invoice Amount</p>
              <p className="text-2xl font-bold">₹{invoice.grand_total.toFixed(2)}</p>
            </div>
            <div className="bg-card border p-4 rounded-lg">
              <p className="text-sm text-muted-foreground mb-1">Outstanding</p>
              <p className="text-2xl font-bold text-red-500">₹{invoice.grand_total.toFixed(2)}</p>
            </div>
            <div className="bg-card border p-4 rounded-lg">
              <p className="text-sm text-muted-foreground mb-1">Status</p>
              <p className="text-xl font-medium">{invoice.payment_status || 'UNPAID'}</p>
            </div>
          </div>
        )}

        {activeTab === 'documents' && (
          <div className="p-6 bg-card border rounded-lg">
            <h3 className="font-bold mb-6">DOCUMENT HISTORY</h3>
            <div className="flex flex-col items-center space-y-4">
              <div className="w-64 p-4 border rounded shadow-sm text-center">
                <p className="text-xs text-muted-foreground font-bold uppercase">Supply Out</p>
                <p className="font-medium">SO-000083</p>
              </div>
              <div className="h-6 w-px bg-border"></div>
              <div className="w-64 p-4 border-2 border-primary rounded shadow-md text-center bg-primary/5">
                <p className="text-xs text-primary font-bold uppercase">Invoice</p>
                <p className="font-bold">{invoice.invoice_number}</p>
              </div>
              <div className="h-6 w-px bg-border"></div>
              <div className="grid grid-cols-2 gap-8 relative">
                <div className="w-48 p-4 border rounded shadow-sm text-center">
                  <p className="text-xs text-muted-foreground font-bold uppercase">Payment</p>
                  <p className="font-medium text-green-600">PAY-000315</p>
                </div>
                <div className="w-48 p-4 border rounded shadow-sm text-center">
                  <p className="text-xs text-muted-foreground font-bold uppercase">Credit Note</p>
                  <p className="font-medium text-orange-600">CN-000025</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="space-y-4">
             <div className="flex gap-4">
               <div className="w-24 text-sm text-muted-foreground mt-1">Today 10:00</div>
               <div className="border-l-2 pl-4 pb-6 border-border">
                 <p className="font-medium">Invoice Finalized</p>
                 <p className="text-sm text-muted-foreground">Invoice number {invoice.invoice_number} was assigned.</p>
               </div>
             </div>
             <div className="flex gap-4">
               <div className="w-24 text-sm text-muted-foreground mt-1">Yesterday</div>
               <div className="border-l-2 pl-4 pb-6 border-transparent">
                 <p className="font-medium">Invoice Draft Created</p>
                 <p className="text-sm text-muted-foreground">Draft was created.</p>
               </div>
             </div>
          </div>
        )}
      </div>
    </div>
  );
}

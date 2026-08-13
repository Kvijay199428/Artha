import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useLocation, Link } from 'react-router-dom';
import { invoicesApi, type InvoiceResponse } from '../../api/invoices';
import { Button } from '../../components/common/Button';

export default function InvoiceListPage() {
  const location = useLocation();
  const queryClient = useQueryClient();
  const [selectedInvoice, setSelectedInvoice] = useState<InvoiceResponse | null>(null);
  
  const isPurchase = location.pathname.includes('purchase-bills');
  const transactionType = isPurchase ? 'PURCHASE' : 'SALES';
  const pageTitle = isPurchase ? 'Purchase Bills' : 'Sales Invoices';
  const partyLabel = isPurchase ? 'Supplier' : 'Customer';

  const { data, isLoading } = useQuery({
    queryKey: ['invoices', transactionType],
    queryFn: () => invoicesApi.getAll(transactionType)
  });
  
  const invoices = data?.items || [];

  const finalizeMutation = useMutation({
    mutationFn: invoicesApi.finalize,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['invoices'] });
      setSelectedInvoice(null);
    }
  });

  const cancelMutation = useMutation({
    mutationFn: ({ id, reason }: { id: string, reason: string }) => invoicesApi.cancel(id, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['invoices'] });
      setSelectedInvoice(null);
    }
  });

  const handleFinalize = (id: string) => {
    if (confirm('Are you sure you want to finalize this invoice? Once finalized, it will be locked and an Invoice Number will be generated.')) {
      finalizeMutation.mutate(id);
    }
  };

  const handleCancel = (id: string) => {
    const reason = prompt('Please enter a reason for cancelling this invoice:');
    if (reason && reason.length >= 5) {
      cancelMutation.mutate({ id, reason });
    } else if (reason !== null) {
      alert('Cancellation reason must be at least 5 characters long.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">{pageTitle}</h2>
          <p className="mt-1 text-sm text-gray-500">Manage your {pageTitle.toLowerCase()}.</p>
        </div>
        {!isPurchase && (
          <Link to="/invoices/new" className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 font-medium text-sm">
            + Create Invoice
          </Link>
        )}
      </div>

      {isLoading ? (
        <div>Loading invoices...</div>
      ) : (
        <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{isPurchase ? 'Bill #' : 'Invoice #'}</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{partyLabel}</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {invoices.map((inv) => (
                <tr key={inv.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {inv.invoice_number.startsWith('DRAFT-') ? <span className="text-gray-400 italic">DRAFT</span> : inv.invoice_number}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{inv.invoice_date}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{inv.customer_name_snapshot}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-right text-gray-900">₹{inv.grand_total.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${inv.invoice_status === 'DRAFT' ? 'bg-yellow-100 text-yellow-800' : 
                        inv.invoice_status === 'FINALIZED' ? 'bg-green-100 text-green-800' : 
                        'bg-red-100 text-red-800'}`}>
                      {inv.invoice_status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button 
                      onClick={() => setSelectedInvoice(inv)}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      View
                    </button>
                  </td>
                </tr>
              ))}
              {invoices.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                    No invoices found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* View Modal */}
      {selectedInvoice && (
        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" onClick={() => setSelectedInvoice(null)}></div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
            <div className="inline-block px-4 pt-5 pb-4 overflow-hidden text-left align-bottom transition-all transform bg-white rounded-lg shadow-xl sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6">
              
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">
                    {selectedInvoice.invoice_status === 'DRAFT' ? 'Draft Invoice' : `Tax Invoice: ${selectedInvoice.invoice_number}`}
                  </h3>
                  <p className="text-sm text-gray-500">Date: {selectedInvoice.invoice_date}</p>
                </div>
                <div className={`px-3 py-1 rounded text-sm font-bold 
                  ${selectedInvoice.invoice_status === 'FINALIZED' ? 'bg-green-100 text-green-800' : 
                    selectedInvoice.invoice_status === 'CANCELLED' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>
                  {selectedInvoice.invoice_status}
                </div>
              </div>

              <div className="border rounded-md p-4 mb-6 bg-gray-50">
                <h4 className="text-sm font-semibold text-gray-700 mb-2">{isPurchase ? 'From Supplier:' : 'Billed To:'}</h4>
                <p className="font-medium text-gray-900">{selectedInvoice.customer_name_snapshot}</p>
                <p className="text-sm text-gray-600">Place of Supply: {selectedInvoice.place_of_supply}</p>
              </div>

              <div className="overflow-x-auto mb-6">
                <table className="min-w-full text-sm">
                  <thead className="bg-gray-100">
                    <tr>
                      <th className="px-3 py-2 text-left">Item</th>
                      <th className="px-3 py-2 text-right">Qty</th>
                      <th className="px-3 py-2 text-right">Rate</th>
                      <th className="px-3 py-2 text-right">GST %</th>
                      <th className="px-3 py-2 text-right">Total</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {selectedInvoice.lines.map((line: any) => (
                      <tr key={line.id}>
                        <td className="px-3 py-2">{line.item_name}</td>
                        <td className="px-3 py-2 text-right">{line.quantity} {line.unit_symbol_snapshot}</td>
                        <td className="px-3 py-2 text-right">₹{line.rate.toFixed(2)}</td>
                        <td className="px-3 py-2 text-right">{line.gst_rate}%</td>
                        <td className="px-3 py-2 text-right">₹{line.line_total.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="flex justify-end mb-6">
                <div className="w-64 space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Subtotal:</span>
                    <span className="font-medium">₹{selectedInvoice.subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Taxable Value:</span>
                    <span className="font-medium">₹{selectedInvoice.taxable_total.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between font-bold text-lg border-t pt-2 mt-2">
                    <span>Grand Total:</span>
                    <span>₹{selectedInvoice.grand_total.toFixed(2)}</span>
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t flex justify-end space-x-3">
                <Button type="button" variant="secondary" onClick={() => setSelectedInvoice(null)}>Close</Button>
                
                <Button 
                  type="button" 
                  variant="secondary"
                  onClick={() => invoicesApi.getPdf(selectedInvoice.id)}
                >
                  View PDF
                </Button>

                {selectedInvoice.invoice_status === 'FINALIZED' && (
                  <Button 
                    type="button" 
                    variant="danger" 
                    onClick={() => handleCancel(selectedInvoice.id)}
                    isLoading={cancelMutation.isPending}
                  >
                    Cancel Invoice
                  </Button>
                )}

                {selectedInvoice.invoice_status === 'DRAFT' && (
                  <Button 
                    type="button" 
                    onClick={() => handleFinalize(selectedInvoice.id)}
                    isLoading={finalizeMutation.isPending}
                  >
                    Finalize & Generate Number
                  </Button>
                )}
              </div>

            </div>
          </div>
        </div>
      )}
    </div>
  );
}

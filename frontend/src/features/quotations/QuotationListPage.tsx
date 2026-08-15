import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useLocation, Link } from 'react-router-dom';
import { quotationsApi, type QuotationResponse } from '../../api/quotations';
import { Button } from '../../components/common/Button';

export default function QuotationListPage() {
  const location = useLocation();
  const queryClient = useQueryClient();
  const [selectedQuotation, setSelectedQuotation] = useState<QuotationResponse | null>(null);

  const isSupplyIn = location.pathname.includes('supply-in');
  const quotationType = isSupplyIn ? 'PURCHASE' : 'SALES';
  const pageTitle = isSupplyIn ? 'Purchase Quotations' : 'Sales Quotations';
  const partyLabel = isSupplyIn ? 'Supplier' : 'Customer';

  const { data, isLoading } = useQuery({
    queryKey: ['quotations', quotationType],
    queryFn: () => quotationsApi.getAll(quotationType)
  });

  const approveMutation = useMutation({
    mutationFn: quotationsApi.approve,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quotations'] });
      setSelectedQuotation(null);
    }
  });

  const acceptMutation = useMutation({
    mutationFn: (id: string) => quotationsApi.accept(id, "USER_ACCEPTED"),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quotations'] });
      setSelectedQuotation(null);
    }
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">{pageTitle}</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage your {quotationType.toLowerCase()} quotations.
          </p>
        </div>
        <Link to={`${isSupplyIn ? '/supply-in' : '/supply-out'}/quotations/new`}>
          <Button>+ Create Quotation</Button>
        </Link>
      </div>

      <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
        <table className="min-w-full divide-y divide-border">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Quotation No</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">{partyLabel}</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Valid Until</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Amount</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-card divide-y divide-border">
            {isLoading ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-muted-foreground">Loading quotations...</td></tr>
            ) : data?.items.length === 0 ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-muted-foreground">No quotations found.</td></tr>
            ) : (
              data?.items.map((q) => (
                <tr key={q.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{new Date(q.quotation_date).toLocaleDateString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground font-medium">{q.quotation_number || 'DRAFT'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{q.party_id.substring(0,8)}...</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    {new Date(q.valid_until).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${q.status === 'DRAFT' ? 'bg-muted text-muted-foreground' : 
                        q.status === 'APPROVED' ? 'bg-blue-100 text-blue-800' : 
                        q.status === 'ACCEPTED' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {q.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground text-right font-bold">₹{q.grand_total.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button onClick={() => setSelectedQuotation(q)} className="text-primary-600 hover:text-primary-900">View</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* View Modal */}
      {selectedQuotation && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
            <div className="p-6 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-foreground">
                  {selectedQuotation.quotation_number || 'Draft Quotation'}
                </h3>
                <p className="text-sm text-muted-foreground">Rev: {selectedQuotation.revision} | Valid Until: {new Date(selectedQuotation.valid_until).toLocaleDateString()}</p>
              </div>
              <button onClick={() => setSelectedQuotation(null)} className="text-gray-400 hover:text-muted-foreground text-2xl font-bold">&times;</button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1">
              <table className="min-w-full divide-y divide-border border mb-6 text-sm">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-4 py-2 text-left text-muted-foreground font-medium">Item</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Qty</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Rate</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Discount</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">GST</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {selectedQuotation.lines.map((line: any) => (
                    <tr key={line.id}>
                      <td className="px-4 py-2">
                        {line.item_name_snapshot}
                        {line.description && <div className="text-xs text-muted-foreground">{line.description}</div>}
                      </td>
                      <td className="px-4 py-2 text-right">
                        {line.quantity} {line.unit_snapshot}
                      </td>
                      <td className="px-4 py-2 text-right">₹{line.rate.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right text-red-500">
                        {line.discount_amount > 0 ? `-₹${line.discount_amount.toFixed(2)}` : '-'}
                      </td>
                      <td className="px-4 py-2 text-right">{line.gst_rate}%</td>
                      <td className="px-4 py-2 text-right font-medium">₹{line.line_total.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="flex justify-end">
                <div className="w-64 space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Subtotal</span>
                    <span>₹{selectedQuotation.subtotal.toFixed(2)}</span>
                  </div>
                  {selectedQuotation.discount_total > 0 && (
                    <div className="flex justify-between text-red-600">
                      <span>Total Discount</span>
                      <span>-₹{selectedQuotation.discount_total.toFixed(2)}</span>
                    </div>
                  )}
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Taxable Value</span>
                    <span>₹{selectedQuotation.taxable_total.toFixed(2)}</span>
                  </div>
                  {selectedQuotation.tax_treatment === 'GST' && (
                    <>
                      {selectedQuotation.cgst_total > 0 && (
                        <div className="flex justify-between text-muted-foreground text-xs">
                          <span>CGST</span>
                          <span>₹{selectedQuotation.cgst_total.toFixed(2)}</span>
                        </div>
                      )}
                      {selectedQuotation.sgst_total > 0 && (
                        <div className="flex justify-between text-muted-foreground text-xs">
                          <span>SGST</span>
                          <span>₹{selectedQuotation.sgst_total.toFixed(2)}</span>
                        </div>
                      )}
                      {selectedQuotation.igst_total > 0 && (
                        <div className="flex justify-between text-muted-foreground text-xs">
                          <span>IGST</span>
                          <span>₹{selectedQuotation.igst_total.toFixed(2)}</span>
                        </div>
                      )}
                    </>
                  )}
                  <div className="flex justify-between font-bold text-lg pt-2 border-t mt-2">
                    <span>Grand Total</span>
                    <span>₹{selectedQuotation.grand_total.toFixed(2)}</span>
                  </div>
                </div>
              </div>

              {selectedQuotation.notes && (
                <div className="mt-6 p-4 bg-yellow-50 text-yellow-800 text-sm rounded">
                  <strong>Notes:</strong> {selectedQuotation.notes}
                </div>
              )}
              {selectedQuotation.terms && (
                <div className="mt-4 p-4 bg-muted text-foreground text-sm rounded">
                  <strong>Terms & Conditions:</strong>
                  <pre className="whitespace-pre-wrap font-sans mt-2">{selectedQuotation.terms}</pre>
                </div>
              )}
            </div>

            <div className="p-6 border-t bg-muted flex justify-end space-x-3 rounded-b-lg">
              <Button variant="secondary" onClick={() => setSelectedQuotation(null)}>Close</Button>
              {selectedQuotation.status === 'DRAFT' && (
                <Button 
                  onClick={() => approveMutation.mutate(selectedQuotation.id)}
                  isLoading={approveMutation.isPending}
                >
                  Approve Quotation
                </Button>
              )}
              {selectedQuotation.status === 'APPROVED' && (
                <Button 
                  onClick={() => acceptMutation.mutate(selectedQuotation.id)}
                  isLoading={acceptMutation.isPending}
                >
                  Accept Quotation
                </Button>
              )}
              {selectedQuotation.status === 'ACCEPTED' && !selectedQuotation.fully_converted && (
                <Link to={`${isSupplyIn ? '/supply-in' : '/supply-out'}/new?quotation_id=${selectedQuotation.id}`}>
                  <Button variant="default">Convert to Order</Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

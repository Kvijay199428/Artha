import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useLocation, Link } from 'react-router-dom';
import { returnsApi, type ReturnOrderResponse } from '../../api/returns';
import { Button } from '../../components/common/Button';

export default function ReturnListPage() {
  const location = useLocation();
  const queryClient = useQueryClient();
  const [selectedReturn, setSelectedReturn] = useState<ReturnOrderResponse | null>(null);
  const [showSettlementModal, setShowSettlementModal] = useState(false);
  const [settlementForm, setSettlementForm] = useState({
    settlement_type: 'ADJUST_RECEIVABLE',
    amount: 0,
    reference_number: '',
    notes: ''
  });

  const isSupplyIn = location.pathname.includes('supply-in');
  const returnType = isSupplyIn ? 'SUPPLY_IN_RETURN' : 'SUPPLY_OUT_RETURN';
  const pageTitle = isSupplyIn ? 'Purchase Returns (Supply In)' : 'Sales Returns (Supply Out)';
  const partyLabel = isSupplyIn ? 'Supplier' : 'Customer';

  const { data, isLoading } = useQuery({
    queryKey: ['returns', returnType],
    queryFn: () => returnsApi.getAll(returnType)
  });

  const approveMutation = useMutation({
    mutationFn: returnsApi.approve,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['returns'] });
      setSelectedReturn(null);
    }
  });

  const postMutation = useMutation({
    mutationFn: returnsApi.post,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['returns'] });
      setSelectedReturn(null);
    }
  });

  const settlementMutation = useMutation({
    mutationFn: (data: { id: string, payload: any }) => returnsApi.addSettlement(data.id, data.payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['returns'] });
      setShowSettlementModal(false);
      setSelectedReturn(null);
    },
    onError: (err: any) => {
      alert(err?.response?.data?.detail || "Failed to process settlement");
    }
  });

  const handleSettlementSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedReturn) {
      settlementMutation.mutate({
        id: selectedReturn.id,
        payload: settlementForm
      });
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">{pageTitle}</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage your {returnType.toLowerCase().replace('_', ' ')}s.
          </p>
        </div>
        <Link to={`${isSupplyIn ? '/supply-in' : '/supply-out'}/returns/new`}>
          <Button>+ Create Return</Button>
        </Link>
      </div>

      <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
        <table className="min-w-full divide-y divide-border">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Return No</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">{partyLabel}</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Financial</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Amount</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-card divide-y divide-border">
            {isLoading ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-muted-foreground">Loading returns...</td></tr>
            ) : data?.items.length === 0 ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-muted-foreground">No returns found.</td></tr>
            ) : (
              data?.items.map((ret) => (
                <tr key={ret.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{ret.return_date}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground font-medium">{ret.return_number || 'DRAFT'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{ret.party_id.substring(0,8)}...</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${ret.status === 'DRAFT' ? 'bg-muted text-muted-foreground' : 
                        ret.status === 'APPROVED' ? 'bg-blue-100 text-blue-800' : 
                        ret.status === 'COMPLETED' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {ret.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-muted text-foreground">
                      {ret.financial_status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground text-right font-bold">₹{ret.grand_total.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button onClick={() => setSelectedReturn(ret)} className="text-primary-600 hover:text-primary-900">View</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* View Modal */}
      {selectedReturn && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
            <div className="p-6 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-foreground">
                  {selectedReturn.return_number || 'Draft Return'}
                </h3>
                <p className="text-sm text-muted-foreground">Original Order: {selectedReturn.original_order_id.substring(0, 8)}...</p>
              </div>
              <button onClick={() => setSelectedReturn(null)} className="text-gray-400 hover:text-muted-foreground text-2xl font-bold">&times;</button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1">
              <table className="min-w-full divide-y divide-border border mb-6 text-sm">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-4 py-2 text-left text-muted-foreground font-medium">Item</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Return Qty</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Rate</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">GST</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {selectedReturn.lines.map((line: any) => (
                    <tr key={line.id}>
                      <td className="px-4 py-2">
                        {line.item_name_snapshot}
                        <div className="text-xs text-muted-foreground">Condition: {line.condition}</div>
                      </td>
                      <td className="px-4 py-2 text-right font-medium text-red-600">
                        {line.return_quantity} {line.unit_snapshot}
                      </td>
                      <td className="px-4 py-2 text-right">₹{line.rate.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right">{line.gst_rate}%</td>
                      <td className="px-4 py-2 text-right font-medium">₹{line.line_total.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="flex flex-col md:flex-row justify-between mt-6 pt-4 border-t gap-6">
                <div className="w-full md:w-1/2">
                  <h4 className="font-semibold text-foreground mb-2">Settlements</h4>
                  {selectedReturn.settlements.length > 0 ? (
                    <div className="space-y-2">
                      {selectedReturn.settlements.map((s: any) => (
                        <div key={s.id} className="bg-card border rounded p-3 text-sm flex justify-between items-center shadow-sm">
                          <div>
                            <div className="font-medium text-foreground">{s.settlement_type.replace(/_/g, ' ')}</div>
                            <div className="text-muted-foreground text-xs">{new Date(s.settlement_date).toLocaleDateString()} {s.reference_number ? `| Ref: ${s.reference_number}` : ''}</div>
                            {s.notes && <div className="text-muted-foreground text-xs italic">Note: {s.notes}</div>}
                          </div>
                          <div className="font-bold text-green-600">
                            ₹{s.amount.toFixed(2)}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-sm text-muted-foreground italic">No settlements recorded yet.</div>
                  )}
                </div>
                
                <div className="w-full md:w-64 space-y-2 text-sm bg-muted p-4 rounded-lg self-start border">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Subtotal</span>
                    <span>₹{selectedReturn.subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between font-bold text-lg pt-2 border-t mt-2">
                    <span>Grand Total</span>
                    <span>₹{selectedReturn.grand_total.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-green-600 font-semibold pt-1">
                    <span>Settled</span>
                    <span>₹{selectedReturn.settlements.reduce((sum: number, s: any) => sum + s.amount, 0).toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-red-600 font-bold pt-2 border-t mt-2">
                    <span>Balance</span>
                    <span>₹{(selectedReturn.grand_total - selectedReturn.settlements.reduce((sum: number, s: any) => sum + s.amount, 0)).toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="p-6 border-t bg-muted flex justify-end space-x-3 rounded-b-lg">
              <Button variant="secondary" onClick={() => setSelectedReturn(null)}>Close</Button>
              {selectedReturn.status === 'DRAFT' && (
                <Button 
                  onClick={() => approveMutation.mutate(selectedReturn.id)}
                  isLoading={approveMutation.isPending}
                >
                  Approve Return
                </Button>
              )}
              {selectedReturn.status === 'APPROVED' && (
                <Button 
                  onClick={() => postMutation.mutate(selectedReturn.id)}
                  isLoading={postMutation.isPending}
                >
                  Post Return (Process)
                </Button>
              )}
              {selectedReturn.status === 'COMPLETED' && selectedReturn.financial_status !== 'REFUNDED' && (
                <Button 
                  onClick={() => {
                    setSettlementForm({
                      settlement_type: isSupplyIn ? 'ADJUST_PAYABLE' : 'ADJUST_RECEIVABLE',
                      amount: selectedReturn.grand_total - selectedReturn.settlements.reduce((sum: number, s: any) => sum + s.amount, 0),
                      reference_number: '',
                      notes: ''
                    });
                    setShowSettlementModal(true);
                  }}
                >
                  Process Settlement
                </Button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Settlement Modal */}
      {showSettlementModal && selectedReturn && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-lg shadow-xl max-w-md w-full">
            <div className="p-6 border-b flex justify-between items-center">
              <h3 className="text-xl font-bold text-foreground">Process Settlement</h3>
              <button onClick={() => setShowSettlementModal(false)} className="text-gray-400 hover:text-muted-foreground text-2xl font-bold">&times;</button>
            </div>
            <form onSubmit={handleSettlementSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-muted-foreground">Settlement Type</label>
                <select 
                  className="mt-1 w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  value={settlementForm.settlement_type}
                  onChange={(e) => setSettlementForm({...settlementForm, settlement_type: e.target.value})}
                  required
                >
                  {isSupplyIn ? (
                    <>
                      <option value="ADJUST_PAYABLE">Adjust Payable (Reduce what we owe)</option>
                      <option value="SUPPLIER_REFUND">Supplier Refund (Cash/Bank received)</option>
                      <option value="SUPPLIER_CREDIT">Supplier Credit (Credit Note)</option>
                    </>
                  ) : (
                    <>
                      <option value="ADJUST_RECEIVABLE">Adjust Receivable (Reduce what they owe)</option>
                      <option value="CUSTOMER_REFUND">Customer Refund (Cash/Bank paid)</option>
                      <option value="CUSTOMER_CREDIT">Customer Credit (Credit Note)</option>
                    </>
                  )}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-muted-foreground">Amount (₹)</label>
                <input 
                  type="number" 
                  step="0.01"
                  min="0.01"
                  className="mt-1 w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  value={settlementForm.amount}
                  onChange={(e) => setSettlementForm({...settlementForm, amount: parseFloat(e.target.value)})}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-muted-foreground">Reference Number</label>
                <input 
                  type="text" 
                  className="mt-1 w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  value={settlementForm.reference_number}
                  onChange={(e) => setSettlementForm({...settlementForm, reference_number: e.target.value})}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-muted-foreground">Notes</label>
                <textarea 
                  className="mt-1 w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  value={settlementForm.notes}
                  onChange={(e) => setSettlementForm({...settlementForm, notes: e.target.value})}
                  rows={2}
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <Button type="button" variant="secondary" onClick={() => setShowSettlementModal(false)}>Cancel</Button>
                <Button type="submit" isLoading={settlementMutation.isPending}>Confirm Settlement</Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

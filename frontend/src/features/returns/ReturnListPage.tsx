import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useLocation, Link } from 'react-router-dom';
import { returnsApi, type ReturnOrderResponse } from '../../api/returns';
import { Button } from '../../components/common/Button';

export default function ReturnListPage() {
  const location = useLocation();
  const queryClient = useQueryClient();
  const [selectedReturn, setSelectedReturn] = useState<ReturnOrderResponse | null>(null);

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

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">{pageTitle}</h2>
          <p className="mt-1 text-sm text-gray-500">
            Manage your {returnType.toLowerCase().replace('_', ' ')}s.
          </p>
        </div>
        <Link to={`${isSupplyIn ? '/supply-in' : '/supply-out'}/returns/new`}>
          <Button>+ Create Return</Button>
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Return No</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{partyLabel}</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Financial</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {isLoading ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-gray-500">Loading returns...</td></tr>
            ) : data?.items.length === 0 ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-gray-500">No returns found.</td></tr>
            ) : (
              data?.items.map((ret) => (
                <tr key={ret.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{ret.return_date}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">{ret.return_number || 'DRAFT'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{ret.party_id.substring(0,8)}...</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${ret.status === 'DRAFT' ? 'bg-gray-100 text-gray-800' : 
                        ret.status === 'APPROVED' ? 'bg-blue-100 text-blue-800' : 
                        ret.status === 'COMPLETED' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {ret.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                      {ret.financial_status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-bold">₹{ret.grand_total.toFixed(2)}</td>
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
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
            <div className="p-6 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-gray-900">
                  {selectedReturn.return_number || 'Draft Return'}
                </h3>
                <p className="text-sm text-gray-500">Original Order: {selectedReturn.original_order_id.substring(0, 8)}...</p>
              </div>
              <button onClick={() => setSelectedReturn(null)} className="text-gray-400 hover:text-gray-500 text-2xl font-bold">&times;</button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1">
              <table className="min-w-full divide-y divide-gray-200 border mb-6 text-sm">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left text-gray-500 font-medium">Item</th>
                    <th className="px-4 py-2 text-right text-gray-500 font-medium">Return Qty</th>
                    <th className="px-4 py-2 text-right text-gray-500 font-medium">Rate</th>
                    <th className="px-4 py-2 text-right text-gray-500 font-medium">GST</th>
                    <th className="px-4 py-2 text-right text-gray-500 font-medium">Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {selectedReturn.lines.map((line: any) => (
                    <tr key={line.id}>
                      <td className="px-4 py-2">
                        {line.item_name_snapshot}
                        <div className="text-xs text-gray-500">Condition: {line.condition}</div>
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

              <div className="flex justify-end">
                <div className="w-64 space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Subtotal</span>
                    <span>₹{selectedReturn.subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between font-bold text-lg pt-2 border-t mt-2">
                    <span>Grand Total</span>
                    <span>₹{selectedReturn.grand_total.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="p-6 border-t bg-gray-50 flex justify-end space-x-3 rounded-b-lg">
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
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

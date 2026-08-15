import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link, useLocation } from 'react-router-dom';
import { ordersApi, type SupplyOrderResponse } from '../../api/orders';
import { Button } from '../../components/common/Button';

export default function OrderListPage() {
  const location = useLocation();
  const queryClient = useQueryClient();
  const [selectedOrder, setSelectedOrder] = useState<SupplyOrderResponse | null>(null);

  const isPurchase = location.pathname.includes('supply-in');
  const orderType = isPurchase ? 'PURCHASE' : 'SALES';
  const pageTitle = isPurchase ? 'Supply In (Purchase Orders)' : 'Supply Out (Sales Orders)';
  const newLink = isPurchase ? '/supply-in/new' : '/supply-out/new';
  const partyLabel = isPurchase ? 'Supplier' : 'Customer';

  const { data, isLoading } = useQuery({
    queryKey: ['orders', orderType],
    queryFn: () => ordersApi.getAll(orderType)
  });

  const confirmMutation = useMutation({
    mutationFn: ordersApi.confirm,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      setSelectedOrder(null);
    }
  });

  const convertMutation = useMutation({
    mutationFn: ordersApi.convert,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      queryClient.invalidateQueries({ queryKey: ['invoices'] });
      alert('Order successfully converted to ' + (isPurchase ? 'Purchase Bill' : 'Sales Invoice') + '!');
      setSelectedOrder(null);
    }
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">{pageTitle}</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage your {orderType.toLowerCase()} orders.
          </p>
        </div>
        <Link to={newLink}>
          <Button>Create {isPurchase ? 'Purchase' : 'Sales'} Order</Button>
        </Link>
      </div>

      <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
        <table className="min-w-full divide-y divide-border">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Order No</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">{partyLabel}</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Tax Type</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Amount</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-card divide-y divide-border">
            {isLoading ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-muted-foreground">Loading orders...</td></tr>
            ) : data?.items.length === 0 ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-muted-foreground">No {orderType.toLowerCase()} orders found.</td></tr>
            ) : (
              data?.items.map((order) => (
                <tr key={order.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{order.order_date}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground font-medium">{order.order_number || 'DRAFT'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{order.party_id.substring(0,8)}...</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${order.status === 'DRAFT' ? 'bg-muted text-muted-foreground' : 
                        order.status === 'CONFIRMED' ? 'bg-blue-100 text-blue-800' : 
                        order.status === 'CANCELLED' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                      {order.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{order.tax_treatment.replace('_', ' ')}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground text-right font-bold">₹{order.grand_total.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button onClick={() => setSelectedOrder(order)} className="text-primary-600 hover:text-primary-900">View</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* View Modal */}
      {selectedOrder && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
            <div className="p-6 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-foreground">
                  {selectedOrder.order_number || 'Draft Order'}
                </h3>
                <p className="text-sm text-muted-foreground">Date: {selectedOrder.order_date} | Type: {selectedOrder.order_type} | Tax: {selectedOrder.tax_treatment.replace('_', ' ')}</p>
              </div>
              <button onClick={() => setSelectedOrder(null)} className="text-gray-400 hover:text-muted-foreground text-2xl font-bold">&times;</button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1">
              <table className="min-w-full divide-y divide-border border mb-6 text-sm">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-4 py-2 text-left text-muted-foreground font-medium">Item</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Qty</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Rate</th>
                    {selectedOrder.tax_treatment === 'GST' && (
                      <>
                        <th className="px-4 py-2 text-right text-muted-foreground font-medium">Taxable</th>
                        <th className="px-4 py-2 text-right text-muted-foreground font-medium">GST</th>
                      </>
                    )}
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {selectedOrder.lines.map((line: any) => (
                    <tr key={line.id}>
                      <td className="px-4 py-2">{line.item_name_snapshot}</td>
                      <td className="px-4 py-2 text-right">{line.quantity} {line.unit_symbol_snapshot}</td>
                      <td className="px-4 py-2 text-right">₹{line.rate.toFixed(2)}</td>
                      {selectedOrder.tax_treatment === 'GST' && (
                        <>
                          <td className="px-4 py-2 text-right">₹{line.taxable_value.toFixed(2)}</td>
                          <td className="px-4 py-2 text-right">{line.gst_rate}% (₹{(line.cgst_amount+line.sgst_amount+line.igst_amount).toFixed(2)})</td>
                        </>
                      )}
                      <td className="px-4 py-2 text-right font-medium">₹{line.line_total.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="flex justify-end">
                <div className="w-64 space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Subtotal</span>
                    <span>₹{selectedOrder.subtotal.toFixed(2)}</span>
                  </div>
                  {selectedOrder.tax_treatment === 'GST' && (
                    <>
                      {selectedOrder.igst_total > 0 ? (
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">IGST</span>
                          <span>₹{selectedOrder.igst_total.toFixed(2)}</span>
                        </div>
                      ) : (
                        <>
                          <div className="flex justify-between">
                            <span className="text-muted-foreground">CGST</span>
                            <span>₹{selectedOrder.cgst_total.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-muted-foreground">SGST</span>
                            <span>₹{selectedOrder.sgst_total.toFixed(2)}</span>
                          </div>
                        </>
                      )}
                    </>
                  )}
                  <div className="flex justify-between font-bold text-lg pt-2 border-t mt-2">
                    <span>Grand Total</span>
                    <span>₹{selectedOrder.grand_total.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="p-6 border-t bg-muted flex justify-end space-x-3 rounded-b-lg">
              <Button variant="secondary" onClick={() => setSelectedOrder(null)}>Close</Button>
              {selectedOrder.status === 'DRAFT' && (
                <Button 
                  onClick={() => confirmMutation.mutate(selectedOrder.id)}
                  isLoading={confirmMutation.isPending}
                >
                  Confirm Order
                </Button>
              )}
              {selectedOrder.status === 'CONFIRMED' && (
                <Button 
                  onClick={() => convertMutation.mutate(selectedOrder.id)}
                  isLoading={convertMutation.isPending}
                >
                  Convert to {isPurchase ? 'Purchase Bill' : 'Sales Invoice'}
                </Button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

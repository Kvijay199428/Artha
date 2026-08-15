import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useForm, useFieldArray } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { returnsApi, type ReturnOrderCreateRequest, type ReturnableLinesResponse } from '../../api/returns';
import { ordersApi } from '../../api/orders';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const returnLineSchema = z.object({
  original_order_line_id: z.string().min(1),
  item_name_snapshot: z.string(),
  unit_snapshot: z.string().optional(),
  returnable_quantity: z.number(),
  rate: z.number(),
  return_quantity: z.number().min(0),
  condition: z.string().optional(),
  warehouse_action: z.string().optional(),
});

const returnSchema = z.object({
  original_order_id: z.string().min(1, 'Order ID is required'),
  reason: z.string().optional(),
  lines: z.array(returnLineSchema),
});

export default function ReturnBuilderPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const isSupplyIn = location.pathname.includes('supply-in');
  const returnType = isSupplyIn ? 'SUPPLY_IN_RETURN' : 'SUPPLY_OUT_RETURN';
  const orderType = isSupplyIn ? 'PURCHASE' : 'SALES';
  
  const [orderId, setOrderId] = useState<string>('');
  const [returnableData, setReturnableData] = useState<ReturnableLinesResponse | null>(null);

  const { data: orders } = useQuery({
    queryKey: ['orders', orderType],
    queryFn: () => ordersApi.getAll(orderType)
  });

  const { register, control, handleSubmit, setValue, watch } = useForm<any>({
    resolver: zodResolver(returnSchema),
    defaultValues: {
      original_order_id: '',
      reason: '',
      lines: []
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'lines'
  });

  const fetchLinesMutation = useMutation({
    mutationFn: returnsApi.getReturnableLines,
    onSuccess: (data) => {
      setReturnableData(data);
      // Populate fields automatically
      remove();
      data.lines.forEach(line => {
        append({
          original_order_line_id: line.original_order_line_id,
          item_name_snapshot: line.item_name_snapshot,
          unit_snapshot: line.unit_symbol_snapshot || '',
          returnable_quantity: line.returnable_quantity,
          rate: line.rate,
          return_quantity: 0,
          condition: 'GOOD',
          warehouse_action: 'RETURN_TO_STOCK'
        });
      });
    },
    onError: () => {
      alert("Failed to fetch returnable lines or order not found.");
      setReturnableData(null);
    }
  });

  const handleOrderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    setOrderId(val);
    setValue('original_order_id', val);
    if (val) {
      fetchLinesMutation.mutate(val);
    } else {
      setReturnableData(null);
      remove();
    }
  };

  const createMutation = useMutation({
    mutationFn: returnsApi.create,
    onSuccess: () => {
      navigate(`${isSupplyIn ? '/supply-in' : '/supply-out'}/returns`);
    },
    onError: (err: any) => {
      alert(err?.response?.data?.detail || "Failed to create return");
    }
  });

  const onSubmit = (data: any) => {
    // filter out lines with 0 return qty
    const filteredLines = data.lines.filter((l: any) => l.return_quantity > 0);
    if (filteredLines.length === 0) {
      alert("Please enter a return quantity for at least one item.");
      return;
    }
    
    // validate max qty
    const invalid = filteredLines.find((l: any) => l.return_quantity > l.returnable_quantity);
    if (invalid) {
      alert(`Cannot return more than ${invalid.returnable_quantity} for ${invalid.item_name_snapshot}`);
      return;
    }
    
    const request: ReturnOrderCreateRequest = {
      original_order_id: data.original_order_id,
      return_type: returnType,
      reason: data.reason,
      lines: filteredLines.map((l: any) => ({
        original_order_line_id: l.original_order_line_id,
        return_quantity: l.return_quantity,
        condition: l.condition,
        warehouse_action: l.warehouse_action
      }))
    };
    
    createMutation.mutate(request);
  };

  const formLines = watch('lines');
  
  const estimatedTotal = formLines?.reduce((sum: number, line: any) => {
    return sum + (Number(line.return_quantity || 0) * Number(line.rate || 0));
  }, 0) || 0;

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-foreground">
          Create {isSupplyIn ? 'Purchase Return' : 'Sales Return'}
        </h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Initiate a return against a confirmed {orderType.toLowerCase()} order.
        </p>
      </div>

      <div className="bg-card rounded-lg shadow-sm border p-6">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Select Original Order *</label>
              <select
                className="w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
                value={orderId}
                onChange={handleOrderChange}
                required
              >
                <option value="">-- Select Order --</option>
                {orders?.items.filter(o => o.status === 'CONFIRMED').map(o => (
                  <option key={o.id} value={o.id}>
                    {o.order_number || 'DRAFT'} - {o.party_id.substring(0,8)} (₹{o.grand_total.toFixed(2)})
                  </option>
                ))}
              </select>
            </div>
            
            <Input
              label="Reason for Return"
              {...register('reason')}
              placeholder="e.g. Damaged goods, wrong item..."
            />
          </div>
          
          {fetchLinesMutation.isPending && (
            <div className="text-sm text-muted-foreground py-4">Fetching returnable items...</div>
          )}

          {returnableData && fields.length > 0 && (
            <div className="mt-8">
              <h3 className="text-lg font-medium text-foreground mb-4">Return Items</h3>
              
              <div className="overflow-x-auto border rounded-lg">
                <table className="min-w-full divide-y divide-border">
                  <thead className="bg-muted/50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase">Item</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase">Returnable Max</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase">Rate</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase">Condition</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase w-32">Return Qty</th>
                    </tr>
                  </thead>
                  <tbody className="bg-card divide-y divide-border">
                    {fields.map((field, index) => {
                      const line = formLines[index];
                      return (
                        <tr key={field.id} className={line.return_quantity > 0 ? 'bg-red-50' : ''}>
                          <td className="px-4 py-3 text-sm font-medium text-foreground">
                            {line.item_name_snapshot}
                          </td>
                          <td className="px-4 py-3 text-sm text-muted-foreground text-right">
                            {line.returnable_quantity} {line.unit_snapshot}
                          </td>
                          <td className="px-4 py-3 text-sm text-muted-foreground text-right">
                            ₹{line.rate.toFixed(2)}
                          </td>
                          <td className="px-4 py-3">
                            <select
                              {...register(`lines.${index}.condition`)}
                              className="text-sm rounded border-input w-full"
                            >
                              <option value="GOOD">Good / Resaleable</option>
                              <option value="DAMAGED">Damaged</option>
                              <option value="DEFECTIVE">Defective</option>
                              <option value="SCRAP">Scrap</option>
                            </select>
                          </td>
                          <td className="px-4 py-3">
                            <input
                              type="number"
                              step="0.01"
                              min="0"
                              max={line.returnable_quantity}
                              {...register(`lines.${index}.return_quantity`, { valueAsNumber: true })}
                              className="w-full rounded border-input text-right text-sm font-medium text-red-600 focus:ring-red-500 focus:border-red-500"
                            />
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              <div className="mt-4 flex justify-between items-center text-sm">
                <div className="text-muted-foreground italic">
                  Note: The exact tax reversals will be calculated automatically by the server.
                </div>
                <div className="font-medium text-lg">
                  Estimated Base Return Value: <span className="text-red-600">₹{estimatedTotal.toFixed(2)}</span>
                </div>
              </div>
            </div>
          )}

          {returnableData && fields.length === 0 && (
            <div className="text-sm text-red-500 py-4 font-medium">
              This order has no remaining items that can be returned.
            </div>
          )}

          <div className="flex justify-end space-x-4 pt-6 border-t">
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate(-1)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              isLoading={createMutation.isPending}
              disabled={!returnableData || fields.length === 0}
            >
              Create Draft Return
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

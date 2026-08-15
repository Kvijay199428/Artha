import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { itemsApi } from '../../api/items';
import { unitsApi } from '../../api/units';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const itemSchema = z.object({
  type: z.string().min(1, 'Type is required'),
  name: z.string().min(1, 'Name is required'),
  sku: z.string().optional(),
  description: z.string().optional(),
  hsn_sac: z.string().optional(),
  gst_rate: z.coerce.number().min(0).max(100),
  cess_rate: z.coerce.number().min(0).max(100).optional(),
  sale_price: z.coerce.number().min(0),
  purchase_price: z.coerce.number().min(0),
  unit_id: z.string().min(1, 'Unit is required'),
  stock_quantity: z.coerce.number().optional(),
  low_stock_warning: z.coerce.number().optional(),
});

type ItemForm = z.infer<typeof itemSchema>;

export default function ItemsPage() {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const { data: items = [], isLoading: itemsLoading } = useQuery({
    queryKey: ['items'],
    queryFn: itemsApi.getAll
  });

  const { data: units = [] } = useQuery({
    queryKey: ['units'],
    queryFn: unitsApi.getAll
  });

  const { register, handleSubmit, watch, formState: { errors }, reset } = useForm<any>({
    resolver: zodResolver(itemSchema),
    defaultValues: {
      type: 'Product',
      gst_rate: 18,
      cess_rate: 0,
      sale_price: 0,
      purchase_price: 0,
      stock_quantity: 0,
      low_stock_warning: 0
    }
  });

  const itemType = watch('type');

  const createMutation = useMutation({
    mutationFn: itemsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
      setIsModalOpen(false);
      reset();
    },
    onError: (error: any) => {
      setApiError(error.message || 'Failed to create item');
    }
  });

  const deleteMutation = useMutation({
    mutationFn: itemsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
    }
  });

  const onSubmit = (data: any) => {
    setApiError(null);
    createMutation.mutate({
      ...(data as ItemForm),
      unit_id: parseInt(data.unit_id),
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Products & Services</h2>
          <p className="mt-1 text-sm text-muted-foreground">Manage your inventory, pricing, and HSN/SAC codes.</p>
        </div>
        <Button onClick={() => setIsModalOpen(true)}>Add New Item</Button>
      </div>

      {itemsLoading ? (
        <div>Loading items...</div>
      ) : (
        <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
          <table className="min-w-full divide-y divide-border">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Item Name / SKU</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Type & HSN</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Sale Price</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Stock</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-card divide-y divide-border">
              {items.map((item) => (
                <tr key={item.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-foreground">{item.name}</div>
                    <div className="text-xs text-muted-foreground">{item.sku || 'No SKU'}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${item.type === 'Service' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'}`}>
                      {item.type}
                    </span>
                    <div className="text-xs text-muted-foreground mt-1">{item.hsn_sac ? `HSN: ${item.hsn_sac}` : '-'}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-foreground font-medium">
                    ₹{item.sale_price.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                    {item.type === 'Product' ? (
                      <span className={item.stock_quantity <= item.low_stock_warning ? 'text-red-600 font-semibold' : 'text-green-600 font-semibold'}>
                        {item.stock_quantity}
                      </span>
                    ) : (
                      <span className="text-gray-400">N/A</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button 
                      onClick={() => {
                        if (confirm('Are you sure you want to delete this item?')) {
                          deleteMutation.mutate(item.id);
                        }
                      }}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
              {items.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-muted-foreground">
                    No items found. Click "Add New Item" to create one.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {isModalOpen && (
        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity bg-black/60" onClick={() => setIsModalOpen(false)}></div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
            <div className="inline-block px-4 pt-5 pb-4 overflow-hidden text-left align-bottom transition-all transform bg-card rounded-xl shadow-xl sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6">
              <h3 className="text-lg font-medium leading-6 text-foreground mb-4 border-b pb-2">Add New Item</h3>
              
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                {apiError && (
                  <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm border border-red-100">
                    {apiError}
                  </div>
                )}
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Basic Details */}
                  <div className="space-y-4 md:col-span-2 grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-muted-foreground mb-1">Item Type</label>
                      <select className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('type')}>
                        <option value="Product">Product (Goods)</option>
                        <option value="Service">Service</option>
                      </select>
                    </div>
                    <Input label="Name" {...register('name')} error={errors.name?.message} />
                  </div>

                  <Input label="SKU / Item Code" {...register('sku')} error={errors.sku?.message} />
                  <Input label="HSN/SAC Code" {...register('hsn_sac')} error={errors.hsn_sac?.message} />
                  
                  <div className="md:col-span-2">
                    <Input label="Description (Optional)" {...register('description')} error={errors.description?.message} />
                  </div>

                  {/* Pricing Details */}
                  <div className="md:col-span-2 bg-muted p-4 rounded-md border border">
                    <h4 className="text-sm font-semibold text-muted-foreground mb-3">Pricing & Tax</h4>
                    <div className="grid grid-cols-2 gap-4">
                      <Input label="Sale Price" type="number" step="0.01" {...register('sale_price')} error={errors.sale_price?.message} />
                      <Input label="Purchase Price" type="number" step="0.01" {...register('purchase_price')} error={errors.purchase_price?.message} />
                      <Input label="GST Rate (%)" type="number" step="0.1" {...register('gst_rate')} error={errors.gst_rate?.message} />
                      <Input label="CESS Rate (%)" type="number" step="0.1" {...register('cess_rate')} error={errors.cess_rate?.message} />
                    </div>
                  </div>

                  {/* Inventory Details */}
                  <div className="md:col-span-2">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-muted-foreground mb-1">Primary Unit</label>
                        <select className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('unit_id')}>
                          <option value="">Select a unit...</option>
                          {units.map(u => (
                            <option key={u.id} value={u.id}>{u.name} ({u.abbreviation})</option>
                          ))}
                        </select>
                        {errors.unit_id?.message && <p className="mt-1 text-sm text-red-600">{errors.unit_id.message as string}</p>}
                      </div>
                      
                      {itemType === 'Product' && (
                        <div className="grid grid-cols-2 gap-4">
                          <Input label="Opening Stock" type="number" step="any" {...register('stock_quantity')} error={errors.stock_quantity?.message} />
                          <Input label="Low Stock Warning" type="number" step="any" {...register('low_stock_warning')} error={errors.low_stock_warning?.message} />
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                <div className="pt-4 border-t flex justify-end space-x-3">
                  <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
                  <Button type="submit" isLoading={createMutation.isPending}>Save Item</Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

import { useNavigate, useLocation } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useForm, useFieldArray } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { quotationsApi, type QuotationCreateRequest } from '../../api/quotations';
import { partiesApi } from '../../api/parties';
import { itemsApi } from '../../api/items';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const quotationLineSchema = z.object({
  item_id: z.string().optional(),
  item_name_snapshot: z.string().min(1, 'Item name is required'),
  description: z.string().optional(),
  quantity: z.number().min(0.001, 'Quantity must be greater than 0'),
  rate: z.number().min(0, 'Rate must be >= 0'),
  discount_type: z.string().optional(),
  discount_value: z.number().optional().default(0),
  gst_rate: z.number().optional().default(0),
});

const quotationSchema = z.object({
  party_id: z.string().min(1, 'Party is required'),
  tax_treatment: z.enum(['GST', 'WITHOUT_GST']),
  valid_until: z.string().min(1, 'Valid until date is required'),
  place_of_supply: z.string().min(1, 'Place of supply is required'),
  notes: z.string().optional(),
  terms: z.string().optional(),
  lines: z.array(quotationLineSchema).min(1, 'At least one item is required'),
});

export default function QuotationBuilderPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const isSupplyIn = location.pathname.includes('supply-in');
  const quotationType = isSupplyIn ? 'PURCHASE' : 'SALES';
  
  const { data: parties } = useQuery({
    queryKey: ['parties'],
    queryFn: () => partiesApi.getAll()
  });

  const { data: items } = useQuery({
    queryKey: ['items'],
    queryFn: () => itemsApi.getAll()
  });

  const { register, control, handleSubmit, watch, setValue, formState: { errors } } = useForm<any>({
    resolver: zodResolver(quotationSchema),
    defaultValues: {
      tax_treatment: 'GST',
      valid_until: new Date(Date.now() + 30*24*60*60*1000).toISOString().split('T')[0],
      place_of_supply: 'State',
      lines: [{ item_name_snapshot: '', quantity: 1, rate: 0, discount_value: 0, gst_rate: 18 }]
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'lines'
  });

  const watchTaxTreatment = watch('tax_treatment');

  const createMutation = useMutation({
    mutationFn: quotationsApi.create,
    onSuccess: () => {
      navigate(`${isSupplyIn ? '/supply-in' : '/supply-out'}/quotations`);
    },
    onError: (err: any) => {
      alert(err?.response?.data?.detail || "Failed to create quotation");
    }
  });

  const handleItemSelect = (index: number, itemId: string) => {
    const item = items?.find((i: any) => i.id === itemId || String(i.id) === itemId);
    if (item) {
      setValue(`lines.${index}.item_id`, String(item.id));
      setValue(`lines.${index}.item_name_snapshot`, item.name);
      setValue(`lines.${index}.rate`, isSupplyIn ? (item.purchase_price || 0) : (item.sale_price || 0));
      if (watchTaxTreatment === 'GST') {
        setValue(`lines.${index}.gst_rate`, item.gst_rate || 18);
      }
    }
  };

  const onSubmit = (data: any) => {
    const request: QuotationCreateRequest = {
      ...data,
      quotation_type: quotationType,
      lines: data.lines.map((l: any) => ({
        ...l,
        discount_type: l.discount_value > 0 ? 'FIXED' : null
      }))
    };
    createMutation.mutate(request);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">
          Create {isSupplyIn ? 'Purchase Quotation' : 'Sales Quotation'}
        </h2>
        <p className="mt-1 text-sm text-gray-500">
          Create a non-binding quotation for your {isSupplyIn ? 'supplier' : 'customer'}.
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-sm border p-6">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {isSupplyIn ? 'Supplier' : 'Customer'} *
              </label>
              <select
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                {...register('party_id')}
              >
                <option value="">-- Select Party --</option>
                {parties?.map((p: any) => (
                  <option key={p.id} value={p.id}>{p.legal_name || p.name}</option>
                ))}
              </select>
              {errors.party_id && <p className="text-red-500 text-xs mt-1">{errors.party_id.message as string}</p>}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tax Treatment</label>
              <select
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                {...register('tax_treatment')}
              >
                <option value="GST">GST</option>
                <option value="WITHOUT_GST">Without GST</option>
              </select>
            </div>

            <Input
              label="Valid Until *"
              type="date"
              {...register('valid_until')}
              error={errors.valid_until?.message as string}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Input
              label="Place of Supply *"
              {...register('place_of_supply')}
              error={errors.place_of_supply?.message as string}
            />
          </div>

          <div className="mt-8 border-t pt-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">Quotation Items</h3>
              <Button type="button" variant="secondary" onClick={() => append({ item_name_snapshot: '', quantity: 1, rate: 0, discount_value: 0, gst_rate: 18 })}>
                + Add Row
              </Button>
            </div>
            
            <div className="overflow-x-auto border rounded-lg">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Item Selection</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-48">Item Name *</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-24">Qty *</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-32">Rate *</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-32">Disc (₹)</th>
                    {watchTaxTreatment === 'GST' && (
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-24">GST %</th>
                    )}
                    <th className="px-4 py-3"></th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {fields.map((field, index) => (
                    <tr key={field.id}>
                      <td className="px-4 py-2">
                        <select 
                          className="w-full text-sm rounded border-gray-300"
                          onChange={(e) => handleItemSelect(index, e.target.value)}
                        >
                          <option value="">-- Catalog --</option>
                          {items?.map((i: any) => (
                            <option key={i.id} value={i.id}>{i.name}</option>
                          ))}
                        </select>
                      </td>
                      <td className="px-4 py-2">
                        <input
                          {...register(`lines.${index}.item_name_snapshot`)}
                          className="w-full text-sm rounded border-gray-300"
                          placeholder="Manual name"
                        />
                      </td>
                      <td className="px-4 py-2">
                        <input
                          type="number" step="any" min="0"
                          {...register(`lines.${index}.quantity`, { valueAsNumber: true })}
                          className="w-full text-sm rounded border-gray-300"
                        />
                      </td>
                      <td className="px-4 py-2">
                        <input
                          type="number" step="any" min="0"
                          {...register(`lines.${index}.rate`, { valueAsNumber: true })}
                          className="w-full text-sm rounded border-gray-300"
                        />
                      </td>
                      <td className="px-4 py-2">
                        <input
                          type="number" step="any" min="0"
                          {...register(`lines.${index}.discount_value`, { valueAsNumber: true })}
                          className="w-full text-sm rounded border-gray-300"
                        />
                      </td>
                      {watchTaxTreatment === 'GST' && (
                        <td className="px-4 py-2">
                          <input
                            type="number" step="any" min="0"
                            {...register(`lines.${index}.gst_rate`, { valueAsNumber: true })}
                            className="w-full text-sm rounded border-gray-300"
                          />
                        </td>
                      )}
                      <td className="px-4 py-2 text-right">
                        <button type="button" onClick={() => remove(index)} className="text-red-500 hover:text-red-700 text-xl font-bold">&times;</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {errors.lines && <p className="text-red-500 text-xs p-4">{errors.lines.message as string}</p>}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Notes / Remarks</label>
              <textarea
                {...register('notes')}
                rows={3}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Terms & Conditions</label>
              <textarea
                {...register('terms')}
                rows={3}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
          </div>

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
            >
              Create Quotation
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useNavigate, useLocation } from 'react-router-dom';
import { ordersApi, type SupplyOrderCalculateRequest, type SupplyOrderCreateRequest } from '../../api/orders';
import { itemsApi } from '../../api/items';
import { unitsApi } from '../../api/units';
import { partiesApi } from '../../api/parties';
import { quotationsApi } from '../../api/quotations';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const orderLineSchema = z.object({
  item_id: z.string().optional(),
  item_name: z.string().min(1, 'Item name is required'),
  description: z.string().optional(),
  sku: z.string().optional(),
  hsn_sac: z.string().optional(),
  quantity: z.coerce.number().min(0.001, 'Quantity must be > 0'),
  unit_id: z.string().min(1, 'Unit is required'),
  unit_name: z.string(),
  unit_symbol: z.string(),
  rate: z.coerce.number().min(0),
  discount_type: z.string().default('NONE'),
  discount_value: z.coerce.number().default(0),
  gst_rate: z.coerce.number().default(0),
});

const orderSchema = z.object({
  order_type: z.enum(['PURCHASE', 'SALES']),
  tax_treatment: z.enum(['GST', 'WITHOUT_GST']),
  order_date: z.string().min(1, 'Date is required'),
  expected_date: z.string().optional(),
  party_id: z.string().min(1, 'Party is required'),
  place_of_supply: z.string().min(1, 'Place of supply is required'),
  lines: z.array(orderLineSchema).min(1, 'At least one line is required'),
  notes: z.string().optional(),
  terms: z.string().optional(),
});



export default function OrderBuilderPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const queryClient = useQueryClient();
  const [apiError, setApiError] = useState<string | null>(null);

  // Determine order type from URL (e.g. /supply-in/new -> PURCHASE)
  const isPurchase = location.pathname.includes('supply-in');
  const defaultOrderType = isPurchase ? 'PURCHASE' : 'SALES';

  const { data: items = [] } = useQuery({ queryKey: ['items'], queryFn: itemsApi.getAll });
  const { data: units = [] } = useQuery({ queryKey: ['units'], queryFn: unitsApi.getAll });
  const { data: parties = [] } = useQuery({ 
    queryKey: ['parties', isPurchase ? 'VENDOR' : 'CUSTOMER'], 
    queryFn: () => partiesApi.getAll(isPurchase ? 'VENDOR' : 'CUSTOMER') 
  });

  const searchParams = new URLSearchParams(location.search);
  const quotationId = searchParams.get('quotation_id');

  const { data: quotation } = useQuery({
    queryKey: ['quotations', quotationId],
    queryFn: () => quotationsApi.getById(quotationId!),
    enabled: !!quotationId
  });

  const { register, control, handleSubmit, watch, setValue, reset, formState: { errors } } = useForm<any>({
    resolver: zodResolver(orderSchema),
    defaultValues: {
      order_type: defaultOrderType,
      tax_treatment: 'GST',
      order_date: new Date().toISOString().split('T')[0],
      expected_date: '',
      place_of_supply: '',
      lines: [{ item_name: '', quantity: 1, rate: 0, discount_type: 'NONE', discount_value: 0, gst_rate: 0, unit_name: '', unit_symbol: '', unit_id: '' }]
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'lines'
  });

  const watchAll = watch();
  const taxTreatment = watchAll.tax_treatment;

  // Pre-fill form if quotation is loaded
  useEffect(() => {
    if (quotation && units.length > 0) {
      reset({
        quotation_id: quotation.id,
        order_type: quotation.quotation_type,
        tax_treatment: quotation.tax_treatment,
        order_date: new Date().toISOString().split('T')[0],
        expected_date: '',
        party_id: quotation.party_id,
        place_of_supply: quotation.place_of_supply,
        notes: quotation.notes || '',
        terms: quotation.terms || '',
        lines: quotation.lines.map((l: any) => {
          const unit = units.find((u: any) => String(u.id) === String(l.unit_id));
          return {
            item_id: l.item_id || '',
            item_name: l.item_name_snapshot,
            sku: l.sku_snapshot || '',
            hsn_sac: l.hsn_sac_snapshot || '',
            description: l.description || '',
            quantity: l.quantity,
            unit_id: l.unit_id || '',
            unit_name: unit?.name || l.unit_snapshot || '',
            unit_symbol: unit?.abbreviation || l.unit_snapshot || '',
            rate: l.rate,
            discount_type: l.discount_type || 'NONE',
            discount_value: l.discount_value || 0,
            gst_rate: l.gst_rate || 0
          };
        })
      });
    }
  }, [quotation, units, reset]);

  const calculateMutation = useMutation({
    mutationFn: ordersApi.calculate,
  });

  const createMutation = useMutation({
    mutationFn: ordersApi.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      alert(`Order Draft Created! ID: ${data.id}`);
      navigate(isPurchase ? '/supply-in' : '/supply-out');
    },
    onError: (error: any) => {
      setApiError(error.message || 'Failed to create order');
    }
  });

  // Debounced calculate
  useEffect(() => {
    if (!watchAll.lines || watchAll.lines.length === 0) return;
    
    // Quick validation before hitting backend
    const isValidForCalc = watchAll.lines.every((l: any) => l.item_name && l.quantity > 0 && l.unit_id);
    if (!isValidForCalc) return;

    const timeoutId = setTimeout(() => {
      const calcData: SupplyOrderCalculateRequest = {
        tax_treatment: watchAll.tax_treatment as 'GST' | 'WITHOUT_GST',
        party_id: watchAll.party_id || null,
        place_of_supply: watchAll.place_of_supply || '29', // Default state code fallback
        lines: watchAll.lines.map((l: any) => ({
          item_id: l.item_id,
          item_name: l.item_name,
          sku: l.sku,
          description: l.description,
          hsn_sac: l.hsn_sac,
          quantity: Number(l.quantity) || 0,
          unit_id: l.unit_id,
          unit_name: l.unit_name || 'Unit',
          unit_symbol: l.unit_symbol || 'U',
          rate: Number(l.rate) || 0,
          discount_type: l.discount_type,
          discount_value: Number(l.discount_value) || 0,
          gst_rate: Number(l.gst_rate) || 0,
        }))
      };
      
      calculateMutation.mutate(calcData);
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [JSON.stringify(watchAll.lines), watchAll.party_id, watchAll.place_of_supply, watchAll.tax_treatment]);

  const handleItemSelect = (index: number, itemId: string) => {
    const item = items.find((i: any) => i.id.toString() === itemId);
    if (item) {
      setValue(`lines.${index}.item_id`, item.id.toString());
      setValue(`lines.${index}.item_name`, item.name);
      setValue(`lines.${index}.sku`, item.sku || '');
      setValue(`lines.${index}.description`, item.description || '');
      setValue(`lines.${index}.hsn_sac`, item.hsn_sac || '');
      setValue(`lines.${index}.rate`, isPurchase ? (item.purchase_price || 0) : item.sale_price);
      setValue(`lines.${index}.gst_rate`, item.gst_rate);
      
      const unit = units.find((u: any) => u.id === item.unit_id);
      if (unit) {
        setValue(`lines.${index}.unit_id`, unit.id.toString());
        setValue(`lines.${index}.unit_name`, unit.name);
        setValue(`lines.${index}.unit_symbol`, unit.abbreviation);
      }
    }
  };

  const handlePartySelect = (partyId: string) => {
    const party = parties.find((p: any) => p.id === partyId);
    if (party) {
      setValue('place_of_supply', party.state_code);
    }
  };

  const handleUnitSelect = (index: number, unitId: string) => {
    const unit = units.find((u: any) => u.id.toString() === unitId);
    if (unit) {
      setValue(`lines.${index}.unit_id`, unit.id.toString());
      setValue(`lines.${index}.unit_name`, unit.name);
      setValue(`lines.${index}.unit_symbol`, unit.abbreviation);
    }
  };

  const onSubmit = (data: any) => {
    setApiError(null);
    createMutation.mutate(data as SupplyOrderCreateRequest);
  };

  const calcData = calculateMutation.data;
  const partyLabel = isPurchase ? 'Supplier' : 'Customer';

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-20">
      <div className="flex justify-between items-center border-b pb-4">
        <div>
          <h2 className="text-2xl font-bold text-foreground">
            {isPurchase ? 'Create Supply In (Purchase Order)' : 'Create Supply Out (Sales Order)'}
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">
            {quotationId ? 'Draft a new order from accepted quotation.' : `Draft a new ${isPurchase ? 'purchase' : 'sales'} order.`}
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {apiError && (
          <div className="bg-red-50 text-red-600 p-4 rounded-md text-sm border border-red-100 font-medium">
            Error: {apiError}
          </div>
        )}

        {/* Header Information */}
        <div className="bg-card p-6 rounded-lg shadow-sm border grid grid-cols-1 md:grid-cols-4 gap-6">
          
          <div className="md:col-span-4 border-b pb-4 mb-2 flex space-x-6">
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Order Type</label>
              <div className="flex items-center space-x-2 mt-2">
                <input type="radio" value="PURCHASE" disabled {...register('order_type')} /> <span className="text-sm">Purchase Order</span>
                <input type="radio" value="SALES" disabled {...register('order_type')} className="ml-4" /> <span className="text-sm">Sales Order</span>
              </div>
            </div>
            
            <div className="pl-6 border-l">
              <label className="block text-sm font-medium text-muted-foreground mb-1">Tax Treatment</label>
              <div className="flex items-center space-x-2 mt-2">
                <input type="radio" value="GST" {...register('tax_treatment')} /> <span className="text-sm">GST</span>
                <input type="radio" value="WITHOUT_GST" {...register('tax_treatment')} className="ml-4" /> <span className="text-sm">Without GST</span>
              </div>
            </div>
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-muted-foreground mb-1">{partyLabel}</label>
            <select 
              className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500"
              {...register('party_id')}
              onChange={(e) => {
                register('party_id').onChange(e);
                handlePartySelect(e.target.value);
              }}
            >
              <option value="">Select {partyLabel}...</option>
              {parties.map((p: any) => (
                <option key={p.id} value={p.id}>{p.legal_name} {p.gstin ? `(${p.gstin})` : ''}</option>
              ))}
            </select>
            {errors.party_id?.message && <p className="mt-1 text-sm text-red-600">{errors.party_id.message as string}</p>}
          </div>

          <Input label="Order Date" type="date" {...register('order_date')} error={errors.order_date?.message} />
          <Input label="Expected Date" type="date" {...register('expected_date')} error={errors.expected_date?.message} />
          
          <div className="md:col-span-2">
            <Input label="Place of Supply (State Code)" {...register('place_of_supply')} error={errors.place_of_supply?.message} placeholder="e.g. 29" />
          </div>
        </div>

        {/* Invoice Lines */}
        <div className="bg-card p-6 rounded-lg shadow-sm border space-y-4">
          <h3 className="text-lg font-medium text-foreground border-b pb-2 mb-4">Items & Services</h3>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-border text-sm">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-3 py-2 text-left font-medium text-muted-foreground w-1/4">Item / Product</th>
                  <th className="px-3 py-2 text-left font-medium text-muted-foreground w-24">HSN/SKU</th>
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-24">Qty</th>
                  <th className="px-3 py-2 text-left font-medium text-muted-foreground w-28">Unit</th>
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-28">Rate (₹)</th>
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-24">Discount</th>
                  {taxTreatment === 'GST' && <th className="px-3 py-2 text-right font-medium text-muted-foreground w-20">GST %</th>}
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-32">Amount</th>
                  <th className="px-3 py-2 w-10"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {fields.map((field, index) => {
                  const calculatedLine = calcData?.lines?.[index];
                  return (
                    <tr key={field.id} className="hover:bg-muted/50">
                      <td className="px-3 py-2">
                        <select 
                          className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1 mb-1"
                          onChange={(e) => handleItemSelect(index, e.target.value)}
                        >
                          <option value="">Select Item...</option>
                          {items.map((i: any) => (
                            <option key={i.id} value={i.id}>{i.name}</option>
                          ))}
                        </select>
                        <input type="text" placeholder="Item Name" className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.item_name`)} />
                      </td>
                      <td className="px-3 py-2 space-y-1">
                        <input type="text" placeholder="HSN" className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.hsn_sac`)} />
                        <input type="text" placeholder="SKU" className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.sku`)} />
                      </td>
                      <td className="px-3 py-2">
                        <input type="number" step="any" className="block w-full text-right rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.quantity`)} />
                      </td>
                      <td className="px-3 py-2">
                        <select 
                          className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1"
                          {...register(`lines.${index}.unit_id`)}
                          onChange={(e) => {
                            register(`lines.${index}.unit_id`).onChange(e);
                            handleUnitSelect(index, e.target.value);
                          }}
                        >
                          <option value="">Unit...</option>
                          {units.map((u: any) => (
                            <option key={u.id} value={u.id}>{u.abbreviation}</option>
                          ))}
                        </select>
                      </td>
                      <td className="px-3 py-2">
                        <input type="number" step="any" className="block w-full text-right rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.rate`)} />
                      </td>
                      <td className="px-3 py-2">
                        <div className="flex space-x-1">
                          <input type="number" step="any" className="block w-full text-right rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.discount_value`)} />
                          <select className="block rounded border-input shadow-sm text-xs border px-1 py-1 bg-muted/50" {...register(`lines.${index}.discount_type`)}>
                            <option value="NONE">None</option>
                            <option value="PERCENT">%</option>
                            <option value="FIXED">₹</option>
                          </select>
                        </div>
                      </td>
                      {taxTreatment === 'GST' && (
                        <td className="px-3 py-2">
                          <input type="number" step="any" className="block w-full text-right rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.gst_rate`)} />
                        </td>
                      )}
                      <td className="px-3 py-2 text-right font-medium text-foreground bg-muted/50">
                        {calculateMutation.isPending ? '...' : (calculatedLine?.line_total ? `₹${calculatedLine.line_total.toFixed(2)}` : '₹0.00')}
                      </td>
                      <td className="px-3 py-2 text-center">
                        <button type="button" onClick={() => remove(index)} className="text-red-500 hover:text-red-700 font-bold p-1">×</button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
          
          <Button 
            type="button" 
            variant="secondary" 
            onClick={() => append({ item_name: '', quantity: 1, rate: 0, discount_type: 'NONE', discount_value: 0, gst_rate: 0, unit_name: '', unit_symbol: '', unit_id: '' })}
          >
            + Add Line
          </Button>
        </div>

        {/* Totals & Notes */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Order Notes</label>
              <textarea rows={3} className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('notes')} />
            </div>
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Terms & Conditions</label>
              <textarea rows={3} className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('terms')} />
            </div>
          </div>

          <div className="bg-card p-6 rounded-lg shadow-sm border">
            <h3 className="text-lg font-medium text-foreground border-b pb-2 mb-4">Order Summary</h3>
            
            <div className="space-y-3 text-sm">
              <div className="flex justify-between text-muted-foreground">
                <span>Gross Amount</span>
                <span>₹{(calcData?.subtotal || 0).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-red-600">
                <span>Discount</span>
                <span>- ₹{(calcData?.discount_total || 0).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-foreground font-medium pt-2 border-t">
                <span>{taxTreatment === 'GST' ? 'Taxable Value' : 'Net Amount'}</span>
                <span>₹{(calcData?.taxable_total || 0).toFixed(2)}</span>
              </div>
              
              {taxTreatment === 'GST' && (
                <>
                  {(calcData?.igst_total || 0) > 0 ? (
                    <div className="flex justify-between text-muted-foreground">
                      <span>IGST</span>
                      <span>₹{(calcData?.igst_total || 0).toFixed(2)}</span>
                    </div>
                  ) : (
                    <>
                      <div className="flex justify-between text-muted-foreground">
                        <span>CGST</span>
                        <span>₹{(calcData?.cgst_total || 0).toFixed(2)}</span>
                      </div>
                      <div className="flex justify-between text-muted-foreground">
                        <span>SGST / UTGST</span>
                        <span>₹{(calcData?.sgst_total || 0).toFixed(2)}</span>
                      </div>
                    </>
                  )}
                </>
              )}

              <div className="flex justify-between text-xl font-bold text-foreground pt-4 border-t mt-4">
                <span>Grand Total</span>
                <span>₹{(calcData?.grand_total || 0).toFixed(2)}</span>
              </div>

              {calcData?.amount_in_words && (
                <div className="text-xs text-muted-foreground text-right italic mt-1">
                  Rupees {calcData.amount_in_words}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="fixed bottom-0 left-0 right-0 bg-card border-t p-4 shadow-lg flex justify-end space-x-4 z-10 md:ml-64">
          <Button type="button" variant="secondary" onClick={() => navigate(isPurchase ? '/supply-in' : '/supply-out')}>Cancel</Button>
          <Button type="submit" isLoading={createMutation.isPending} disabled={calculateMutation.isPending || !calcData?.grand_total}>
            Save Draft Order
          </Button>
        </div>
      </form>
    </div>
  );
}

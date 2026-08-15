import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { adjustmentNotesApi } from '../../api/adjustmentNotes';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { InvoiceReferenceSelector } from '../../components/invoice/InvoiceReferenceSelector';
import { type InvoiceResponse } from '../../api/invoices';

const schema = z.object({
  party_id: z.string().min(1, "Party is required"),
  party_role: z.enum(['CUSTOMER', 'SUPPLIER']),
  note_date: z.string().min(1, "Date is required"),
  reason_code: z.string().min(1, "Reason is required"),
  tax_treatment: z.enum(['GST', 'WITHOUT_GST']),
  place_of_supply: z.string().min(1, "Place of supply is required"),
});

type FormData = z.infer<typeof schema>;

export default function AdjustmentNoteBuilderPage({ noteType }: { noteType: 'CREDIT_NOTE' | 'DEBIT_NOTE' }) {
  const navigate = useNavigate();
  const [sourceInvoice, setSourceInvoice] = useState<InvoiceResponse | null>(null);

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
    values: sourceInvoice ? {
      party_id: sourceInvoice.customer_id,
      party_role: 'CUSTOMER',
      note_date: new Date().toISOString().split('T')[0],
      reason_code: 'SALES_RETURN',
      tax_treatment: sourceInvoice.tax_treatment as any,
      place_of_supply: sourceInvoice.place_of_supply || '',
    } : undefined
  });

  const createMutation = useMutation({
    mutationFn: adjustmentNotesApi.create,
    onSuccess: () => {
      navigate(`/${noteType === 'CREDIT_NOTE' ? 'credit-notes' : 'debit-notes'}`);
    }
  });

  const onSubmit = (data: FormData) => {
    createMutation.mutate({
      note_type: noteType,
      ...data,
      lines: [] // Expand with a LineItem builder component
    });
  };

  if (!sourceInvoice) {
    return (
      <InvoiceReferenceSelector 
        onSelect={setSourceInvoice} 
        title={`Select Invoice for ${noteType === 'CREDIT_NOTE' ? 'Credit Note' : 'Debit Note'}`}
      />
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">New {noteType === 'CREDIT_NOTE' ? 'Credit Note' : 'Debit Note'}</h1>
        <Button variant="outline" onClick={() => setSourceInvoice(null)}>Change Invoice</Button>
      </div>

      <div className="bg-muted p-4 rounded-lg flex justify-between">
        <div>
          <p className="text-sm text-muted-foreground">Original Invoice</p>
          <p className="font-bold">{sourceInvoice.invoice_number}</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground">Customer</p>
          <p className="font-bold">{sourceInvoice.customer_name_snapshot}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-muted-foreground">Amount</p>
          <p className="font-bold">₹{sourceInvoice.grand_total.toFixed(2)}</p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Party ID</label>
            <Input {...register('party_id')} disabled />
            {errors.party_id && <p className="text-red-500 text-xs mt-1">{errors.party_id.message}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Party Role</label>
            <select {...register('party_role')} className="w-full p-2 border rounded-md" disabled>
              <option value="CUSTOMER">Customer</option>
              <option value="SUPPLIER">Supplier</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Date</label>
            <Input type="date" {...register('note_date')} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Reason Code</label>
            <select {...register('reason_code')} className="w-full p-2 border rounded-md">
              <option value="SALES_RETURN">Sales Return</option>
              <option value="EXCESS_BILLING">Excess Billing</option>
              <option value="EXCESS_TAX">Excess Tax</option>
              <option value="POST_SALE_DISCOUNT">Post-Sale Discount</option>
              <option value="UNDER_BILLING">Under Billing</option>
              <option value="SHORT_CHARGED_TAX">Short-charged Tax</option>
              <option value="OTHER">Other</option>
            </select>
          </div>
        </div>

        <div className="flex justify-end pt-4">
          <Button type="submit" disabled={createMutation.isPending}>
            {createMutation.isPending ? 'Saving...' : 'Create Note'}
          </Button>
        </div>
      </form>
    </div>
  );
}

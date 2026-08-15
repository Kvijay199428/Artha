import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { partiesApi } from '../../api/parties';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { GSTINInput, PhoneInput, BankAccountTypeSelect } from '../../components/gst';

const partySchema = z.object({
  legal_name: z.string().min(1, 'Legal name is required'),
  trade_name: z.string().optional(),
  party_type: z.string().min(1, 'Party type is required'),
  account_type: z.string().min(1, 'Account type is required'),
  contact_person: z.string().optional(),
  mobile: z.string().optional(),
  mobile_country_code: z.string().optional(),
  mobile_e164: z.string().optional(),
  office_phone: z.string().optional(),
  office_phone_country_code: z.string().optional(),
  office_phone_e164: z.string().optional(),
  email: z.string().email('Invalid email').optional().or(z.literal('')),
  website: z.string().optional(),
  gstin: z.string().optional(),
  gst_registration_type: z.string().optional(),
  pan: z.string().optional(),
  tan: z.string().optional(),
  state: z.string().min(1, 'State is required'),
  state_code: z.string().min(1, 'State code is required'),
  bank_account_type: z.string().optional(),
});

type PartyForm = z.infer<typeof partySchema>;

export default function PartiesPage() {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const [gstinValid, setGstinValid] = useState(false);

  const { data: parties = [], isLoading } = useQuery({
    queryKey: ['parties'],
    queryFn: () => partiesApi.getAll()
  });

  const { register, handleSubmit, watch, setValue, control, formState: { errors }, reset } = useForm<PartyForm>({
    resolver: zodResolver(partySchema),
    defaultValues: {
      party_type: 'BUSINESS',
      account_type: 'CUSTOMER',
      gst_registration_type: 'UNREGISTERED',
      state: 'Karnataka',
      state_code: '29',
      mobile_country_code: '+91',
      office_phone_country_code: '+91',
    }
  });

  const createMutation = useMutation({
    mutationFn: partiesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['parties'] });
      setIsModalOpen(false);
      reset();
      setGstinValid(false);
    },
    onError: (error: any) => {
      setApiError(error.message || 'Failed to create party');
    }
  });

  const onSubmit = (data: PartyForm) => {
    setApiError(null);
    createMutation.mutate(data);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Customers & Suppliers</h2>
          <p className="mt-1 text-sm text-muted-foreground">Manage your sundry debtors and creditors.</p>
        </div>
        <Button onClick={() => { setIsModalOpen(true); reset(); setGstinValid(false); }}>Add New Party</Button>
      </div>

      {isLoading ? (
        <div>Loading parties...</div>
      ) : (
        <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
          <table className="min-w-full divide-y divide-border">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Party Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">GSTIN / Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Contact</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">State</th>
              </tr>
            </thead>
            <tbody className="bg-card divide-y divide-border">
              {parties.map((party) => (
                <tr key={party.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-foreground">{party.legal_name}</div>
                    {party.trade_name && <div className="text-xs text-muted-foreground">{party.trade_name}</div>}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${party.account_type === 'CUSTOMER' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'}`}>
                      {party.account_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-foreground">{party.gstin || 'No GSTIN'}</div>
                    <div className="text-xs text-muted-foreground">{party.gst_registration_type}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                    <div>{party.contact_person || '-'}</div>
                    <div>{party.mobile || '-'}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                    {party.state} ({party.state_code})
                  </td>
                </tr>
              ))}
              {parties.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-muted-foreground">
                    No parties found. Click "Add New Party" to create one.
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
              <h3 className="text-lg font-medium leading-6 text-foreground mb-4 border-b pb-2">Add New Party</h3>
              
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                {apiError && (
                  <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm border border-red-100">
                    {apiError}
                  </div>
                )}
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Basic Details */}
                  <div className="md:col-span-2 grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-muted-foreground mb-1">Account Type</label>
                      <select className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('account_type')}>
                        <option value="CUSTOMER">Customer (Debtor)</option>
                        <option value="VENDOR">Vendor (Creditor)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-muted-foreground mb-1">Party Type</label>
                      <select className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('party_type')}>
                        <option value="BUSINESS">Business (B2B)</option>
                        <option value="INDIVIDUAL">Individual (B2C)</option>
                      </select>
                    </div>
                  </div>

                  <Input label="Legal Name" {...register('legal_name')} error={errors.legal_name?.message} />
                  <Input label="Trade Name (Optional)" {...register('trade_name')} error={errors.trade_name?.message} />
                  
                  {/* Tax Details */}
                  <div className="md:col-span-2 bg-muted p-4 rounded-md border border">
                    <h4 className="text-sm font-semibold text-muted-foreground mb-3">Tax & Location Details</h4>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-muted-foreground mb-1">GST Registration</label>
                        <select className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('gst_registration_type')}>
                          <option value="REGISTERED">Registered Regular</option>
                          <option value="COMPOSITION">Registered Composition</option>
                          <option value="UNREGISTERED">Unregistered</option>
                          <option value="CONSUMER">Consumer</option>
                        </select>
                      </div>
                      
                      <Controller
                        name="gstin"
                        control={control}
                        render={({ field }) => (
                          <GSTINInput
                            label="GSTIN"
                            value={field.value || ''}
                            onChange={(v) => field.onChange(v)}
                            error={errors.gstin?.message}
                            onValidated={(parsed, valid) => {
                              if (valid && parsed) {
                                setValue('state_code', parsed.stateCode, { shouldValidate: true });
                                setValue('state', parsed.stateName || '', { shouldValidate: true });
                                setValue('pan', parsed.pan, { shouldValidate: true });
                                setGstinValid(true);
                              } else {
                                setGstinValid(false);
                              }
                            }}
                          />
                        )}
                      />
                      
                      <Input 
                        label="PAN" 
                        {...register('pan')} 
                        error={errors.pan?.message}
                        disabled={gstinValid}
                        className={gstinValid ? "bg-gray-100" : ""}
                      />

                      <Input label="TAN" {...register('tan')} error={errors.tan?.message} />
                      
                      <div className="grid grid-cols-2 gap-2 col-span-2 md:col-span-1">
                        <Input 
                          label="State" 
                          {...register('state')} 
                          error={errors.state?.message} 
                          placeholder="e.g. Karnataka"
                          readOnly={gstinValid}
                          className={gstinValid ? "bg-muted cursor-not-allowed" : ""}
                        />
                        <Input 
                          label="State Code" 
                          {...register('state_code')} 
                          error={errors.state_code?.message} 
                          placeholder="e.g. 29"
                          readOnly={gstinValid}
                          className={gstinValid ? "bg-muted cursor-not-allowed" : ""}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Bank Details */}
                  <div className="md:col-span-2">
                    <h4 className="text-sm font-semibold text-muted-foreground mb-3">Bank Information</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <BankAccountTypeSelect 
                        label="Bank Account Type" 
                        {...register('bank_account_type')} 
                        error={errors.bank_account_type?.message} 
                      />
                    </div>
                  </div>

                  {/* Contact Details */}
                  <div className="md:col-span-2">
                    <h4 className="text-sm font-semibold text-muted-foreground mb-3">Contact Information</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <Input label="Contact Person" {...register('contact_person')} error={errors.contact_person?.message} />
                      
                      <PhoneInput 
                        label="Mobile Number" 
                        value={watch('mobile') || ''} 
                        countryCode={watch('mobile_country_code') || '+91'} 
                        onValueChange={(phone, cc, e164, _iso) => { 
                          setValue('mobile', phone); 
                          setValue('mobile_country_code', cc); 
                          setValue('mobile_e164', e164); 
                        }} 
                        error={errors.mobile?.message}
                      />

                      <PhoneInput 
                        label="Office Contact" 
                        optional 
                        value={watch('office_phone') || ''} 
                        countryCode={watch('office_phone_country_code') || '+91'} 
                        onValueChange={(phone, cc, e164, _iso) => { 
                          setValue('office_phone', phone); 
                          setValue('office_phone_country_code', cc); 
                          setValue('office_phone_e164', e164); 
                        }} 
                        error={errors.office_phone?.message}
                      />

                      <Input label="Email Address" type="email" {...register('email')} error={errors.email?.message} />
                      
                      <Input label="Website" type="url" {...register('website')} placeholder="https://..." error={errors.website?.message} />
                    </div>
                  </div>
                </div>

                <div className="pt-4 border-t flex justify-end space-x-3">
                  <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
                  <Button type="submit" isLoading={createMutation.isPending}>Save Party</Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

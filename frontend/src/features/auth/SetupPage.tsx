import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { authApi } from '../../api/auth';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { GSTINInput, PhoneInput, BankAccountTypeSelect } from '../../components/gst';

const setupSchema = z.object({
  company_name: z.string().min(1, 'Company Name is required'),
  ownership_type: z.string().min(1, 'Ownership Type is required'),
  mobile: z.string().min(1, 'Mobile is required'),
  mobile_country_code: z.string().optional(),
  mobile_e164: z.string().optional(),
  email: z.string().email('Invalid email address'),
  authorized_person_name: z.string().min(1, 'Authorized Person is required'),
  gst_registered: z.boolean(),
  gstin: z.string().optional(),
  address_line_1: z.string().min(1, 'Address is required'),
  city: z.string().min(1, 'City is required'),
  district: z.string().min(1, 'District is required'),
  state: z.string().min(1, 'State is required'),
  state_code: z.string().length(2, 'State Code must be 2 digits'),
  pincode: z.string().length(6, 'Pincode must be 6 digits'),
  country: z.string().default('India'),
  bank_account_holder_name: z.string().min(1, 'Account Holder Name is required'),
  bank_account_number: z.string().min(1, 'Account Number is required'),
  bank_ifsc: z.string().min(1, 'IFSC is required'),
  bank_name: z.string().min(1, 'Bank Name is required'),
  bank_branch: z.string().min(1, 'Branch is required'),
  bank_account_type: z.string().min(1, 'Account Type is required'),
  pin: z.string().length(4, 'PIN must be exactly 4 digits').regex(/^\d+$/, 'PIN must contain only numbers'),
  confirm_pin: z.string().length(4, 'PIN must be exactly 4 digits'),
}).refine((data) => data.pin === data.confirm_pin, {
  message: "PINs don't match",
  path: ["confirm_pin"],
}).refine((data) => {
  if (data.gst_registered) return !!data.gstin && data.gstin.length === 15;
  return true;
}, {
  message: "Valid GSTIN is required if GST registered",
  path: ["gstin"],
});

type SetupForm = z.infer<typeof setupSchema>;

export default function SetupPage() {
  const navigate = useNavigate();
  const [apiError, setApiError] = useState<string | null>(null);
  const [gstinValid, setGstinValid] = useState(false);

  const { register, handleSubmit, watch, setValue, control, formState: { errors } } = useForm<any>({
    resolver: zodResolver(setupSchema),
    defaultValues: {
      gst_registered: true,
      country: 'India',
      ownership_type: 'Proprietorship',
      bank_account_type: 'CURRENT',
      mobile_country_code: '+91'
    }
  });

  const isGstRegistered = watch('gst_registered');

  const mutation = useMutation({
    mutationFn: authApi.setup,
    onSuccess: () => {
      navigate('/login');
    },
    onError: (error: any) => {
      setApiError(error.message || 'Setup failed. Please check your inputs.');
    }
  });

  const onSubmit = (data: any) => {
    setApiError(null);
    mutation.mutate(data as SetupForm);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-8 bg-white p-10 rounded-xl shadow-lg border border-gray-100">
        <div>
          <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight">
            Company Setup
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Initialize your organization profile to start billing.
          </p>
        </div>
        
        <form className="mt-8 space-y-8" onSubmit={handleSubmit(onSubmit)}>
          {apiError && (
            <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm border border-red-100">
              {apiError}
            </div>
          )}
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-6 md:col-span-2">
              <h3 className="text-lg font-medium border-b pb-2 text-gray-800">Basic Details</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input label="Company Name" {...register('company_name')} error={errors.company_name?.message as string} />
                <Input label="Ownership Type" {...register('ownership_type')} error={errors.ownership_type?.message as string} />
                
                <PhoneInput 
                  label="Mobile" 
                  value={watch('mobile') || ''} 
                  countryCode={watch('mobile_country_code') || '+91'} 
                  onValueChange={(phone, cc, e164) => { 
                    setValue('mobile', phone); 
                    setValue('mobile_country_code', cc); 
                    setValue('mobile_e164', e164); 
                  }} 
                  error={errors.mobile?.message as string}
                />

                <Input label="Email" type="email" {...register('email')} error={errors.email?.message as string} />
                <Input label="Authorized Person" {...register('authorized_person_name')} error={errors.authorized_person_name?.message as string} />
              </div>
            </div>

            <div className="space-y-6 md:col-span-2">
              <h3 className="text-lg font-medium border-b pb-2 text-gray-800">Tax Details</h3>
              <div className="grid grid-cols-1 gap-6">
                <div className="flex items-center h-10">
                  <input type="checkbox" id="gst_registered" className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" {...register('gst_registered')} />
                  <label htmlFor="gst_registered" className="ml-2 block text-sm text-gray-900">GST Registered</label>
                </div>
                {isGstRegistered && (
                  <Controller
                    name="gstin"
                    control={control}
                    render={({ field }) => (
                      <GSTINInput
                        label="GSTIN"
                        value={field.value || ''}
                        onChange={(v) => field.onChange(v)}
                        error={errors.gstin?.message as string}
                        onValidated={(parsed, valid) => {
                          if (valid && parsed) {
                            setValue('state_code', parsed.stateCode, { shouldValidate: true });
                            setValue('state', parsed.stateName || '', { shouldValidate: true });
                            setGstinValid(true);
                          } else {
                            setGstinValid(false);
                          }
                        }}
                      />
                    )}
                  />
                )}
              </div>
            </div>

            <div className="space-y-6 md:col-span-2">
              <h3 className="text-lg font-medium border-b pb-2 text-gray-800">Address</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input label="Address Line 1" className="md:col-span-2" {...register('address_line_1')} error={errors.address_line_1?.message as string} />
                <Input label="City" {...register('city')} error={errors.city?.message as string} />
                <Input label="District" {...register('district')} error={errors.district?.message as string} />
                <Input 
                  label="State" 
                  {...register('state')} 
                  error={errors.state?.message as string} 
                  readOnly={isGstRegistered && gstinValid}
                  className={isGstRegistered && gstinValid ? "bg-gray-100 cursor-not-allowed" : ""}
                />
                <Input 
                  label="State Code (e.g. 27 for MH)" 
                  {...register('state_code')} 
                  error={errors.state_code?.message as string} 
                  readOnly={isGstRegistered && gstinValid}
                  className={isGstRegistered && gstinValid ? "bg-gray-100 cursor-not-allowed" : ""}
                />
                <Input label="Pincode" {...register('pincode')} error={errors.pincode?.message as string} />
              </div>
            </div>

            <div className="space-y-6 md:col-span-2">
              <h3 className="text-lg font-medium border-b pb-2 text-gray-800">Bank Details</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input label="Account Holder Name" {...register('bank_account_holder_name')} error={errors.bank_account_holder_name?.message as string} />
                <Input label="Account Number" {...register('bank_account_number')} error={errors.bank_account_number?.message as string} />
                <Input label="IFSC Code" {...register('bank_ifsc')} error={errors.bank_ifsc?.message as string} />
                <Input label="Bank Name" {...register('bank_name')} error={errors.bank_name?.message as string} />
                <Input label="Branch" {...register('bank_branch')} error={errors.bank_branch?.message as string} />
                
                <BankAccountTypeSelect 
                  label="Account Type" 
                  {...register('bank_account_type')} 
                  error={errors.bank_account_type?.message as string} 
                />
              </div>
            </div>

            <div className="space-y-6 md:col-span-2">
              <h3 className="text-lg font-medium border-b pb-2 text-gray-800">Security</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input label="Create 4-Digit Login PIN" type="password" maxLength={4} {...register('pin')} error={errors.pin?.message as string} />
                <Input label="Confirm PIN" type="password" maxLength={4} {...register('confirm_pin')} error={errors.confirm_pin?.message as string} />
              </div>
            </div>

          </div>

          <div className="pt-5 border-t">
            <Button
              type="submit"
              className="w-full md:w-auto px-8"
              isLoading={mutation.isPending}
            >
              Complete Setup
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

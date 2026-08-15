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

// ── Schema ────────────────────────────────────────────────────────────────────
const setupSchema = z.object({
  // Business
  company_name: z.string().min(2, 'Company name must be at least 2 characters'),
  ownership_type: z.string().min(1, 'Ownership type is required'),
  authorized_person_name: z.string().min(1, 'Authorized person name is required'),
  authorized_person_designation: z.string().optional(),
  // GST
  gst_registered: z.boolean(),
  gstin: z.string().optional(),
  tan: z.string().optional(),
  // Address
  address_line_1: z.string().min(1, 'Address is required'),
  address_line_2: z.string().optional(),
  city: z.string().min(1, 'City is required'),
  district: z.string().optional(),
  state: z.string().min(1, 'State is required'),
  state_code: z.string().min(1, 'State code is required'),
  pincode: z.string().min(4, 'Valid pincode required').max(10),
  country: z.string().default('India'),
  // Contact
  mobile: z.string().min(7, 'Mobile number required'),
  mobile_country_code: z.string().default('+91'),
  mobile_e164: z.string().optional(),
  office_phone: z.string().optional(),
  office_phone_country_code: z.string().optional(),
  office_phone_e164: z.string().optional(),
  email: z.string().email('Valid email required'),
  website: z.string().optional(),
  // Security
  pin: z.string().length(4, 'PIN must be exactly 4 digits').regex(/^\d{4}$/, 'PIN must be digits'),
  confirm_pin: z.string().length(4, 'Confirm PIN must be 4 digits'),
  // Bank — all optional
  bank_account_holder_name: z.string().optional(),
  bank_account_number: z.string().optional(),
  bank_ifsc: z.string().optional(),
  bank_name: z.string().optional(),
  bank_branch: z.string().optional(),
  bank_account_type: z.string().optional(),
}).refine(d => d.pin === d.confirm_pin, {
  message: "PINs don't match",
  path: ['confirm_pin'],
}).refine(d => {
  if (d.gst_registered && d.gstin && d.gstin.length > 0) {
    return d.gstin.length === 15;
  }
  return true;
}, { message: 'GSTIN must be exactly 15 characters', path: ['gstin'] });

type SetupForm = z.infer<typeof setupSchema>;

const OWNERSHIP_TYPES = [
  'Proprietorship', 'Partnership', 'LLP',
  'Private Limited', 'Public Limited', 'OPC',
  'HUF', 'Trust', 'Society', 'Other',
];

const TABS = [
  { id: 0, label: 'Business',  icon: '🏢' },
  { id: 1, label: 'GST & Tax', icon: '📋' },
  { id: 2, label: 'Address',   icon: '📍' },
  { id: 3, label: 'Contact',   icon: '📞' },
  { id: 4, label: 'Security',  icon: '🔐' },
  { id: 5, label: 'Bank',      icon: '🏦', optional: true },
];

// Removed CreationTransition

// ── Main wizard ───────────────────────────────────────────────────────────────
export default function SetupPage() {
  const navigate = useNavigate();
  const [tab, setTab]                 = useState(0);
  const [apiError, setApiError]       = useState<string | null>(null);
  const [gstinValid, setGstinValid]   = useState(false);
  const [skipBank, setSkipBank]       = useState(false);

  const {
    register, handleSubmit, watch, setValue, control,
    trigger, formState: { errors },
  } = useForm<any>({
    resolver: zodResolver(setupSchema),
    mode: 'onBlur',
    defaultValues: {
      gst_registered: true,
      country: 'India',
      ownership_type: 'Proprietorship',
      bank_account_type: 'CURRENT',
      mobile_country_code: '+91',
      office_phone_country_code: '+91',
    },
  });

  const mutation = useMutation({
    mutationFn: authApi.setup,
    onSuccess: () => navigate('/login'),
    onError: (error: any) => {
      setApiError(error.message || 'Setup failed. Please check your inputs.');
    },
  });

  const isGstRegistered = watch('gst_registered');
  const currentPin      = watch('pin');
  const confirmPin      = watch('confirm_pin');
  const stateValue      = watch('state');

  const pinsMatch    = currentPin?.length === 4 && confirmPin?.length === 4 && currentPin === confirmPin;
  const pinsMismatch = confirmPin?.length === 4 && currentPin !== confirmPin;

  const onSubmit = (data: SetupForm) => {
    setApiError(null);
    if (skipBank) {
      data = { ...data };
      delete (data as any).bank_account_holder_name;
      delete (data as any).bank_account_number;
      delete (data as any).bank_ifsc;
      delete (data as any).bank_name;
      delete (data as any).bank_branch;
      delete (data as any).bank_account_type;
    }
    mutation.mutate(data as any);
  };

  // Fields to validate per tab before proceeding
  const tabFields: Record<number, (keyof SetupForm)[]> = {
    0: ['company_name', 'ownership_type', 'authorized_person_name'],
    1: ['gstin'],
    2: ['address_line_1', 'city', 'state', 'state_code', 'pincode'],
    3: ['mobile', 'email'],
    4: ['pin', 'confirm_pin'],
    5: [],
  };

  const goNext = async () => {
    const valid = await trigger(tabFields[tab]);
    if (valid) setTab(t => Math.min(t + 1, TABS.length - 1));
  };

  const goBack = () => {
    setApiError(null);
    setTab(t => Math.max(t - 1, 0));
  };

  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 py-8 px-4">

        {/* ── Header / Branding ── */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-3">
            <div
              className="w-10 h-10 rounded-xl bg-slate-900 dark:bg-white flex items-center justify-center shadow-md"
              style={{ animation: 'waveFloat 3s ease-in-out infinite' }}
            >
              <span className="text-white dark:text-slate-900 text-lg font-black">A</span>
            </div>
            <span className="text-2xl font-black tracking-widest text-slate-900 dark:text-white uppercase">
              ARTHA
            </span>
          </div>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-2">Company Setup Wizard</p>
        </div>

        {/* ── Tab progress bar ── */}
        <div className="max-w-3xl mx-auto mb-6">
          <div className="flex items-center justify-center gap-1 flex-wrap">
            {TABS.map((t, i) => (
              <div key={t.id} className="flex items-center">
                <button
                  type="button"
                  onClick={() => i <= tab && setTab(i)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200 ${
                    i === tab
                      ? 'bg-slate-900 dark:bg-white text-white dark:text-slate-900 shadow-md'
                      : i < tab
                      ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 cursor-pointer'
                      : 'bg-slate-100 dark:bg-slate-700 text-slate-400 cursor-default'
                  }`}
                >
                  <span>{i < tab ? '✓' : t.icon}</span>
                  <span className="hidden sm:inline">{t.label}</span>
                  {t.optional && <span className="opacity-50 text-[10px]">(opt)</span>}
                </button>
                {i < TABS.length - 1 && (
                  <div className={`w-4 h-px mx-1 ${i < tab ? 'bg-green-400' : 'bg-slate-200 dark:bg-slate-600'}`} />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* ── Form card ── */}
        <div className="max-w-3xl mx-auto">
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-100 dark:border-slate-700 overflow-hidden">

            {apiError && (
              <div className="bg-red-50 dark:bg-red-900/20 border-b border-red-100 dark:border-red-800 px-6 py-3 text-sm text-red-600 dark:text-red-400">
                {apiError}
              </div>
            )}

            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="p-6 md:p-8 min-h-[360px]">

                {/* ── TAB 0: Business ── */}
                {tab === 0 && (
                  <div className="space-y-5">
                    <div>
                      <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Business Information</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">Your company's legal identity</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="md:col-span-2">
                        <Input
                          label="Legal Company Name"
                          {...register('company_name')}
                          error={errors.company_name?.message}
                          placeholder="e.g. Acme Pvt. Ltd."
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                          Ownership Type
                        </label>
                        <select
                          {...register('ownership_type')}
                          className="block w-full rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white text-sm px-3 py-2 outline-none focus:border-slate-500 transition-colors"
                        >
                          {OWNERSHIP_TYPES.map(t => (
                            <option key={t} value={t}>{t}</option>
                          ))}
                        </select>
                      </div>
                      <Input
                        label="Authorized Person"
                        {...register('authorized_person_name')}
                        error={errors.authorized_person_name?.message}
                        placeholder="Full legal name"
                      />
                      <div className="md:col-span-2">
                        <Input
                          label="Designation (Optional)"
                          {...register('authorized_person_designation')}
                          placeholder="e.g. Director, Proprietor, Managing Partner"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* ── TAB 1: GST & Tax ── */}
                {tab === 1 && (
                  <div className="space-y-5">
                    <div>
                      <h3 className="text-lg font-semibold text-slate-900 dark:text-white">GST & Tax Identity</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                        GSTIN automatically populates State Code and PAN
                      </p>
                    </div>
                    <div className="flex items-center gap-3">
                      <input
                        type="checkbox"
                        id="gst_reg"
                        className="w-4 h-4 rounded border-slate-300 text-slate-900 dark:text-white"
                        {...register('gst_registered')}
                      />
                      <label htmlFor="gst_reg" className="text-sm font-medium text-slate-700 dark:text-slate-300">
                        GST Registered
                      </label>
                    </div>

                    {isGstRegistered && (
                      <>
                        <Controller
                          name="gstin"
                          control={control}
                          render={({ field }) => (
                            <GSTINInput
                              label="GSTIN"
                              value={field.value || ''}
                              onChange={v => field.onChange(v)}
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
                        {gstinValid && (
                          <div className="grid grid-cols-2 gap-4">
                            <Input
                              label="State Code (auto-filled)"
                              {...register('state_code')}
                              readOnly
                              className="bg-slate-50 dark:bg-slate-700 cursor-not-allowed font-mono"
                            />
                            <Input
                              label="State (auto-filled)"
                              {...register('state')}
                              readOnly
                              className="bg-slate-50 dark:bg-slate-700 cursor-not-allowed"
                            />
                          </div>
                        )}
                      </>
                    )}

                    <Input
                      label="TAN (Optional)"
                      {...register('tan')}
                      placeholder="e.g. BLRA12345B"
                    />

                    <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-3">
                      <p className="text-xs text-amber-700 dark:text-amber-300">
                        ✓ Structural GSTIN validation (15-char format + checksum). Government portal verification not performed.
                      </p>
                    </div>
                  </div>
                )}

                {/* ── TAB 2: Address ── */}
                {tab === 2 && (
                  <div className="space-y-5">
                    <div>
                      <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Registered Address</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                        Your company's registered office address
                      </p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="md:col-span-2">
                        <Input
                          label="Address Line 1"
                          {...register('address_line_1')}
                          error={errors.address_line_1?.message}
                          placeholder="Street, Building No., Floor"
                        />
                      </div>
                      <div className="md:col-span-2">
                        <Input
                          label="Address Line 2 (Optional)"
                          {...register('address_line_2')}
                          placeholder="Area, Locality, Landmark"
                        />
                      </div>
                      <Input
                        label="City"
                        {...register('city')}
                        error={errors.city?.message}
                      />
                      <div>
                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                          District <span className="text-slate-400 font-normal text-xs">(Optional)</span>
                        </label>
                        <input
                          {...register('district')}
                          disabled={!stateValue}
                          placeholder={!stateValue ? 'Enter state first' : 'District'}
                          className={`block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors ${
                            !stateValue
                              ? 'bg-slate-50 dark:bg-slate-700/50 border-slate-200 dark:border-slate-600 text-slate-400 cursor-not-allowed'
                              : 'bg-white dark:bg-slate-700 border-slate-300 dark:border-slate-600 text-slate-900 dark:text-white focus:border-slate-500'
                          }`}
                        />
                      </div>
                      <Input
                        label="State"
                        {...register('state')}
                        error={errors.state?.message}
                        readOnly={gstinValid}
                        className={gstinValid ? 'bg-slate-50 dark:bg-slate-700 cursor-not-allowed' : ''}
                      />
                      <Input
                        label="State Code"
                        {...register('state_code')}
                        error={errors.state_code?.message}
                        readOnly={gstinValid}
                        className={gstinValid ? 'bg-slate-50 dark:bg-slate-700 cursor-not-allowed font-mono' : 'font-mono'}
                        maxLength={2}
                      />
                      <Input
                        label="Pincode"
                        {...register('pincode')}
                        error={errors.pincode?.message}
                        maxLength={10}
                        inputMode="numeric"
                      />
                      <Input
                        label="Country"
                        {...register('country')}
                        defaultValue="India"
                      />
                    </div>
                  </div>
                )}

                {/* ── TAB 3: Contact ── */}
                {tab === 3 && (
                  <div className="space-y-5">
                    <div>
                      <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Contact Details</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">How customers reach your business</p>
                    </div>
                    <PhoneInput
                      label="Mobile Number"
                      required
                      value={watch('mobile') || ''}
                      countryCode={watch('mobile_country_code') || '+91'}
                      onValueChange={(phone, cc, e164, _iso) => {
                        setValue('mobile', phone);
                        setValue('mobile_country_code', cc);
                        setValue('mobile_e164', e164);
                      }}
                      error={errors.mobile?.message as string}
                    />
                    <Input
                      label="Email"
                      type="email"
                      {...register('email')}
                      error={errors.email?.message}
                      placeholder="billing@yourcompany.com"
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
                    />
                    <Input
                      label="Website (Optional)"
                      type="url"
                      {...register('website')}
                      placeholder="https://www.yourcompany.com"
                    />
                  </div>
                )}

                {/* ── TAB 4: Security ── */}
                {tab === 4 && (
                  <div className="space-y-5">
                    <div>
                      <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Security PIN</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                        4-digit numeric PIN to access your dashboard
                      </p>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Input
                          label="Create PIN"
                          type="password"
                          inputMode="numeric"
                          maxLength={4}
                          placeholder="••••"
                          className="text-center text-2xl tracking-[0.5em]"
                          {...register('pin')}
                          error={errors.pin?.message}
                          onChange={(e) => {
                            const digits = e.target.value.replace(/\D/g, '').slice(0, 4);
                            setValue('pin', digits, { shouldValidate: true });
                          }}
                        />
                      </div>
                      <div>
                        <Input
                          label="Confirm PIN"
                          type="password"
                          inputMode="numeric"
                          maxLength={4}
                          placeholder="••••"
                          className="text-center text-2xl tracking-[0.5em]"
                          {...register('confirm_pin')}
                          error={errors.confirm_pin?.message}
                          onChange={(e) => {
                            const digits = e.target.value.replace(/\D/g, '').slice(0, 4);
                            setValue('confirm_pin', digits, { shouldValidate: true });
                          }}
                        />
                      </div>
                    </div>

                    {pinsMatch && (
                      <div className="flex items-center gap-2 text-green-600 dark:text-green-400 text-sm">
                        <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        PINs match
                      </div>
                    )}
                    {pinsMismatch && (
                      <div className="flex items-center gap-2 text-red-500 text-sm">
                        <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                        PINs don't match
                      </div>
                    )}

                    <div className="bg-slate-50 dark:bg-slate-700/50 border border-slate-200 dark:border-slate-600 rounded-lg p-3">
                      <p className="text-xs text-slate-500 dark:text-slate-400">
                        Your PIN is hashed server-side using bcrypt. After 5 failed attempts, the account locks for 15 minutes.
                      </p>
                    </div>
                  </div>
                )}

                {/* ── TAB 5: Bank (Optional) ── */}
                {tab === 5 && (
                  <div className="space-y-5">
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Bank Details</h3>
                        <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                          Optional — shown on invoices and receipts
                        </p>
                      </div>
                      <span className="text-xs bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400 px-2 py-1 rounded-full font-medium">
                        Optional
                      </span>
                    </div>

                    <div className="flex items-center gap-3 p-3 bg-slate-50 dark:bg-slate-700/50 rounded-lg border border-slate-200 dark:border-slate-600">
                      <input
                        type="checkbox"
                        id="skip_bank"
                        checked={skipBank}
                        onChange={e => setSkipBank(e.target.checked)}
                        className="w-4 h-4 rounded border-slate-300"
                      />
                      <label htmlFor="skip_bank" className="text-sm text-slate-600 dark:text-slate-300 cursor-pointer">
                        Skip bank details — I'll add them later from Settings
                      </label>
                    </div>

                    {!skipBank && (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Input
                          label="Account Holder Name"
                          {...register('bank_account_holder_name')}
                          placeholder="As per bank records"
                        />
                        <Input
                          label="Account Number"
                          {...register('bank_account_number')}
                        />
                        <Input
                          label="IFSC Code"
                          {...register('bank_ifsc')}
                          placeholder="e.g. SBIN0001234"
                          className="uppercase"
                          onChange={e => {
                            setValue('bank_ifsc', e.target.value.toUpperCase());
                          }}
                        />
                        <Input
                          label="Bank Name"
                          {...register('bank_name')}
                        />
                        <Input
                          label="Branch"
                          {...register('bank_branch')}
                        />
                        <BankAccountTypeSelect
                          label="Account Type"
                          {...register('bank_account_type')}
                        />
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* ── Footer navigation ── */}
              <div className="px-6 md:px-8 py-4 bg-slate-50 dark:bg-slate-900/50 border-t border-slate-100 dark:border-slate-700 flex items-center justify-between gap-3">
                <div>
                  {tab > 0 && (
                    <button
                      type="button"
                      onClick={goBack}
                      className="px-4 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-lg transition-colors hover:shadow-sm"
                    >
                      ← Back
                    </button>
                  )}
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 dark:text-slate-500 tabular-nums">
                    {tab + 1} / {TABS.length}
                  </span>
                  {tab < TABS.length - 1 ? (
                    <button
                      type="button"
                      onClick={goNext}
                      className="px-5 py-2 text-sm font-semibold text-white bg-slate-900 dark:bg-white dark:text-slate-900 rounded-lg hover:bg-slate-700 dark:hover:bg-slate-100 transition-colors shadow-sm active:scale-[0.97]"
                    >
                      Continue →
                    </button>
                  ) : (
                    <Button
                      type="submit"
                      isLoading={mutation.isPending}
                      className="px-6"
                    >
                      Complete Setup
                    </Button>
                  )}
                </div>
              </div>
            </form>
          </div>
        </div>

        {/* Wave animation */}
        <style>{`
          @keyframes waveFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            33%       { transform: translateY(-4px) rotate(-3deg); }
            66%       { transform: translateY(2px) rotate(2deg); }
          }
        `}</style>
      </div>
    </>
  );
}

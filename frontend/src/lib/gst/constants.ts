export const BANK_ACCOUNT_TYPES = [
  { value: 'CURRENT',     label: 'Current Account' },
  { value: 'SAVINGS',     label: 'Savings Account' },
  { value: 'CASH_CREDIT', label: 'Cash Credit Account' },
  { value: 'OVERDRAFT',   label: 'Overdraft Account' },
  { value: 'NRE',         label: 'NRE Account' },
  { value: 'NRO',         label: 'NRO Account' },
  { value: 'OTHER',       label: 'Other' },
] as const;

export type BankAccountTypeValue = typeof BANK_ACCOUNT_TYPES[number]['value'];

// Country code list removed — PhoneInput now uses libphonenumber-js
// getCountries() + getCountryCallingCode() for the full dynamic list.

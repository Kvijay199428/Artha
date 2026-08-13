export const BANK_ACCOUNT_TYPES = [
  { value: 'CURRENT', label: 'Current Account' },
  { value: 'SAVINGS', label: 'Savings Account' },
  { value: 'CASH_CREDIT', label: 'Cash Credit Account' },
  { value: 'OVERDRAFT', label: 'Overdraft Account' },
  { value: 'NRE', label: 'NRE Account' },
  { value: 'NRO', label: 'NRO Account' },
  { value: 'OTHER', label: 'Other' },
] as const;

export const COMMON_COUNTRY_CODES = [
  { code: '+91', country: 'IN', name: 'India', flag: '🇮🇳' },
  { code: '+1', country: 'US', name: 'United States', flag: '🇺🇸' },
  { code: '+44', country: 'GB', name: 'United Kingdom', flag: '🇬🇧' },
  { code: '+971', country: 'AE', name: 'UAE', flag: '🇦🇪' },
  { code: '+65', country: 'SG', name: 'Singapore', flag: '🇸🇬' },
  { code: '+60', country: 'MY', name: 'Malaysia', flag: '🇲🇾' },
  { code: '+61', country: 'AU', name: 'Australia', flag: '🇦🇺' },
  { code: '+49', country: 'DE', name: 'Germany', flag: '🇩🇪' },
  { code: '+33', country: 'FR', name: 'France', flag: '🇫🇷' },
  { code: '+81', country: 'JP', name: 'Japan', flag: '🇯🇵' },
  { code: '+86', country: 'CN', name: 'China', flag: '🇨🇳' },
  { code: '+880', country: 'BD', name: 'Bangladesh', flag: '🇧🇩' },
  { code: '+94', country: 'LK', name: 'Sri Lanka', flag: '🇱🇰' },
  { code: '+977', country: 'NP', name: 'Nepal', flag: '🇳🇵' },
  { code: '+92', country: 'PK', name: 'Pakistan', flag: '🇵🇰' },
] as const;

export type CountryCode = typeof COMMON_COUNTRY_CODES[number];

import { useState } from 'react';
import { COMMON_COUNTRY_CODES } from '../../lib/gst/constants';

interface PhoneInputProps {
  value?: string; // The local phone number
  countryCode?: string; // e.g. "+91"
  onValueChange?: (phone: string, countryCode: string, e164: string) => void;
  label?: string;
  placeholder?: string;
  required?: boolean;
  error?: string;
  disabled?: boolean;
  optional?: boolean;
  name?: string;
  countryCodeName?: string;
}

export function PhoneInput({
  value = '',
  countryCode = '+91',
  onValueChange,
  label,
  placeholder = 'Phone number',
  required,
  error,
  disabled,
  optional,
  name,
  countryCodeName,
}: PhoneInputProps) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [search, setSearch] = useState('');
  const selectedCountry = COMMON_COUNTRY_CODES.find(c => c.code === countryCode) ?? COMMON_COUNTRY_CODES[0];

  const filteredCountries = COMMON_COUNTRY_CODES.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase()) ||
    c.code.includes(search) ||
    c.country.toLowerCase().includes(search.toLowerCase())
  );

  const handleCountrySelect = (country: typeof COMMON_COUNTRY_CODES[number]) => {
    setIsDropdownOpen(false);
    setSearch('');
    const e164 = `${country.code}${value.replace(/^0/, '')}`.replace(/\s+/g, '');
    onValueChange?.(value, country.code, e164);
  };

  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const phone = e.target.value;
    const e164 = `${countryCode}${phone.replace(/^0/, '')}`.replace(/\s+/g, '');
    onValueChange?.(phone, countryCode, e164);
  };

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}{optional && <span className="text-gray-400 font-normal ml-1">(Optional)</span>}
          {required && <span className="text-red-500 ml-0.5">*</span>}
        </label>
      )}
      <div className={`flex rounded-md shadow-sm border transition-colors ${
        error ? 'border-red-400' : 'border-gray-300'
      } ${disabled ? 'bg-gray-50' : 'bg-white'}`}>
        {/* Country Code Selector */}
        <div className="relative">
          <button
            type="button"
            disabled={disabled}
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className={`flex items-center gap-1.5 px-3 py-2 border-r border-gray-300 rounded-l-md text-sm font-medium text-gray-700 hover:bg-gray-50 whitespace-nowrap ${
              disabled ? 'cursor-not-allowed opacity-60' : 'cursor-pointer'
            }`}
          >
            <span className="text-base">{selectedCountry.flag}</span>
            <span className="text-gray-600">{selectedCountry.code}</span>
            <svg className="w-3 h-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          
          {isDropdownOpen && (
            <div className="absolute top-full left-0 z-50 mt-1 w-64 bg-white border border-gray-200 rounded-md shadow-lg overflow-hidden">
              <div className="p-2 border-b border-gray-100">
                <input
                  type="text"
                  value={search}
                  onChange={e => setSearch(e.target.value)}
                  placeholder="Search country..."
                  className="w-full px-2 py-1 text-sm border border-gray-300 rounded outline-none focus:border-blue-500"
                  autoFocus
                />
              </div>
              <div className="max-h-48 overflow-y-auto">
                {filteredCountries.map((country) => (
                  <button
                    key={country.code}
                    type="button"
                    onClick={() => handleCountrySelect(country)}
                    className={`w-full flex items-center gap-2 px-3 py-2 text-sm hover:bg-blue-50 text-left transition-colors ${
                      country.code === countryCode ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700'
                    }`}
                  >
                    <span className="text-base">{country.flag}</span>
                    <span>{country.name}</span>
                    <span className="ml-auto text-gray-400">{country.code}</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
        
        {/* Phone Number Input */}
        <input
          name={name}
          type="tel"
          value={value}
          onChange={handlePhoneChange}
          disabled={disabled}
          placeholder={placeholder}
          className={`flex-1 px-3 py-2 text-sm rounded-r-md outline-none border-0 bg-transparent ${
            disabled ? 'text-gray-500' : 'text-gray-900'
          } w-full min-w-0`}
        />
      </div>
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
      {/* Hidden field for country code - for form libraries */}
      {countryCodeName && <input type="hidden" name={countryCodeName} value={countryCode} />}
    </div>
  );
}

import { BANK_ACCOUNT_TYPES } from '../../lib/gst/constants';
import React from 'react';
import type { SelectHTMLAttributes } from 'react';

interface BankAccountTypeSelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
}

export const BankAccountTypeSelect = React.forwardRef<
  HTMLSelectElement,
  BankAccountTypeSelectProps
>(({ label, error, className = '', id, required, ...props }, ref) => {
  const selectId = id || `bank-account-type-${Math.random().toString(36).substring(7)}`;

  return (
    <div className="w-full">
      {label && (
        <label htmlFor={selectId} className="block text-sm font-medium text-gray-700 mb-1">
          {label}{required && <span className="text-red-500 ml-0.5">*</span>}
        </label>
      )}
      <select
        ref={ref}
        id={selectId}
        required={required}
        className={`block w-full rounded-md border shadow-sm sm:text-sm px-3 py-2 outline-none transition-colors ${
          error ? 'border-red-400 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
        } ${props.disabled ? 'bg-gray-50 text-gray-500' : 'bg-white text-gray-900'} ${className}`}
        {...props}
      >
        <option value="">Select Account Type</option>
        {BANK_ACCOUNT_TYPES.map((type) => (
          <option key={type.value} value={type.value}>
            {type.label}
          </option>
        ))}
      </select>
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
});
BankAccountTypeSelect.displayName = 'BankAccountTypeSelect';

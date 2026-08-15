import { useState, useCallback } from 'react';
import { validateGSTIN, parseGSTIN } from '../../lib/gst/validator';
import type { GSTINParseResult } from '../../lib/gst/validator';

interface GSTINInputProps {
  value?: string;
  onChange?: (value: string) => void;
  onValidated?: (result: GSTINParseResult | null, isValid: boolean) => void;
  name?: string;
  error?: string;
  disabled?: boolean;
  label?: string;
  showBreakdown?: boolean;
  className?: string;
}

export function GSTINInput({
  value = '',
  onChange,
  onValidated,
  name,
  error,
  disabled,
  label = 'GSTIN',
  showBreakdown = true,
  className = '',
}: GSTINInputProps) {
  const [internalValue, setInternalValue] = useState(value);

  // Sync with controlled value
  const currentValue = onChange !== undefined ? value : internalValue;

  const handleInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    // Normalize: uppercase, no spaces, only valid GSTIN chars
    const raw = e.target.value;
    const normalized = raw.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 15);
    
    if (onChange) {
      onChange(normalized);
    } else {
      setInternalValue(normalized);
    }

    if (normalized.length === 15) {
      const validation = validateGSTIN(normalized);
      if (validation.valid) {
        const parsed = parseGSTIN(normalized);
        onValidated?.(parsed, true);
      } else {
        onValidated?.(null, false);
      }
    } else {
      onValidated?.(null, false);
    }
  }, [onChange, onValidated]);

  const validation = currentValue.length > 0 ? validateGSTIN(currentValue) : null;
  const parsed = validation?.valid ? parseGSTIN(currentValue) : null;

  // Determine border color
  const borderClass = (() => {
    if (error) return 'border-red-400 focus:border-red-500 focus:ring-red-500';
    if (!validation) return 'border-input focus:border-blue-500 focus:ring-blue-500';
    if (currentValue.length === 15 && validation.valid) return 'border-green-400 focus:border-green-500 focus:ring-green-500';
    if (currentValue.length === 15 && !validation.valid) return 'border-red-400 focus:border-red-500 focus:ring-red-500';
    return 'border-input focus:border-blue-500 focus:ring-blue-500';
  })();

  return (
    <div className={`w-full ${className}`}>
      {label && (
        <label className="block text-sm font-medium text-muted-foreground mb-1">
          {label}
        </label>
      )}
      
      {/* Input */}
      <div className="relative">
        <input
          name={name}
          type="text"
          value={currentValue}
          onChange={handleInput}
          disabled={disabled}
          maxLength={15}
          placeholder="e.g. 29ABCDE1234F1Z5"
          className={`block w-full rounded-md border shadow-sm sm:text-sm px-3 py-2 outline-none font-mono tracking-wider transition-colors ${
            disabled ? 'bg-muted text-muted-foreground cursor-not-allowed' : 'bg-background'
          } ${borderClass}`}
          spellCheck={false}
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="characters"
        />
        {/* Valid checkmark */}
        {validation?.valid && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2 text-green-500">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          </div>
        )}
        {/* Invalid X */}
        {currentValue.length === 15 && !validation?.valid && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2 text-red-500">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
        )}
      </div>

      {/* Character count + status */}
      <div className="mt-1 flex items-center justify-between">
        <div className="text-xs">
          {error ? (
            <span className="text-red-600">{error}</span>
          ) : currentValue.length === 0 ? (
            <span className="text-muted-foreground">GSTIN format: 15 characters — State Code (2) + PAN (10) + Entity (1) + Z + Check digit</span>
          ) : currentValue.length < 15 ? (
            <span className="text-muted-foreground">Enter a valid 15-character GSTIN</span>
          ) : validation?.valid ? (
            <span className="text-green-600 font-medium">✓ Valid GSTIN format</span>
          ) : (
            <span className="text-red-600">{validation?.errors[0] || '✕ Invalid GSTIN format'}</span>
          )}
        </div>
        <div className={`text-xs font-mono ${
          currentValue.length === 15 ? 'text-foreground' : 'text-muted-foreground'
        }`}>
          {currentValue.length} / 15
        </div>
      </div>

      {/* GSTIN Breakdown when valid */}
      {showBreakdown && parsed && (
        <div className="mt-2 bg-green-50 border border-green-200 rounded-md p-3">
          <div className="font-mono text-sm text-foreground flex items-center gap-1 flex-wrap">
            <span className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded font-bold">{parsed.stateCode}</span>
            <span className="text-muted-foreground">|</span>
            <span className="bg-purple-100 text-purple-800 px-2 py-0.5 rounded font-bold">{parsed.pan}</span>
            <span className="text-muted-foreground">|</span>
            <span className="bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded font-bold">{parsed.entityNumber}</span>
            <span className="text-muted-foreground">|</span>
            <span className="bg-muted text-foreground px-2 py-0.5 rounded font-bold">{parsed.defaultCharacter}</span>
            <span className="text-muted-foreground">|</span>
            <span className="bg-orange-100 text-orange-800 px-2 py-0.5 rounded font-bold">{parsed.checkDigit}</span>
          </div>
          <div className="font-mono text-xs text-muted-foreground mt-1 flex items-center gap-1 flex-wrap">
            <span className="w-[28px] text-center">State</span>
            <span className="text-transparent">|</span>
            <span className="w-[80px] text-center">PAN</span>
            <span className="text-transparent">|</span>
            <span className="w-[16px] text-center">Ent</span>
            <span className="text-transparent">|</span>
            <span className="w-[16px] text-center">Dflt</span>
            <span className="text-transparent">|</span>
            <span className="w-[16px] text-center">Chk</span>
          </div>
          <div className="mt-2 grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-muted-foreground">
            <span><span className="font-medium">State:</span> {parsed.stateName || parsed.stateCode}</span>
            <span><span className="font-medium">PAN:</span> {parsed.pan}</span>
          </div>
        </div>
      )}
    </div>
  );
}

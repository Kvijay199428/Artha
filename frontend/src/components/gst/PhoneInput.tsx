import { useState, useRef, useEffect } from 'react';
import {
  parsePhoneNumber,
  getCountries,
  getCountryCallingCode,
  AsYouType,
  isValidPhoneNumber,
  type CountryCode,
} from 'libphonenumber-js';

// ── Country metadata ──────────────────────────────────────────────────────────
// Emoji flag from ISO 3166-1 alpha-2 code
function flagEmoji(iso: CountryCode): string {
  return iso
    .toUpperCase()
    .replace(/./g, (char) => String.fromCodePoint(char.charCodeAt(0) + 127397));
}

// Display name from browser Intl if available, fallback to code
const displayName = new Intl.DisplayNames(['en'], { type: 'region' });
function countryName(iso: CountryCode): string {
  try { return displayName.of(iso) ?? iso; } catch { return iso; }
}

// Build the full country list from libphonenumber-js at module load time
const ALL_COUNTRIES = getCountries()
  .map((iso) => ({
    iso,
    callingCode: `+${getCountryCallingCode(iso)}`,
    name: countryName(iso),
    flag: flagEmoji(iso),
  }))
  .sort((a, b) => {
    // Pin India first, then sort alphabetically
    if (a.iso === 'IN') return -1;
    if (b.iso === 'IN') return 1;
    return a.name.localeCompare(b.name);
  });

// ── Component ─────────────────────────────────────────────────────────────────
interface PhoneInputProps {
  value?: string;           // local/national number
  countryCode?: string;     // e.g. "+91"
  onValueChange?: (
    nationalNumber: string,
    callingCode: string,    // e.g. "+91"
    e164: string,           // e.g. "+919876543210"
    iso: string,            // e.g. "IN"
    isValid: boolean
  ) => void;
  label?: string;
  placeholder?: string;
  required?: boolean;
  optional?: boolean;
  error?: string;
  disabled?: boolean;
  name?: string;
  countryCodeName?: string;
}

export function PhoneInput({
  value = '',
  countryCode = '+91',
  onValueChange,
  label,
  placeholder,
  required,
  optional,
  error,
  disabled,
  name,
  countryCodeName,
}: PhoneInputProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [formatted, setFormatted] = useState(value);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLInputElement>(null);

  // Resolve the selected country from the calling code
  const selectedCountry =
    ALL_COUNTRIES.find((c) => c.callingCode === countryCode) ??
    ALL_COUNTRIES.find((c) => c.iso === 'IN')!;

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
        setSearch('');
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  // Auto-focus search when dropdown opens
  useEffect(() => {
    if (isOpen) setTimeout(() => searchRef.current?.focus(), 50);
  }, [isOpen]);

  const filtered = search
    ? ALL_COUNTRIES.filter(
        (c) =>
          c.name.toLowerCase().includes(search.toLowerCase()) ||
          c.callingCode.includes(search) ||
          c.iso.toLowerCase().includes(search.toLowerCase())
      )
    : ALL_COUNTRIES;

  const handleCountrySelect = (c: typeof ALL_COUNTRIES[number]) => {
    setIsOpen(false);
    setSearch('');
    emitChange(formatted, c.callingCode, c.iso);
  };

  const handleInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const raw = e.target.value;
    // Format as you type using libphonenumber-js
    const asYouType = new AsYouType(selectedCountry.iso);
    const fmt = asYouType.input(raw);
    setFormatted(fmt);
    emitChange(fmt, selectedCountry.callingCode, selectedCountry.iso);
  };

  const emitChange = (national: string, calling: string, iso: string) => {
    if (!onValueChange) return;
    // Strip non-digits for e164 building
    const digits = national.replace(/\D/g, '');
    const e164candidate = `${calling}${digits}`;
    let e164 = e164candidate;
    let valid = false;
    try {
      const parsed = parsePhoneNumber(e164candidate, iso as CountryCode);
      if (parsed) {
        e164 = parsed.format('E.164');
        valid = parsed.isValid();
      }
    } catch {
      // partial input — leave e164 as-is, valid = false
    }
    // Fallback: also try isValidPhoneNumber
    if (!valid && digits.length >= 7) {
      try { valid = isValidPhoneNumber(e164candidate); } catch { /* noop */ }
    }
    onValueChange(national, calling, e164, iso, valid);
  };

  // Parse an incoming full e164 into national + country when value prop changes externally
  useEffect(() => {
    if (!value) return;
    if (value.startsWith('+')) {
      try {
        const parsed = parsePhoneNumber(value);
        if (parsed) setFormatted(parsed.formatNational());
      } catch { /* partial */ }
    } else {
      setFormatted(value);
    }
  }, [value]);

  const borderClass = error
    ? 'border-destructive focus-within:ring-destructive/50'
    : 'border-input focus-within:border-ring focus-within:ring-ring/30';

  return (
    <div className="w-full space-y-1">
      {label && (
        <label className="text-sm font-medium text-foreground">
          {label}
          {required && <span className="text-destructive ml-0.5">*</span>}
          {optional && <span className="text-muted-foreground font-normal ml-1">(Optional)</span>}
        </label>
      )}

      <div
        className={`flex rounded-lg border bg-background transition-all focus-within:ring-[3px] ${borderClass} ${
          disabled ? 'opacity-60 cursor-not-allowed' : ''
        }`}
      >
        {/* Country selector */}
        <div ref={dropdownRef} className="relative flex-shrink-0">
          <button
            type="button"
            disabled={disabled}
            onClick={() => setIsOpen((v) => !v)}
            className="flex items-center gap-1.5 h-9 px-3 border-r border-input rounded-l-lg text-sm font-medium text-foreground hover:bg-muted transition-colors whitespace-nowrap disabled:cursor-not-allowed"
          >
            <span className="text-base leading-none">{selectedCountry.flag}</span>
            <span className="text-muted-foreground">{selectedCountry.callingCode}</span>
            <svg className="w-3 h-3 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={isOpen ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'} />
            </svg>
          </button>

          {isOpen && (
            <div className="absolute top-full left-0 z-50 mt-1 w-72 bg-popover border border-border rounded-lg shadow-lg overflow-hidden">
              {/* Search */}
              <div className="p-2 border-b border-border">
                <input
                  ref={searchRef}
                  type="text"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search country or code…"
                  className="w-full px-3 py-1.5 text-sm bg-background border border-input rounded-md outline-none focus:border-ring text-foreground placeholder:text-muted-foreground"
                />
              </div>
              {/* List */}
              <div className="max-h-52 overflow-y-auto">
                {filtered.length === 0 ? (
                  <p className="px-3 py-4 text-sm text-muted-foreground text-center">No results</p>
                ) : (
                  filtered.map((c) => (
                    <button
                      key={c.iso}
                      type="button"
                      onClick={() => handleCountrySelect(c)}
                      className={`w-full flex items-center gap-2.5 px-3 py-2 text-sm text-left transition-colors hover:bg-accent hover:text-accent-foreground ${
                        c.iso === selectedCountry.iso
                          ? 'bg-accent text-accent-foreground font-medium'
                          : 'text-foreground'
                      }`}
                    >
                      <span className="text-base">{c.flag}</span>
                      <span className="flex-1 truncate">{c.name}</span>
                      <span className="text-muted-foreground tabular-nums">{c.callingCode}</span>
                    </button>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* Number input */}
        <input
          name={name}
          type="tel"
          value={formatted}
          onChange={handleInput}
          disabled={disabled}
          placeholder={placeholder ?? (selectedCountry.iso === 'IN' ? '98765 43210' : 'Phone number')}
          className="flex-1 h-9 px-3 text-sm bg-transparent outline-none text-foreground placeholder:text-muted-foreground disabled:cursor-not-allowed min-w-0 rounded-r-lg"
        />
      </div>

      {error && <p className="text-sm text-destructive">{error}</p>}

      {/* Hidden field for form libraries that read by name */}
      {countryCodeName && (
        <input type="hidden" name={countryCodeName} value={selectedCountry.callingCode} />
      )}
    </div>
  );
}

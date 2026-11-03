import * as React from 'react';
import { cn } from '@/lib/utils';

/**
 * Input — token-driven replacement for `.form-input`.
 * No literal colour: border-input / bg-background / text-foreground, with the
 * focus ring coming from --ring, so it is correct in both themes by default.
 */
function Input({ className, type, ...props }) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        'flex h-9 w-full min-w-0 rounded-md border border-input bg-background px-3 py-1 text-sm text-foreground shadow-xs outline-none transition-[color,box-shadow]',
        'placeholder:text-muted-foreground',
        'selection:bg-primary selection:text-primary-foreground',
        'file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium',
        'disabled:cursor-not-allowed disabled:opacity-50',
        'focus-visible:border-ring focus-visible:ring-2 focus-visible:ring-ring/50',
        'aria-invalid:border-destructive aria-invalid:ring-2 aria-invalid:ring-destructive/20',
        className,
      )}
      {...props}
    />
  );
}

export { Input };

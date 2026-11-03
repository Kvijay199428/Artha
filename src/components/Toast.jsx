import React, { useState, useEffect, useCallback } from 'react';
import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-react';
import { cn } from '@/lib/utils';

// Toast — in-app notices.
//
// Ported to Tailwind + tokens. The four tones used to be hard-coded light
// hexes (`#ecfdf5`, `#fef2f2`, …) with no dark variant at all, so every toast
// stayed pale-green/red on a dark page. They now read from the status tokens
// in src/styles/tokens.css and follow the theme.
//
// The API is unchanged: `toast(message, type, duration)`.

const ICONS = {
  success: CheckCircle,
  error: XCircle,
  warning: AlertTriangle,
  info: Info,
};

const TONES = {
  success: {
    box: 'border-success/35 bg-success/10 text-success-foreground',
    rail: 'bg-success',
    icon: 'text-success',
  },
  error: {
    box: 'border-destructive/35 bg-destructive/10 text-destructive-foreground',
    rail: 'bg-destructive',
    icon: 'text-destructive',
  },
  warning: {
    box: 'border-warning-border bg-warning text-warning-foreground',
    rail: 'bg-warning-border',
    icon: 'text-warning-foreground',
  },
  info: {
    box: 'border-info-border bg-info text-info-foreground',
    rail: 'bg-info-border',
    icon: 'text-info-foreground',
  },
};

let toastId = 0;
let addToastFn = null;

export function toast(message, type = 'info', duration = 3500) {
  if (addToastFn) {
    addToastFn({ id: ++toastId, message, type, duration });
  }
}

export default function ToastContainer() {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((t) => {
    // v1.9.15 — collapse duplicate consecutive toasts. Clicking the same
    // preset three times used to stack three identical "Applied X" cards.
    // Now: if an identical-message toast is already visible, refresh its
    // timer instead of pushing a duplicate. Cap total on-screen at 4.
    setToasts((prev) => {
      const dupe = prev.find((x) => x.message === t.message && x.type === t.type);
      if (dupe) return prev.map((x) => (x === dupe ? { ...x, id: t.id } : x));
      const next = [...prev, t];
      return next.length > 4 ? next.slice(-4) : next;
    });
    setTimeout(() => {
      setToasts((prev) => prev.filter((x) => x.id !== t.id));
    }, t.duration);
  }, []);

  useEffect(() => {
    addToastFn = addToast;
    return () => { addToastFn = null; };
  }, [addToast]);

  const dismiss = (id) => {
    setToasts((prev) => prev.filter((x) => x.id !== id));
  };

  return (
    <div className="pointer-events-none fixed bottom-5 right-5 z-[11000] flex w-[min(360px,calc(100vw-2.5rem))] flex-col gap-2">
      {toasts.map((t) => {
        const Icon = ICONS[t.type] || ICONS.info;
        const tone = TONES[t.type] || TONES.info;
        return (
          <div
            key={t.id}
            role="status"
            className={cn(
              'pointer-events-auto flex items-start gap-2.5 overflow-hidden rounded-lg border py-2.5 pl-3 pr-2 shadow-lg',
              'animate-in slide-in-from-bottom-2 fade-in-0',
              tone.box,
            )}
          >
            <span className={cn('-ml-3 -my-2.5 w-1 self-stretch', tone.rail)} aria-hidden="true" />
            <Icon size={18} className={cn('mt-px shrink-0', tone.icon)} />
            <span className="flex-1 text-sm leading-snug">{t.message}</span>
            <button
              type="button"
              onClick={() => dismiss(t.id)}
              aria-label="Dismiss"
              className="shrink-0 rounded p-1 opacity-70 transition-opacity hover:opacity-100"
            >
              <X size={14} />
            </button>
          </div>
        );
      })}
    </div>
  );
}

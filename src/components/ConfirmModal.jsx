import { useState, useEffect, useCallback, useRef } from 'react';
import { AlertTriangle, Trash2, HelpCircle } from 'lucide-react';
import { Dialog, DialogContent, DialogDescription, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

// v1.10.34 — In-app replacement for `window.confirm()` and `window.prompt()`.
// The native dialogs look like OS chrome (title bar with the URL, generic
// OK/Cancel buttons, no branding, no icon), which broke the product's
// visual identity every time the user hit Delete on an invoice. Now every
// destructive / decision-requiring action opens a proper themed modal that
// matches the rest of the app.
//
// API mirrors the native calls so replacement is mechanical:
//   BEFORE:  if (!confirm('Delete this invoice?')) return;
//   AFTER:   if (!await confirmAction({ title: 'Delete invoice?', ... })) return;
//
//   BEFORE:  const v = window.prompt('Custom rate (%)', '12');
//   AFTER:   const v = await promptAction({ title: 'Custom rate (%)', defaultValue: '12' });
//
// The container mounts once at App root. All active calls are queued; only
// one modal shows at a time so the visual flow stays clean.
//
// Ported to shadcn Dialog + tokens. Two behaviours are preserved on purpose
// because other code depends on them: the promise must resolve exactly once,
// and the fallback to native dialogs before the container mounts stays.

let dispatchFn = null;

/**
 * Open an in-app confirmation modal.
 *
 * @param {Object} options
 * @param {string} options.title - Bold headline of the modal
 * @param {string} [options.message] - Optional detail below the title
 * @param {string} [options.confirmLabel='Confirm'] - Text on the primary action button
 * @param {string} [options.cancelLabel='Cancel'] - Text on the secondary/dismiss button
 * @param {'danger'|'warning'|'default'} [options.tone='default'] - Colour scheme
 * @returns {Promise<boolean>} - true if user confirmed, false if cancelled or dismissed
 */
export function confirmAction(options) {
  return new Promise((resolve) => {
    if (typeof dispatchFn !== 'function') {
      resolve(window.confirm(options?.message || options?.title || 'Are you sure?'));
      return;
    }
    dispatchFn({ ...options, kind: 'confirm', resolve });
  });
}

/**
 * Open an in-app text-prompt modal.
 *
 * @param {Object} options
 * @param {string} options.title - Bold headline of the modal (what to enter)
 * @param {string} [options.message] - Optional hint below the title
 * @param {string} [options.defaultValue] - Prefilled input value
 * @param {string} [options.placeholder] - Input placeholder text
 * @param {string} [options.confirmLabel='OK'] - Text on the primary button
 * @param {string} [options.cancelLabel='Cancel'] - Text on the dismiss button
 * @param {'text'|'number'} [options.inputType='text'] - HTML input type
 * @returns {Promise<string|null>} - the entered string, or null on cancel
 */
export function promptAction(options) {
  return new Promise((resolve) => {
    if (typeof dispatchFn !== 'function') {
      resolve(window.prompt(options?.message || options?.title || '', options?.defaultValue || ''));
      return;
    }
    dispatchFn({ ...options, kind: 'prompt', resolve });
  });
}

export default function ConfirmModalContainer() {
  const [modal, setModal] = useState(null);
  const [value, setValue] = useState('');
  const inputRef = useRef(null);
  const primaryRef = useRef(null);
  const previousActiveElement = useRef(null);

  const dispatch = useCallback((next) => {
    setModal(next);
    setValue(next?.defaultValue || '');
  }, []);

  useEffect(() => {
    dispatchFn = dispatch;
    return () => { dispatchFn = null; };
  }, [dispatch]);

  // Autofocus the input on prompt, or the confirm button on confirm.
  useEffect(() => {
    if (!modal) {
      previousActiveElement.current?.focus?.();
      previousActiveElement.current = null;
      return undefined;
    }
    previousActiveElement.current = document.activeElement;
    const t = setTimeout(() => {
      if (modal.kind === 'prompt' && inputRef.current) {
        inputRef.current.focus();
        inputRef.current.select();
      } else {
        primaryRef.current?.focus?.();
      }
    }, 30);
    return () => clearTimeout(t);
  }, [modal]);

  // Keyboard: Enter → confirm, Esc → cancel.
  useEffect(() => {
    if (!modal) return undefined;
    const onKey = (e) => {
      if (e.key === 'Escape') { e.preventDefault(); cancel(); }
      else if (e.key === 'Enter' && modal.kind === 'confirm') {
        e.preventDefault();
        confirm();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [modal]);

  const cancel = useCallback(() => {
    if (!modal) return;
    modal.resolve(modal.kind === 'prompt' ? null : false);
    setModal(null);
  }, [modal]);

  const confirm = useCallback(() => {
    if (!modal) return;
    modal.resolve(modal.kind === 'prompt' ? value : true);
    setModal(null);
  }, [modal, value]);

  if (!modal) return null;

  const tone = modal.tone || 'default';
  const isDanger = tone === 'danger';
  const isWarning = tone === 'warning';
  const Icon = isDanger ? Trash2 : isWarning ? AlertTriangle : HelpCircle;

  const iconBox = isDanger
    ? 'bg-destructive/10 text-destructive'
    : isWarning
      ? 'bg-warning text-warning-foreground'
      : 'bg-primary/10 text-primary';

  const primaryLabel = modal.confirmLabel || (modal.kind === 'prompt' ? 'OK' : (isDanger ? 'Delete' : 'Confirm'));
  const secondaryLabel = modal.cancelLabel || 'Cancel';

  return (
    <Dialog open onOpenChange={(open) => { if (!open) cancel(); }}>
      <DialogContent
        showCloseButton={false}
        className="confirm-modal-content z-[10000] max-w-[440px] gap-0 overflow-hidden p-6"
        overlayClassName="z-[10000]"
        onKeyDown={(e) => e.stopPropagation()}
      >
        <div className="flex items-start gap-[0.9rem]">
          <div className={cn('flex size-10 shrink-0 items-center justify-center rounded-full', iconBox)}>
            <Icon size={20} />
          </div>
          <div className="min-w-0 flex-1">
            <DialogTitle id="confirm-modal-title" className="text-[1.05rem] leading-[1.35]">
              {modal.title}
            </DialogTitle>
            {modal.message && (
              <DialogDescription className="mt-[0.4rem] whitespace-pre-wrap text-[0.87rem] leading-relaxed">
                {modal.message}
              </DialogDescription>
            )}
            {modal.kind === 'prompt' && (
              <form onSubmit={(e) => { e.preventDefault(); confirm(); }}>
                <Input
                  ref={inputRef}
                  type={modal.inputType || 'text'}
                  className="mt-[0.9rem] w-full"
                  value={value}
                  onChange={(e) => setValue(e.target.value)}
                  placeholder={modal.placeholder || ''}
                />
              </form>
            )}
          </div>
        </div>
        <div className="mt-5 flex justify-end gap-2">
          <Button type="button" variant="outline" className="h-auto px-4 py-2 text-[0.85rem]" onClick={cancel}>
            {secondaryLabel}
          </Button>
          <Button
            ref={primaryRef}
            type="button"
            variant={isDanger ? 'destructive' : 'default'}
            className="confirm-modal-primary h-auto px-[1.1rem] py-2 text-[0.85rem]"
            onClick={confirm}
          >
            {primaryLabel}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}

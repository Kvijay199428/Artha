import * as React from 'react';
import { Toaster as SonnerToaster } from 'sonner';

/**
 * Toaster — Sonner, wired to the same light/dark switch as the rest of the app.
 *
 * The app's own `<Toast>` component still exists for in-app notices; this is
 * the shadcn-compatible `toast()` API new code should use. Palette classes are
 * token-driven so it follows the theme in both modes.
 */
function Toaster({ ...props }) {
  return (
    <SonnerToaster
      theme="system"
      className="toaster group"
      toastOptions={{
        classNames: {
          toast:
            'group toast group-[.toaster]:bg-card group-[.toaster]:text-card-foreground group-[.toaster]:border-border group-[.toaster]:shadow-lg',
          description: 'group-[.toast]:text-muted-foreground',
          actionButton: 'group-[.toast]:bg-primary group-[.toast]:text-primary-foreground',
          cancelButton: 'group-[.toast]:bg-muted group-[.toast]:text-muted-foreground',
        },
      }}
      {...props}
    />
  );
}

export { Toaster };

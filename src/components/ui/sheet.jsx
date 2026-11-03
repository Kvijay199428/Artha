import * as React from 'react';
import { cn } from '@/lib/utils';

const Sheet = ({ open, onOpenChange, children }) => {
  const [internal, setInternal] = React.useState(false);
  const isOpen = open !== undefined ? open : internal;
  const setOpen = onOpenChange || setInternal;
  React.useEffect(() => {
    document.body.style.overflow = isOpen ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [isOpen]);
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-[10000]">
      <div className="absolute inset-0 bg-black/50" onClick={() => setOpen(false)} />
      {children}
    </div>
  );
};

const SheetContent = React.forwardRef(({ className, side = 'right', children, ...props }, ref) => {
  const sideCls = side === 'left' ? 'left-0 border-r' : 'right-0 border-l';
  return (
    <div
      ref={ref}
      role="dialog"
      aria-modal="true"
      className={cn(
        'absolute top-0 h-full w-3/4 gap-4 border-border bg-card p-6 text-card-foreground shadow-lg transition ease-in-out sm:max-w-sm',
        sideCls,
        className,
      )}
      {...props}
    >
      {children}
    </div>
  );
});
SheetContent.displayName = 'SheetContent';

const SheetHeader = ({ className, ...props }) => (
  <div className={cn('flex flex-col space-y-2 text-center sm:text-left', className)} {...props} />
);

const SheetFooter = ({ className, ...props }) => (
  <div className={cn('flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2', className)} {...props} />
);

const SheetTitle = React.forwardRef(({ className, ...props }, ref) => (
  <h3 ref={ref} className={cn('text-lg font-semibold text-foreground', className)} {...props} />
));
SheetTitle.displayName = 'SheetTitle';

const SheetDescription = React.forwardRef(({ className, ...props }, ref) => (
  <p ref={ref} className={cn('text-sm text-muted-foreground', className)} {...props} />
));
SheetDescription.displayName = 'SheetDescription';

export { Sheet, SheetContent, SheetHeader, SheetFooter, SheetTitle, SheetDescription };

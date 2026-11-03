// v1.10.37 — Reusable page-header card.
//
// Ported to Tailwind + design tokens. Nothing here names a colour: the card
// gradient is built from --primary-rgb (kept as rgb channels because
// html2canvas cannot parse oklch/color-mix, see src/styles/tokens.css) and the
// surface comes from --card. That is why this header follows the theme in both
// modes without a `[data-theme="dark"]` patch.
//
// Props:
//   icon        emoji / string / element rendered inside the 44px badge
//   title       page title (h1)
//   subtitle    one-line description shown below the title
//   meta        optional short string rendered as a pill next to the subtitle
//   children    right-hand slot for action buttons, HelpButton, etc.
//   compact     slim title row, no card/icon/subtitle (the Dashboard)
import { cn } from '@/lib/utils';

const CARD_GRADIENT =
  'bg-[linear-gradient(135deg,rgba(var(--primary-rgb),0.12),var(--card))]';

export default function PageHeader({ icon, title, subtitle, meta, children, compact = false, className = '' }) {
  if (compact) {
    return (
      <div className={cn('page-header page-header-compact mb-[0.9rem] flex flex-wrap items-center gap-3', className)}>
        <h1 className="page-title m-0 text-[1.3rem] text-foreground">{title}</h1>
        {meta && <span className="text-xs font-semibold text-muted-foreground">{meta}</span>}
        <div className="ml-auto flex items-center gap-2">{children}</div>
      </div>
    );
  }

  return (
    <div
      className={cn(
        'page-header mb-5 flex flex-wrap items-center justify-between gap-4',
        'rounded-xl border border-border px-[1.35rem] py-[1.1rem]',
        CARD_GRADIENT,
        className,
      )}
    >
      <div className="flex min-w-0 flex-1 items-center gap-[0.85rem]">
        {icon !== undefined && (
          <div
            className="flex size-11 shrink-0 items-center justify-center rounded-xl bg-[linear-gradient(135deg,var(--primary),var(--primary-darker))] text-[1.15rem] text-primary-foreground shadow-[0_6px_18px_rgba(var(--primary-rgb),0.35)]"
          >
            {icon}
          </div>
        )}
        <div className="min-w-0 flex-1">
          <h1 className="page-title m-0 text-foreground">{title}</h1>
          {(subtitle || meta) && (
            <p className="page-subtitle mt-[0.15rem] flex flex-wrap items-center gap-[0.55rem]">
              {subtitle && <span>{subtitle}</span>}
              {meta && (
                <span className="rounded-full border border-border bg-muted px-2 py-[0.1rem] text-[0.7rem] font-semibold text-foreground">
                  {meta}
                </span>
              )}
            </p>
          )}
        </div>
      </div>
      {children}
    </div>
  );
}

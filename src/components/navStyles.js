/**
 * Sidebar navigation styles — one place for the rail's repeated classes.
 *
 * The rail follows the theme (white in Light Mode, navy in Dark Mode), so it
 * reads from the `--sidebar-*` tokens rather than from `--card` /
 * `--background`: the rail needs its own hover and muted tones, not the page's.
 * Keeping the class strings here means the App shell, the company switcher and
 * the lock button cannot drift apart.
 *
 * `nav-btn` is still on the element on purpose: the auto-hide rail is driven
 * by legacy CSS that keys off it (`> span:not(.nav-badge) { display:none }`
 * when the rail is collapsed). The colours and spacing come from the Tailwind
 * classes below, which live in the utilities layer and therefore win.
 */
export const NAV_BTN =
  'nav-btn flex w-full items-center gap-3 rounded-lg border border-transparent px-4 py-2.5 text-left text-sm font-medium text-sidebar-foreground transition-colors hover:bg-sidebar-accent hover:text-sidebar-foreground-strong focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary';

export const NAV_BTN_ACTIVE =
  'nav-btn-active border-primary bg-primary text-primary-foreground shadow-[0_4px_12px_rgba(37,99,235,0.35)] hover:bg-primary hover:text-primary-foreground';

export const NAV_BADGE =
  'nav-badge absolute right-3 top-2 flex h-[18px] min-w-[18px] items-center justify-center rounded-full bg-destructive px-1.5 text-[0.65rem] font-bold text-destructive-foreground';

// "Support & About" keeps its rose identity in both modes. It cannot simply
// reuse NAV_BTN: two `text-*` utilities would fight, and which one wins would
// depend on stylesheet order rather than intent.
export const NAV_BTN_SUPPORT =
  'nav-btn flex w-full items-center gap-3 rounded-lg border border-rose-500/35 bg-rose-500/15 px-4 py-2.5 text-left text-sm font-medium text-rose-800 transition-colors hover:bg-rose-500/25 hover:text-rose-900 dark:text-rose-200 dark:hover:text-white [&>svg]:text-rose-600 dark:[&>svg]:text-rose-400';

export const NAV_BTN_SUPPORT_ACTIVE =
  'nav-btn flex w-full items-center gap-3 rounded-lg border border-rose-600 bg-rose-600 px-4 py-2.5 text-left text-sm font-medium text-white shadow-[0_4px_12px_rgba(225,29,72,0.35)] transition-colors hover:bg-rose-600 hover:text-white [&>svg]:text-white';

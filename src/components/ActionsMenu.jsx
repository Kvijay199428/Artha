import { useEffect, useRef, useState } from 'react';
import { MoreHorizontal } from 'lucide-react';
import { cn } from '@/lib/utils';

// v1.10.80 (#100) - a "⋯" drop-down for the less-used row actions, so an
// Actions column shows a few buttons instead of a long row of icons.
// Requested: "Convert Actions into a drop-down menu with icon to provide a
// cleaner and more compact interface."
//
// items: [{ label, icon: LucideIcon, onClick, title?, tone?: 'danger' | 'green', hidden? }]
// The menu is position: fixed, so a table that scrolls sideways can't clip it.
//
// Ported to Tailwind + tokens.

function placeFor(r, count) {
  const below = window.innerHeight - r.bottom > count * 36 + 16;
  return { right: Math.max(8, window.innerWidth - r.right), ...(below ? { top: r.bottom + 4 } : { bottom: window.innerHeight - r.top + 4 }) };
}

export default function ActionsMenu({ items, label = 'More actions' }) {
  const [pos, setPos] = useState(null); // { top, right } while open
  const btn = useRef(null);
  const menu = useRef(null);
  const visible = (items || []).filter((i) => i && !i.hidden);
  const count = visible.length;

  useEffect(() => {
    if (!pos) return undefined;
    const close = (e) => {
      if (e.type === 'keydown' && e.key !== 'Escape') return;
      if (e.type === 'mousedown' && (menu.current?.contains(e.target) || btn.current?.contains(e.target))) return;
      setPos(null);
    };
    const follow = () => {
      const r = btn.current?.getBoundingClientRect();
      if (!r || r.bottom < 0 || r.top > window.innerHeight) { setPos(null); return; }
      setPos(placeFor(r, count));
    };
    document.addEventListener('mousedown', close);
    document.addEventListener('keydown', close);
    window.addEventListener('scroll', follow, true);
    window.addEventListener('resize', follow);
    return () => {
      document.removeEventListener('mousedown', close);
      document.removeEventListener('keydown', close);
      window.removeEventListener('scroll', follow, true);
      window.removeEventListener('resize', follow);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [!!pos]);

  if (!visible.length) return null;
  const toggle = () => setPos(pos ? null : placeFor(btn.current.getBoundingClientRect(), visible.length));

  return (
    <>
      <button
        ref={btn}
        type="button"
        className="icon-btn inline-flex h-8 w-8 items-center justify-center rounded-md border border-border bg-card text-foreground/80 transition-colors hover:bg-accent hover:text-foreground"
        onClick={toggle}
        title={label}
        aria-label={label}
        aria-haspopup="menu"
        aria-expanded={!!pos}
      >
        <MoreHorizontal size={15} />
      </button>
      {pos && (
        <div
          ref={menu}
          role="menu"
          className="fixed z-[1000] min-w-[190px] overflow-hidden rounded-lg border border-border bg-popover p-1 text-popover-foreground shadow-xl"
          style={{ ...pos }}
        >
          {visible.map((item) => {
            const Icon = item.icon;
            const tone =
              item.tone === 'danger'
                ? 'text-destructive hover:bg-destructive/10'
                : item.tone === 'green'
                  ? 'text-emerald-600 hover:bg-emerald-500/10 dark:text-emerald-400'
                  : 'text-foreground hover:bg-accent hover:text-accent-foreground';
            return (
              <button
                key={item.label}
                type="button"
                role="menuitem"
                title={item.title || item.label}
                onClick={() => { setPos(null); item.onClick(); }}
                className={cn(
                  'flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-sm transition-colors',
                  tone,
                )}
              >
                {Icon && <Icon size={15} className="shrink-0" />} {item.label}
              </button>
            );
          })}
        </div>
      )}
    </>
  );
}

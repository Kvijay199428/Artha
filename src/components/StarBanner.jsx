// v1.10.75 - a slim "star us on GitHub" line at the top of the app. Asked
// for by the maintainer: closable like a notification, at most once a month.
// First shown 3 days after the app was first opened in this browser, never
// to someone on day one. ✕ hides it for 30 days; "Star on GitHub" or
// "Already starred" hides it for good. Per browser (localStorage), which is
// fine for a reminder: losing it only means one more polite line.
//
// Ported to Tailwind: the callout read --info-bg / --info-border / --info-text,
// which have dark values, but the ✕ and "Already starred" used `color:
// inherit`, so they only worked because of that. They are explicit now.
import { useState } from 'react';
import { Star, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

const KEY = 'freegstbill_starBanner';
const REPO = 'https://github.com/Kvijay199428/Artha';
const DAY = 86400000;
const FIRST_AFTER_DAYS = 3;
const EVERY_DAYS = 30;

const load = () => {
  let s = {};
  try { s = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch { /* blocked storage: treat as new */ }
  if (!s.firstSeen) {
    s = { ...s, firstSeen: Date.now() };
    try { localStorage.setItem(KEY, JSON.stringify(s)); } catch { /* private mode */ }
  }
  return s;
};

const due = (s, now = Date.now()) => !s.done && (s.closedAt
  ? now - s.closedAt >= EVERY_DAYS * DAY
  : now - s.firstSeen >= FIRST_AFTER_DAYS * DAY);

export default function StarBanner() {
  const [state, setState] = useState(load);
  if (!due(state)) return null;
  const save = (patch) => {
    const next = { ...state, ...patch };
    try { localStorage.setItem(KEY, JSON.stringify(next)); } catch { /* private mode */ }
    setState(next);
  };
  return (
    <div
      role="status"
      className="mb-4 flex flex-wrap items-center gap-3 rounded-[10px] border border-info-border bg-info px-3.5 py-2.5 text-[0.85rem] text-info-foreground"
    >
      <Star size={18} className="shrink-0 fill-amber-500 text-amber-500" />
      <span className="flex-[1_1_240px]">
        Finding Free GST Billing useful? A star on GitHub helps other businesses find it. It takes one click.
      </span>
      <Button asChild size="sm" className="h-auto px-3 py-1.5 text-[0.8rem]">
        <a href={REPO} target="_blank" rel="noopener noreferrer" onClick={() => save({ done: true })}>
          <Star size={14} /> Star on GitHub
        </a>
      </Button>
      <button
        type="button"
        onClick={() => save({ done: true })}
        className="cursor-pointer border-0 bg-transparent p-1 text-[0.78rem] text-info-foreground underline underline-offset-2 opacity-90 hover:opacity-100"
      >
        Already starred
      </button>
      <button
        type="button"
        onClick={() => save({ closedAt: Date.now() })}
        title="Close (asks again in a month)"
        aria-label="Close"
        className="cursor-pointer border-0 bg-transparent p-1 leading-none opacity-80 hover:opacity-100"
      >
        <X size={16} />
      </button>
    </div>
  );
}

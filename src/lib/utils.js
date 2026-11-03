/**
 * `cn` — merge class names the way shadcn/ui expects.
 *
 * Why it exists: a component receives `className="px-4"` from the caller and
 * also carries its own `px-2`. Plain string concatenation leaves both, and
 * whichever rule Tailwind emitted last wins — usually not the caller's. `twMerge`
 * removes the earlier conflicting utility so the caller always wins, and `clsx`
 * handles the conditional/array/object forms.
 *
 * Not a styling helper: it never decides colours. Colours come from the tokens
 * in `src/styles/tokens.css`.
 */
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

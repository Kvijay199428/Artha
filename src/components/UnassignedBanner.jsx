import { Building2 } from 'lucide-react';
import { confirmAction } from './ConfirmModal';
import { toast } from './Toast';
import { Button } from '@/components/ui/button';

/**
 * Offers to attach records that predate multi-business separation to the
 * business currently selected.
 *
 * v1.10.65 (#58 item 3) — expenses, purchase bills and recurring templates
 * saved before businesses were kept apart carry no owner, so they appear
 * under every business. Hiding them would be far worse than showing them
 * twice, so they stay visible and the user is offered this instead.
 *
 * Two things this deliberately does NOT do:
 *
 *   * It does not assign anything automatically. Which business a past
 *     expense belonged to is a fact only the user knows, and guessing it
 *     would quietly file records into the wrong books.
 *   * It does not appear unless there is something to assign, so it is not
 *     a permanent banner nagging at the top of the page.
 *
 * Assigning is one-way — it names the business in the confirmation so the
 * user cannot do it while looking at the wrong company by accident.
 *
 * Ported to Tailwind: the tint is `bg-primary/10` over `bg-card`, so it stays
 * a light blue wash on light and a deep blue wash on dark instead of a fixed
 * rgba that only suited one mode.
 */
export default function UnassignedBanner({ count, businessName, noun, onAssign }) {
  if (!count || !businessName) return null;

  const label = count === 1 ? `1 ${noun}` : `${count} ${noun}s`;

  const handleClick = async () => {
    const ok = await confirmAction({
      title: `Assign ${label} to ${businessName}?`,
      message:
        `${label} ${count === 1 ? 'was' : 'were'} saved before you began keeping `
        + `businesses separate, so ${count === 1 ? 'it appears' : 'they appear'} under every business. `
        + `Assigning ${count === 1 ? 'it' : 'them'} to ${businessName} means `
        + `${count === 1 ? 'it' : 'they'} will no longer show under your other businesses. `
        + `Only do this if ${count === 1 ? 'it belongs' : 'they belong'} to ${businessName}.`,
      confirmLabel: `Assign to ${businessName}`,
    });
    if (!ok) return;
    try {
      await onAssign();
      toast(`${label} assigned to ${businessName}`, 'success');
    } catch {
      toast('Could not assign — please try again', 'error');
    }
  };

  return (
    <div className="mb-4 flex flex-wrap items-center justify-between gap-4 rounded-[10px] border border-border bg-primary/10 px-4 py-[0.7rem] text-foreground">
      <span className="flex items-center gap-[0.55rem] text-[0.88rem]">
        <Building2 size={18} className="shrink-0 text-primary" />
        <span>
          <strong>{label}</strong> {count === 1 ? 'is' : 'are'} not assigned to a business,
          so {count === 1 ? 'it shows' : 'they show'} under all of them.
        </span>
      </span>
      <Button type="button" size="sm" className="text-[0.85rem]" onClick={handleClick}>
        Assign to {businessName}
      </Button>
    </div>
  );
}

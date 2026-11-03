// v1.10.75 - a small line at the end of the Dashboard only (on other screens
// it took working space; floating, it covered the table - #83): the app's
// name and version, who makes it, and the Support page. Only the user sees
// it; it is never printed on an invoice. The version comes from the local
// server, so it works offline.
//
// Ported to Tailwind + tokens: the pill used --card-bg / --border /
// --text-muted, which had to be duplicated in the dark patch. Now the same
// classes are correct in every mode.
import { useEffect, useState } from 'react';
import { Heart } from 'lucide-react';

export default function AppFooter({ onOpenSupport }) {
  const [version, setVersion] = useState('');
  useEffect(() => {
    let live = true;
    fetch('/api/version').then((r) => r.json()).then((d) => { if (live && d?.current) setVersion(d.current); }).catch(() => {});
    return () => { live = false; };
  }, []);

  return (
    <footer className="mt-auto pt-6 text-center text-[0.72rem] text-muted-foreground">
      <span className="inline-flex flex-wrap items-center justify-center gap-[0.45rem] rounded-full border border-border bg-card px-[0.85rem] py-[0.3rem] backdrop-blur-md">
        <span>ARTHA{version ? ` v${version}` : ''}</span>
        <span aria-hidden="true">·</span>
        <a
          href="https://vijaykrsha.online"
          target="_blank"
          rel="noopener noreferrer"
          className="font-semibold text-foreground/80 underline-offset-2 hover:text-foreground hover:underline"
        >
          by VIJAYKRSHA.ONLINE
        </a>
        <span aria-hidden="true">·</span>
        <button
          type="button"
          onClick={onOpenSupport}
          className="inline-flex cursor-pointer items-center gap-1 border-0 bg-transparent p-0 font-semibold text-foreground/80 hover:text-foreground"
        >
          <Heart size={11} className="fill-rose-600 text-rose-600" /> Support
        </button>
      </span>
    </footer>
  );
}

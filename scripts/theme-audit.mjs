/**
 * theme-audit — finds places that cannot follow the theme.
 *
 * WHY
 * ---
 * The "some parts stay light in dark mode" bug came from two habits:
 *   1. a CSS rule that paints a light colour and has no
 *      `[data-theme="dark"]` counterpart, and
 *   2. a JSX inline style that hardcodes a colour, which no theme can reach.
 *
 * This script lists both. It is a guard, not a formatter: it never edits code.
 * Run it before and after a screen is ported to Tailwind; the counts should
 * only go down.
 *
 * USAGE
 *   node scripts/theme-audit.mjs            # summary + top offenders
 *   node scripts/theme-audit.mjs --list     # every offending selector/line
 *   node scripts/theme-audit.mjs --json     # machine-readable
 */

import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const ROOT = process.cwd();
const SRC = join(ROOT, 'src');
const CSS_FILE = join(SRC, 'index.css');
const ARGS = new Set(process.argv.slice(2));

/* ---------------------------------------------------------------- helpers */

const rel = (p) => relative(ROOT, p).split(sep).join('/');

function walk(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    const p = join(dir, entry);
    if (statSync(p).isDirectory()) {
      if (entry === 'node_modules' || entry === '.git') continue;
      walk(p, out);
    } else {
      out.push(p);
    }
  }
  return out;
}

/** Colours that only look right on a white surface. */
const LIGHT_LITERALS = [
  /\bwhite\b/i,
  /#fff(?:fff)?\b/i,
  /#f8fafc\b/i, /#f9fafb\b/i, /#fafafa\b/i, /#f1f5f9\b/i,
  /#f0f2f5\b/i, /#e5e7eb\b/i, /#e2e8f0\b/i, /#f3f4f6\b/i,
  /#fefce8\b/i, /#fef2f2\b/i, /#fef3c7\b/i, /#ecfdf5\b/i,
  /#eff6ff\b/i, /#fffbeb\b/i, /#f5f3ff\b/i, /#f0fdf4\b/i,
  /rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0\.[0-9]+\s*\)/i,
];

const isLightLiteral = (value) => LIGHT_LITERALS.some((re) => re.test(value));

/**
 * Selectors that are dark ON PURPOSE in both modes — the "server is down"
 * takeover and the install banner both sit outside the page palette.
 *
 * The navigation rail, profile switcher, nav buttons and server-status dot are
 * deliberately NOT listed: they follow the theme now (white rail in Light Mode,
 * navy in Dark Mode), so the audit must keep watching them.
 *
 * The invoice/print subtree is listed because it is rasterised by html2canvas,
 * which cannot parse oklch()/color-mix(); it keeps its own fixed hex palette.
 */
const INTENTIONAL_DARK = [
  /^\.server-down/,
  /^\.server-start-btn/,
  /^\.pwa-install/,
  /^\.pwa-dismiss/,
  /^\.inv-/,
  /^\.invoice-preview/,
  /^\.paper-/,
  /^body:has\(#invoice-preview\)/,
  /^\.template-(corporate|minimalist|modern|classic)\b/,
];

/**
 * `html:not([data-theme="dark"]) .x { … }` is the legacy way of saying "this
 * rule is the Light Mode override". It is not an unpatched light colour — it is
 * the patch itself — so the worklist skips it instead of asking for a dark
 * twin it must never have.
 */
const isLightCompanion = (selector) => /html:not\(\[data-theme=["']?dark["']?\]\)/.test(selector);

const isIntentionalDark = (selector) =>
  INTENTIONAL_DARK.some((re) => re.test(normaliseSelector(selector).replace(/^\[data-theme=["']?dark["']?\]\s*/, '')));


/** Only the declarations that actually paint something. */
const PAINT_PROP = /^(background|background-color|background-image|color|border|border-color|border-top|border-right|border-bottom|border-left|border-.*-color|fill|stroke|box-shadow)$/i;

/* ------------------------------------------------------------- CSS parser */

function stripComments(css) {
  return css.replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, ' '));
}

/**
 * Walk the stylesheet and produce one record per declaration that paints a
 * light literal, tagged with the at-rule context it sits in (so `@media`
 * copies are not confused with the base rule) and the line number.
 */
function analyseCss() {
  const raw = readFileSync(CSS_FILE, 'utf8');
  const css = stripComments(raw);
  const lines = raw.split(/\r?\n/);

  const records = [];
  const ruleIndex = [];       // every selector seen, dark or not
  const stack = [];           // { selector, kind: 'rule' | 'at' }
  let buf = '';
  let line = 1;

  for (let i = 0; i < css.length; i += 1) {
    const ch = css[i];
    if (ch === '\n') line += 1;

    if (ch === '{') {
      const header = buf.trim().replace(/\s+/g, ' ');
      buf = '';
      if (header.startsWith('@')) {
        stack.push({ kind: 'at', selector: header });
      } else {
        stack.push({ kind: 'rule', selector: header, line });
        ruleIndex.push({
          selector: header,
          isDark: /\[data-theme=["']?dark["']?\]/.test(header) || /(^|[\s,])\.dark[\s,:]/.test(header),
        });
      }
      continue;
    }

    if (ch === '}') {
      const top = stack[stack.length - 1];
      // A rule body was being collected right before this closing brace.
      if (top && top.kind === 'rule' && buf.trim()) {
        emitDeclarations(buf, top, stack);
      }
      buf = '';
      stack.pop();
      continue;
    }

    if (ch === ';') {
      const top = stack[stack.length - 1];
      if (top && top.kind === 'rule') emitDeclarations(buf + ';', top, stack);
      buf = '';
      continue;
    }

    buf += ch;
  }

  function emitDeclarations(body, rule, stackNow) {
    const atRules = stackNow.filter((s) => s.kind === 'at').map((s) => s.selector);
    const isDark = /\[data-theme=["']?dark["']?\]/.test(rule.selector);
    for (const decl of body.split(';')) {
      const idx = decl.indexOf(':');
      if (idx === -1) continue;
      const prop = decl.slice(0, idx).trim().toLowerCase();
      const value = decl.slice(idx + 1).trim();
      if (!prop || !value) continue;
      if (!PAINT_PROP.test(prop)) continue;
      // Pure white text is only wrong when the surface behind it is light, and
      // that surface is reported by its own `background` declaration. Skipping
      // it here keeps `.btn-primary { color: white }` out of the worklist.
      if (prop === 'color' && /^(white|#fff(?:fff)?)$/i.test(value)) continue;
      if (!isLightLiteral(value)) continue;
      records.push({
        selector: rule.selector,
        prop,
        value,
        isDark,
        atRules,
        line: rule.line,
        text: lines[rule.line - 1]?.trim() ?? '',
      });
    }
  }

  return { records, ruleIndex };
}

/* --------------------------------------------- does a dark patch exist? */

const normaliseSelector = (s) => s.replace(/\s+/g, ' ').trim();

function buildDarkSubjectSet(ruleIndex) {
  // Every selector that appears under a dark rule, e.g.
  //   [data-theme="dark"] .card  ->  ".card"
  //   [data-theme="dark"] .card, .dark .card -> ".card"
  // Built from ALL dark rules, not just the ones that happen to contain a
  // light literal — a dark override sets a dark colour, which the light-literal
  // scan never sees.
  const subjects = new Set();
  for (const r of ruleIndex) {
    if (!r.isDark) continue;
    for (const part of r.selector.split(',')) {
      const stripped = normaliseSelector(part)
        .replace(/^\[data-theme=["']?dark["']?\]\s*/, '')
        .replace(/^\.dark\s*/, '');
      if (stripped) subjects.add(stripped);
    }
  }
  return subjects;
}

/**
 * The same idea, but for the legacy Light Mode overrides:
 *   html:not([data-theme="dark"]) .sidebar  ->  ".sidebar"
 * A base rule whose light colour is corrected by one of these is already safe
 * in both modes, so it is not a bug.
 */
function buildLightCompanionSet(ruleIndex) {
  const subjects = new Set();
  for (const r of ruleIndex) {
    if (!isLightCompanion(r.selector)) continue;
    for (const part of r.selector.split(',')) {
      const stripped = normaliseSelector(part)
        .replace(/^html:not\(\[data-theme=["']?dark["']?\]\)\s*/, '');
      if (stripped) subjects.add(stripped);
    }
  }
  return subjects;
}

/* ------------------------------------------------------------- JSX scan */

const COLOUR_PROP = /\b(background|backgroundColor|backgroundImage|color|border|borderColor|borderTop|borderRight|borderBottom|borderLeft|boxShadow|fill|stroke|outline|outlineColor)\s*:/;

function analyseJsx(files) {
  const out = [];
  for (const file of files) {
    const text = readFileSync(file, 'utf8');
    const lines = text.split(/\r?\n/);
    lines.forEach((ln, i) => {
      if (!/style=\{\{/.test(ln) && !/style=\{\{/.test(lines[i - 1] || '')) return;
      // Look at this line and the next one: style objects are often multi-line.
      const window = [ln, lines[i + 1] || ''].join(' ');
      const m = window.match(COLOUR_PROP);
      if (!m) return;
      // Only complain about literals, not var(...) / token references.
      const valuePart = window.slice(window.indexOf(m[0]) + m[0].length);
      if (/var\(|props\.|\.length|theme|#[0-9a-f]{3,8}/i.test(valuePart) === false) return;
      if (!isLightLiteral(valuePart) && !/#[0-9a-f]{3,8}/i.test(valuePart)) return;
      if (/var\(/.test(valuePart.split(',')[0])) return;
      out.push({ file: rel(file), line: i + 1, text: ln.trim().slice(0, 160) });
    });
  }
  return out;
}

/* ---------------------------------------------------------------- report */

const { records: cssRecords, ruleIndex } = analyseCss();
const darkSubjects = buildDarkSubjectSet(ruleIndex);
const lightCompanions = buildLightCompanionSet(ruleIndex);

const hasSubject = (set, subject) =>
  subject.split(',').some((part) => set.has(normaliseSelector(part)));

const lightRules = cssRecords.filter((r) => !r.isDark);
const unpatchedMap = new Map();
for (const r of lightRules) {
  const subject = normaliseSelector(r.selector);
  if (isIntentionalDark(subject)) continue;
  if (isLightCompanion(subject)) continue;
  const patched = hasSubject(darkSubjects, subject) || hasSubject(lightCompanions, subject);
  if (patched) continue;
  const key = subject;
  if (!unpatchedMap.has(key)) unpatchedMap.set(key, { selector: subject, line: r.line, props: new Set(), values: new Set() });
  const e = unpatchedMap.get(key);
  e.props.add(r.prop);
  e.values.add(r.value);
}

const unpatched = [...unpatchedMap.values()].sort((a, b) => a.line - b.line);

const jsxFiles = walk(SRC).filter((f) => f.endsWith('.jsx'));
const jsx = analyseJsx(jsxFiles);
const jsxByFile = new Map();
for (const j of jsx) jsxByFile.set(j.file, (jsxByFile.get(j.file) ?? 0) + 1);

if (ARGS.has('--json')) {
  console.log(JSON.stringify({
    css: { unpatched: unpatched.map((u) => ({ selector: u.selector, line: u.line, props: [...u.props], values: [...u.values] })) },
    jsx: jsx,
  }, null, 2));
} else {
  const totalCssRules = new Set(cssRecords.map((r) => normaliseSelector(r.selector))).size;
  console.log('');
  console.log('Theme audit — places that cannot follow dark mode');
  console.log('=================================================');
  console.log('');
  console.log(`CSS   : ${unpatched.length} rule(s) paint a light colour with no [data-theme="dark"] patch`);
  console.log(`        (${cssRecords.length} painting declarations scanned across ${totalCssRules} selectors)`);
  console.log(`JSX   : ${jsx.length} inline colour literal(s) in ${jsxByFile.size} file(s)`);
  console.log('');

  if (ARGS.has('--list')) {
    console.log('--- CSS rules ---');
    for (const u of unpatched) {
      console.log(`index.css:${u.line}  ${u.selector}`);
      console.log(`    ${[...u.props].join(', ')}: ${[...u.values].join(' | ')}`);
    }
    console.log('');
    console.log('--- JSX literals ---');
    for (const j of jsx) console.log(`${j.file}:${j.line}  ${j.text}`);
    console.log('');
  } else {
    console.log('Top files by inline colour literal:');
    [...jsxByFile.entries()].sort((a, b) => b[1] - a[1]).slice(0, 15)
      .forEach(([f, n]) => console.log(`  ${String(n).padStart(3)}  ${f}`));
    console.log('');
    console.log('First 15 unpatched CSS rules:');
    unpatched.slice(0, 15).forEach((u) => console.log(`  index.css:${u.line}  ${u.selector}`));
    console.log('');
    console.log('Add --list for the full list.');
  }
  console.log('');
}

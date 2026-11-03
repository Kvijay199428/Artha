// ============================================================================
// ARTHA - multi-company core
// ----------------------------------------------------------------------------
// Every company owns one folder:   data/COMP0001/   data/COMP0002/   ...
// Everything that used to live straight under data/ (bills, clients, meta.json,
// profile.json, backups, Saved Invoices ...) now lives inside that folder.
//
// The server never touches a company folder directly. Each request runs inside
// an AsyncLocalStorage "company context" that is set from the login session, and
// server.js asks dataDir() for the folder. A request without a session has no
// context, so it cannot read or write any company's files.
// ============================================================================
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { AsyncLocalStorage } from 'async_hooks';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Global (not per company): the registry, the port file, the error log.
export const DATA_ROOT = path.join(__dirname, 'data');
export const REGISTRY_FILE = path.join(DATA_ROOT, 'companies.json');
export const COMPANY_FILE = 'company.json'; // describes one company, lives inside its folder

// Sub-folders every company gets (JSON documents, one file per record).
export const COMPANY_DIRS = ['bills', 'clients', 'templates', 'products', 'expenses', 'recurring', 'receipts', 'profiles', 'purchases'];

// "COMP0001", "COMP0002" ... (4 digits minimum, grows past COMP9999 if ever needed)
export const ID_RE = /^COMP\d{4,}$/;
export const formatCompanyId = (n) => `COMP${String(n).padStart(4, '0')}`;
const seqOf = (id) => parseInt(String(id).slice(4), 10) || 0;

// ---------------------------------------------------------------------------
// Company context (which company is this request for?)
// ---------------------------------------------------------------------------
const als = new AsyncLocalStorage();

export class NoCompanyError extends Error {
  constructor() { super('No company is open'); this.code = 'no-company'; }
}

export const companyDirOf = (id) => path.join(DATA_ROOT, id);
export const currentCompanyId = () => als.getStore()?.companyId || null;
export const currentSessionId = () => als.getStore()?.sessionId || null;
export function dataDir() {
  const s = als.getStore();
  if (!s) throw new NoCompanyError();
  return s.companyDir;
}
export const runInCompany = (companyId, fn, extra = {}) =>
  als.run({ companyId, companyDir: companyDirOf(companyId), ...extra }, fn);

export function ensureCompanyDirs(companyId) {
  const base = companyDirOf(companyId);
  fs.mkdirSync(base, { recursive: true });
  for (const d of COMPANY_DIRS) fs.mkdirSync(path.join(base, d), { recursive: true });
}

// ---------------------------------------------------------------------------
// Small file helpers (kept local so this module has no dependency on server.js)
// ---------------------------------------------------------------------------
function readJson(file, fallback) {
  try { if (fs.existsSync(file)) return JSON.parse(fs.readFileSync(file, 'utf-8')); } catch { /* corrupt: use fallback */ }
  return fallback;
}
function writeJsonAtomic(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = `${file}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2), 'utf-8');
  fs.renameSync(tmp, file);
}

// ---------------------------------------------------------------------------
// Registry: data/companies.json  ->  { companies: [{ id, name, createdAt, lastOpenedAt }] }
// The company folders are the truth. syncRegistry() re-adds a folder that is
// missing from the file (hand-copied company, lost companies.json) and drops
// entries whose folder is gone.
// ---------------------------------------------------------------------------
const readRegistry = () => {
  const reg = readJson(REGISTRY_FILE, { companies: [] });
  return Array.isArray(reg?.companies) ? reg : { companies: [] };
};
const writeRegistry = (reg) => writeJsonAtomic(REGISTRY_FILE, reg);

function companyFolders() {
  try {
    return fs.readdirSync(DATA_ROOT, { withFileTypes: true })
      .filter((e) => e.isDirectory() && ID_RE.test(e.name))
      .map((e) => e.name)
      .sort((a, b) => seqOf(a) - seqOf(b));
  } catch { return []; }
}

function nameFromFolder(id) {
  const dir = companyDirOf(id);
  const own = readJson(path.join(dir, COMPANY_FILE), null);
  if (own?.name) return String(own.name);
  const profile = readJson(path.join(dir, 'profile.json'), null);
  if (profile?.businessName) return String(profile.businessName);
  return id;
}

export function syncRegistry() {
  const reg = readRegistry();
  const folders = companyFolders();
  const byId = new Map(reg.companies.filter((c) => c && ID_RE.test(c.id)).map((c) => [c.id, c]));
  let changed = reg.companies.length !== byId.size;
  const next = [];
  for (const id of folders) {
    let entry = byId.get(id);
    if (!entry) {
      const own = readJson(path.join(companyDirOf(id), COMPANY_FILE), {});
      entry = { id, name: nameFromFolder(id), createdAt: own.createdAt || new Date().toISOString(), lastOpenedAt: null };
      changed = true;
    }
    next.push(entry);
  }
  if (next.length !== byId.size) changed = true;
  if (changed || !fs.existsSync(REGISTRY_FILE)) writeRegistry({ companies: next });
  return next;
}

export const listRegistry = () => syncRegistry();
export const getCompany = (id) => (ID_RE.test(String(id)) ? listRegistry().find((c) => c.id === id) || null : null);

export function nextCompanyId() {
  const used = new Set([...companyFolders(), ...readRegistry().companies.map((c) => c?.id)]);
  let n = 1;
  for (const id of used) n = Math.max(n, seqOf(id) + 1);
  return formatCompanyId(n);
}

export function createCompany(rawName) {
  const name = String(rawName ?? '').replace(/\s+/g, ' ').trim().slice(0, 100);
  if (!name) { const e = new Error('Company name is required'); e.code = 'name-required'; throw e; }
  const id = nextCompanyId();
  ensureCompanyDirs(id);
  const createdAt = new Date().toISOString();
  writeJsonAtomic(path.join(companyDirOf(id), COMPANY_FILE), { id, name, createdAt });
  const reg = readRegistry();
  reg.companies.push({ id, name, createdAt, lastOpenedAt: null });
  writeRegistry(reg);
  return { id, name, createdAt, lastOpenedAt: null };
}

export function touchCompany(id) {
  const reg = readRegistry();
  const c = reg.companies.find((x) => x.id === id);
  if (c) { c.lastOpenedAt = new Date().toISOString(); writeRegistry(reg); }
}

// Size of one company in MB (backups excluded: they only repeat the same data).
// Cached for a few seconds so the company list stays quick.
const sizeCache = new Map();
export function companySizeMB(id) {
  const hit = sizeCache.get(id);
  if (hit && Date.now() - hit.at < 10_000) return hit.value;
  let total = 0;
  const walk = (dir, top) => {
    let entries = [];
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
    for (const e of entries) {
      if (top && e.name === 'backups') continue;
      const p = path.join(dir, e.name);
      if (e.isDirectory()) walk(p, false);
      else { try { total += fs.statSync(p).size; } catch { /* vanished */ } }
    }
  };
  walk(companyDirOf(id), true);
  const value = Math.round((total / (1024 * 1024)) * 10) / 10;
  sizeCache.set(id, { at: Date.now(), value });
  return value;
}

// Run fn once for every company, each inside its own company context. Used by
// the background jobs (daily backup, trash purge, recurring invoices).
export async function forEachCompany(fn) {
  for (const c of listRegistry()) {
    try {
      ensureCompanyDirs(c.id);
      await runInCompany(c.id, async () => fn(c));
    } catch (err) {
      console.warn(`[${c.id}] background job failed:`, err?.message || err);
    }
  }
}

// ---------------------------------------------------------------------------
// Login sessions (in memory: a server restart asks for the company again)
// ---------------------------------------------------------------------------
export const SESSION_COOKIE = 'artha_sid';
const sessions = new Map(); // token -> { companyId, createdAt }

export function createSession(companyId) {
  const token = crypto.randomBytes(32).toString('hex');
  sessions.set(token, { companyId, createdAt: Date.now() });
  return token;
}
export const getSession = (token) => (token ? sessions.get(token) || null : null);
export const destroySession = (token) => { if (token) sessions.delete(token); };

export function parseCookies(header) {
  const out = {};
  for (const part of String(header || '').split(';')) {
    const i = part.indexOf('=');
    if (i < 0) continue;
    const k = part.slice(0, i).trim();
    if (k) { try { out[k] = decodeURIComponent(part.slice(i + 1).trim()); } catch { out[k] = part.slice(i + 1).trim(); } }
  }
  return out;
}
export const sessionCookie = (token) => `${SESSION_COOKIE}=${token}; Path=/; HttpOnly; SameSite=Strict`;
export const clearedSessionCookie = () => `${SESSION_COOKIE}=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0`;

// ---------------------------------------------------------------------------
// One-time move of a pre-multi-company install into data/COMP0001
// ---------------------------------------------------------------------------
// Pre-multi-company layout -> where it goes inside the company folder.
const LEGACY_IN_DATA = [
  ...COMPANY_DIRS, 'trash', 'backups', 'cancelled-pdf-originals',
  'profile.json', 'meta.json', 'local-prefs.json',
].map((n) => ({ from: path.join(DATA_ROOT, n), to: n }));
const LEGACY_AT_APP_ROOT = [
  { from: path.join(__dirname, 'Saved Invoices'), to: 'Saved Invoices' },
  // Renamed: "Trash" and the bill-trash folder "trash" would be the same
  // folder on Windows and macOS (case-insensitive file systems).
  { from: path.join(__dirname, 'Trash'), to: 'pdf-trash' },
];
const LEGACY_ALL = [...LEGACY_IN_DATA, ...LEGACY_AT_APP_ROOT];
const MIGRATION_MARKER = path.join(DATA_ROOT, '.legacy-migration');

const hasContent = (p) => {
  try {
    const st = fs.statSync(p);
    if (!st.isDirectory()) return true;
    return fs.readdirSync(p).length > 0;
  } catch { return false; }
};

function moveEntry(src, dst) {
  if (!fs.existsSync(src)) return;
  if (fs.existsSync(dst)) {
    // The company folder was just created with empty sub-folders: those make way.
    // Anything that already has content is never overwritten.
    if (fs.statSync(dst).isDirectory() && fs.readdirSync(dst).length === 0) fs.rmdirSync(dst);
    else { console.warn(`[migrate] ${dst} already has content, left ${src} where it is`); return; }
  }
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  try {
    fs.renameSync(src, dst);
  } catch (err) {
    if (err.code !== 'EXDEV') throw err;
    fs.cpSync(src, dst, { recursive: true });
    fs.rmSync(src, { recursive: true, force: true });
  }
}

export function migrateLegacyData() {
  fs.mkdirSync(DATA_ROOT, { recursive: true });
  let target = null;
  if (fs.existsSync(MIGRATION_MARKER)) {
    // A previous run was interrupted: carry on into the same company.
    const t = fs.readFileSync(MIGRATION_MARKER, 'utf-8').trim();
    if (ID_RE.test(t)) target = t;
  } else if (companyFolders().length === 0 && LEGACY_ALL.some((e) => hasContent(e.from))) {
    target = formatCompanyId(1);
    fs.writeFileSync(MIGRATION_MARKER, target, 'utf-8');
  }
  if (!target) {
    // Nothing to migrate. Sweep the empty folders old versions created at start-up.
    for (const e of LEGACY_IN_DATA) {
      try { if (fs.statSync(e.from).isDirectory() && fs.readdirSync(e.from).length === 0) fs.rmdirSync(e.from); } catch { /* not there */ }
    }
    return { migrated: false };
  }

  console.log(`[migrate] Moving your existing data into data/${target} ...`);
  ensureCompanyDirs(target);
  const dir = companyDirOf(target);
  for (const e of LEGACY_ALL) {
    if (fs.existsSync(e.from)) {
      if (hasContent(e.from)) moveEntry(e.from, path.join(dir, e.to));
      else { try { fs.rmSync(e.from, { recursive: true, force: true }); } catch { /* ignore */ } }
    }
  }
  const profile = readJson(path.join(dir, 'profile.json'), {});
  const file = path.join(dir, COMPANY_FILE);
  if (!fs.existsSync(file)) {
    writeJsonAtomic(file, {
      id: target,
      name: (profile.businessName && String(profile.businessName).trim()) || 'My Company',
      createdAt: new Date().toISOString(),
      migratedFromSingleCompany: true,
    });
  }
  fs.rmSync(MIGRATION_MARKER, { force: true });
  syncRegistry();
  console.log(`[migrate] Done. Your previous data is now company ${target}.`);
  return { migrated: true, companyId: target };
}

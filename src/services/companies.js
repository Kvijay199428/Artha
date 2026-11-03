// ============================================================================
// ARTHA - companies, login and logout (browser side)
// ----------------------------------------------------------------------------
// The server keeps one folder per company (data/COMP0001, data/COMP0002 ...)
// and knows which company this browser opened from a session cookie. This file
// is the only place that talks to /api/companies and /api/auth/*.
//
// Several settings live in the browser (Print & PDF, Region, theme ...). They
// belong to a company too, so they are cleared when another company is opened;
// the new company's own copy is then restored from its data folder (see
// utils/prefsMirror.js) when the page reloads.
// ============================================================================
import { flushPrefs, pauseMirroring } from '../utils/prefsMirror';
import { UNLOCKED_KEY } from '../utils/appLock';

export const AUTH_REQUIRED_EVENT = 'artha-auth-required';
const ACTIVE_COMPANY_KEY = 'artha_activeCompany'; // which company this browser last opened

async function call(url, options = {}) {
  const res = await fetch(url, { headers: { 'Content-Type': 'application/json' }, ...options });
  let body = null;
  try { body = await res.json(); } catch { /* empty body */ }
  if (!res.ok) {
    const err = new Error(body?.error || `Request failed (${res.status})`);
    err.status = res.status;
    err.body = body;
    throw err;
  }
  return body;
}

export const getSession = () => call('/api/auth/session');
export const listCompanies = () => call('/api/companies');
export const createCompanyOnServer = (name) => call('/api/companies', { method: 'POST', body: JSON.stringify({ name }) });
export const loginToCompany = (companyId, pin) => call('/api/auth/login', {
  method: 'POST', body: JSON.stringify(pin ? { companyId, pin } : { companyId }),
});
export const logoutOnServer = () => call('/api/auth/logout', { method: 'POST' });

// Any API answer "401 + X-Artha-Auth: required" means the company was closed
// (the app was restarted, or another tab logged out): show the company list.
export function installAuthWatcher() {
  if (window.__arthaAuthWatcher) return;
  window.__arthaAuthWatcher = true;
  const original = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const res = await original(...args);
    if (res.status === 401 && res.headers.get('X-Artha-Auth') === 'required') {
      window.dispatchEvent(new Event(AUTH_REQUIRED_EVENT));
    }
    return res;
  };
}

// What belongs to the company that is open, and must not leak into the next one.
// App-level notices (PWA install, update banner) are not company data.
const KEEP_KEYS = new Set(['freegstbill_pwa_dismissed_at', 'freegstbill_dismissedUpdate', ACTIVE_COMPANY_KEY]);
const COMPANY_PREFIXES = ['gst_', 'freegstbill_', 'fgsb_'];

export function clearCompanyScopedStorage() {
  pauseMirroring(); // clearing must not wipe the closing company's saved copy
  try {
    const doomed = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k && !KEEP_KEYS.has(k) && COMPANY_PREFIXES.some((p) => k.startsWith(p))) doomed.push(k);
    }
    doomed.forEach((k) => localStorage.removeItem(k));
  } catch { /* storage blocked */ }
  try { sessionStorage.clear(); } catch { /* storage blocked */ }
}

// Cached API answers (offline copy) are per company too.
async function dropOfflineApiCache() {
  try { if (typeof caches !== 'undefined') await caches.delete('api-cache'); } catch { /* none */ }
}

export const rememberedCompany = () => { try { return localStorage.getItem(ACTIVE_COMPANY_KEY); } catch { return null; } };

// Call after a successful login / company creation. Reloads the page so the
// whole app starts fresh for that company (its own settings, its own data).
export async function enterCompany(companyId, { keepStorage = false } = {}) {
  const switching = rememberedCompany() !== companyId;
  if (switching) {
    await dropOfflineApiCache();
    // keepStorage: a company that was just created already holds its first
    // settings (from the setup wizard); they must survive the reload.
    if (!keepStorage) clearCompanyScopedStorage();
  }
  try {
    localStorage.setItem(ACTIVE_COMPANY_KEY, companyId);
    // The PIN (if the company has one) was just checked by the login.
    sessionStorage.setItem(UNLOCKED_KEY, '1');
  } catch { /* storage blocked */ }
  window.location.reload();
}

// Close the company: save what is pending, end the session, back to the list.
export async function logoutAndReload() {
  try { await flushPrefs(); } catch { /* best effort */ }
  try { await logoutOnServer(); } catch { /* the server may be gone already */ }
  clearCompanyScopedStorage();
  await dropOfflineApiCache();
  try { localStorage.removeItem(ACTIVE_COMPANY_KEY); } catch { /* storage blocked */ }
  window.location.reload();
}

// "COMP0007" -> 7
export const companySeq = (id) => parseInt(String(id).slice(4), 10) || 0;
export const nextCompanyCode = (companies) => {
  const n = companies.reduce((m, c) => Math.max(m, companySeq(c.id)), 0) + 1;
  return `COMP${String(n).padStart(4, '0')}`;
};

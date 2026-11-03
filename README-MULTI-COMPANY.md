# ARTHA — Multiple Companies

ARTHA now opens on a **Select Company for Operation** page (like BusyWin). Every company has its
own login, its own settings and its own folder: `data/COMP0001`, `data/COMP0002`, `data/COMP0003` …
Nothing is shared between companies.

---

## 1. Install the update

1. **Close ARTHA** and **copy your whole `data` folder somewhere safe** (one-time precaution).
2. Copy the files from this package into your ARTHA folder, keeping the same paths
   (replace when asked). New files: `companies.js`, `src/services/companies.js`,
   `src/components/CompanyGate.jsx`, `CompanySelect.jsx`, `CompanySelect.css`, `CompanySwitcher.jsx`.
3. Rebuild and start as you always do:
   ```
   npm run build
   npm run server        (or your normal launcher / "npm start")
   ```
   If you use the Windows launcher (`launcher/ServerManager.cs`), rebuild it with `npm run launcher:build`.
4. Open ARTHA in the browser.

### Your existing data
On the first start the server moves everything you already had into **`data/COMP0001`** automatically
(bills, clients, products, settings, backups, `Saved Invoices`, `Trash`). The company is named after your
business name. Nothing is deleted. If the move is interrupted, start ARTHA again and it carries on.

---

## 2. Daily use

| You want to… | Do this |
|---|---|
| Open a company | Click it (or use ↑ ↓) then press **Enter**, double-click it, or press **Open Company** |
| Find a company | Type in **Search Company** (name or code) |
| Add a company | Press **Setup New Company** → the setup wizard opens |
| Switch company / leave | In the app: left menu → **Switch / Logout**. You return to the list |

### Setup New Company (the wizard)
1. **Company name** (the code `COMP000N` is assigned automatically)
2. Business type
3. Paper size and language
4. **Create company** — the company is created, opened, and its first settings saved in its own folder.

*Cancel* returns to the list without creating anything. Add GSTIN, address and bank details afterwards in
**Settings**, as usual.

### PIN
If a company has an app-lock PIN (**Settings → App lock**), the list shows a 🔒 and asks for the PIN when you
open it. Wrong PINs are counted per company (5 wrong → 30 s wait). Forgot PIN: create a file named
`RESET-PIN` in the ARTHA folder, then open the company.

---

## 3. Where things are stored

```
data/
  companies.json          list of companies (rebuilt automatically from the folders if lost)
  port.txt, errors.log    shared by the app
  COMP0001/
    company.json          id, name, created date
    bills/ clients/ products/ purchases/ expenses/ receipts/ recurring/ templates/ profiles/
    profile.json  meta.json  local-prefs.json
    Saved Invoices/       PDF archive of this company
    pdf-trash/            deleted PDFs (was "Trash")
    trash/                deleted invoices (30 days)
    backups/              daily backups of THIS company (30 days)
  COMP0002/ …
```
* Every request is served from the folder of the company that is logged in. A browser with no login cannot read any data.
* Daily backup, trash clean-up and recurring invoices run for **every** company.
* Daily backups no longer copy `Saved Invoices` / `pdf-trash` (they are large and re-creatable).
* Extra backup folder (Control Panel): copies go to `<your folder>/FreeGSTBill Backups/COMPxxxx/<date>`.
  Copies made before this update stay in `<your folder>/FreeGSTBill Backups/<date>`.
* To move or back up a company: copy its `data/COMPxxxx` folder. To bring one in, paste a `COMPxxxx`
  folder into `data/` and restart (it appears in the list).

---

## 4. Login / logout API

All under the same address as the app. The login is a cookie (`artha_sid`, HttpOnly, SameSite=Strict) kept
in memory on the server — **restarting ARTHA logs everyone out** and the list shows again.

| Method & path | Purpose |
|---|---|
| `GET  /api/companies` | List companies (id, name, created, last opened, size, locked) |
| `POST /api/companies` `{ "name": "…" }` | Create `COMP000N` + its folder, and log in to it |
| `POST /api/auth/login` `{ "companyId": "COMP0001", "pin": "123456" }` | Log in (`pin` only if locked; answers `401 pin-required` first) |
| `POST /api/auth/logout` | Log out |
| `GET  /api/auth/session` | `{ authenticated, company }` |
| everything else under `/api` | needs a login, otherwise `401` (`X-Artha-Auth: required`). `/api/health`, `/api/version`, `/api/check-update` stay open |

Example (command line):
```
curl -c jar -H "Content-Type: application/json" -d '{"companyId":"COMP0001"}' http://localhost:11001/api/auth/login
curl -b jar http://localhost:11001/api/bills
```

---

## 5. Good to know
* One company is open per browser at a time. Two tabs in the same browser share the login.
* Browser-side settings (print style, region, theme, GST filing marks …) are per company; they are
  cleared and restored from the company's folder whenever you switch.
* `import-busywin.py` now imports **into one company**: `python scripts/import-busywin.py --artha-company COMP0002`
  (create that company in ARTHA first). `--company` is still the BusyWin folder.
* The "Fin. Year(s)" column of BusyWin is shown here as **Created / Last Opened**.
* Start-up checks (launcher, `start-*.ps1/.sh`) now call `/api/health`, because `/api/profile` needs a login.
* **Tests:** `tests/smoke.mjs` and `scripts/verify-release.mjs` call company APIs without logging in; add a
  login (`POST /api/auth/login`) first, or they will get `401`.
* Deleting or renaming a company is not in this version: to remove one, close ARTHA and delete its
  `data/COMPxxxx` folder; to rename, edit `name` in its `company.json` and in `data/companies.json`.

## 6. Troubleshooting
| Problem | Fix |
|---|---|
| List is empty after the update | Normal on a brand-new install: press **Setup New Company**. If you expected data, check that `data/COMP0001` exists and restart |
| "Cannot reach the ARTHA server" | ARTHA is not running — start it and press *Try again* |
| "Your session ended" notice | ARTHA was restarted; open the company again |
| Old data still in `data/bills` | Both old and new folders existed; ARTHA never overwrites — move the files into `data/COMP0001/bills` yourself |

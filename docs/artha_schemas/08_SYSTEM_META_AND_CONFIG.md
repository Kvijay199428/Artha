# ARTHA Database Schema: System Meta, Config & Security

## 1. System Metadata (`data/meta.json`)

`data/meta.json` acts as ARTHA's operational catalog, managing atomic sequence generation, display defaults, and import audit stamps.

### Core Keys in `meta.json`

| Key | Type | Description |
| :--- | :--- | :--- |
| `regionMode` | `String` | Regional tax mode enum: `'india'`, `'international'`, `'both'`. Controls visibility of GST-only fields. |
| `invoiceNumberSettings` | `Object` | Global numbering sequence configuration (see below). |
| `invoiceNumberSeries` | `Object` | Map of per-business custom numbering sequences `{ [businessKey]: settings }`. |
| `invoiceDisplayOptions` | `Object` | Default toggle states for invoice sections (bank, logo, HSN, UPI QR, round-off, terms). |
| `stockAlertSettings` | `Object` | Global inventory warning settings (`{ enabled: true, threshold: 5 }`). |
| `lastBusyWinImport` | `Object` | Audit trail of BusyWin ERP data migration (timestamp, file paths, entity counts). |
| `counter_*` | `Integer` | Atomic integer counters for sequential voucher generation. |

### `invoiceNumberSettings` Schema
```json
{
  "format": "branded",
  "brandPrefix": "HPS",
  "separator": "/",
  "showFinYear": true,
  "startNumber": 1,
  "padDigits": 5
}
```
*Generated output example:* `HPS00001/2026-27`

### `invoiceDisplayOptions` Schema
Controls rendering flags across invoice PDFs and printouts:
- `showGST`, `showGSTIN`, `showPlaceOfSupply`: Statutory tax indicators.
- `showHSN`: HSN/SAC column visibility.
- `showBankDetails`, `showUPI`: Bank credentials and dynamic UPI QR code.
- `showLogo`, `showSignature`: Visual brand assets.
- `showTerms`, `showNotes`: Legal disclaimers and customer memos.
- `showRoundOff`: Mathematical 50-paise rounding row.
- `paperSize`: Standard paper layout (`'A4'`, `'A5'`, `'thermal'`).
- `thermalFontSize`, `thermalCompact`: POS slip formatting options.
- `showTDS`, `tdsSection`, `tdsRate`: Tax Deducted at Source (Section 194Q/194C).
- `showTCS`, `tcsSection`, `tcsRate`: Tax Collected at Source (Section 206C).

---

## 2. Local Preferences & User State (`data/local-prefs.json`)

Maintains user interface state and client preferences across app launches:
- `freegstbill_theme`: Active color theme (`'light'` or `'dark'`).
- `gst_dashboardColumns`: JSON map of column visibility toggles for the Dashboard invoices table.
- `freegstbill_sidebarAutoHide`: Automatic sidebar collapse preference.
- `gst_printSettings`: Thermal printing font family, pitch, and capitalization presets.
- `gst_itrCalcInputs`: Income Tax regime comparison tool inputs (salary, business turnover, 80C deductions).
- `gst_itrPresumptive`: Presumptive taxation model inputs (Section 44AD / 44ADA).
- `gst_itrAdvanceTax`: Advance tax quarterly installment payment records.

---

## 3. Security, Locks & Trash Bin

### PIN Lock (`data/lock.json`)
If enabled, ARTHA's Express backend locks API routes until authenticated by client PIN:
- Stores salted hash of 4-6 digit numeric PIN.
- Verified on boot via `POST /api/lock/verify`.

### Trash Bin (`data/trash/`)
When documents or bills are deleted:
- The JSON document moves to `data/trash/<id>.json`.
- The corresponding generated PDF moves from `Saved Invoices/` to `data/trash/<filename>.pdf`.
- Can be restored to active collections or permanently purged.

### Daily Automatic Backups (`data/backups/`)
ARTHA takes automatic daily directory snapshots at midnight and before major imports:
```
data/backups/
  ├── 2026-10-29/
  ├── 2026-10-30/
  └── 2026-10-31/
        ├── bills/
        ├── clients/
        ├── products/
        ├── purchases/
        ├── expenses/
        ├── receipts/
        ├── profiles/
        ├── meta.json
        └── profile.json
```
- Preserves 30 days of rollback snapshots.
- Users can trigger manual snapshots via `POST /api/backups/now`.
- Supports secondary offsite backup target folder on external or secondary drives (e.g. `D:\Backups\ARTHA`).


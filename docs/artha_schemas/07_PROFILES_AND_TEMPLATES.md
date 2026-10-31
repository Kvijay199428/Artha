# ARTHA Database Schema: Business Profiles & Templates

## 1. Business Profiles (`data/profiles/` & `data/profile.json`)

ARTHA supports multi-company and multi-state GST accounting. The active company profile is persisted at `data/profile.json` (as well as individual profile files in `data/profiles/<profileId>.json` for multi-profile installations).

### Field Specifications

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `businessName` | `String` | Legal trade or registered enterprise name (e.g., `'HPS FURNITURE & DECORATION'`). |
| `address` | `String` | Registered street address, premises name, road. |
| `city` | `String` | City / District. |
| `state` | `String` | Indian State or Union Territory name (determines origin for GST routing). |
| `country` | `String` | Country name (defaults to `'India'`). |
| `pin` | `String` | 6-digit postal PIN code. |
| `gstin` | `String (15 Chars)` | 15-character statutory GSTIN. |
| `pan` | `String (10 Chars)` | 10-character Income Tax Permanent Account Number. |
| `email` | `String` | Official corporate communication email. |
| `phone` | `String` | Primary telephone or mobile number. |
| `bankName` | `String` | Primary settlement bank name (e.g. `'STATE BANK OF INDIA'`). |
| `accountNumber` | `String` | Bank account number. |
| `ifsc` | `String (11 Chars)`| Indian Financial System Code (e.g. `'SBIN0018817'`). |
| `swift` | `String` | SWIFT / BIC code for inward foreign remittances. |
| `upiId` | `String` | Virtual Payment Address (VPA) for invoice UPI QR code generation. |
| `logo` | `String (Base64)` | Brand logo image encoded as a data URL (`data:image/png;base64,...`). |
| `signature` | `String (Base64)` | Authorized signatory stamp/signature image data URL. |
| `googleClientId` | `String` | Google OAuth Client ID for cloud drive synchronization. |
| `googleDriveFolder` | `String` | Target Google Drive folder name for offsite PDF backups. |
| `paymentAccounts` | `Array<Account>` | Multi-bank accounts directory (see below). |

### `paymentAccounts` Schema
Allows users to switch which bank account appears on invoices (e.g. HDFC Current vs SBI Overdraft):
```json
{
  "id": "acc_1793257592700_8eaypd",
  "label": "Primary SBI Current",
  "bankName": "STATE BANK OF INDIA",
  "accountHolderName": "HPS FURNITURE AND DECORATION",
  "accountNumber": "45552725264",
  "accountType": "current",
  "ifsc": "SBIN0018817",
  "swift": "",
  "upiId": "hpsfurniture@sbi",
  "isDefault": true,
  "isActive": true,
  "notes": "Main operating account"
}
```

---

## 2. Terms & Conditions Templates (`data/templates/`)

Stores reusable Terms of Sale, Payment Clauses, Warranty Conditions, and Jurisdiction Disclaimers. Persisted under `data/templates/<templateId>.json`.

### Field Specifications

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `id` | `String` | Template identifier (e.g. `'default'`, `'service_terms'`, `'export_terms'`). |
| `name` | `String` | Descriptive name shown in the UI dropdown (e.g. `'Standard Retail Terms'`). |
| `content` | `String (HTML/Text)`| Sanitized multi-line terms and conditions text. |

### Sample Template Document
```json
{
  "id": "default",
  "name": "Standard Terms",
  "content": "1. Payment is due within 15 days of invoice date unless otherwise agreed in writing.\n2. Goods once sold will not be taken back or exchanged.\n3. All disputes are subject to Faridabad jurisdiction only."
}
```

---

## 3. Recurring Invoice Schedules (`data/recurring/`)

Automates periodic billing (retainers, rent, monthly AMC contracts, subscriptions). Persisted under `data/recurring/<id>.json`.

### Field Specifications

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `id` | `String` | Unique schedule identifier (e.g. `rec_1793257592000`). |
| `clientName` | `String` | Target client name. |
| `frequency` | `String` | Enum: `'weekly'`, `'monthly'`, `'quarterly'`, `'annually'`. |
| `interval` | `Integer` | Step interval (e.g. every `1` month, every `2` quarters). |
| `nextDate` | `String (YYYY-MM-DD)` | Date when the next automatic invoice will be created. |
| `endDate` | `String (YYYY-MM-DD)` | Expiration date of recurring contract (optional). |
| `maxOccurrences`| `Integer` | Maximum billing cycles to generate before auto-stopping. |
| `active` | `Boolean` | True if active, false if paused. |
| `items` | `Array<Item>` | Line items template with prices, tax slabs, and quantities. |
| `ownerGstin` | `String` | Business profile owner. |

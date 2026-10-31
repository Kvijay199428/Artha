# ARTHA Database Schema: Clients & Customers (`data/clients/`)

## 1. Overview & Purpose
The `clients` collection acts as ARTHA's customer and debtor master directory. It maintains party details, statutory identifiers (GSTIN, PAN), billing addresses, contact channels, and state coding required for automated inter-state vs. intra-state GST tax determination.

Files are stored individually under `data/clients/` as `cli_<id>.json`.

---

## 2. Field Specifications

| Field Name | Type | Required | Description & Constraints |
| :--- | :--- | :---: | :--- |
| `id` | `String` | Yes | Unique client ID (e.g., `cli_1102`, `cli_1793257592000`). |
| `name` | `String` | Yes | Legal party or trade name of the client/customer. Must be non-empty. |
| `address` | `String` | No | Street address, building number, industrial area. |
| `city` | `String` | No | City or town name (e.g., `'Faridabad'`, `'Noida'`). |
| `state` | `String` | No | Indian State or Union Territory name (e.g., `'Haryana'`, `'Uttar Pradesh'`). Used to determine place of supply. |
| `stateCode` | `String (2 Digits)`| No | 2-digit Indian GST State Code (e.g., `'06'` for Haryana, `'09'` for Uttar Pradesh, `'07'` for Delhi). Derived automatically from GSTIN or state name. |
| `country` | `String` | No | Country name. Defaults to `'India'`. In international mode, foreign countries trigger export invoice flows. |
| `pin` | `String (6 Digits)`| No | 6-digit postal PIN code. |
| `gstin` | `String (15 Chars)`| No | 15-character alphanumeric GST Identification Number. Validated against standard GSTIN checksum. |
| `pan` | `String (10 Chars)`| No | 10-character alphanumeric Permanent Account Number (chars 3 to 12 of GSTIN). |
| `phone` | `String` | No | Contact telephone or mobile number (for WhatsApp document sharing and SMS alerts). |
| `email` | `String` | No | Email address for digital invoice and payment reminder delivery. |
| `isSEZ` | `Boolean` | No | Flag indicating Special Economic Zone client (enabling IGST LUT supply or tax-paid export). |
| `notes` | `String` | No | Internal notes, payment terms, or client account remarks. |
| `ownerGstin` | `String` | No | Business profile ownership stamp for multi-company isolation. |
| `ownerName` | `String` | No | Legal name of the business profile that owns this client account. |

---

## 3. GST State Code Mapping Logic
When a client's `gstin` is supplied, ARTHA's `decodeGstin()` utility automatically decodes:
- State Code (`gstin.slice(0, 2)`)
- PAN (`gstin.slice(2, 12)`)
- State Name (mapped from the Ministry of Finance state code dictionary).

For B2C unregistered consumers, `gstin` remains blank, and `state` dictates place of supply.

---

## 4. Sample JSON Document
```json
{
  "id": "cli_1432",
  "name": "ARK INTERNO LLP",
  "address": "PLOT NO-10, ECOTECH-X, Greater Noida",
  "city": "Greater Noida",
  "state": "Uttar Pradesh",
  "stateCode": "09",
  "pin": "201308",
  "country": "India",
  "gstin": "09ACGFA8344K1Z0",
  "pan": "ACGFA8344K",
  "phone": "+91-9876543210",
  "email": "accounts@arkinterno.com",
  "isSEZ": false,
  "notes": "Payment terms 30 days net"
}
```


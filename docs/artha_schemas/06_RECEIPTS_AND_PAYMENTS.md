# ARTHA Database Schema: Receipts & Payment Vouchers (`data/receipts/`)

## 1. Overview & Purpose
The `receipts` collection stores formal Payment Receipt Vouchers issued to clients upon receiving payment settlements, advances, or security deposits.

Key capabilities:
- **Bi-Directional Invoice Synchronization:** Saving a receipt linked to an invoice (`againstInvoice`) automatically updates the corresponding sales invoice's `paidAmount`, appends to its `payments` ledger, and transitions its status (`unpaid` -> `partial` -> `paid`).
- **Audit Numbering:** Sequenced with the document numbering engine (`RCP` prefix) or company-specific custom series.

Files are stored individually under `data/receipts/` as `rcp_<id>.json`.

---

## 2. Field Specifications

| Field Name | Type | Required | Description & Constraints |
| :--- | :--- | :---: | :--- |
| `id` | `String` | Yes | Unique receipt identifier (e.g. `rcp_1793257592000`). |
| `receiptNo` | `String` | Yes | Official serialized receipt number (e.g., `RCP-0042/2026-27`). |
| `date` | `String (YYYY-MM-DD)` | Yes | Date on which the funds were received. |
| `clientName` | `String` | Yes | Payer party or client legal name. |
| `clientAddress`| `String` | No | Address of the client. |
| `amount` | `Number (Float)` | Yes | Net amount received. |
| `paymentMode` | `String` | Yes | Enum: `'Bank Transfer'`, `'UPI'`, `'Cash'`, `'Cheque'`, `'Card'`, `'Other'`. |
| `referenceNo` | `String` | No | Cheque number, IMPS/NEFT UTR reference, or UPI transaction ID. |
| `againstInvoice`| `String` | No | Invoice number or bill ID being settled. Leave blank for unallocated advances. |
| `ownerGstin` | `String` | No | Business profile ownership stamp for multi-company isolation. |
| `ownerName` | `String` | No | Business profile name. |
| `note` | `String` | No | Settlement remarks, balance confirmation, or receipt acknowledgment text. |

---

## 3. Sample JSON Document
```json
{
  "id": "rcp_1793257592005",
  "receiptNo": "RCP-0012/2026-27",
  "date": "2026-10-31",
  "clientName": "ARK INTERNO LLP",
  "clientAddress": "PLOT NO-10, ECOTECH-X, Greater Noida",
  "amount": 7930.0,
  "paymentMode": "Bank Transfer",
  "referenceNo": "NEFT-SBIN2630592817",
  "againstInvoice": "HPS00001",
  "ownerGstin": "06BPSPS2861B1ZO",
  "ownerName": "HPS FURNITURE & DECORATION",
  "note": "Full and final settlement against invoice HPS00001"
}
```


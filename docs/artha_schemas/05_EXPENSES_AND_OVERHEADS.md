# ARTHA Database Schema: Expenses & Overheads (`data/expenses/`)

## 1. Overview & Purpose
The `expenses` collection records operational overheads, administrative costs, utility bills, capital expenditure, and vendor payments that do not flow through standard merchandise purchase bills (e.g. rent, electricity, freight, SaaS subscriptions, legal fees).

Expenses tracking fulfills:
- **Net Profit & Loss Reporting:** Subtracts operating overheads from gross margin to report Net Profit.
- **Service ITC Eligibility:** Identifies eligible GST paid on operational expenses (e.g. AWS, telecom, freight) for inclusion in **GSTR-3B Table 4(A)(5) - All Other ITC**.

Files are stored individually under `data/expenses/` as `exp_<id>.json`.

---

## 2. Field Specifications

| Field Name | Type | Required | Description & Constraints |
| :--- | :--- | :---: | :--- |
| `id` | `String` | Yes | Unique expense identifier (e.g., `exp_1793257592000`). |
| `date` | `String (YYYY-MM-DD)` | Yes | Expense voucher or bill date (defaults to `localToday()`). |
| `description` | `String` | Yes | Description of expense (e.g., `'Office Rent May 2026'`, `'Cloud Hosting'`). |
| `category` | `String` | Yes | Accounting category enum: `'Rent'`, `'Utilities'`, `'Salaries'`, `'Office Supplies'`, `'Travel'`, `'Marketing'`, `'Repairs'`, `'Freight'`, `'Professional Fees'`, `'Other'`. |
| `amount` | `Number (Float)` | Yes | Total gross expense amount paid or incurred. |
| `gstAmount` | `Number (Float)` | No | Statutory GST component included in or added to the amount. |
| `gstPercent` | `Number (Float)` | No | Tax slab percentage (e.g. `18`, `12`, `5`, `28`). |
| `interstate` | `Boolean` | Yes | True if vendor is out-of-state (IGST), false for local (CGST + SGST). |
| `vendorName` | `String` | No | Service provider, landlord, or vendor entity name. |
| `vendorGstin` | `String (15 Chars)`| No | Vendor's GSTIN (required if claiming Input Tax Credit). |
| `invoiceNo` | `String` | No | Vendor's original bill or receipt reference number. |
| `paymentMode` | `String` | Yes | Enum: `'Bank Transfer'`, `'UPI'`, `'Cash'`, `'Cheque'`, `'Card'`, `'Other'`. |
| `ownerGstin` | `String` | No | Business profile ownership stamp for multi-company isolation. |
| `ownerName` | `String` | No | Business profile name. |
| `note` | `String` | No | Additional remarks, voucher references, or internal comments. |

---

## 3. Sample JSON Document
```json
{
  "id": "exp_1793257592001",
  "date": "2026-10-31",
  "description": "High-Speed Commercial Internet Lease",
  "category": "Utilities",
  "amount": 2360.0,
  "gstAmount": 360.0,
  "gstPercent": 18.0,
  "interstate": false,
  "vendorName": "Airtel Telecommunications Ltd",
  "vendorGstin": "06AAACA2892G1ZV",
  "invoiceNo": "DEL/OCT26/90214",
  "paymentMode": "Bank Transfer",
  "ownerGstin": "06BPSPS2861B1ZO",
  "ownerName": "HPS FURNITURE & DECORATION",
  "note": "Office fiber connection 200 Mbps"
}
```

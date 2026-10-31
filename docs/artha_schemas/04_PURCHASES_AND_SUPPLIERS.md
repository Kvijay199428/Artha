# ARTHA Database Schema: Purchases & Suppliers (`data/purchases/`)

## 1. Overview & Purpose
The `purchases` collection stores inward supply bills received from registered suppliers and vendors. It serves two primary accounting functions:
1. **Input Tax Credit (ITC) Ledger:** Tracks CGST, SGST, IGST, and Cess eligible for setoff against sales liabilities in **GSTR-3B** return filing.
2. **Accounts Payable & Stock Receipt:** Tracks creditor balances and automatically replenishes product stock on hand.

Files are stored individually under `data/purchases/` as `<billId>.json`.

---

## 2. Field Specifications

| Field Name | Type | Required | Description & Constraints |
| :--- | :--- | :---: | :--- |
| `id` | `String` | Yes | Unique purchase ID (e.g., `PUR-1-24-25`, `pur_1793257592000`). |
| `billNumber` | `String` | Yes | Supplier's invoice or bill number as printed on their physical invoice. |
| `billDate` | `String (YYYY-MM-DD)` | Yes | Date on the supplier's invoice. |
| `dueDate` | `String (YYYY-MM-DD)` | No | Payment due date to the vendor. |
| `supplierName` | `String` | Yes | Legal vendor / supplier party name. |
| `supplierGstin` | `String (15 Chars)`| No | Supplier's 15-character GSTIN. Blank for unregistered purchases. |
| `supplierAddress` | `String` | No | Supplier's registered address. |
| `ownerGstin` | `String` | No | Buyer's GSTIN (which of your business profiles purchased this). |
| `ownerName` | `String` | No | Business profile name of the buyer. |
| `items` | `Array<PurchaseItem>` | Yes | Line item breakdown of procured goods/services (see below). |
| `taxableAmount` | `Number (Float)` | Yes | Subtotal taxable amount before GST. |
| `totalTax` | `Number (Float)` | Yes | Cumulative tax amount (CGST + SGST + IGST + Cess). |
| `roundOff` | `Number (Float)` | No | Round-off fraction applied to the bill. |
| `totalAmount` | `Number (Float)` | Yes | Final payable amount on the supplier's bill. |
| `paymentStatus` | `String` | Yes | Enum: `'Paid'`, `'Unpaid'`, `'Partial'`. |
| `interstate` | `Boolean` | Yes | True if supply was inter-state (IGST), false for intra-state (CGST + SGST). |
| `notes` | `String` | No | Internal notes, batch references, or transport details. |

---

## 3. The `items` Line Items Array Schema

Each object in `purchase.items` contains:
```json
{
  "name": "PLYWOOD 18MM COMM",
  "hsn": "4412",
  "quantity": 50.0,
  "rate": 1850.0,
  "taxPercent": 18.0,
  "cessPercent": 0.0
}
```

---

## 4. Sample JSON Document
```json
{
  "id": "PUR-1-24-25",
  "billNumber": "PUR-1-24-25",
  "billDate": "2024-08-02",
  "supplierName": "A.B. ENTERPRISES",
  "supplierGstin": "07ACBPB7902P1ZJ",
  "supplierAddress": "12/4 Industrial Area, Kirti Nagar, New Delhi",
  "ownerGstin": "06BPSPS2861B1ZO",
  "ownerName": "HPS FURNITURE & DECORATION",
  "items": [
    {
      "name": "PLYWOOD 18MM COMM",
      "hsn": "4412",
      "quantity": 2.0,
      "rate": 1816.52,
      "taxPercent": 18.0,
      "cessPercent": 0.0
    }
  ],
  "taxableAmount": 3633.04,
  "totalTax": 653.96,
  "roundOff": 0.0,
  "totalAmount": 4287.0,
  "paymentStatus": "Paid",
  "interstate": true,
  "notes": "Imported from BusyWin FY 2024-25"
}
```


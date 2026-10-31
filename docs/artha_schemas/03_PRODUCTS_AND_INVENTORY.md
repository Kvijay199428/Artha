# ARTHA Database Schema: Products & Inventory (`data/products/`)

## 1. Overview & Purpose
The `products` collection maintains the catalog of goods, services, consumables, and labor items traded or supplied by the business. It tracks:
- Commodity identification (HSN for goods, SAC for services).
- Statutory GST tax brackets (0%, 5%, 12%, 18%, 28%).
- Dual pricing (Selling Price for sales invoices, Purchase Price for cost of goods sold).
- Real-time stock on hand (quantity in stock).
- Low-stock warning thresholds.

Files are stored individually under `data/products/` as `prod_<id>.json`.

---

## 2. Field Specifications

| Field Name | Type | Required | Description & Constraints |
| :--- | :--- | :---: | :--- |
| `id` | `String` | Yes | Unique product identifier (e.g. `prod_1323`, `prod_1793257592000`). |
| `name` | `String` | Yes | Commercial product or service title. Must be unique per business. |
| `description` | `String` | No | Extended specification, dimensions, technical parameters, or catalog notes. |
| `hsn` | `String` | No | Harmonized System of Nomenclature (4, 6, or 8 digits) for goods, or Service Accounting Code (6 digits) for services. Required for GSTR-1 HSN summary. |
| `unit` | `String` | Yes | Unit Quantity Code / Measurement Unit (e.g., `'Pcs'`, `'Nos'`, `'Kg'`, `'Mtr'`, `'Sq.ft'`, `'Hours'`, `'Bags'`). |
| `sellingPrice` | `Number (Float)` | Yes | Standard sale rate per unit excluding GST (or inclusive if tax-inclusive mode active). |
| `purchasePrice` | `Number (Float)` | No | Latest procurement cost per unit from supplier purchase bills. Used to compute gross profit margin. |
| `taxPercent` | `Number (Float)` | Yes | Statutory GST tax rate (e.g. `0`, `5`, `12`, `18`, `28`). |
| `cessPercent` | `Number (Float)` | No | Statutory compensation cess percentage (if applicable). |
| `stock` | `Number (Float)` | Yes | Current physical stock on hand. Automatically adjusted by sales bills (`-qty`), credit notes (`+qty`), and purchase bills (`+qty`). |
| `lowStockThreshold` | `Number (Float)`| No | Per-item threshold for low-stock ticker warnings. Falls back to global app setting if unset. |
| `barcode` | `String` | No | EAN-13, UPC, Code 128, or internal barcode string for scanner entry. |
| `ownerGstin` | `String` | No | Business profile ownership stamp for multi-company isolation. |

---

## 3. Real-Time Stock Movement Engine
Stock changes in ARTHA are event-driven:
1. **Sales Invoice Issued:** Deducts sold quantity from `stock`:
   $$\text{stock}_{\text{new}} = \text{stock}_{\text{current}} - \text{invoiceQty}$$
2. **Sales Invoice Cancelled:** Reverses the deduction (+qty).
3. **Credit Note Issued:** Adds returned goods back to stock (+qty).
4. **Purchase Bill Booked:** Increases inventory (+qty) and updates `purchasePrice` with the latest purchase rate.
5. **Quotations & Delivery Challans:** Have zero effect on physical accounting stock.

---

## 4. Sample JSON Document
```json
{
  "id": "prod_1323",
  "name": "ACP SHEET WORK",
  "description": "Aluminum Composite Panel 4mm exterior grade work",
  "hsn": "998891",
  "unit": "Sq.ft",
  "sellingPrice": 200.0,
  "purchasePrice": 140.0,
  "taxPercent": 18.0,
  "cessPercent": 0.0,
  "stock": 250.0,
  "lowStockThreshold": 20.0
}
```

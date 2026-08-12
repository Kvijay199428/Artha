# Phase 5 — GST Invoice Generation, Modification & Transaction Control System

## 1. Objective

Phase 5 introduces the complete **Sales GST Invoice Generation and Modification System**.

This phase builds on:

```text
Phase 1 → Company / Business Profile
Phase 2 → Unit Engine
Phase 3 → Item / SKU Master
Phase 4 → Universal Modification / Audit System
```

Phase 5 creates the transactional layer where company, customer, item, unit, HSN/SAC, GST and pricing data are combined into a legally controlled invoice.

The fundamental architecture is:

```text
MASTER DATA
    │
    ├── Company
    ├── Customer
    ├── Item
    ├── Unit
    └── GST Configuration
            │
            ↓
      INVOICE DRAFT
            │
            ↓
       VALIDATION
            │
            ↓
      TAX CALCULATION
            │
            ↓
      PREVIEW / REVIEW
            │
            ↓
        FINALIZE
            │
            ↓
      INVOICE NUMBER
            │
            ↓
    IMMUTABLE TRANSACTION
            │
            ├── PDF
            ├── Print
            ├── Share
            ├── Email
            └── GST / Accounting Data
```

---

# 2. Core Principle

An invoice is a **transaction**, not master data.

Therefore:

```text
Company Master
Item Master
Customer Master
Unit Master
GST Master
```

provide defaults.

But once an invoice is finalized:

```text
Invoice
Invoice Lines
Tax
Amounts
Customer Details
Seller Details
HSN/SAC
Unit
GST Rate
```

must retain their historical transaction snapshot.

Changing a master record later must never silently modify a finalized invoice.

---

# 3. Invoice Types

Phase 5 should initially support:

```text
TAX INVOICE
```

Future invoice/document types can include:

```text
BILL OF SUPPLY
EXPORT INVOICE
CREDIT NOTE
DEBIT NOTE
DELIVERY CHALLAN
PROFORMA INVOICE
QUOTATION
ESTIMATE
```

The architecture should be extensible so these are separate document types rather than unrelated systems.

---

# 4. Invoice Lifecycle

Recommended invoice states:

```text
DRAFT
    ↓
PENDING_REVIEW
    ↓
FINALIZED
    ↓
PARTIALLY_PAID
    ↓
PAID
```

Additional states:

```text
CANCELLED
VOID
```

For drafts:

```text
DRAFT → EDITABLE
```

For finalized invoices:

```text
FINALIZED → NOT ORDINARY EDITABLE
```

Changes should use controlled modification/correction mechanisms.

---

# 5. Invoice Creation Entry Point

The application should provide:

```text
[ + New Invoice ]
```

Opening:

```text
┌──────────────────────────────────────────────────────────────┐
│                     CREATE INVOICE                           │
├──────────────────────────────────────────────────────────────┤
│ Invoice Type       [ Tax Invoice ▼ ]                         │
│ Invoice Date       [ DD-MM-YYYY ]                            │
│ Supply Type        [ Goods / Services ]                      │
│                                                              │
│ Customer                                                     │
│ [ Search Customer __________________ ▼ ] [ + Add Customer ] │
│                                                              │
│ Place of Supply    [ Karnataka ▼ ]                           │
│                                                              │
│ Items                                                        │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Item | HSN/SAC | Qty | Unit | Rate | Discount | GST     │ │
│ ├──────────────────────────────────────────────────────────┤ │
│ │ [Select Item ▼]                                         │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ [ + Add Item ]                                               │
│                                                              │
│ Notes                                                        │
│ [_______________________________________________]            │
│                                                              │
│                         [Save Draft] [Review Invoice]        │
└──────────────────────────────────────────────────────────────┘
```

---

# 6. Seller / Supplier Information

The invoice should automatically load the company's information from Phase 1.

Required/commonly applicable fields:

```text
Legal Name
Trade Name
GSTIN
Address
State
State Code
PIN Code
Phone
Email
Logo
Bank Details
```

The invoice must use a transaction snapshot.

Example:

```text
seller_name_snapshot
seller_gstin_snapshot
seller_address_snapshot
seller_state_snapshot
seller_state_code_snapshot
seller_contact_snapshot
```

Do not rely only on live company master data when rendering historical invoices.

---

# 7. Customer Information

The invoice requires a customer/buyer section.

Phase 5 should support:

```text
Registered Customer
Unregistered Customer
Consumer / Retail Customer
```

Recommended fields:

```text
Customer Name
Business Name
GSTIN
Address
State
State Code
PIN Code
Phone
Email
Place of Supply
```

The customer master can be introduced as part of Phase 5 or a dedicated future phase, but invoice data must support customer snapshots.

---

# 8. Customer GST Status

The invoice engine should distinguish at least:

```text
REGISTERED
UNREGISTERED
```

Future tax statuses may include:

```text
COMPOSITION
SEZ
EXPORT
OTHER_SPECIAL_STATUS
```

Tax treatment must be determined from applicable transaction rules, not only from a customer dropdown.

---

# 9. Invoice Number

Invoice number generation must be controlled.

Recommended structure:

```text
Invoice Series
+
Sequential Number
```

Example:

```text
INV-000001
INV-000002
INV-000003
```

or:

```text
2026-27/INV/000001
```

The user should be able to configure the numbering format subject to the application's accounting controls.

---

# 10. Invoice Number Rules

For finalized tax invoices:

```text
Invoice number must be unique within the applicable company/document series.
```

The system should prevent:

```text
Duplicate invoice number
```

The number should be assigned atomically to avoid two concurrent users receiving the same number.

---

# 11. Invoice Number Assignment

Recommended:

```text
Draft Creation
    ↓
Temporary Draft ID
    ↓
Review
    ↓
Finalize
    ↓
Reserve / Assign Invoice Number
    ↓
Commit
```

The exact numbering strategy should be configured carefully so that abandoned drafts do not create unexplained finalized invoice numbers.

If a numbering sequence requires a number to be consumed, the system should retain a traceable record rather than silently reusing it.

---

# 12. Invoice Date

Fields:

```text
Invoice Date
```

Optional future fields:

```text
Due Date
Supply Date
Dispatch Date
Delivery Date
```

Validation should ensure that the date is valid and consistent with company accounting periods.

---

# 13. Accounting Period

The system should maintain accounting/fiscal periods.

Example:

```text
FY 2026-27
```

Invoice date determines the applicable accounting period unless the user has an authorized period-selection workflow.

A closed accounting period should prevent normal invoice creation/modification.

---

# 14. Place of Supply

The invoice must capture the applicable place of supply.

Example:

```text
Place of Supply
[ Karnataka (29) ▼ ]
```

The tax engine should use:

```text
Supplier State
+
Customer State
+
Place of Supply
+
Transaction Type
+
Applicable GST Rules
```

to determine the applicable tax treatment.

Do not simply assume:

```text
Different state = IGST
```

without applying the appropriate GST place-of-supply rules.

---

# 15. Invoice Items

Each invoice line should support:

```text
Item
Description
HSN/SAC
Quantity
Unit
Rate
Discount
Taxable Value
GST Rate
Tax
Line Total
```

Example:

```text
┌──────────────────────────────────────────────────────────────────┐
│ Item         HSN     Qty   Unit   Rate    Disc.   GST   Amount │
├──────────────────────────────────────────────────────────────────┤
│ Water 500ml   XXXX     10   PCS    ₹20     ₹0     18%    ₹236  │
└──────────────────────────────────────────────────────────────────┘
```

---

# 16. Add Item

The invoice should integrate Phase 3.

Workflow:

```text
[ + Add Item ]
      ↓
Item Search
      ↓
Select Existing Item
```

or:

```text
[ + Add New Item ]
      ↓
Phase 3 Item Modal
      ↓
Save Item
      ↓
Return to Invoice
      ↓
New Item Automatically Selected
```

The invoice draft must not be lost during this process.

---

# 17. Item Snapshot

When an item is selected, copy relevant values into the invoice line:

```text
item_id
item_name_snapshot
sku_snapshot
description_snapshot
unit_id
unit_name_snapshot
unit_symbol_snapshot
hsn_sac_snapshot
gst_rate_snapshot
```

The invoice line should also store the actual values used in calculation.

---

# 18. Quantity

Quantity must be numeric and greater than zero for normal sales lines.

Example:

```text
Quantity:
10
```

Support:

```text
Integer
Decimal
Fractional quantity
```

depending on the selected unit.

Examples:

```text
PCS → 10
KG  → 12.500
MTR → 7.250
```

Quantity precision should be controlled by the selected unit configuration.

---

# 19. Unit

The invoice line should load the item's default unit.

Example:

```text
PCS
```

The user may be allowed to select another compatible unit if Phase 2 conversion rules support it.

Example:

```text
Item Base Unit:
PCS

Invoice Unit:
BOX

Conversion:
1 BOX = 12 PCS
```

The conversion used for the transaction must be snapshotted.

---

# 20. Unit Conversion

If an alternate unit is used:

```text
Entered Quantity:
5 BOX

Conversion:
1 BOX = 12 PCS

Base Quantity:
60 PCS
```

The invoice must retain:

```text
entered_quantity = 5
entered_unit = BOX
conversion_factor = 12
base_quantity = 60
```

Changing the unit conversion later must not alter the historical invoice.

---

# 21. Rate

Rate means the unit selling price before applicable tax.

Example:

```text
Quantity:
10

Rate:
₹1,000
```

Taxable value before discount:

```text
₹10,000
```

The invoice should store the actual transaction rate rather than referencing a live item price.

---

# 22. Discount

Support:

```text
No Discount
Percentage Discount
Fixed Amount Discount
```

Example:

```text
Rate:
₹1,000

Quantity:
10

Gross:
₹10,000

Discount:
10%

Discount Amount:
₹1,000

Taxable Value:
₹9,000
```

The exact discount calculation order must be consistent and documented.

---

# 23. Discount Rules

Recommended invoice-line calculation:

```text
Gross Line Value
=
Quantity × Rate
```

Then:

```text
Discount Amount
=
Gross Line Value × Discount %
```

Then:

```text
Taxable Value
=
Gross Line Value - Discount Amount
```

Additional charges may be added according to the configured invoice calculation model and applicable tax treatment.

---

# 24. GST Rate

GST rate should be derived from the applicable item/tax configuration.

Example:

```text
GST:
18%
```

The user should not be allowed to enter arbitrary GST rates unless the application has an authorized tax configuration mechanism.

The rate used by the invoice must be stored as a transaction snapshot.

---

# 25. GST Tax Calculation

For a taxable value of:

```text
₹10,000
```

and GST:

```text
18%
```

tax:

```text
₹1,800
```

For an applicable intra-state transaction:

```text
CGST = ₹900
SGST/UTGST = ₹900
```

For an applicable inter-state transaction:

```text
IGST = ₹1,800
```

The actual tax treatment must be determined by the tax engine based on applicable rules.

---

# 26. Taxable Value

Each invoice line must calculate:

```text
Taxable Value
```

Example:

```text
Qty × Rate
       ↓
Gross
       ↓
Less Discount
       ↓
Taxable Value
```

The taxable value must be stored with appropriate decimal precision.

---

# 27. Tax Rounding

The application must define a single consistent rounding policy.

Possible approaches:

```text
Line-level rounding
Invoice-level rounding
Tax-component rounding
```

The chosen approach must be applied consistently across:

```text
UI
Backend
PDF
Reports
Exports
Accounting
```

The backend must be authoritative.

Never rely on frontend floating-point arithmetic as the final accounting calculation.

---

# 28. Currency

Phase 5 should initially support:

```text
INR ₹
```

The invoice should store:

```text
currency_code
currency_symbol
```

Future multi-currency support can add:

```text
USD
EUR
GBP
AED
etc.
```

with exchange-rate snapshots.

---

# 29. Invoice Totals

Recommended totals:

```text
Subtotal
Total Discount
Total Taxable Value
CGST
SGST/UTGST
IGST
Cess
Other Charges
Round Off
Grand Total
```

Example:

```text
Subtotal:              ₹10,000
Discount:              ₹1,000
Taxable Value:          ₹9,000
CGST:                     ₹810
SGST:                     ₹810
IGST:                       ₹0
Other Charges:              ₹0
Round Off:                  ₹0
Grand Total:            ₹10,620
```

The exact fields shown should depend on the transaction.

---

# 30. Other Charges

Future-ready invoice architecture should support:

```text
Shipping
Freight
Packing
Handling
Insurance
Other Charges
```

Each charge should have a defined tax treatment.

Do not automatically assume every charge is taxable or non-taxable.

---

# 31. Round Off

The system may optionally support:

```text
Round Off
```

Example:

```text
Calculated Total:
₹10,620.40

Round Off:
-₹0.40

Grand Total:
₹10,620.00
```

The round-off amount must be explicitly stored.

---

# 32. Total in Words

The PDF/invoice display may show:

```text
Amount in Words:
Rupees Ten Thousand Six Hundred Twenty Only
```

The amount in words should be generated from the final grand total, not manually entered.

---

# 33. Payment Terms

Invoice may support:

```text
Payment Terms
Due Date
Credit Period
```

Example:

```text
Payment Terms:
Due within 30 days
```

Payment terms should not change the tax calculation.

---

# 34. Payment Status

Invoice status and payment status should be separate.

Invoice:

```text
DRAFT
FINALIZED
CANCELLED
```

Payment:

```text
UNPAID
PARTIALLY_PAID
PAID
```

Example:

```text
Invoice Status:
FINALIZED

Payment Status:
PARTIALLY_PAID
```

---

# 35. Payment Recording

A future payment system can record:

```text
Payment ID
Invoice ID
Payment Date
Amount
Payment Mode
Reference Number
Bank / Cash Account
Notes
```

Payment modifications must not rewrite invoice totals.

---

# 36. Payment Modes

Possible modes:

```text
CASH
BANK_TRANSFER
UPI
CARD
CHEQUE
NEFT
RTGS
IMPS
OTHER
```

This is payment information, not invoice tax information.

---

# 37. Invoice Notes

Optional:

```text
Notes
Terms & Conditions
Customer Notes
Internal Notes
```

Internal notes must not accidentally appear on customer-facing invoices.

Separate:

```text
internal_notes
customer_notes
```

---

# 38. Transport Information — Future Extension

The architecture should allow:

```text
Transporter
Vehicle Number
E-Way Bill Number
Distance
Dispatch From
Ship To
Delivery Address
```

These should be separate structured fields rather than embedded only in free-text notes.

---

# 39. E-Invoice / E-Way Bill — Future Integration

The system should be designed for future integration with applicable government systems.

Potential fields:

```text
IRN
Ack Number
Ack Date
Signed QR
E-Way Bill Number
E-Way Bill Date
E-Way Bill Status
```

Do not generate fake IRNs, acknowledgment numbers or government validation identifiers.

These values must come from the applicable official integration/process.

---

# 40. Invoice PDF

The finalized invoice should support:

```text
Preview
Print
Download PDF
Share
Email
```

The PDF should contain the transaction snapshot.

Recommended sections:

```text
Company Header
Invoice Metadata
Customer Details
Item Table
Tax Details
Totals
Amount in Words
Bank Details
Terms & Conditions
Authorized Signatory
QR / Government Details where applicable
```

---

# 41. Invoice Preview

The preview should use the same data that will be finalized.

Workflow:

```text
Draft
 ↓
Preview
 ↓
Validate
 ↓
Finalize
```

The preview should clearly distinguish:

```text
DRAFT
```

from:

```text
FINAL TAX INVOICE
```

A draft must not appear to be a finalized legal invoice.

---

# 42. Draft Invoice Modification

Draft invoices are fully editable subject to validation.

User may modify:

```text
Customer
Date
Place of Supply
Items
Quantity
Unit
Rate
Discount
Tax Configuration
Notes
Payment Terms
```

Workflow:

```text
Open Draft
 ↓
Edit
 ↓
Validate
 ↓
Save Draft
```

No finalized invoice number should be treated as permanently issued merely because a draft exists.

---

# 43. Finalized Invoice Modification

A finalized invoice should **not** support ordinary unrestricted editing.

Do not provide:

```text
Edit Invoice
→ silently overwrite finalized invoice
```

Instead:

```text
FINALIZED INVOICE
        ↓
Controlled Correction
        ↓
Credit Note / Debit Note / Cancellation / Amendment
```

The correct mechanism depends on the nature of the correction and applicable GST/accounting rules.

---

# 44. Invoice Cancellation

The application should support controlled cancellation.

Example:

```text
Invoice:
INV-000123

Status:
FINALIZED
```

Action:

```text
[ Cancel Invoice ]
```

Require:

```text
Cancellation Reason
Confirmation
User Authorization
Timestamp
```

The system must retain:

```text
Original Invoice
Cancellation Event
Reason
User
Date/Time
```

Do not physically delete the invoice.

---

# 45. Cancellation Rules

Cancellation must respect:

```text
Applicable GST rules
Accounting period
E-invoice status
E-way bill status
Payment status
Credit note requirements
```

The software should not assume that every finalized invoice can be cancelled at any time.

If external government reporting has already occurred, the application should use the appropriate correction/cancellation workflow.

---

# 46. Credit Note

A credit note should reference the original invoice.

Example:

```text
Credit Note
CN-00001

Against Invoice:
INV-000123
```

Store:

```text
original_invoice_id
original_invoice_number
reason
credit_lines
tax_adjustment
```

Reasons may include:

```text
Sales Return
Rate Difference
Discount After Sale
Tax Correction
Other Applicable Reason
```

The exact tax/accounting treatment must follow applicable rules.

---

# 47. Debit Note

A debit note should similarly reference the original transaction where applicable.

Example:

```text
Debit Note
DN-00001

Against Invoice:
INV-000123
```

The system should preserve the relationship between:

```text
Original Invoice
Debit Note
Accounting Adjustment
```

---

# 48. Invoice Amendment

If the business workflow requires amendments, the system should not simply overwrite the original invoice.

Use:

```text
Original Version
       ↓
Amendment Record
       ↓
New Corrected Representation
```

The original transaction remains traceable.

---

# 49. Invoice Modification History

Every invoice should have:

```text
[ View History ]
```

Example:

```text
Invoice History

10 Aug 2026
Invoice Finalized

10 Aug 2026
Customer updated in draft

10 Aug 2026
Item quantity changed
10 → 12

10 Aug 2026
Draft created
```

After finalization, all correction events must be separately traceable.

---

# 50. Invoice Audit Log

Recommended fields:

```text
audit_id
company_id
invoice_id
event_type
old_status
new_status
changed_by
changed_at
reason
metadata
```

Events:

```text
INVOICE_CREATED
INVOICE_UPDATED
INVOICE_FINALIZED
INVOICE_CANCELLED
INVOICE_CREDITED
INVOICE_DEBITED
INVOICE_PRINTED
INVOICE_PDF_GENERATED
PAYMENT_RECORDED
PAYMENT_UPDATED
```

---

# 51. Invoice Database Structure

Recommended core table:

```text
invoices
├── invoice_id
├── company_id
├── invoice_number
├── invoice_series
├── invoice_type
├── invoice_date
├── accounting_period_id
├── customer_id
├── customer_name_snapshot
├── customer_gstin_snapshot
├── customer_address_snapshot
├── customer_state_snapshot
├── customer_state_code_snapshot
├── place_of_supply
├── seller_name_snapshot
├── seller_gstin_snapshot
├── seller_address_snapshot
├── currency_code
├── subtotal
├── discount_total
├── taxable_total
├── cgst_total
├── sgst_total
├── igst_total
├── cess_total
├── other_charges
├── round_off
├── grand_total
├── amount_in_words
├── invoice_status
├── payment_status
├── notes
├── terms
├── created_by
├── created_at
├── updated_by
├── updated_at
└── version
```

---

# 52. Invoice Line Structure

Recommended:

```text
invoice_lines
├── invoice_line_id
├── invoice_id
├── item_id
├── item_name_snapshot
├── sku_snapshot
├── description_snapshot
├── hsn_sac_snapshot
├── quantity
├── unit_id
├── unit_name_snapshot
├── unit_symbol_snapshot
├── conversion_factor
├── base_quantity
├── rate
├── discount_type
├── discount_value
├── discount_amount
├── taxable_value
├── gst_rate
├── cgst_rate
├── sgst_rate
├── igst_rate
├── cgst_amount
├── sgst_amount
├── igst_amount
├── cess_amount
└── line_total
```

---

# 53. Decimal Precision

Monetary fields must use fixed-precision decimal types.

Do not use binary floating point for final accounting values.

Recommended conceptual model:

```text
DECIMAL(precision, scale)
```

with scale selected according to the application's accounting requirements.

Quantity precision may differ from monetary precision.

Example:

```text
Quantity:
3 decimal places

Rate:
2 or more decimal places

Tax:
2 decimal places

Grand Total:
2 decimal places
```

The exact scale should be centrally configured.

---

# 54. Calculation Engine

All invoice calculations should happen in a centralized backend calculation service.

Example:

```text
InvoiceCalculationEngine
```

Input:

```text
Invoice Draft
```

Output:

```text
Validated Invoice Calculation
```

The frontend may display live calculations, but the backend must recalculate before finalization.

---

# 55. Calculation Sequence

Recommended conceptual sequence:

```text
1. Load transaction inputs
2. Validate item/unit
3. Calculate quantity conversion
4. Calculate gross line amount
5. Calculate line discount
6. Determine taxable value
7. Determine applicable GST treatment
8. Calculate tax components
9. Calculate line total
10. Aggregate invoice totals
11. Apply permitted charges
12. Apply round-off
13. Calculate final grand total
14. Generate amount in words
```

The exact sequence must be documented and applied consistently.

---

# 56. Server-Side Recalculation

Never trust values such as:

```text
taxable_total
gst_amount
grand_total
```

submitted by the frontend.

The backend should calculate them again from trusted inputs.

Client:

```text
quantity
rate
discount
selected item
```

Backend:

```text
authoritative calculation
```

---

# 57. Tax Calculation Rules

The tax engine should consider:

```text
Seller GST registration
Customer GST status
Customer GSTIN
Supplier state
Place of supply
Item HSN/SAC
Item GST applicability
GST rate
Transaction type
Applicable exemptions
Applicable special rules
```

Do not hardcode all GST logic into invoice UI components.

---

# 58. GST Exempt / Non-Taxable Items

The invoice engine must support applicable non-taxable treatments.

Examples may include:

```text
GST Applicable = NO
```

or other tax treatment configured by the tax engine.

The exact treatment must be represented explicitly rather than by:

```text
GST = 0%
```

alone.

A zero rate and non-taxable/exempt treatment are not necessarily semantically identical.

---

# 59. Reverse Charge

The architecture should be future-ready for:

```text
Reverse Charge
```

Example fields:

```text
reverse_charge_applicable
reverse_charge_type
```

The invoice engine must not assume reverse charge simply because an item has a particular rate.

Applicable rules must determine the treatment.

---

# 60. Composition Scheme

The system should be able to represent company/customer tax status that affects invoice behavior.

If a business is under a tax scheme where a normal tax invoice is not applicable, the document type and tax presentation must follow the relevant rules.

Do not merely hide GST fields and continue generating an ordinary tax invoice.

---

# 61. Invoice Numbering Configuration

Recommended table:

```text
invoice_series
├── series_id
├── company_id
├── document_type
├── prefix
├── suffix
├── starting_number
├── current_number
├── fiscal_year
├── reset_policy
├── status
└── created_at
```

Example:

```text
Series:
INV

Prefix:
INV-

Current:
000124
```

---

# 62. Numbering Concurrency

Invoice numbering must be protected against concurrent requests.

Use:

```text
Database transaction
+
row-level locking / atomic sequence
```

Never generate:

```text
MAX(invoice_number) + 1
```

without concurrency protection.

Two simultaneous users could otherwise receive the same number.

---

# 63. Draft Autosave

Optional but recommended:

```text
Auto-save Draft
```

The system may save drafts periodically.

Example:

```text
Draft saved:
15:42:10
```

Autosave must never finalize an invoice.

---

# 64. Browser Refresh Protection

If the user refreshes or closes the invoice screen:

```text
Draft remains recoverable
```

The application should provide:

```text
Continue Draft
Discard Draft
```

Drafts should have:

```text
draft_id
company_id
created_by
updated_at
```

---

# 65. Duplicate Invoice Prevention

The backend should prevent accidental duplicate finalization.

Example:

```text
User clicks Finalize twice
```

The system should create only one finalized invoice.

Use:

```text
idempotency key
```

or equivalent transaction-level protection.

---

# 66. Finalization Workflow

Recommended:

```text
Draft
 ↓
Validate
 ↓
Recalculate
 ↓
Check customer
 ↓
Check item lines
 ↓
Check tax
 ↓
Check invoice date
 ↓
Check accounting period
 ↓
Check numbering
 ↓
Assign invoice number
 ↓
Persist invoice + lines
 ↓
Audit event
 ↓
Commit
 ↓
FINALIZED
```

---

# 67. Finalization Confirmation

Display:

```text
FINALIZE INVOICE

Invoice Total:
₹10,620.00

Customer:
ABC Enterprises

Items:
3

GST:
₹1,620.00

Once finalized, normal editing will not be available.

[Back] [Finalize Invoice]
```

---

# 68. Invoice Locking

After finalization:

```text
invoice_status = FINALIZED
```

The normal edit endpoint should reject unrestricted changes.

Example:

```text
PATCH /api/invoices/{id}
```

Response:

```text
INVOICE_LOCKED
```

Instead use controlled operations:

```text
Cancel
Credit Note
Debit Note
Amendment
Payment
```

as appropriate.

---

# 69. Invoice Modification Rules Matrix

| Data | Draft | Finalized | Historical Protection |
|---|---:|---:|---:|
| Customer | Edit | Controlled correction | Yes |
| Customer GSTIN | Edit | Controlled correction | Yes |
| Invoice Date | Edit | Restricted | Yes |
| Place of Supply | Edit | Controlled correction | Yes |
| Item | Edit | Controlled correction | Yes |
| Quantity | Edit | Credit/debit/correction | Yes |
| Unit | Edit | Controlled correction | Yes |
| Rate | Edit | Credit/debit/correction | Yes |
| Discount | Edit | Credit/debit/correction | Yes |
| HSN/SAC | Edit | Controlled correction | Yes |
| GST Rate | Edit | Controlled correction | Yes |
| Tax Amount | Recalculated | Not directly edited | Yes |
| Grand Total | Recalculated | Not directly edited | Yes |
| Notes | Edit | Limited/controlled | Yes |
| Payment Status | Separate workflow | Separate workflow | Yes |
| Invoice Number | Before finalization only | Immutable | Yes |

---

# 70. What Must Never Be Directly Editable After Finalization

Do not expose direct edit fields for:

```text
Invoice Number
Tax Amount
Taxable Total
CGST
SGST/UTGST
IGST
Grand Total
Finalized Invoice Date
```

These values should be derived or corrected through controlled transaction mechanisms.

---

# 71. Invoice Cancellation vs Deletion

Never use:

```text
DELETE /api/invoices/{id}
```

for a finalized tax invoice.

Instead:

```text
POST /api/invoices/{id}/cancel
```

with:

```text
reason
authorized_by
timestamp
```

The original invoice remains in the database.

---

# 72. Invoice Correction

For a draft:

```text
Edit directly.
```

For finalized:

```text
Determine correction type.

        ┌──────────────┐
        ↓              ↓
     Cancel         Adjust
        │              │
        │       ┌──────┴──────┐
        │       ↓             ↓
        │   Credit Note    Debit Note
        │
        ↓
 Preserve Original
```

The exact legal/accounting mechanism must be determined according to the transaction and applicable GST rules.

---

# 73. Customer Modification After Invoice Creation

If a customer master changes:

```text
Customer Master
GSTIN changed
```

existing invoices must remain unchanged.

Future invoices use the new customer information.

Example:

```text
Customer Master
     ↓
New GSTIN

Old Invoice
     ↓
Old GSTIN Snapshot

New Invoice
     ↓
New GSTIN
```

---

# 74. Item Modification After Invoice Creation

If item master changes:

```text
GST rate
HSN
Description
Unit
SKU
```

existing invoices remain unchanged.

Example:

```text
Item Master:
GST 18% → 12%

Old Invoice:
18%

New Invoice:
12%
```

---

# 75. Unit Modification After Invoice Creation

If:

```text
1 BOX = 12 PCS
```

changes to:

```text
1 BOX = 24 PCS
```

existing invoices retain:

```text
Original conversion
Original quantity
Original unit
Original calculated amount
```

New invoices use the new configuration where applicable.

---

# 76. Invoice Search

Search by:

```text
Invoice Number
Customer Name
Customer GSTIN
Invoice Date
Item Name
SKU
HSN/SAC
Status
Payment Status
Amount
```

Filters:

```text
Date Range
Customer
Status
Payment Status
GST Treatment
```

---

# 77. Invoice List

Example:

```text
Sales Invoices

[ Search __________________ ]

Date       Invoice       Customer        Amount      Status
────────────────────────────────────────────────────────────
10-08-26   INV-000124    ABC Ltd         ₹10,620     Finalized
10-08-26   INV-000123    XYZ Traders     ₹5,900      Paid
09-08-26   INV-000122    PQR Store       ₹8,450      Unpaid
```

Actions:

```text
View
Print
PDF
Share
Payment
History
Cancel
Credit Note
```

---

# 78. Invoice Detail Page

The invoice detail page should show:

```text
Invoice Header
Customer
Items
Tax Breakdown
Totals
Payment Status
Document Status
Audit History
Related Documents
```

Related documents:

```text
Credit Notes
Debit Notes
Payments
E-Invoice Data
E-Way Bill
```

---

# 79. Tax Summary

Invoice should provide:

```text
Taxable Value
CGST
SGST/UTGST
IGST
Cess
Total Tax
```

Example:

```text
Taxable Value: ₹9,000

CGST 9%: ₹810
SGST 9%: ₹810

Total GST: ₹1,620
```

---

# 80. HSN/SAC Summary

For reporting, the invoice should be able to group lines by:

```text
HSN/SAC
GST Rate
Taxable Value
CGST
SGST
IGST
```

Example:

```text
HSN      Taxable      GST       CGST      SGST
XXXX     ₹9,000       18%       ₹810      ₹810
```

---

# 81. Invoice PDF Consistency

The PDF must be generated from the finalized invoice snapshot.

Do not generate historical PDFs by reloading:

```text
Current Company Master
Current Item Master
Current GST Master
```

because those values may have changed.

Use:

```text
Invoice Snapshot
```

as the authoritative source.

---

# 82. PDF Regeneration

A finalized invoice PDF may be regenerated later.

Regeneration must reproduce the same transaction data.

If the visual template changes:

```text
Invoice Data
    ↓
New PDF Template
```

but:

```text
Invoice Data ≠ Changed
```

The historical transaction remains unchanged.

For legally/significantly issued documents, the application should retain the original generated document or document hash where required by the business's record-retention policy.

---

# 83. Document Hash

Future enhancement:

```text
invoice_document_hash
```

can be stored to detect whether a generated document has changed.

Example:

```text
SHA-256:
abc123...
```

Useful for:

```text
Document integrity
Audit
Storage verification
```

---

# 84. Invoice Attachments

Future support:

```text
Purchase Order
Delivery Challan
Supporting Document
Payment Proof
Other Attachment
```

Attachments should be associated with:

```text
invoice_id
```

and protected by company-level access control.

---

# 85. Invoice Sharing

Support:

```text
Download PDF
Print
Email
Share
```

Future:

```text
WhatsApp Business API
SMS
Customer Portal
```

Sharing must not expose invoices to unauthorized recipients.

---

# 86. Email Invoice

Future email workflow:

```text
Invoice
 ↓
Generate PDF
 ↓
Select Customer Email
 ↓
Confirm
 ↓
Send
 ↓
Record Delivery Event
```

Store:

```text
sent_at
recipient
delivery_status
```

Do not modify invoice accounting data when sending.

---

# 87. Invoice API

Recommended APIs:

```text
GET    /api/invoices
GET    /api/invoices/{invoice_id}
POST   /api/invoices
PATCH  /api/invoices/{invoice_id}
POST   /api/invoices/{invoice_id}/finalize
POST   /api/invoices/{invoice_id}/cancel
GET    /api/invoices/{invoice_id}/history
GET    /api/invoices/{invoice_id}/pdf
POST   /api/invoices/{invoice_id}/credit-note
POST   /api/invoices/{invoice_id}/debit-note
```

---

# 88. Draft API

```text
POST   /api/invoice-drafts
GET    /api/invoice-drafts
GET    /api/invoice-drafts/{draft_id}
PATCH  /api/invoice-drafts/{draft_id}
DELETE /api/invoice-drafts/{draft_id}
POST   /api/invoice-drafts/{draft_id}/validate
```

Deleting a draft is acceptable if it has not become a finalized accounting document.

---

# 89. Calculation API

Recommended:

```text
POST /api/invoices/calculate
```

Input:

```json
{
  "customer_id": "CUSTOMER-001",
  "place_of_supply": "29",
  "lines": [
    {
      "item_id": "ITEM-001",
      "quantity": 10,
      "rate": "20.00",
      "discount_type": "PERCENT",
      "discount_value": "5.00"
    }
  ]
}
```

The backend returns:

```json
{
  "subtotal": "200.00",
  "discount_total": "10.00",
  "taxable_total": "190.00",
  "cgst_total": "17.10",
  "sgst_total": "17.10",
  "igst_total": "0.00",
  "grand_total": "224.20"
}
```

Actual tax results must be generated from the configured tax engine.

---

# 90. Finalization API

```text
POST /api/invoices/{invoice_id}/finalize
```

The server must:

```text
Authenticate
Authorize
Validate
Recalculate
Check accounting period
Check numbering
Check concurrency
Persist
Audit
Commit
```

---

# 91. Idempotency

Finalization requests should support:

```text
Idempotency-Key
```

Example:

```text
POST /api/invoices/123/finalize
Idempotency-Key: abc-123
```

If the request is accidentally repeated:

```text
Do not create another invoice.
```

---

# 92. Invoice Modification API Rules

Draft:

```text
PATCH allowed
```

Finalized:

```text
PATCH normal fields → rejected
```

Controlled operations:

```text
/cancel
/credit-note
/debit-note
/payment
/amend
```

This keeps the transaction ledger consistent.

---

# 93. Security

All invoice endpoints must enforce:

```text
Authentication
Company isolation
Role/permission checks
Input validation
Server-side calculation
Audit logging
Concurrency protection
```

Never trust:

```text
company_id
seller_gstin
tax amounts
grand total
invoice number
user role
```

from the browser as authoritative values.

---

# 94. Data Integrity

Database constraints should enforce:

```text
invoice_id → PRIMARY KEY
company_id → NOT NULL
invoice_number → UNIQUE within applicable series/company
invoice_date → NOT NULL
invoice_status → constrained
payment_status → constrained
invoice_lines.invoice_id → FOREIGN KEY
```

Use database transactions for:

```text
Invoice
+
Invoice Lines
+
Number Assignment
+
Audit Log
```

---

# 95. Accounting Period Lock

A finalized invoice should belong to an accounting period.

If the period is locked:

```text
New invoice → BLOCKED
Modification → BLOCKED
Cancellation → Controlled process
```

Example:

```text
FY 2025-26
Status:
CLOSED
```

Do not allow normal transactions into a closed period.

---

# 96. Invoice Export

Future support:

```text
Excel
CSV
PDF
JSON
```

Exports should preserve:

```text
Invoice Number
Date
Customer
GSTIN
HSN/SAC
Taxable Value
GST
Grand Total
Status
```

---

# 97. GST Reporting Readiness

Invoice records should be structured so that future reports can aggregate:

```text
B2B
B2C
Credit Notes
Debit Notes
HSN Summary
Tax Rate Summary
Taxable Value
CGST
SGST/UTGST
IGST
Cess
```

Do not make reports dependent on parsing invoice PDF text.

---

# 98. Invoice Data Model Relationships

```text
COMPANY
   │
   ├───────────────┐
   ↓               ↓
CUSTOMER         INVOICE
                   │
                   ├── Invoice Header
                   │
                   ├── Invoice Lines
                   │      │
                   │      └── ITEM SNAPSHOT
                   │
                   ├── Tax Summary
                   │
                   ├── Payment Records
                   │
                   ├── Credit Notes
                   │
                   ├── Debit Notes
                   │
                   └── Audit History
```

---

# 99. Relationship to Phase 1

Phase 5 consumes:

```text
Company Name
GSTIN
Address
State
State Code
Contact
Logo
Bank Details
```

but creates an immutable invoice snapshot.

---

# 100. Relationship to Phase 2

Phase 5 consumes:

```text
Unit
Unit Symbol
Unit Code
Conversion
Precision
```

and snapshots the transaction-specific values.

---

# 101. Relationship to Phase 3

Phase 5 consumes:

```text
Item
SKU
HSN/SAC
GST Rate
Description
Default Unit
```

and snapshots them into invoice lines.

---

# 102. Relationship to Phase 4

Phase 5 uses Phase 4's:

```text
Authentication
Permissions
Audit
Versioning
Modification Rules
Concurrency Protection
Historical Data Protection
```

but invoice finalization adds stronger transaction controls.

---

# 103. Invoice Creation Workflow

Complete workflow:

```text
LOGIN
  ↓
DASHBOARD
  ↓
SALES
  ↓
NEW INVOICE
  ↓
SELECT CUSTOMER
  ↓
ENTER INVOICE DATE
  ↓
SELECT PLACE OF SUPPLY
  ↓
ADD ITEMS
  ↓
SELECT UNIT / QUANTITY
  ↓
ENTER RATE
  ↓
DISCOUNT
  ↓
GST CALCULATION
  ↓
ADD OTHER CHARGES
  ↓
ROUND OFF
  ↓
CALCULATE TOTAL
  ↓
VALIDATE
  ↓
PREVIEW
  ↓
SAVE DRAFT
  ↓
FINALIZE
  ↓
ASSIGN INVOICE NUMBER
  ↓
FINALIZED INVOICE
  ↓
PDF / PRINT / SHARE
```

---

# 104. Invoice Modification Workflow

## Draft

```text
Open Draft
   ↓
Edit
   ↓
Validate
   ↓
Recalculate
   ↓
Save
```

## Finalized

```text
Open Invoice
   ↓
Identify Correction
   ↓
Determine Correct Mechanism
   ├── Cancellation
   ├── Credit Note
   ├── Debit Note
   └── Other Authorized Amendment
   ↓
Create Related Transaction
   ↓
Preserve Original
   ↓
Audit
```

---

# 105. Example — Draft Modification

Original:

```text
Item:
Water Bottle

Qty:
10

Rate:
₹20

GST:
18%
```

User changes:

```text
Qty:
10 → 15
```

System:

```text
Recalculate
↓
Update taxable value
↓
Update GST
↓
Update grand total
↓
Save draft
```

No historical issue exists because the invoice is still a draft.

---

# 106. Example — Finalized Invoice Correction

Original:

```text
INV-000123

Quantity:
10

Finalized:
YES
```

User discovers:

```text
Actual quantity should have been 8.
```

Do not:

```text
UPDATE invoice_lines SET quantity = 8
```

Instead determine the applicable correction mechanism.

Possible workflow:

```text
Original Invoice
      ↓
Correction Transaction
      ↓
Credit/Debit Note or other applicable mechanism
      ↓
Reference Original Invoice
      ↓
Audit
```

The exact mechanism depends on the circumstances and applicable GST/accounting rules.

---

# 107. Example — Item GST Master Change

Item master:

```text
Water Bottle
GST:
18%
```

Later changed to:

```text
12%
```

Existing:

```text
INV-000100
GST:
18%
```

New:

```text
INV-000150
GST:
12%
```

No historical invoice rewriting.

---

# 108. Example — Company Address Change

Company master:

```text
Old Address
```

changed to:

```text
New Address
```

Existing invoices:

```text
Old Address Snapshot
```

New invoices:

```text
New Address Snapshot
```

This is essential for historical document integrity.

---

# 109. Invoice Locking Rules

The invoice should become locked when:

```text
invoice_status = FINALIZED
```

Additional lock conditions may include:

```text
accounting_period = CLOSED
government_submission = COMPLETED
payment_reconciliation = LOCKED
```

The UI should clearly show:

```text
🔒 FINALIZED
```

---

# 110. Finalized Invoice UI

Example:

```text
┌──────────────────────────────────────────────────────────┐
│ INV-000124                         🔒 FINALIZED           │
├──────────────────────────────────────────────────────────┤
│ Date: 10-08-2026                                         │
│ Customer: ABC Enterprises                                │
│ GSTIN: XXXXX                                             │
│                                                          │
│ Items                                                    │
│                                                          │
│ Taxable Value: ₹9,000                                    │
│ CGST:          ₹810                                      │
│ SGST:          ₹810                                      │
│ Grand Total:   ₹10,620                                   │
│                                                          │
│ [PDF] [Print] [Share] [Payment] [History] [More ▼]      │
└──────────────────────────────────────────────────────────┘
```

More:

```text
Cancel
Credit Note
Debit Note
View Audit
```

---

# 111. Draft UI

```text
┌──────────────────────────────────────────────────────────┐
│ DRAFT INVOICE                                             │
├──────────────────────────────────────────────────────────┤
│ Customer: ABC Enterprises                                │
│                                                          │
│ Items                                                    │
│                                                          │
│ Total: ₹10,620                                           │
│                                                          │
│ [Save Draft] [Preview] [Finalize]                       │
└──────────────────────────────────────────────────────────┘
```

---

# 112. Invoice Validation Checklist

Before finalization:

```text
□ Company is active
□ Company GST configuration valid
□ Invoice date valid
□ Accounting period open
□ Customer valid
□ Customer GST details valid where applicable
□ Place of supply selected
□ At least one invoice line
□ Item active
□ Unit valid
□ Quantity valid
□ Rate valid
□ Discount valid
□ HSN/SAC valid where required
□ GST treatment valid
□ Tax calculated
□ Totals calculated
□ Numbering series available
□ No duplicate finalization
```

---

# 113. Finalization Failure

If any validation fails:

```text
Invoice remains DRAFT.
```

No partial finalized record should be created.

Example:

```text
Tax calculation failed
        ↓
ROLLBACK
        ↓
Draft preserved
```

---

# 114. Transaction Atomicity

Finalization must be atomic.

Conceptually:

```text
BEGIN

Create invoice
Create invoice lines
Assign number
Calculate/store totals
Create audit event

COMMIT
```

If anything fails:

```text
ROLLBACK
```

The application must not end with:

```text
Invoice created
but invoice lines missing
```

or:

```text
Invoice number consumed
but no finalized invoice
```

without an intentional, traceable numbering policy.

---

# 115. Performance

The invoice screen should remain responsive with:

```text
Large customer database
Large item database
Hundreds/thousands of historical invoices
```

Use:

```text
Search-as-you-type
Pagination
Debounced search
Server-side filtering
Cached master data
```

Do not load the entire item master into the browser for every invoice.

---

# 116. Accessibility

Invoice entry should support:

```text
Keyboard navigation
Tab order
Enter to select
Esc to close modal
Screen-reader labels
Clear validation messages
Accessible dropdowns
Mobile-friendly layout
```

---

# 117. Invoice Draft Recovery

If the application crashes:

```text
Reopen Sales
   ↓
Recover Draft
```

Display:

```text
Unsaved Draft Found

Invoice started:
10 Aug 2026 15:20

Last saved:
10 Aug 2026 15:41

[Continue Draft] [Discard]
```

---

# 118. Duplicate Customer / Item Creation Protection

When quick-adding:

```text
Customer
Item
```

the system should search existing records first.

Example:

```text
Possible existing item found:

Water Bottle 500ml
SKU: WTR-500ML-001

[Use Existing] [Create New]
```

This reduces duplicate master records.

---

# 119. Invoice Template

The system should separate:

```text
Invoice Data
```

from:

```text
Invoice Presentation
```

Example:

```text
Invoice Data
      ↓
Template Engine
      ↓
PDF / HTML / Print
```

Changing the visual template must not alter the accounting transaction.

---

# 120. Multiple Invoice Templates

Future support:

```text
Default
Modern
Compact
Retail
Professional
Custom
```

Each template uses the same invoice data.

---

# 121. Custom Fields — Future Extension

The architecture may support company-defined invoice fields:

```text
PO Number
Project Number
Salesperson
Vehicle Number
Department
Reference Number
```

Custom fields should be separate from core accounting fields.

---

# 122. Salesperson — Future Extension

Future invoice support:

```text
salesperson_id
commission_rule
```

Commission calculation should be a separate module.

---

# 123. Customer Portal — Future Extension

Customers may later access:

```text
Invoice
PDF
Payment Status
Payment Link
Credit Notes
Statements
```

Access must be authenticated and scoped to the customer.

---

# 124. Payment Link — Future Extension

Invoice can later expose:

```text
[ Pay Now ]
```

with a secure payment system.

Payment status should update separately:

```text
Invoice
    ↓
Payment Request
    ↓
Payment Gateway
    ↓
Payment Confirmation
    ↓
Payment Record
    ↓
Invoice Payment Status
```

Do not mark an invoice as paid based solely on a client-side success page.

---

# 125. Invoice Statement

Future customer statement:

```text
Opening Balance
Invoices
Credit Notes
Payments
Adjustments
Closing Balance
```

This should be calculated from accounting transactions, not from invoice status alone.

---

# 126. Invoice Number and Fiscal Year

The application should explicitly define whether numbering:

```text
resets every fiscal year
```

or:

```text
continues across years
```

The configured policy must be consistent within a series and traceable.

---

# 127. Data Retention

Finalized invoices and related accounting records should not be physically deleted through ordinary UI operations.

The application should implement a configurable retention policy consistent with applicable legal/accounting requirements.

---

# 128. Backup Considerations

Invoice data should be included in:

```text
Database Backup
Document Backup
Audit Backup
```

Important records:

```text
Invoice
Invoice Lines
Audit History
PDF / Document
Credit Notes
Debit Notes
Payments
```

---

# 129. Disaster Recovery

The system should support recovery of:

```text
Finalized Invoice
Invoice Number
Invoice Lines
Tax Calculations
Audit Trail
PDF
Related Documents
```

from backup.

Invoice numbering state should also be recoverable without creating duplicate numbers.

---

# 130. Security Audit

Administrators should be able to identify:

```text
Who created invoice
Who finalized invoice
Who cancelled invoice
Who created credit note
Who created debit note
Who recorded payment
Who modified draft
```

---

# 131. Invoice Event Timeline

Example:

```text
10 Aug 15:10
Draft Created

10 Aug 15:12
Customer Selected

10 Aug 15:14
Item Added

10 Aug 15:16
Draft Updated

10 Aug 15:20
Invoice Finalized

10 Aug 15:21
PDF Generated

11 Aug 10:30
Payment Recorded
```

This gives a complete transaction history.

---

# 132. Recommended Phase 5 Modules

Frontend:

```text
InvoiceList
InvoiceCreate
InvoiceEditDraft
InvoicePreview
InvoiceDetail
InvoiceHistory
InvoiceItemTable
InvoiceTotals
TaxBreakdown
CustomerSelector
ItemSelector
InvoicePdfViewer
CancellationModal
CreditNoteModal
DebitNoteModal
PaymentModal
```

Backend:

```text
InvoiceService
InvoiceCalculationService
InvoiceNumberService
InvoiceTaxService
InvoiceValidationService
InvoiceFinalizationService
InvoiceCancellationService
CreditNoteService
DebitNoteService
InvoiceAuditService
InvoicePdfService
```

---

# 133. Recommended Service Boundaries

```text
InvoiceService
      │
      ├── Draft Management
      │
      ├── Validation
      │
      ├── Calculation
      │
      ├── Finalization
      │
      └── Audit

TaxService
      │
      ├── GST Determination
      ├── CGST
      ├── SGST/UTGST
      ├── IGST
      └── Cess

DocumentService
      │
      ├── PDF
      ├── Print
      └── Share

CorrectionService
      │
      ├── Cancellation
      ├── Credit Note
      └── Debit Note
```

---

# 134. Final Database Relationship

```text
COMPANY
   │
   ├── CUSTOMERS
   │       │
   │       └── INVOICES
   │
   ├── ITEMS
   │       │
   │       └── INVOICE_LINES
   │
   ├── UNITS
   │       │
   │       └── ITEM / INVOICE_LINES
   │
   └── INVOICE_SERIES
           │
           └── INVOICES
                    │
                    ├── INVOICE_LINES
                    ├── TAX
                    ├── PAYMENTS
                    ├── CREDIT_NOTES
                    ├── DEBIT_NOTES
                    ├── DOCUMENTS
                    └── AUDIT_EVENTS
```

---

# 135. Complete Phase 5 Rules

The following rules are mandatory design principles:

```text
1. Draft invoices are editable.

2. Finalized invoices are locked against unrestricted editing.

3. Finalized invoices must never be physically deleted.

4. Historical invoices must retain transaction snapshots.

5. Master-data changes must not rewrite historical invoices.

6. Invoice totals must be calculated server-side.

7. Frontend-submitted tax totals must not be trusted.

8. Invoice numbering must be concurrency-safe.

9. Finalization must be atomic.

10. Duplicate finalization must be prevented.

11. Accounting periods must be respected.

12. Tax treatment must be determined by a dedicated tax engine.

13. HSN/SAC must be stored on invoice lines as a snapshot.

14. GST rate must be stored as a transaction snapshot.

15. Unit and conversion information must be snapshotted.

16. Customer information must be snapshotted.

17. Company information must be snapshotted.

18. Finalized corrections must use controlled mechanisms.

19. Cancellation must retain the original invoice.

20. Credit notes must reference original invoices where applicable.

21. Debit notes must reference original invoices where applicable.

22. All important changes must be audited.

23. High-impact corrections require confirmation.

24. Critical changes may require authorization.

25. Sensitive data must be masked in normal audit views.

26. Multi-company data must be strictly isolated.

27. Closed accounting periods must not accept ordinary changes.

28. Payment status must be separate from invoice status.

29. PDF generation must use invoice snapshots.

30. Reports must use structured database data, not PDF parsing.
```

---

# 136. Phase 5 Completion Criteria

Phase 5 is complete when the system supports:

```text
✓ New GST Tax Invoice
✓ Draft Invoice
✓ Draft Auto-save
✓ Customer Selection
✓ Quick Customer Creation
✓ Item Selection
✓ Quick Item Creation
✓ Unit Integration
✓ Quantity
✓ Unit Conversion
✓ Rate
✓ Discount
✓ HSN/SAC
✓ GST Applicability
✓ GST Rate
✓ CGST
✓ SGST/UTGST
✓ IGST
✓ Cess Architecture
✓ Other Charges Architecture
✓ Round Off
✓ Grand Total
✓ Amount in Words
✓ Place of Supply
✓ Invoice Numbering
✓ Invoice Series
✓ Fiscal Year
✓ Accounting Period
✓ Invoice Preview
✓ Invoice PDF
✓ Browser Print
✓ Download
✓ Share
✓ Finalization
✓ Invoice Locking
✓ Cancellation
✓ Credit Note Architecture
✓ Debit Note Architecture
✓ Payment Status
✓ Payment Recording Architecture
✓ Invoice History
✓ Audit Trail
✓ Server-Side Calculation
✓ Tax Calculation Engine
✓ Historical Snapshots
✓ Concurrency Protection
✓ Idempotent Finalization
✓ Multi-Company Isolation
✓ Permission Control
```

---

# 137. Final Phase 5 Architecture

```text
                         COMPANY
                            │
                            ↓
                    COMPANY CONFIGURATION
                            │
        ┌───────────────────┼────────────────────┐
        ↓                   ↓                    ↓
     CUSTOMER             ITEM                 UNIT
        │                   │                    │
        │                   ├── SKU              │
        │                   ├── HSN/SAC          │
        │                   ├── GST              │
        │                   └── Description      │
        │                                        │
        └───────────────────┬────────────────────┘
                            ↓
                       INVOICE DRAFT
                            │
                            ↓
                       VALIDATION
                            │
                            ↓
                    CALCULATION ENGINE
                            │
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
          Taxable          GST           Totals
           Value         Components
             │              │              │
             └──────────────┼──────────────┘
                            ↓
                         PREVIEW
                            │
                            ↓
                        FINALIZE
                            │
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
        Invoice Number   Snapshot      Audit
              │             │             │
              └─────────────┼─────────────┘
                            ↓
                     FINALIZED INVOICE
                            │
        ┌───────────────────┼────────────────────┐
        ↓                   ↓                    ↓
       PDF                 PRINT               SHARE
        │
        ↓
   DOCUMENT STORAGE

FINALIZED INVOICE
        │
        ├── PAYMENT
        ├── CREDIT NOTE
        ├── DEBIT NOTE
        ├── CANCELLATION
        └── AUDIT HISTORY
```

---

# 138. Core Accounting Rule

The most important Phase 5 rule is:

```text
A FINALIZED INVOICE IS A HISTORICAL TRANSACTION.
```

Therefore:

```text
Do not overwrite it.
Do not delete it.
Do not silently recalculate it from current master data.
Do not silently change its tax.
Do not silently change its customer.
Do not silently change its amount.
```

Instead:

```text
DRAFT
→ Edit freely

FINALIZED
→ Lock

CORRECTION
→ Controlled transaction

CANCELLATION
→ Preserve original + cancellation event

CREDIT
→ Related credit note

DEBIT
→ Related debit note

PAYMENT
→ Separate payment transaction
```

This structure gives the GST billing application a reliable foundation for future accounting, inventory, GST reporting, e-invoice/e-way bill integrations, customer statements, payment reconciliation and audit requirements.

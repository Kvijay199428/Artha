I re-checked the latest Artha source artifact (artha (4).md) against the Phase 0–5 specifications rather than relying only on the earlier source snapshot.

First: Phase 0–5 is not fully complete yet

The latest source is definitely further along than the previous artha (3).md. In particular, the frontend now contains an actual InvoiceBuilderPage.tsx, using React Query, React Hook Form, Zod, and the item/unit/party APIs. 

So my previous assessment that the frontend was essentially empty is outdated for the latest source.

However, I would not mark Phase 0–5 as 100% complete yet.

Remaining items before Phase 6

Area	Status

Phase 0 foundation	🟢 Mostly complete
Phase 1 company/PIN	🟢 Mostly complete
Phase 2 units/formulas	🟢 Mostly complete
Phase 3 items/SKU	🟢 Mostly complete
Phase 4 modification/versioning	🟡 Needs completion/verification
Phase 5 invoice	🟢 Core workflow implemented, but production rules need verification
Frontend integration	🟡 Needs full end-to-end testing
Automated tests	🔴 Insufficient evidence
Production GST/accounting validation	🔴 Must be completed before calling the system finished


The Phase 4 specification is particularly extensive: version comparison, restore, effective dating, optimistic locking, impact analysis, historical protection, high-risk controls, etc. 

Similarly, Phase 5 explicitly requires draft → review → finalize → numbering → immutable invoice → PDF/print/share, plus controlled modification of finalized invoices. 

So I recommend treating Phase 6 as the next development phase, while keeping a Phase 0–5 hardening checklist running in parallel.


---

Phase 6 — Supply In & Supply Out

I recommend one important terminology change before implementation.

Your definition:

SUPPLY IN  = Purchase Order
SUPPLY OUT = Sale Order

is perfectly usable inside Artha, but technically these are orders, not completed supplies.

Therefore the architecture should explicitly distinguish:

SUPPLY IN
    Purchase Order
         ↓
    Goods/Service Received
         ↓
    Purchase Bill / Purchase Invoice
         ↓
    Creditor Ledger / Inventory

SUPPLY OUT
    Sales Order
         ↓
    Goods/Service Delivered
         ↓
    GST Sales Invoice
         ↓
    Debtor Ledger / Inventory

This distinction will become extremely important later when you implement inventory, outstanding balances and accounting.


---

Phase 6 Architecture

ARTHA
                           │
             ┌─────────────┴─────────────┐
             │                           │
         SUPPLY IN                   SUPPLY OUT
       Purchase Order                Sales Order
             │                           │
       ┌─────┴─────┐               ┌─────┴─────┐
       │           │               │           │
     GST        Without GST      GST       Without GST
       │           │               │           │
       └─────┬─────┘               └─────┬─────┘
             │                           │
       Purchase flow                Sales flow
             │                           │
       Supplier                     Customer
             │                           │
       Item/Service                 Item/Service
             │                           │
       Quantity/Rate                Quantity/Rate
             │                           │
       Order total                  Order total


---

6.1 Supply In — Purchase Order

The user enters a purchase order to a supplier.

Header

Purchase Order No.
Order Date
Expected Delivery Date
Supplier
Supplier GSTIN
Supplier Address
Supplier Contact
Place of Supply
Reference Number
Payment Terms
Delivery Terms
Notes

The supplier should come from the Party Master.

This is important because your existing party architecture already distinguishes customers/suppliers and contains GST, address, bank and accounting information. 


---

6.2 Supply In — GST Type

The first major selection should be:

Tax Treatment

○ GST
○ Without GST

Do not simply interpret "Without GST" as "GST rate = 0".

They are conceptually different.

GST Purchase Order

Item
HSN/SAC
Qty
Unit
Rate
Discount
Taxable Value
GST %
CGST
SGST
IGST
Line Total

Without GST

Item
Qty
Unit
Rate
Discount
Amount

No GST tax component should be generated.

The order should retain:

tax_treatment = WITHOUT_GST

rather than:

gst_rate = 0

because later reports need to know why GST is absent.


---

6.3 Supply In — GST determination

For GST purchase orders, don't blindly trust a manually selected CGST/SGST/IGST option.

Determine tax from:

Company GST registration state
          +
Supplier state
          +
Place of Supply
          +
Transaction type
          ↓
GST treatment

Typical intra-state:

Taxable Value
      │
 ┌────┴────┐
CGST      SGST

Inter-state:

Taxable Value
      │
     IGST

The same principle is already present in Artha's invoice tax architecture.


---

6.4 Supply Out — Sales Order

Supply Out should represent a customer sales order.

Header:

Sales Order No.
Order Date
Expected Delivery Date
Customer
Customer GSTIN
Customer Address
Customer Contact
Place of Supply
Reference Number
Payment Terms
Delivery Terms
Notes


---

6.5 Supply Out — GST Type

Exactly the same two-mode selector:

Tax Treatment

○ GST
○ Without GST

GST Sales Order

Item
HSN/SAC
Qty
Unit
Rate
Discount
Taxable Value
GST %
CGST
SGST
IGST
Line Total

Without GST

Item
Qty
Unit
Rate
Discount
Amount

Again:

GST

and

WITHOUT_GST

must be explicit transaction states.


---

6.6 Important rule: Item GST vs Order GST

Your Item Master already contains:

HSN/SAC
GST applicability
GST rate

But Phase 6 should not permanently copy the item's current GST configuration without allowing transaction-level determination.

Use:

ITEM MASTER
     ↓
Default transaction configuration
     ↓
ORDER
     ↓
Transaction snapshot

For example:

Item GST = 18%

Sales Order
GST = GST
GST Rate = 18%

The order stores its own snapshot.

If the item is later changed to:

GST = 12%

the old order must remain 18%.

That follows the same historical-snapshot principle already established for Phase 5. 


---

6.7 Order line architecture

I recommend a shared order-line structure.

SupplyOrderLine
----------------
id
order_id
item_id
item_name_snapshot
sku_snapshot
hsn_sac_snapshot
unit_id
unit_name_snapshot
unit_symbol_snapshot

quantity
rate

discount_type
discount_value

tax_treatment
gst_rate

taxable_value
cgst_rate
cgst_amount
sgst_rate
sgst_amount
igst_rate
igst_amount
cess_rate
cess_amount

line_total
description

The critical concept is snapshot.

Never depend on the current Item Master to render an old order.


---

6.8 Order statuses

Both Supply In and Supply Out should have a controlled lifecycle.

Purchase Order

DRAFT
   ↓
CONFIRMED
   ↓
PARTIALLY_RECEIVED
   ↓
RECEIVED
   ↓
CLOSED

With:

CANCELLED

available from appropriate states.

Sales Order

DRAFT
   ↓
CONFIRMED
   ↓
PARTIALLY_FULFILLED
   ↓
FULFILLED
   ↓
CLOSED

With:

CANCELLED

available where permitted.


---

6.9 Never delete confirmed orders

This should be a hard rule.

DRAFT
    → can edit
    → can delete

CONFIRMED
    → cannot delete
    → controlled modification

PARTIALLY_RECEIVED/FULFILLED
    → cannot freely modify quantity
    → modification must account for fulfilled quantity

CLOSED
    → immutable

CANCELLED
    → immutable

Corrections should create an auditable modification/revision rather than silently changing historical information.

This is consistent with the existing Artha principle that posted financial transactions should not be silently overwritten. 


---

6.10 Modification rules

For Draft:

Edit
↓
Validate
↓
Recalculate
↓
Save

For Confirmed:

Edit Request
↓
Impact Analysis
↓
Change Preview
↓
Confirm
↓
Create Revision
↓
Audit

For partially fulfilled orders:

Ordered Qty = 100
Fulfilled Qty = 60
Remaining Qty = 40

You cannot modify:

100 → 20

because 60 have already been fulfilled.

You could modify the remaining quantity according to business rules, but never invalidate already fulfilled quantities.


---

6.11 GST vs Without GST — important accounting rule

Don't mix tax treatment within the same order unless you deliberately decide to support it.

I recommend:

> One order = one tax treatment.



Therefore:

Purchase Order
    └── GST

or:

Purchase Order
    └── WITHOUT_GST

Same for Sales Order.

This gives you a much cleaner reporting architecture.

If later you need mixed treatment, you can introduce:

ORDER
    ├── GST lines
    └── non-GST lines

but I would not introduce that complexity in Phase 6 unless there is a concrete business requirement.


---

6.12 Order totals

For GST:

Gross Amount
      ↓
Discount
      ↓
Taxable Amount
      ↓
GST
 ┌────┼────┐
CGST SGST IGST
      ↓
Cess
      ↓
Other Charges
      ↓
Round Off
      ↓
Grand Total

For Without GST:

Gross Amount
      ↓
Discount
      ↓
Taxable/Net Amount
      ↓
Other Charges
      ↓
Round Off
      ↓
Grand Total


---

6.13 Purchase Order → Purchase Bill

Phase 6 should not treat a purchase order as a purchase invoice.

Instead:

Purchase Order
      ↓
Receive Goods/Services
      ↓
Purchase Bill

The future Purchase Bill can inherit:

Supplier
Items
Quantities
Rates
GST
Discount
Order reference

but the actual received quantities and final invoice values must be independently recorded.

Example:

PO:
100 units

Received:
70 units

Purchase Bill:
70 units

Remaining:

30 units pending


---

6.14 Sales Order → Sales Invoice

Similarly:

Sales Order
      ↓
Delivery / Fulfilment
      ↓
Sales Invoice

Example:

SO:
100 units

Delivered:
60 units

Invoice:
60 units

Remaining:
40 units

This is especially important once Artha gets inventory management.


---

6.15 Database architecture

I recommend one generic order architecture rather than duplicating everything.

supply_orders
----------------
id
company_id

order_type
    PURCHASE
    SALES

tax_treatment
    GST
    WITHOUT_GST

order_number
order_date
expected_date

party_id
place_of_supply

status

subtotal
discount_total
taxable_total

cgst_total
sgst_total
igst_total
cess_total

other_charges
round_off
grand_total

notes
terms

revision
created_at
updated_at

Then:

supply_order_lines
------------------
id
order_id
item_id

item_name_snapshot
sku_snapshot
hsn_sac_snapshot

unit_id
unit_name_snapshot
unit_symbol_snapshot

quantity
fulfilled_quantity

rate

discount_type
discount_value

tax_treatment
gst_rate

taxable_value

cgst_amount
sgst_amount
igst_amount
cess_amount

line_total

This gives you:

supply_orders
                       │
              ┌────────┴────────┐
              │                 │
          PURCHASE             SALES
              │                 │
       SUPPLY IN           SUPPLY OUT
              │                 │
       Purchase Order       Sales Order


---

6.16 API architecture

I'd create:

/api/v1/supply-in
/api/v1/supply-out

or, preferably, one unified API:

/api/v1/orders

with:

{
  "order_type": "PURCHASE",
  "tax_treatment": "GST"
}

and:

{
  "order_type": "SALES",
  "tax_treatment": "WITHOUT_GST"
}

Then frontend routes can remain intuitive:

/supply-in
/supply-in/new
/supply-in/:id

/supply-out
/supply-out/new
/supply-out/:id

This avoids duplicating business logic in the backend.


---

6.17 UI design

I would make the modal/page begin with:

┌──────────────────────────────────────────────┐
│              CREATE SUPPLY IN                │
├──────────────────────────────────────────────┤
│                                              │
│  Order Type                                  │
│  ● Purchase Order                            │
│                                              │
│  Tax Treatment                               │
│  ● GST             ○ Without GST             │
│                                              │
│  Supplier        [ Select Supplier ▼ ]       │
│  Order Date      [ DD/MM/YYYY ]              │
│  Expected Date   [ DD/MM/YYYY ]              │
│                                              │
├──────────────────────────────────────────────┤
│ ITEMS                                        │
│                                              │
│ Item | HSN | Qty | Unit | Rate | GST | Total│
│                                              │
│ [+ Add Item]                                 │
│                                              │
├──────────────────────────────────────────────┤
│ Subtotal                         ₹           │
│ Discount                         ₹           │
│ Taxable Value                    ₹           │
│ CGST                             ₹           │
│ SGST                             ₹           │
│ IGST                             ₹           │
│ Other Charges                   ₹            │
│ Round Off                        ₹           │
│ GRAND TOTAL                     ₹            │
│                                              │
│ [Save Draft] [Review] [Confirm Order]        │
└──────────────────────────────────────────────┘

When Without GST is selected:

CGST
SGST
IGST
Cess

should disappear rather than displaying zeros everywhere.


---

6.18 Supply In vs Supply Out

Feature	Supply In	Supply Out

Meaning	Purchase Order	Sales Order
Party	Supplier	Customer
Direction	Incoming	Outgoing
GST	Yes/No	Yes/No
Item	Yes	Yes
Service	Yes	Yes
HSN/SAC	Yes	Yes
Quantity	Yes	Yes
Unit	Yes	Yes
Discount	Yes	Yes
Tax calculation	Yes when GST	Yes when GST
Expected date	Delivery/receipt	Delivery
Fulfilment	Received	Delivered
Future document	Purchase Bill	Sales Invoice
Ledger impact	Eventually creditor	Eventually debtor
Inventory	Incoming	Outgoing



---

6.19 Relationship with Debtors/Creditors

This phase connects directly to the debtor/creditor architecture we already specified.

SUPPLY IN
Purchase Order
      ↓
Supplier
      ↓
Purchase Bill
      ↓
Sundry Creditor
      ↓
Payment
      ↓
Outstanding

And:

SUPPLY OUT
Sales Order
      ↓
Customer
      ↓
Sales Invoice
      ↓
Sundry Debtor
      ↓
Receipt
      ↓
Outstanding

The existing Artha ledger design already follows the principle:

PARTY MASTER
      ↓
DOCUMENT
      ↓
LEDGER POSTING
      ↓
PAYMENT / RECEIPT
      ↓
ALLOCATION
      ↓
OUTSTANDING
      ↓
AGING



That is exactly the architecture we should preserve.


---

Phase 6 implementation order

I recommend implementing it in this order:

6.1 Shared order engine

SupplyOrder
SupplyOrderLine
SupplyOrderRevision
SupplyOrderAudit

6.2 Tax-treatment engine

GST
WITHOUT_GST

6.3 Purchase Order

Supplier
Purchase Order
GST/Without GST
Items
Totals
Status
Revision

6.4 Sales Order

Customer
Sales Order
GST/Without GST
Items
Totals
Status
Revision

6.5 Fulfilment tracking

ordered_quantity
fulfilled_quantity
remaining_quantity

6.6 Conversion

Purchase Order → Purchase Bill

Sales Order → Sales Invoice

6.7 Ledger integration

Purchase Bill → Creditor
Sales Invoice → Debtor

6.8 Inventory integration

Purchase receipt → stock IN
Sales delivery → stock OUT

6.9 Audit/revision

Every confirmed-order modification must produce:

old version
new version
changed fields
actor
timestamp
reason

6.10 Reports

Initially:

Purchase Orders
Pending Purchase Orders
Partially Received
Completed Purchase Orders

Sales Orders
Pending Sales Orders
Partially Fulfilled
Completed Sales Orders

Then later:

GST Supply In
Non-GST Supply In
GST Supply Out
Non-GST Supply Out


---

One architectural decision I strongly recommend

Don't create four separate systems:

GST Purchase
Non-GST Purchase
GST Sales
Non-GST Sales

Create one Supply Order engine with two dimensions:

order_type
──────────
PURCHASE
SALES

tax_treatment
─────────────
GST
WITHOUT_GST

That gives you exactly four combinations:

PURCHASE + GST
PURCHASE + WITHOUT_GST

SALES + GST
SALES + WITHOUT_GST

while maintaining one calculation engine, one revision system, one audit system, one numbering system and one database model.

That will make Artha substantially easier to maintain as you later add inventory, purchase bills, sales invoices, delivery/receipt, GST reports, debtor/creditor accounting and e-invoicing.

And importantly, Phase 6 should consume the existing Phase 1–5 masters rather than creating duplicate supplier/customer/item/unit/GST definitions. The Phase 3 architecture already establishes the Item Master as the central definition used by both sales and purchases. 

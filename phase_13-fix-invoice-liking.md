Worked for 11s

Yes. I examined the updated Artha source, and your concern is correct. In fact, I would change the architecture now, before adding more financial documents.

The current code has some document linking, but it is not yet using the invoice number as the central business reference across the complete document lifecycle. The current DocumentLink is ID-based and currently links, for example, QUOTATION → SUPPLY_ORDER; it stores source_id, target_id, revisions and relationship type. 

The current quotation → order conversion also creates that DocumentLink.  But the order → invoice conversion currently creates the invoice with a temporary DRAFT-... number, and the real invoice number is only assigned when the invoice is finalized.  

So Phase 13 should establish the final document genealogy architecture, rather than treating Credit Note/Debit Note as an isolated feature.

Phase 13 — Invoice-Centric Document Relationship & Genealogy System

1. Core architectural decision

Your proposed principle should become an explicit Artha rule:

> Once a document becomes an invoice, the finalized invoice number becomes the primary human-readable business reference for all subsequent invoice-related transactions.



For example:

Quotation
QT-000125
      ↓
Supply Out
SO-000083
      ↓
Invoice
INV-000421
      │
      ├── Payment
      │
      ├── Sales Return
      │
      ├── Credit Note
      │
      ├── Debit Note
      │
      ├── Refund
      │
      └── Adjustment

For purchase:

Quotation / Purchase Estimate
      ↓
Supply In
PO-000051
      ↓
Purchase Invoice
PINV-000217
      │
      ├── Payment
      ├── Purchase Return
      ├── Credit Note
      ├── Debit Note
      ├── Supplier Refund
      └── Adjustment

But there is one important technical distinction:

Do NOT use invoice number as the database foreign key.

Use:

invoice.id

as the immutable internal relationship key.

Use:

invoice.invoice_number

as the business/reference key shown to users and documents.

That gives you both reliability and usability.


---

2. Why this is necessary

Currently Artha's invoice model has:

invoice.id
invoice_number
invoice_status
payment_status
version

and invoice lines are linked through:

invoice_id



That's good as a base.

But the system currently lacks a comprehensive:

Invoice
   ↕
Document Genealogy

layer.

The existing DocumentLink is generic, which is good, but it must be extended and consistently used across all document conversions and post-invoice transactions.


---

3. The target architecture

I recommend this:

BUSINESS DOCUMENT GRAPH

                               COMPANY
                                  │
                                  │
                       ┌──────────┴──────────┐
                       │                     │
                    SALES                 PURCHASE
                       │                     │
               ┌───────┴───────┐     ┌──────┴───────┐
               │               │     │              │
          QUOTATION          BOQ   ESTIMATE       BOQ
               │               │     │              │
               └───────┬───────┘     └──────┬───────┘
                       │                     │
                       ↓                     ↓
                 SUPPLY OUT             SUPPLY IN
                       │                     │
                       ↓                     ↓
                 SALES INVOICE         PURCHASE INVOICE
                       │                     │
                       └─────────┬───────────┘
                                 │
                          INVOICE NUMBER
                                 │
               ┌─────────────────┼─────────────────┐
               │                 │                 │
             PAYMENT           RETURN          ADJUSTMENT
               │                 │                 │
               │          ┌──────┴──────┐    ┌────┴────┐
               │          │             │    │         │
               │      FULL RETURN   PARTIAL  CREDIT   DEBIT
               │                         │    NOTE     NOTE
               │                         │
               └─────────────────────────┴──────────────


---

4. Invoice becomes the financial anchor

Before invoice generation:

Quotation
Supply Order
BOQ
Estimate

are commercial/pre-financial documents.

After invoice generation:

Invoice
Payment
Return
Credit Note
Debit Note
Refund
Settlement

become financial documents associated with that invoice.

That distinction should be built into the architecture.


---

5. Invoice number assignment

The current implementation is already doing something important correctly.

Invoice number is assigned during finalization:

series.current_number
        ↓
invoice_number
        ↓
invoice.invoice_status = FINALIZED



Keep this.

Do not assign a permanent invoice number while the invoice is merely a draft.

Correct:

Draft invoice
DRAFT-xxxxxxxx

        ↓ Finalize

INV-2026-000421

Then:

invoice.id
    +
invoice.invoice_number

becomes the permanent financial identity.


---

6. But preserve the pre-invoice chain

Suppose:

Quotation QT-001
        ↓
Supply Out SO-001
        ↓
Invoice INV-001

The invoice should retain:

origin_document_type
origin_document_id
origin_document_number

and ideally all intermediary relationships should also remain in document_links.

Do not simply put:

quotation_id
order_id

into every table.

That would create an increasingly complicated schema:

invoice
 ├── quotation_id
 ├── boq_id
 ├── estimate_id
 ├── order_id
 ├── return_id
 ├── credit_note_id
 ├── debit_note_id
 ...

Avoid this.

Use the document graph.


---

7. Upgrade DocumentLink

Current:

source_type
source_id
source_revision

target_type
target_id
target_revision

relationship_type

already provides a useful foundation. 

Phase 13 should extend it to:

document_links
──────────────────────────────
id
company_id

source_type
source_id
source_number
source_revision

target_type
target_id
target_number
target_revision

relationship_type

quantity
amount

created_by
created_at

Where:

source_number
target_number

are snapshots of the business references, not foreign keys.


---

8. Why store both ID and number?

Example:

source_id     = UUID
source_number = QT-000125

target_id     = UUID
target_number = SO-000082

If someone later searches:

QT-000125

you can immediately show:

QT-000125
      ↓
SO-000082
      ↓
INV-000421

while the database still uses UUID relationships.


---

9. New central concept: DocumentReference

I recommend introducing a normalized document-reference abstraction.

Conceptually:

DocumentReference
──────────────────────
document_type
document_id
document_number
company_id
financial_year
status
party_id
document_date

This doesn't necessarily need to be a physical database table if it creates unnecessary complexity. It can initially be a service/schema abstraction.

The important thing is that every document can be represented uniformly.


---

10. Document types

Define a controlled enumeration:

COMPANY

BOQ
ESTIMATE
QUOTATION

SUPPLY_IN
SUPPLY_OUT

PURCHASE_INVOICE
SALES_INVOICE

SUPPLY_IN_RETURN
SUPPLY_OUT_RETURN

CREDIT_NOTE
DEBIT_NOTE

PAYMENT
REFUND

Potentially:

RECEIPT
PAYMENT_VOUCHER
JOURNAL

later.


---

11. Relationship types

Create controlled relationship types.

Commercial

CREATED_FROM
DERIVED_FROM
ESTIMATED_FROM
QUOTED_FROM

Conversion

CONVERTED_TO
CONVERTED_FROM

Fulfilment

FULFILLS
FULFILLED_BY

Financial

INVOICED_FROM
ADJUSTS
REFUNDS
PAID_AGAINST
ALLOCATED_AGAINST

Return

RETURN_AGAINST
RETURNED_FROM


---

12. Example complete chain

BOQ-000001
    │
    │ ESTIMATED_FROM
    ↓
EST-000001
    │
    │ QUOTED_FROM
    ↓
QT-000001
    │
    │ CONVERTED_TO
    ↓
SO-000001
    │
    │ INVOICED_FROM
    ↓
INV-000001

Then:

INV-000001
    │
    ├── PAYMENT PAY-000001
    │
    ├── RETURN SR-000001
    │       │
    │       └── CREDIT NOTE CN-000001
    │
    ├── CREDIT NOTE CN-000002
    │
    └── DEBIT NOTE DN-000001

This is exactly the genealogy you are looking for.


---

13. Credit/Debit Note creation UI

Your proposed UX is correct.

User clicks:

Create Credit Note

Artha should not immediately open an empty form.

Instead:

SELECT SOURCE INVOICE

Search:

Invoice Number
Customer/Supplier
Invoice Date
GSTIN
Amount
Outstanding

Example:

Select Invoice

┌───────────────────────────────────────────────┐
│ INV-2026-00421                                │
│ ABC Traders                                   │
│ 15-Aug-2026                                   │
│ ₹1,18,000                                     │
│ Outstanding: ₹48,000                          │
└───────────────────────────────────────────────┘

Then:

Continue


---

14. After invoice selection

Artha loads the invoice snapshot:

Invoice: INV-2026-00421

Customer:
ABC Traders

Invoice Date:
15-Aug-2026

Tax Treatment:
GST

Lines:
────────────────────────────────
Item        Qty   Rate   GST
────────────────────────────────
Product A   10    1000   18%
Product B    5     500   12%

Then the user chooses:

Adjustment Type

○ Full
○ Partial
○ Item/Quantity based
○ Value based
○ Tax only


---

15. Credit note should inherit invoice data

When an invoice is selected, prefill:

Customer
Customer GSTIN
Address
Place of Supply
Original Invoice Number
Original Invoice Date
Tax treatment
HSN/SAC
GST rates
Unit
Item description

But these are snapshots.

Don't dynamically pull today's item master GST rate into an old invoice's credit note.


---

16. User should not be able to change source identity

Once:

Invoice = INV-000421

has been selected, the note must contain:

original_invoice_id = invoice.id
original_invoice_number = INV-000421

The UI should not allow changing it after note creation.

If they selected the wrong invoice:

Change Invoice

should reset the draft.


---

17. Same mechanism for Debit Note

Create Debit Note
       ↓
Select Invoice
       ↓
Load invoice
       ↓
Select adjustment
       ↓
Calculate
       ↓
Preview
       ↓
Save Draft
       ↓
Finalize


---

18. Don't use invoice number alone internally

This is an important refinement to your idea.

You said:

> everything should be linked through invoice number.



I agree from the business/UI perspective, but not as a database FK.

Use:

invoice_id = UUID
invoice_number = INV-2026-000421

Every related table should have:

invoice_id

where the relationship is directly invoice-specific.

And DocumentLink should provide the general genealogy.

This gives you:

Database identity

invoice_id

Human identity

INV-2026-000421

Search/index identity

company_id + invoice_number


---

19. Direct invoice relationship tables

For high-frequency financial relationships, direct FK is appropriate.

For example:

Payment

payment
    invoice_id

Credit Note

credit_note
    invoice_id

Debit Note

debit_note
    invoice_id

Return

return_order
    invoice_id

Then additionally:

document_links

provides the universal document graph.

This is not redundant in a bad way. These serve different purposes.


---

20. Credit Note model upgrade

Current Artha already exposes:

CreditNote
DebitNote

from models.invoice. 

Phase 13 should upgrade them to something like:

CreditNote
────────────────────────
id
company_id

note_number
note_date

invoice_id
invoice_number_snapshot

party_id
party_name_snapshot
party_gstin_snapshot

reason_code
reason_description

tax_treatment

subtotal
taxable_total
cgst
sgst
igst
cess
grand_total

adjustment_type
settlement_status

status

created_by
approved_by
posted_by

created_at
updated_at
posted_at

Same principle for Debit Note.


---

21. Add note line → invoice line relationship

This is particularly important.

credit_note_lines
────────────────────
id
credit_note_id

invoice_line_id

item_id
item_name_snapshot
hsn_sac_snapshot

original_quantity
returned_quantity
adjusted_quantity

rate

taxable_value
cgst
sgst
igst
cess

line_total

Then Artha can answer:

> Which exact invoice line was adjusted?



Example:

INV-001
 │
 ├── Line 1 Product A
 │       └── CN-001: 3 units
 │
 └── Line 2 Product B
         └── CN-001: 1 unit


---

22. Prevent excessive credit/debit

For each invoice line:

original_quantity
-
already_returned_quantity
-
already_credit_noted_quantity
+
already_debit_noted_quantity

must be evaluated according to the adjustment type.

The UI should show:

Original Qty       10
Already Returned    3
Already Credited    2
Available           5

Therefore user cannot create another credit for 8.

The backend must enforce the same rule.


---

23. Invoice detail page becomes the central workspace

This is one of the biggest changes I recommend.

When user opens:

INV-2026-00421

show tabs:

Overview
Items
Payments
Returns
Credit Notes
Debit Notes
Adjustments
Documents
Audit Trail


---

24. Documents tab

Show the entire genealogy:

DOCUMENT HISTORY

Quotation
QT-000125
       ↓
Supply Out
SO-000083
       ↓
Invoice
INV-000421
       │
       ├── Payment PAY-000315
       │
       ├── Return SR-000012
       │       ↓
       │   Credit Note CN-000021
       │
       ├── Credit Note CN-000025
       │
       └── Debit Note DN-000009

Click any node:

Open Document

This will be much more powerful than simply displaying a list of IDs.


---

25. Invoice number should appear everywhere

For example:

Credit note list

CN-00021
Against Invoice: INV-000421
Customer: ABC Traders
Amount: ₹10,000

Return list

SR-00012
Against Invoice: INV-000421

Payment

PAY-00031
Against Invoice: INV-000421

Debit note

DN-00009
Against Invoice: INV-000421


---

26. Search architecture

Create a universal document search:

Search documents...

Search:

INV-000421
CN-000021
DN-000009
QT-000125
SO-000083

The backend identifies:

document_type
document_id
document_number

and navigates directly to the appropriate document.


---

27. Invoice-centric quick actions

On finalized invoice:

┌──────────────────────────────┐
│ INV-2026-00421               │
│                              │
│ [Payment]                    │
│ [Sales Return]               │
│ [Credit Note]                │
│ [Debit Note]                 │
│ [Print]                      │
│ [Download PDF]               │
└──────────────────────────────┘

For purchase invoice:

[Payment]
[Purchase Return]
[Credit Note]
[Debit Note]
[Print]
[PDF]

The available actions depend on transaction type.


---

28. Conversion architecture

This is another area where the current source needs improvement.

Currently quotation → order has an explicit DocumentLink. 

Order → invoice currently creates an invoice, but the shown implementation does not establish the equivalent complete document-link relationship. 

Phase 13 should require every conversion to create a link.

Required:

Quotation → Supply Order

Supply Order → Invoice

BOQ → Estimate

Estimate → Quotation

Quotation → Invoice

if direct conversion is allowed.


---

29. Direct quotation → invoice

If business workflow permits:

Quotation
    ↓
Invoice

don't artificially create an order.

The graph should simply be:

QT-001
  ↓
INV-001

with:

relationship_type = CONVERTED_TO_INVOICE


---

30. Partial conversion

This is extremely important.

Suppose quotation:

QT-001

Product A = 100
Product B = 50

Invoice 1:

INV-001
Product A = 40

Invoice 2:

INV-002
Product A = 60
Product B = 20

The graph must support:

QT-001
 ├── INV-001
 └── INV-002

Therefore never use one quotation.invoice_id field.

Use DocumentLink.


---

31. Conversion quantity tracking

For line-level conversion, use:

document_line_links

Recommended:

document_line_links
────────────────────────
id

source_document_type
source_document_id
source_line_id

target_document_type
target_document_id
target_line_id

source_quantity
converted_quantity

source_amount
converted_amount

created_at

Then:

Quotation line
Qty 100

Invoice 1
Qty 40

Invoice 2
Qty 60

can be accurately tracked.

This is superior to a simple:

quotation.fully_converted = true

although the existing field can remain as a cached convenience indicator.


---

32. Existing fully_converted needs correction

The current order conversion does:

quotation.fully_converted = True

when creating an order. 

That is dangerous for partial conversion.

Instead calculate:

converted_quantity >= quotation_quantity

for every relevant line.

Then:

fully_converted = true

only when all convertible quantities are exhausted.

Also support:

PARTIALLY_CONVERTED
FULLY_CONVERTED


---

33. Document lineage vs accounting settlement

Keep these separate.

Document lineage

QT → SO → INV → CN

Financial settlement

INV
 │
 ├── Payment
 ├── Credit
 ├── Debit
 └── Refund

Inventory/quantity movement

INV
 │
 └── Return

Do not make one table responsible for all three domains.


---

34. Payment architecture

The current PaymentAllocation uses:

payment_id
invoice_id
allocated_amount



That is exactly the direction we want.

Phase 13 should extend the same concept so payment allocation is explicitly connected to the invoice.

Then:

Invoice
 ↓
Payment
 ↓
PaymentAllocation

and not:

Invoice → manually changed paid_amount


---

35. Credit/debit allocation

Similarly:

adjustment_allocations

should connect:

Credit Note
      ↓
Invoice

or:

Debit Note
      ↓
Invoice

This allows:

CN-001 = ₹10,000

to be applied against:

INV-001 ₹6,000
INV-002 ₹4,000

if your business rules permit customer/supplier credit allocation across invoices.

But when the note is specifically issued against one original GST invoice, retain:

original_invoice_id

separately.


---

36. Important distinction: original invoice vs allocation invoice

These are not necessarily the same.

For example:

Credit Note CN-001
Original invoice = INV-001

But customer may have:

INV-001 ₹10,000
INV-002 ₹20,000

and the credit could be allocated later to INV-002.

Therefore:

original_invoice_id

means:

> Why was this credit note issued?



while:

allocation.invoice_id

means:

> Where was the financial credit applied?



This distinction will prevent major accounting problems later.


---

37. Phase 13 database changes

Implement migrations for:

document_links

upgrade:

credit_notes
debit_notes

add:

credit_note_lines
debit_note_lines

add:

document_line_links

add:

adjustment_allocations

and extend:

payments
payment_allocations
returns

with invoice references where missing.


---

38. Recommended invoice fields

Add/ensure:

invoice.id
invoice_number
invoice_series
financial_year

origin_document_type
origin_document_id
origin_document_number

source_order_id
source_order_number

invoice_status
payment_status

But don't duplicate every possible ancestor.

For example, don't add:

boq_id
estimate_id
quotation_id
order_id
return_id
credit_note_id
debit_note_id
...

The document graph handles those.


---

39. Recommended DocumentLink indexes

SQLite performance will matter.

Add indexes on:

(company_id, source_type, source_id)
(company_id, target_type, target_id)
(company_id, source_number)
(company_id, target_number)
(company_id, relationship_type)

For invoice lookup:

(company_id, invoice_number)

must be unique where appropriate.


---

40. Invoice number uniqueness

Within a company and financial year:

company_id
+
financial_year
+
invoice_number

should be unique.

Do not make:

invoice_number

globally unique across all companies.


---

41. Never modify finalized invoice number

Once:

INV-2026-000421

is assigned:

invoice_number

is immutable.

If an invoice is cancelled:

INV-2026-000421
CANCELLED

do not recycle the number.


---

42. Document number snapshots

When creating:

Credit Note CN-001

store:

invoice_id = UUID
original_invoice_number = INV-001

The number is a snapshot/reference.

This protects printed documents and historical audit records.


---

43. API architecture

Introduce:

GET /api/v1/documents/search?q=INV-000421

and:

GET /api/v1/invoices/{invoice_id}/relations

Return:

{
  "invoice": {},
  "ancestors": [],
  "children": [],
  "payments": [],
  "returns": [],
  "credit_notes": [],
  "debit_notes": [],
  "allocations": []
}

Also:

GET /api/v1/invoices/{invoice_id}/timeline


---

44. Invoice creation from source

Instead of each module independently copying invoice data, create:

InvoiceCreationService

with:

create_from_quotation()
create_from_supply_order()
create_from_estimate()
create_from_manual_entry()

All ultimately call:

create_invoice()

Then:

InvoiceCreationService
        │
        ├── snapshot_party()
        ├── snapshot_company()
        ├── snapshot_items()
        ├── calculate_tax()
        ├── calculate_totals()
        └── create_document_links()


---

45. Finalization transaction

The following must happen atomically:

BEGIN TRANSACTION

Validate invoice
      ↓
Lock invoice series
      ↓
Assign invoice number
      ↓
Finalize invoice
      ↓
Create invoice ledger entry
      ↓
Create source DocumentLink
      ↓
Update conversion quantities
      ↓
Audit
      ↓
COMMIT

If any step fails:

ROLLBACK

This is essential.


---

46. Credit/debit finalization

Similarly:

BEGIN

Load original invoice
       ↓
Validate adjustment capacity
       ↓
Calculate GST
       ↓
Assign note number
       ↓
Finalize note
       ↓
Create invoice relationship
       ↓
Create ledger adjustment
       ↓
Create allocation
       ↓
Audit

COMMIT


---

47. UI architecture

Don't build separate completely independent forms.

Create a reusable:

InvoiceReferenceSelector

used by:

Credit Note
Debit Note
Sales Return
Purchase Return
Payment
Refund

It should support:

Search invoice number
Customer/Supplier
Date range
Status
Outstanding amount
GSTIN


---

48. Reusable invoice context

Once selected:

InvoiceContext

provides:

invoice
party
lines
tax
payment_status
outstanding
available_return_qty
available_credit
available_debit

Then each module consumes that context.


---

49. Frontend flow

Credit Note

Credit Note
    ↓
Select Invoice
    ↓
Invoice Context
    ↓
Select Lines
    ↓
Enter adjustment
    ↓
GST calculation
    ↓
Settlement
    ↓
Preview
    ↓
Save Draft
    ↓
Finalize

Debit Note

Same flow.

Return

Return
 ↓
Select Invoice
 ↓
Select items
 ↓
Quantity
 ↓
Return reason
 ↓
Inventory movement
 ↓
Settlement


---

50. Invoice detail page becomes the main navigation hub

I strongly recommend this UX:

Invoice # INV-2026-000421

[Overview] [Items] [Payments] [Returns]
[Credit Notes] [Debit Notes] [Documents] [Audit]

At the top:

Customer
Invoice Date
GSTIN
Taxable
GST
Total
Paid
Outstanding

And action buttons:

+ Payment
+ Return
+ Credit Note
+ Debit Note


---

51. Document timeline

Add a chronological timeline:

15 Aug 2026
Quotation QT-001 created

16 Aug 2026
Quotation accepted

17 Aug 2026
Supply Order SO-001 created

18 Aug 2026
Invoice INV-001 finalized

19 Aug 2026
Payment PAY-001 ₹50,000

21 Aug 2026
Sales Return SR-001

21 Aug 2026
Credit Note CN-001 ₹10,000

This will make Artha much easier to audit.


---

52. Phase 13 should also fix current conversion weaknesses

Based on the current source, these are specifically remaining:

1. Quotation → Order

Partially implemented.

Existing DocumentLink is created. 

But the fully_converted = True behavior needs to become quantity-aware.

2. Order → Invoice

Conversion exists, but the shown code creates a temporary draft invoice number. 

The conversion must create the invoice relationship.

3. Invoice → downstream documents

Not yet sufficiently centralized.

The existing invoice model and ledger support are present, but a complete invoice-centric document graph is not implemented.

4. Credit/Debit Notes

Models exist, but they need to be upgraded into full source-invoice-linked workflows.

5. Invoice line genealogy

Needs to be added for precise partial conversion/return/adjustment tracking.


---

53. One major existing issue unrelated to the relationship architecture

The current quotation calculation contains:

is_inter_state = False

as a stub. 

That should not survive into production.

Phase 13 should centralize GST calculation rather than allowing quotation, order, invoice, credit note and debit note to independently determine CGST/SGST/IGST.


---

54. Recommended final architecture

ARTHA DOCUMENT ENGINE
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
             DOCUMENT GRAPH              FINANCIAL ENGINE
                    │                           │
             DocumentLink              Ledger / Allocation
                    │                           │
        ┌───────────┼───────────┐       ┌───────┼────────┐
        │           │           │       │       │        │
     QUOTATION    ORDER       INVOICE  PAYMENT RETURN  NOTES
        │           │           │               │      │
        └───────────┴───────────┘               │   ┌──┴──┐
                    │                           │  CN   DN
                    │                           │
                    └──────────────┬────────────┘
                                   │
                            INVOICE CONTEXT
                                   │
                       ┌───────────┼───────────┐
                       │           │           │
                    Invoice     Party       Lines
                       │
                 Invoice Number
                       │
              Human-readable anchor


---

55. The rule I would lock into Artha

This should be added to the Phase 13 specification:

> Every financial document created after an invoice must require an invoice selection or an explicitly defined non-invoice source. When an invoice is selected, Artha must retain the immutable internal invoice ID and the finalized invoice number as the original business reference. All related documents must appear in the invoice's document genealogy and must be navigable from the invoice detail page.



And:

> Invoice number is the primary human-facing business reference; invoice ID is the authoritative database relationship key.



That gives you exactly what you want without sacrificing database integrity.


---

56. Final Phase 13 workflow

PRE-INVOICE
                        │
      ┌─────────────────┼─────────────────┐
      │                 │                 │
     BOQ             ESTIMATE         QUOTATION
      │                 │                 │
      └─────────────────┼─────────────────┘
                        ↓
                   SUPPLY ORDER
                        ↓
                  CREATE INVOICE
                        ↓
                 SAVE DRAFT
                        ↓
                    FINALIZE
                        ↓
             ASSIGN INVOICE NUMBER
                        ↓
                INV-2026-000421
                        │
              ╔═════════╧═════════╗
              ║   INVOICE HUB     ║
              ╚═════════╤═════════╝
                        │
       ┌────────────────┼─────────────────┐
       │                │                 │
    PAYMENT           RETURN          ADJUSTMENT
       │                │                 │
       │         ┌──────┴──────┐      ┌───┴────┐
       │         │             │      │        │
       │       FULL         PARTIAL   CN       DN
       │         │             │      │        │
       └─────────┴─────────────┴──────┴────────┘
                        │
                  PARTY LEDGER
                        │
                PAYMENT / REFUND
                        │
                   AUDIT TRAIL

This is the architecture I recommend locking in before Phase 14. It also gives you a clean foundation for later GST reporting, e-invoice/e-way-bill integration, customer/supplier statements, ageing reports, outstanding reports, and eventually a proper accounting ledger without having to redesign the document relationships again.

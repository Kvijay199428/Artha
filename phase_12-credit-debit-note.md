Worked for 24s

Yes. I checked the latest Artha source before defining this phase.

There is an important finding: Artha already has CreditNote and DebitNote database models, and the party ledger already explicitly supports Credit Note and Debit Note transaction types.  

However, that is not yet a complete Credit/Debit Note module. The existing models are too minimal for the workflow we need: there are no line-item models, no robust note lifecycle, no settlement/allocation model, no proper source-document polymorphism, and no complete UI/API workflow visible in the latest source.

So I would make the next phase:

Phase 10 — Credit Note & Debit Note Management

And I recommend treating it as an accounting adjustment layer above invoices, supply orders and returns, rather than simply adding two more forms.


---

1. First: correct GST terminology and accounting direction

There is an important distinction that Artha must preserve.

Under Section 34 of the CGST Act, a supplier issues a GST credit note when the original taxable value/tax was too high, goods are returned, or goods/services are deficient. A supplier issues a GST debit note when the original taxable value/tax was too low. 

Therefore, don't design the system as:

Customer → Debit Note
Supplier → Credit Note

That is an accounting shortcut and can become wrong for GST.

Instead distinguish:

DOCUMENT TYPE
    CREDIT_NOTE
    DEBIT_NOTE

PARTY ROLE
    CUSTOMER
    SUPPLIER

SOURCE
    SALES
    PURCHASE


---

2. Artha's four important business cases

Sales side

Sales Credit Note

Company
   ↓
Customer

Original Sales Invoice
       ↓
Credit Note
       ↓
Customer payable reduced

Typical reasons:

Sales return

Excess billing

Excess GST

Discount granted after invoice

Deficiency in goods/services

Price reduction

Commercial adjustment


GST credit note can reduce the supplier's output tax subject to the applicable statutory conditions. 


---

Sales Debit Note

Company
   ↓
Customer

Original Sales Invoice
       ↓
Debit Note
       ↓
Customer liability increases

Typical reasons:

Under-billing

Additional quantity

Price increase

GST short-charged

Additional charges discovered later


Under Section 34, a debit note is issued by the supplier when taxable value or tax charged in the original invoice is less than what is actually payable. 


---

3. Purchase side

This is where the software needs careful terminology.

For a purchase transaction, Artha is the recipient, not the supplier.

Supplier's Credit Note received

Supplier
   ↓
Company

Purchase Invoice
       ↓
Supplier Credit Note
       ↓
Company payable reduced

Example:

Purchase             ₹100,000
Supplier credit note  ₹10,000
-----------------------------
Payable               ₹90,000

This is the normal GST-side mechanism when the supplier reduces the taxable value/tax.


---

Supplier's Debit Note received

Supplier
   ↓
Company

Purchase Invoice
       ↓
Supplier Debit Note
       ↓
Company payable increases

Example:

Purchase             ₹100,000
Supplier debit note   ₹10,000
-----------------------------
Payable              ₹110,000

A supplier-issued debit note is relevant to the recipient's input-tax documentation; CBIC rules specifically recognize a supplier's debit note as a document for ITC, subject to the applicable conditions. 


---

4. Don't call every purchase adjustment "Purchase Debit Note"

Artha can provide an accounting convenience:

Purchase Adjustment
    ├── Debit
    └── Credit

but the GST document should retain:

issuer_role
document_type
gst_document = true/false

This prevents the common accounting/GST terminology problem.


---

5. Recommended Phase 10 architecture

ARTHA
                      │
                 DOCUMENT
                      │
       ┌──────────────┼──────────────┐
       │              │              │
    INVOICE        RETURN        ADJUSTMENT
       │              │              │
       │              │       ┌──────┴──────┐
       │              │       │             │
       │              │    CREDIT        DEBIT
       │              │     NOTE           NOTE
       │              │       │             │
       └──────────────┴───────┴─────────────┘
                              │
                         PARTY LEDGER
                              │
                    RECEIVABLE / PAYABLE


---

6. Current Artha source: what must change

The existing model is:

CreditNote
DebitNote

with only:

number
original_invoice_id
party_id
date
reason
taxable_amount
CGST
SGST
IGST
cess
total
status



That is insufficient.

You need to replace/extend this architecture rather than merely adding more columns.


---

7. Recommended database model

adjustment_notes

I recommend one common table:

adjustment_notes
────────────────────────
id
company_id

note_number
note_type
    CREDIT_NOTE
    DEBIT_NOTE

source_type
    SALES_INVOICE
    PURCHASE_BILL
    SUPPLY_OUT
    SUPPLY_IN
    SALES_RETURN
    PURCHASE_RETURN
    OTHER

source_id
source_number

party_id
party_role

note_date
reason_code
reason_description

tax_treatment
    GST
    WITHOUT_GST

gst_document
is_accounting_only

place_of_supply
reverse_charge

subtotal
discount_total
taxable_total

cgst_total
sgst_total
igst_total
cess_total

round_off
grand_total

status

created_by
approved_by
posted_by

created_at
updated_at
posted_at


---

8. Note line table

Do not put all adjustment information into the header.

Create:

adjustment_note_lines
────────────────────────
id
adjustment_note_id

source_line_id
item_id

item_name_snapshot
sku_snapshot
hsn_sac_snapshot

description

quantity
unit_id
unit_snapshot

rate

discount_type
discount_value
discount_amount

tax_treatment
gst_rate

taxable_value
cgst_amount
sgst_amount
igst_amount
cess_amount

line_total

This is especially important because Artha already uses line-level historical snapshots for quotations/orders. 


---

9. Source document rule

Every note should identify its source where applicable.

Example:

Credit Note CN-00045

Against:
Invoice INV-00125

Database:

source_type = SALES_INVOICE
source_id   = INV-00125

For a return:

Credit Note CN-00046

Against:
Sales Return SOR-00012

This provides:

Invoice
   ↓
Return
   ↓
Credit Note

instead of mixing the two concepts.


---

10. Credit note vs return

This distinction is essential.

A return answers:

> What goods/services came back?



A credit note answers:

> What financial/tax adjustment does the supplier make because of that event?



Therefore:

Sales Return
     ↓
Inventory movement
     ↓
Credit Note
     ↓
Receivable adjustment/refund

But not every credit note needs a physical return.

Example:

Invoice = ₹100,000

Post-sale discount = ₹5,000

No goods returned.

Credit Note = ₹5,000

So Artha must support:

Credit Note WITHOUT Return


---

11. Debit note vs return

Similarly:

Under-billed invoice
        ↓
Debit Note

No physical return is required.

Example:

Invoice:
100 × ₹100
= ₹10,000

Actual agreed price:
₹110

Difference:
₹1,000

Debit Note:
₹1,000


---

12. Credit note reasons

Create a controlled master list:

SALES_RETURN
EXCESS_BILLING
EXCESS_TAX
POST_SALE_DISCOUNT
PRICE_REDUCTION
DEFICIENCY_IN_GOODS
DEFICIENCY_IN_SERVICE
CANCELLATION
OTHER


---

13. Debit note reasons

UNDER_BILLING
SHORT_CHARGED_TAX
ADDITIONAL_QUANTITY
PRICE_REVISION
ADDITIONAL_CHARGES
POST_SALE_ADJUSTMENT
OTHER

Don't allow arbitrary free-text reasons as the only classification.

Use:

reason_code
reason_description


---

14. GST vs Without GST

Every note must explicitly contain:

GST

or:

WITHOUT_GST

For GST:

taxable
CGST
SGST
IGST
cess

For Without GST:

taxable/value
GST = 0


---

15. GST credit note calculation

Original:

Taxable = ₹10,000
GST 18% = ₹1,800
Total = ₹11,800

Credit note:

Taxable = ₹2,000
GST = ₹360
Total = ₹2,360

Customer outstanding decreases by:

₹2,360

Supplier's output-tax liability is adjusted according to applicable GST rules.


---

16. GST debit note calculation

Original:

Taxable = ₹10,000
GST = ₹1,800

Actual taxable:

₹12,000

Debit note:

Additional taxable = ₹2,000
GST = ₹360
Total = ₹2,360

Customer outstanding increases by:

₹2,360


---

17. Important GST document fields

A GST credit/debit note should capture the prescribed information, including supplier/recipient details, note number/date and reference to the corresponding invoice/bill of supply. CBIC's GST invoice rules specify these requirements. 

Artha should therefore include:

Supplier Name
Supplier Address
Supplier GSTIN

Recipient Name
Recipient Address
Recipient GSTIN/UIN where applicable

Credit/Debit Note Number
Note Date

Original Invoice Number
Original Invoice Date

HSN/SAC
Description
Quantity
Rate
Taxable Value

GST Rate
CGST
SGST
IGST
Cess

Place of Supply
Reverse Charge

Total


---

18. GST note numbering

Do not use invoice numbering.

Use separate series:

CN-000001
CN-000002

and:

DN-000001
DN-000002

For each financial year.

GST e-invoice systems use document types CRN for credit note and DBN for debit note, and document numbers have specific constraints when e-invoicing applies. 

Therefore Artha should keep:

internal_note_number
gst_document_number

as separate concepts if necessary.


---

19. Note lifecycle

Use:

DRAFT
   ↓
APPROVED
   ↓
POSTED

Alternative terminal states:

CANCELLED
REJECTED

Do not allow:

POSTED → EDIT


---

20. Modification rules

DRAFT

Editable.

APPROVED

No normal editing.

POSTED

Immutable.

If an error occurs:

Original Note
      ↓
Reversal / Cancellation
      ↓
Correct Note

Do not overwrite a posted accounting document.

This matches the existing Artha design principle that posted transactions should not be silently overwritten and corrections should use reversal/adjustment transactions. 


---

21. Partial credit note

Original:

Invoice = ₹100,000

Credit note:

₹20,000

Remaining invoice value:

₹80,000

The system must calculate:

Original invoice adjustment capacity
-
Previous credit notes
+
Previous debit notes

to determine the maximum permissible adjustment where the note is tied to a source.


---

22. Multiple notes against one invoice

Allowed:

INV-001
 │
 ├── CN-001 ₹5,000
 ├── CN-002 ₹3,000
 └── DN-001 ₹2,000

Net adjustment:

-₹5,000
-₹3,000
+₹2,000
──────────
-₹6,000

Remaining invoice:

Original - ₹6,000


---

23. Prevent over-adjustment

The backend must enforce:

total_credit_adjustment
-
total_debit_adjustment
<= allowable_source_adjustment

where the source is applicable.

Never rely only on the React UI.


---

24. Settlement model

Do not directly change:

party.balance

Artha already has a proper party ledger architecture, where invoice/payment/credit/debit note entries are represented as ledger transactions. 

Continue that design.

Create:

note_allocations
────────────────────
id
note_id

party_id

target_type
    INVOICE
    PAYMENT
    ADVANCE
    CREDIT_BALANCE
    PAYABLE

target_id

allocated_amount

allocation_date

created_by


---

25. Sales credit note ledger

For customer:

Sales Credit Note
    ↓
Credit Customer

Example:

Invoice        Dr Customer ₹50,000
Payment        Cr Customer ₹20,000
Credit Note    Cr Customer ₹5,000

Outstanding:

₹25,000

This is also explicitly documented in Artha's existing Sundry Debtors/Creditors specification. 


---

26. Sales debit note

Sales Debit Note
    ↓
Debit Customer

Example:

Invoice = ₹50,000
Debit Note = ₹5,000

Customer outstanding = ₹55,000


---

27. Purchase credit note

Supplier credit note:

Supplier Credit Note
       ↓
Debit Supplier

because company liability decreases.

Example:

Purchase = ₹80,000
Supplier Credit Note = ₹5,000

Payable = ₹75,000


---

28. Purchase debit note

Supplier debit note:

Supplier Debit Note
       ↓
Credit Supplier

because company liability increases.

Example:

Purchase = ₹80,000
Supplier Debit Note = ₹5,000

Payable = ₹85,000

Again, this is consistent with the accounting direction already documented for Artha's creditors. 


---

29. Credit note refund

If the customer has already paid:

Invoice = ₹50,000
Paid = ₹50,000
Credit Note = ₹5,000

Then:

Customer outstanding = ₹0
Customer credit = ₹5,000

The user can choose:

REFUND

or:

CUSTOMER_CREDIT


---

30. Credit note against outstanding

If:

Invoice = ₹50,000
Paid = ₹30,000
Credit Note = ₹5,000

then:

Outstanding before = ₹20,000
Credit note = ₹5,000

Outstanding after = ₹15,000

No refund.


---

31. Credit balance

If:

Outstanding = ₹2,000
Credit Note = ₹5,000

then:

₹2,000 → outstanding adjustment
₹3,000 → customer credit

That ₹3,000 can be:

Refunded

or:

Applied against future invoice


---

32. Debit note payment effect

If:

Outstanding = ₹5,000
Debit Note = ₹2,000

then:

New outstanding = ₹7,000

No separate payment is created.


---

33. Return + credit note integration

This is where Phase 10 should integrate tightly with Phase 7.

Recommended:

Sales Order
    ↓
Sales Return
    ↓
Credit Note
    ↓
Customer Ledger
    ↓
Refund / Credit

For purchase:

Purchase Order
    ↓
Purchase Return
    ↓
Supplier Credit Note
    ↓
Supplier Ledger
    ↓
Refund / Payable Adjustment

But allow a return to exist without a credit note if the financial adjustment is pending.


---

34. Don't automatically create a credit note during return creation

Recommended workflow:

Create Return
      ↓
Approve Return
      ↓
Post Return
      ↓
Financial adjustment decision
      ↓
Create Credit Note

This prevents accidental financial postings before the return is accepted.


---

35. Existing Artha return settlement can be reused

The current source already has:

ReturnSettlement
SettlementType

including:

ADJUST_RECEIVABLE
ADJUST_PAYABLE
CUSTOMER_REFUND
SUPPLIER_REFUND
CUSTOMER_CREDIT
SUPPLIER_CREDIT



Therefore do not build another refund engine for Credit/Debit Notes.

Create a shared:

FinancialAdjustmentService

and have both:

Returns
Credit Notes
Debit Notes

use it.


---

36. Recommended shared accounting service

FinancialAdjustmentService
│
├── create_credit_note()
├── create_debit_note()
├── post_note()
├── allocate_note()
├── reverse_note()
├── calculate_remaining()
└── create_ledger_entry()

Then:

ReturnService
       ↓
FinancialAdjustmentService

CreditNoteService
       ↓
FinancialAdjustmentService

DebitNoteService
       ↓
FinancialAdjustmentService

This avoids three separate implementations of the same accounting logic.


---

37. API design

GET    /api/v1/adjustment-notes
POST   /api/v1/adjustment-notes
GET    /api/v1/adjustment-notes/{id}
PATCH  /api/v1/adjustment-notes/{id}

POST   /api/v1/adjustment-notes/{id}/approve
POST   /api/v1/adjustment-notes/{id}/post
POST   /api/v1/adjustment-notes/{id}/cancel
POST   /api/v1/adjustment-notes/{id}/reverse

GET    /api/v1/adjustment-notes/source/{source_type}/{source_id}

POST   /api/v1/adjustment-notes/{id}/allocations
GET    /api/v1/adjustment-notes/{id}/allocations

POST   /api/v1/adjustment-notes/{id}/refund
POST   /api/v1/adjustment-notes/{id}/apply-credit

Convenience routes can also exist:

GET /api/v1/credit-notes
GET /api/v1/debit-notes

but internally they should use the same adjustment service.


---

38. Frontend routes

Add:

/credit-notes
/credit-notes/new
/credit-notes/:id

/debit-notes
/debit-notes/new
/debit-notes/:id

And optionally:

/supply-out/credit-notes
/supply-out/debit-notes

/supply-in/credit-notes
/supply-in/debit-notes

I prefer the first architecture:

Accounting
 ├── Credit Notes
 └── Debit Notes

with filters for:

Sales
Purchase
Customer
Supplier
GST
Without GST


---

39. UI should reuse existing components

Do not build a new form system.

The current Artha frontend already uses:

React Hook Form

Zod

TanStack Query

Axios

React Router

existing Button

existing Input


The current package.json confirms those dependencies. 

For example, the existing Units page already uses:

react-hook-form
@hookform/resolvers
zod
TanStack Query



Use the same architecture.


---

40. Libraries: use existing libraries instead of custom implementations

Already installed — reuse

Requirement	Library

Forms	react-hook-form
Form validation	zod
Form/Zod integration	@hookform/resolvers
API caching/state	@tanstack/react-query
HTTP	axios
Routing	react-router-dom
Backend validation	pydantic
ORM	SQLAlchemy
DB migrations	Alembic
Password/PIN hashing	argon2-cffi
PDF	reportlab
Exact money calculations	Python decimal
Testing	pytest, pytest-asyncio


The backend already includes FastAPI, SQLAlchemy, Alembic, Pydantic, pytest and ReportLab. 


---

41. Libraries I recommend adding

@tanstack/react-table

Use it for:

Credit Note list
Debit Note list
Ledger allocation
Source invoice selection

Instead of writing your own:

sorting
filtering
pagination
column visibility
row selection


---

date-fns

Use for:

financial year
note dates
due dates
validity
date filtering
date formatting

Don't create your own date utilities.


---

lucide-react

Use for:

Edit
View
Print
Download
Approve
Cancel
Reverse
Credit
Debit
Refund

instead of manually creating SVG icons.


---

react-number-format

Useful for:

₹1,25,000.00

and controlled monetary inputs.

But never trust frontend formatted values for accounting calculations. The backend remains authoritative.


---

42. UI component library decision

Artha currently uses Tailwind and its own simple components.

I would not immediately replace the existing UI with MUI/Ant Design.

Instead:

Tailwind CSS
+
existing Button/Input
+
React Hook Form
+
Zod
+
TanStack Table
+
Lucide

is sufficient.

If you want a complete accessible component system later, shadcn/ui is a good fit with Tailwind because the components become part of your source rather than forcing a large runtime UI framework.

For this phase, don't rewrite existing UI.


---

43. Backend: don't add an accounting package yet

I would not introduce a generic Python accounting package for the core ledger.

Your requirements include:

GST
Indian GSTIN
CGST
SGST
IGST
HSN/SAC
GST returns
E-invoice
E-way bill
Indian financial year

A generic accounting package will not automatically solve those correctly.

Use:

SQLAlchemy
Pydantic
Decimal
Alembic

and keep your domain logic in:

services/
repositories/
schemas/
models/


---

44. Money calculation rule

Artha already uses Decimal in its order calculations. 

Continue this.

Never:

float(quantity) * float(rate)

Use:

Decimal(quantity) * Decimal(rate)

and quantize according to the application's accounting precision.


---

45. GST calculation should be centralized

There is currently duplicated GST calculation logic in some services, and the quotation implementation even contains a placeholder:

is_inter_state = False



For Phase 10, do not duplicate that logic again.

Create:

GSTCalculationService

with:

calculate_tax()
determine_supply_type()
calculate_cgst_sgst()
calculate_igst()
calculate_cess()
calculate_note_tax()

Then:

Invoice
Supply Order
Return
Quotation
Credit Note
Debit Note

all call the same tax engine.


---

46. Important correction to existing GST implementation

The existing quotation/order code has simplified interstate logic. 

Phase 10 should enforce:

Company GST state
        +
Party/place-of-supply state
        +
supply nature
        ↓
INTRA_STATE
or
INTER_STATE

Then:

INTRA_STATE
    → CGST + SGST

INTER_STATE
    → IGST

Do not let each feature decide this independently.


---

47. E-invoice preparation

When e-invoicing applies, GST credit/debit notes are also relevant documents; IRP documentation identifies CRN and DBN document types. 

Therefore store future-ready fields:

irn
ack_number
ack_date
signed_qr_code
signed_invoice
einvoice_status
einvoice_error_code
einvoice_error_message

Do not implement an IRP client in Phase 10 unless you're ready to handle credentials, authentication, cancellation, retry/idempotency and current government APIs.

Just make the schema extensible.


---

48. GST reporting fields

The note needs enough data for future GSTR reporting.

Store:

original_invoice_number
original_invoice_date
note_number
note_date

recipient_gstin

note_type
note_reason

taxable_value
cgst
sgst
igst
cess

place_of_supply
reverse_charge

original_supply_category

GST portal documentation explicitly treats credit/debit notes as separate reporting data and supports amendments to those note records. 


---

49. Audit rules

Every important action:

CREATE
UPDATE
APPROVE
POST
CANCEL
REVERSE
ALLOCATE
REFUND

must generate an audit event.

Artha already has an AuditLog model with:

old_value
new_value
reason
IP
user-agent
metadata



Reuse it.


---

50. Recommended implementation order

PHASE 10.1
Database model
        ↓
PHASE 10.2
Schemas / validation
        ↓
PHASE 10.3
GST calculation integration
        ↓
PHASE 10.4
Credit/Debit Note service
        ↓
PHASE 10.5
Ledger posting
        ↓
PHASE 10.6
Allocation/settlement
        ↓
PHASE 10.7
API
        ↓
PHASE 10.8
Frontend list
        ↓
PHASE 10.9
Frontend creation
        ↓
PHASE 10.10
Source-document selection
        ↓
PHASE 10.11
PDF
        ↓
PHASE 10.12
Audit
        ↓
PHASE 10.13
GST/e-invoice preparation
        ↓
PHASE 10.14
Tests


---

51. Final document flow for Artha

The system should ultimately behave like this:

ARTHA
                           │
          ┌────────────────┼────────────────┐
          │                │                │
       SALES           PURCHASE           OTHER
          │                │
       Invoice          Bill
          │                │
    ┌─────┴─────┐    ┌─────┴─────┐
    │           │    │           │
  Return      Note  Return      Note
    │           │    │           │
    │       ┌───┴───┐│       ┌───┴───┐
    │       │       ││       │       │
    │      CN      DN│      CN      DN
    │       │       ││       │       │
    └───────┴───────┘└───────┴───────┘
              │               │
              └───────┬───────┘
                      ↓
                PARTY LEDGER
                      ↓
             RECEIVABLE / PAYABLE
                      ↓
               ALLOCATION
                      ↓
               REFUND / CREDIT

Critical implementation principle

Do not create separate accounting logic for returns, credit notes and debit notes.

Build one:

FinancialAdjustmentService

and one centralized:

GSTCalculationService

Then connect:

Invoice
Supply In/Out
Return
Credit Note
Debit Note
Payment

to those shared services.

That will prevent Artha from becoming a collection of modules that calculate the same financial event differently.

Also, because Artha's existing source already contains the basic CreditNote/DebitNote models, the correct implementation is an upgrade/migration of the existing models, not creating a second parallel note system. 

Recommended Phase 10 completion criterion

Don't mark Phase 10 complete until this test passes end-to-end:

Invoice ₹100,000
        ↓
Payment ₹70,000
        ↓
Sales Return ₹20,000
        ↓
Credit Note ₹20,000
        ↓
Receivable adjustment ₹20,000
        ↓
Outstanding ₹10,000

and:

Invoice ₹100,000
        ↓
Debit Note ₹10,000
        ↓
Outstanding increases by ₹10,000

and:

Purchase Bill ₹100,000
        ↓
Supplier Credit Note ₹20,000
        ↓
Payable decreases by ₹20,000

and:

Purchase Bill ₹100,000
        ↓
Supplier Debit Note ₹10,000
        ↓
Payable increases by ₹10,000

with GST and Without-GST variants, partial notes, multiple notes, source-document validation, ledger posting, audit trail, cancellation/reversal and settlement allocation all tested.

This is the point at which Artha moves from being primarily a billing/order application toward a proper GST-aware receivables/payables accounting system.

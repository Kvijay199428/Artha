Phase 7 — Supply In Return & Supply Out Return

Phase 7 should be designed as a return-management and financial-adjustment system, not as a simple “negative invoice” feature.

The core principle should be:

> Never modify the original Supply In/Supply Out transaction to represent a return. Create a separate Return transaction linked to the original document, preserve the original transaction, and calculate the financial/quantity reversal from the actual returned quantity/value.



This is important because returns can be full, partial, or phased, and payment may already be settled, partially settled, or completely outstanding.


---

1. Phase 7 terminology

SUPPLY OUT
    Sales Order
         ↓
    Customer receives goods/services
         ↓
    Return initiated by customer
         ↓
SUPPLY OUT RETURN
    Customer → Company

Meaning:

Supply Out Return = Sales Return

The company receives the returned goods/services and owes money back to the customer, or reduces the customer's outstanding balance.


---

SUPPLY IN
    Purchase Order
         ↓
    Company receives goods/services
         ↓
    Company returns goods/services to supplier
         ↓
SUPPLY IN RETURN
    Company → Supplier

Meaning:

Supply In Return = Purchase Return

The company sends goods/services back to the supplier and becomes entitled to a refund/credit, or reduces the amount payable to the supplier.


---

2. The most important rule

Never do this:

Original Sales Order
    quantity: 100
    amount: ₹10,000

Customer returns 20

Original Sales Order
    quantity: 80       ❌

Instead:

Original Sales Order
    quantity: 100
    amount: ₹10,000
    status: partially returned

              │
              ▼

Supply Out Return #SOR-0001
    quantity: 20
    return amount: ₹2,000

The original transaction remains historically accurate.


---

3. Return relationship

Every return must have a parent/original transaction.

Return
│
├── original_order_id
├── original_order_type
├── original_line_id
├── return_number
├── return_date
├── return_quantity
└── return_amount

Therefore:

SO-000123
   │
   ├── Return #1 → 20 units
   ├── Return #2 → 15 units
   └── Return #3 → 10 units

Total returned:

45 units

Remaining:

100 - 45 = 55 units


---

4. Full return

Example:

Sales Order
100 units
₹10,000

Customer returns all:

Supply Out Return
100 units
₹10,000

Result:

Original quantity       100
Returned quantity       100
Remaining quantity        0

Status:

FULLY_RETURNED

Financial result depends on payment state.


---

5. Partial return

Example:

Sales Order
100 units
₹10,000

Customer returns:

30 units

Return:

30 units
₹3,000

Remaining:

70 units
₹7,000

Original order:

PARTIALLY_RETURNED


---

6. Phased return

This is an important requirement from your design.

Example:

Original = 100 units

Return 1:

20 units

Return 2:

15 units

Return 3:

25 units

Total:

20 + 15 + 25 = 60

Remaining:

40

The system must calculate:

Total Ordered
- Total Previously Returned
= Maximum Returnable Quantity

So the user cannot return more than the remaining quantity.


---

7. Supply Out Return financial behavior

Supply Out Return means:

Company
   ↓
refund / credit
   ↓
Customer

But the actual financial treatment depends on the customer's payment status.

There are three important situations.


---

7.1 Customer has not paid

Example:

Sales = ₹10,000
Customer paid = ₹0
Return = ₹3,000

Original receivable:

₹10,000

After return:

₹10,000 - ₹3,000 = ₹7,000

Therefore:

> No immediate cash refund is required. The customer's outstanding balance is reduced.



Ledger concept:

Customer Receivable
    Debit  ₹10,000

Sales Return
    Credit ₹3,000

Net Receivable
    ₹7,000


---

8. Customer partially paid

Example:

Sales = ₹10,000
Customer paid = ₹6,000
Outstanding = ₹4,000

Customer returns goods worth:

₹3,000

After return:

Original outstanding = ₹4,000
Return adjustment    = ₹3,000
Remaining outstanding = ₹1,000

No cash refund is necessary.

The return is first used to reduce the outstanding receivable.


---

9. Customer fully paid

Example:

Sales = ₹10,000
Paid = ₹10,000
Return = ₹3,000

There is no outstanding receivable.

Therefore:

Customer refund due = ₹3,000

The company can:

Refund ₹3,000

or, if the customer agrees:

Customer credit balance = ₹3,000

That credit can later be applied against another invoice/order.


---

10. Return allocation priority

For Supply Out Return, I recommend this rule:

Return Amount
      │
      ▼
Is customer outstanding?
      │
 ┌────┴────┐
YES        NO
 │          │
Reduce      Create
receivable  refund/credit

If:

Return > outstanding

then:

Outstanding → ₹0
Excess → Customer Credit/Refund

Example:

Outstanding = ₹1,000
Return = ₹3,000

Result:

Receivable reduced = ₹1,000
Customer credit    = ₹2,000


---

11. Supply In Return

Supply In Return is the reverse.

The company purchased goods/services from a supplier.

Supplier
    ↓
Company

Company returns:

Company
    ↓
Supplier

The company should receive:

Supplier credit

or:

Refund


---

12. Supplier has not been paid

Example:

Purchase = ₹10,000
Paid = ₹0
Return = ₹3,000

Original payable:

₹10,000

After return:

₹10,000 - ₹3,000
= ₹7,000

Therefore:

> The company simply owes the supplier ₹7,000.



No refund is required.


---

13. Supplier partially paid

Example:

Purchase = ₹10,000
Paid = ₹6,000
Outstanding = ₹4,000

Return = ₹3,000

After return:

Outstanding = ₹1,000

The supplier does not need to immediately refund anything.


---

14. Supplier fully paid

Example:

Purchase = ₹10,000
Paid = ₹10,000
Return = ₹3,000

The supplier now owes the company:

₹3,000

The supplier can:

Refund ₹3,000

or:

Supplier Credit ₹3,000

which can be adjusted against future purchases.


---

15. Supply In Return allocation priority

The reverse rule applies:

Return Amount
      │
      ▼
Is supplier payable outstanding?
      │
 ┌────┴────┐
YES        NO
 │          │
Reduce      Create
payable     supplier credit/refund

If:

Return > outstanding

then:

Payable reduced → ₹0
Excess → Supplier Credit/Refund Receivable


---

16. Payment state must be independent of return state

Do not create a single field such as:

return_status = REFUNDED

and assume that is enough.

You need separate concepts:

Return Status
Payment Status
Refund/Adjustment Status
Fulfilment Status

For example:

Return Status:
PARTIAL

Payment Status:
PAID

Financial Adjustment:
REFUND_PENDING

This accurately represents:

> The customer returned part of the order, but the refund hasn't yet been made.




---

17. Recommended return statuses

Supply Out Return

DRAFT
REQUESTED
APPROVED
RECEIVED
PARTIALLY_RECEIVED
COMPLETED
CANCELLED

Financial status separately:

NOT_REQUIRED
ADJUSTED_AGAINST_RECEIVABLE
REFUND_PENDING
PARTIALLY_REFUNDED
REFUNDED
CREDIT_CREATED

Supply In Return

DRAFT
REQUESTED
APPROVED
DISPATCHED
PARTIALLY_RECEIVED_BY_SUPPLIER
COMPLETED
CANCELLED

Financial status:

NOT_REQUIRED
ADJUSTED_AGAINST_PAYABLE
REFUND_PENDING
PARTIALLY_REFUNDED
REFUNDED
CREDIT_CREATED


---

18. Return quantity rules

This must be enforced at the database/service layer.

For each original line:

Returnable Qty =
Original Qty
- Previously Returned Qty
- Cancelled/Rejected Return Qty

For example:

Original = 100

Return #1 = 20
Return #2 = 30
Return #3 = 10

Previously returned = 60

Maximum new return = 40

Attempt:

Return 50

must be rejected.


---

19. Never use negative quantities

Avoid:

quantity = -20

for a return line.

Use:

return_quantity = 20
transaction_type = RETURN

This makes reporting, validation, inventory and audit much safer.

The accounting direction should be determined by the return transaction type.


---

20. Return price must be based on the original transaction

Suppose:

Original:
10 units × ₹100

Later the Item Master changes:

₹100 → ₹150

Return must still use:

₹100

not ₹150.

Therefore return lines must reference the original transaction snapshot.

Original Line
      ↓
Price Snapshot
      ↓
Return Calculation

Never calculate historical returns using today's Item Master price.


---

21. Discount handling

Suppose:

10 units
₹100 each
Gross = ₹1,000

Discount = ₹100

Taxable = ₹900

If 5 units are returned, don't simply calculate:

₹500

You need to reverse the same proportional commercial calculation used by the original transaction.

Example:

Returned gross value = ₹500
Proportional discount = ₹50
Returned taxable value = ₹450

Then calculate the corresponding tax reversal.

The exact rounding must use the same rounding policy as the original transaction.


---

22. GST return calculation

For a GST transaction:

Original
Taxable Value = ₹1,000
GST = ₹180
Total = ₹1,180

Full return:

Return taxable = ₹1,000
GST reversal = ₹180
Return total = ₹1,180

Partial return:

Return taxable = ₹400
GST reversal = ₹72
Return total = ₹472

The return should retain:

GST rate
CGST
SGST
IGST
Cess

as snapshots.


---

23. Without GST return

For:

tax_treatment = WITHOUT_GST

there should be no tax reversal.

Example:

Original = ₹1,000
Return = ₹400

Return:

Taxable/Net = ₹400
GST = ₹0
Total = ₹400

Do not create a fake 0% GST tax record simply to make the UI work.


---

24. Supply Out Return accounting direction

Conceptually:

Original Sale
─────────────
Customer Receivable     DR
Sales Revenue           CR
GST Liability           CR

Return:

Sales Return            DR
GST Liability           DR
Customer Receivable     CR

If money is actually refunded:

Customer Refund
Customer Receivable     DR
Bank/Cash               CR

The exact account mapping should ultimately be controlled by your accounting engine rather than hard-coded inside the return UI.


---

25. Supply In Return accounting direction

Original purchase:

Purchase/Inventory      DR
Input GST               DR
Supplier Payable        CR

Purchase return:

Supplier Payable        DR
Purchase Return         CR
Input GST reversal      CR

If supplier refunds money:

Bank/Cash                DR
Supplier Receivable/Credit CR

Again, the final posting should go through the accounting/ledger service.


---

26. Inventory rules

This is critical.

Supply Out Return

Customer sends goods back:

Customer
   ↓
Company

Therefore inventory normally:

STOCK IN

Supply In Return

Company sends goods back:

Company
   ↓
Supplier

Therefore inventory:

STOCK OUT

But the system should not automatically assume returned goods are saleable.

A returned item may be:

GOOD
DAMAGED
DEFECTIVE
EXPIRED
REPAIR_REQUIRED
SCRAP

Therefore Phase 7 should introduce return-condition tracking.


---

27. Return condition

Recommended:

condition
────────────
GOOD
DAMAGED
DEFECTIVE
EXPIRED
REPAIR
SCRAP
OTHER

And:

warehouse_action
────────────────
RETURN_TO_STOCK
QUARANTINE
REPAIR
SCRAP
RETURN_TO_SUPPLIER

This will make the future inventory module much more robust.


---

28. Services

Services don't have physical inventory.

Therefore:

Service Return

should not generate:

STOCK IN
STOCK OUT

Instead it only generates:

Financial reversal
GST reversal where applicable

Example:

Consulting Service
₹10,000

Customer cancels ₹4,000 portion

Return:
₹4,000

No inventory transaction.


---

29. Full/partial/phased return across multiple lines

Suppose:

SO-1001

Item A = 100
Item B = 50
Item C = 20

Return #1:

A = 20
B = 10

Return #2:

A = 30
C = 5

Return #3:

B = 20
C = 15

The system must maintain per-line:

Original
Returned
Remaining

not merely document-level totals.


---

30. Return document structure

I recommend a unified model:

returns
──────────────
id
company_id

return_number

return_type
    SUPPLY_OUT_RETURN
    SUPPLY_IN_RETURN

original_order_id
original_order_type

party_id

return_date

status

financial_status

reason

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

created_by
approved_by
created_at
updated_at

And:

return_lines
──────────────
id
return_id
original_order_line_id
item_id

item_name_snapshot
sku_snapshot
hsn_sac_snapshot

unit_id
unit_snapshot

original_quantity
previously_returned_quantity
return_quantity
remaining_quantity

original_rate
rate

discount_snapshot

tax_treatment
gst_rate

taxable_value
cgst_amount
sgst_amount
igst_amount
cess_amount

line_total

condition
warehouse_action


---

31. Financial adjustment table

Do not put all refund information inside returns.

Create a separate financial adjustment model:

return_settlements
──────────────────
id
return_id

settlement_type

ADJUST_RECEIVABLE
ADJUST_PAYABLE
CUSTOMER_REFUND
SUPPLIER_REFUND
CUSTOMER_CREDIT
SUPPLIER_CREDIT

amount

payment_id
ledger_entry_id

status

settlement_date
reference_number
notes

This lets one return be settled in phases.


---

32. Phased refund

Your requirement specifically mentions phased settlement.

Example:

Return = ₹10,000

Customer receives:

Refund #1 = ₹4,000
Refund #2 = ₹3,000
Refund #3 = ₹3,000

System:

Return Amount       ₹10,000
Refunded            ₹7,000
Remaining Refund    ₹3,000

Status:
PARTIALLY_REFUNDED

Never mark it REFUNDED until:

settled_amount == return_amount


---

33. Partial refund + outstanding adjustment

Example:

Return = ₹10,000
Outstanding = ₹4,000

Automatically:

Receivable adjustment = ₹4,000
Remaining refund = ₹6,000

Then:

Refund #1 = ₹3,000
Refund #2 = ₹3,000

Final:

Receivable adjustment = ₹4,000
Cash refund = ₹6,000
Total settled = ₹10,000

This is exactly the type of flexible settlement architecture you need.


---

34. Supplier-side equivalent

Example:

Purchase Return = ₹10,000
Supplier Payable = ₹4,000

System:

Payable adjustment = ₹4,000
Supplier credit/refund = ₹6,000

Then supplier can provide:

Credit ₹3,000
Credit ₹3,000

or refund it.


---

35. Return approval

For non-draft returns, use:

Create
 ↓
Validate
 ↓
Review
 ↓
Approve
 ↓
Post

Validation must check:

Original order exists
Original order belongs to company
Party matches
Line belongs to original order
Return quantity <= returnable quantity
Return date valid
Tax treatment matches original
Rate snapshot valid
GST calculations valid
No closed/cancelled original


---

36. No return after an invalid state

Do not allow returns against:

Deleted order
Draft order
Cancelled order
Invalidated order

unless your business rules explicitly permit a special recovery process.

A closed/finalized transaction should be returned through the dedicated return workflow.


---

37. Return modification rules

Draft

Fully editable.

Approved

Controlled modification only.

Posted

No direct editing.

Settled

Absolutely no direct editing.

If an error exists:

Correction / reversal

must be generated.

Never modify historical financial records silently.


---

38. Audit trail

Every return should record:

Created
Modified
Submitted
Approved
Posted
Cancelled
Refund initiated
Refund partially completed
Refund completed
Credit created
Credit applied

With:

user
timestamp
IP/device/session if available
reason
old value
new value


---

39. Important document relationship

The final architecture should become:

SUPPLY OUT
                    │
              Sales Order
                    │
              Sales Invoice
                    │
              ┌─────┴─────┐
              │           │
           Payment      Return
                          │
                    Supply Out Return
                          │
                    Refund/Credit

And:

SUPPLY IN
                    │
             Purchase Order
                    │
             Purchase Bill
                    │
              ┌─────┴─────┐
              │           │
           Payment      Return
                          │
                    Supply In Return
                          │
                    Refund/Credit


---

40. Phase 7 API structure

I recommend:

POST   /api/v1/returns
GET    /api/v1/returns
GET    /api/v1/returns/{id}
PATCH  /api/v1/returns/{id}

POST   /api/v1/returns/{id}/approve
POST   /api/v1/returns/{id}/post
POST   /api/v1/returns/{id}/cancel

GET    /api/v1/orders/{id}/returnable-lines

POST   /api/v1/returns/{id}/settlements
GET    /api/v1/returns/{id}/settlements

POST   /api/v1/returns/{id}/refund
POST   /api/v1/returns/{id}/credit
POST   /api/v1/returns/{id}/adjust

And frontend:

/supply-out/returns
/supply-out/returns/new
/supply-out/returns/:id

/supply-in/returns
/supply-in/returns/new
/supply-in/returns/:id


---

41. Phase 7 reporting

Add:

Supply Out Returns

Sales Returns
Customer
Original Order
Return No.
Return Date
Returned Qty
Return Amount
GST
Refunded
Credit
Outstanding Adjustment
Status

Supply In Returns

Purchase Returns
Supplier
Original Order
Return No.
Return Date
Returned Qty
Return Amount
GST
Supplier Refund
Supplier Credit
Payable Adjustment
Status

And summary:

Total Sales Returns
Total Purchase Returns
GST Reversal
Customer Refunds
Supplier Refunds
Customer Credits
Supplier Credits
Pending Refunds
Pending Credits


---

42. Phase 7 golden rules

I would make these non-negotiable business rules:

1. Never edit the original order/invoice to represent a return.


2. Every return must reference its original transaction.


3. A return can be full, partial, or phased.


4. Returned quantity can never exceed the remaining returnable quantity.


5. Return price/tax/discount comes from the original transaction snapshot.


6. GST and Without-GST remain explicit transaction types.


7. GST returns reverse the corresponding GST components.


8. Without-GST returns create no GST reversal.


9. Outstanding receivables/payables are adjusted before creating a cash refund/credit for the excess.


10. Refunds/credits can themselves be partial/phased.


11. Payment status and return status must be separate.


12. Goods returns affect inventory; service returns do not.


13. Returned goods must have a condition/disposition.


14. Posted/settled returns cannot be silently edited.


15. Every financial change must produce an audit trail.


16. Cross-company access must be impossible.


17. Historical transaction snapshots must never depend on today's Item/Unit/Party master.


18. All financial calculations must use decimal arithmetic, not floating point.


19. Rounding must be deterministic and consistent with the original transaction.


20. Return settlement must be idempotent—retrying the same request must not create a duplicate refund/ledger posting.




---

Final Phase 7 architecture

The complete flow should therefore be:

ARTHA
                           │
              ┌────────────┴────────────┐
              │                         │
          SUPPLY OUT                 SUPPLY IN
          Sales Order              Purchase Order
              │                         │
          Sales Invoice             Purchase Bill
              │                         │
          Customer                  Supplier
              │                         │
        ┌─────┴─────┐           ┌─────┴─────┐
        │           │           │           │
      Payment     RETURN      Payment      RETURN
                    │                       │
            Supply Out Return       Supply In Return
                    │                       │
             ┌──────┴──────┐         ┌──────┴──────┐
             │             │         │             │
         Adjustment      Refund   Adjustment      Refund
             │             │         │             │
         Receivable     Customer  Payable       Company
             │             │         │             │
             └─────────────┴─────────┴─────────────┘
                           │
                      Ledger Engine
                           │
                      Audit Engine
                           │
                    Inventory Engine

This design gives Artha a proper foundation for the next major accounting stages: inventory movements, purchase/sales bills, debit/credit notes, customer/supplier ledgers, outstanding/aging, GST return reporting, and eventually e-invoicing/e-way bill integration.

# Sundry Debtors and Sundry Creditors — GST Billing Software Specification

## 1. Purpose

This document defines the recommended data structure and accounting requirements for **Sundry Debtors** and **Sundry Creditors** in a GST billing/accounting application.

- **Sundry Debtors**: customers/parties who owe money to the business, generally arising from credit sales.
- **Sundry Creditors**: suppliers/vendors to whom the business owes money, generally arising from credit purchases.

> Important: Sundry Debtor/Creditor is an accounting classification. GST registration status, GSTIN, tax treatment, place of supply, ITC, HSN/SAC, etc. are separate GST attributes.

---

# 2. Common Party Master

A common `Party` master should be used for both customers and suppliers wherever possible.

## 2.1 Basic Party Details

| Field | Required | Description |
|---|---|---|
| party_id | Yes | Unique internal identifier |
| party_code | Recommended | Human-readable party code |
| legal_name | Yes | Legal/business name |
| trade_name | Optional | Trade name |
| party_type | Yes | Individual / Proprietorship / Partnership / LLP / Company / Other |
| account_type | Yes | Customer / Supplier / Both |
| contact_person | Optional | Primary contact person |
| mobile | Optional | Contact number |
| alternate_mobile | Optional | Alternate number |
| email | Optional | Email address |
| website | Optional | Website |
| notes | Optional | Internal remarks |
| status | Yes | Active / Inactive |
| created_at | Yes | Creation timestamp |
| updated_at | Yes | Last update timestamp |

---

# 3. GST Details

GST information should be maintained separately from general party information.

## 3.1 GST Fields

| Field | Required | Description |
|---|---|---|
| gstin | Conditional | 15-character GSTIN for registered parties |
| gst_registration_type | Yes | Regular / Composition / Unregistered / SEZ / Other applicable category |
| gstin_status | Recommended | Active / Cancelled / Suspended / Unknown |
| gst_legal_name | Recommended | Name associated with GSTIN |
| gst_trade_name | Optional | Trade name from GST records |
| gst_registration_date | Optional | GST registration date |
| taxpayer_type | Optional | Taxpayer classification |
| pan | Conditional | PAN associated with the party |
| state | Yes | State of registration/address |
| state_code | Yes | GST state code |
| sez_status | Optional | SEZ status where applicable |
| composition_status | Optional | Composition status |
| reverse_charge_applicable | Yes | Whether RCM treatment may apply |
| einvoice_applicable | Recommended | Whether e-invoicing is applicable based on business rules |
| gst_notes | Optional | GST-related notes |

### Validation

For a registered GST party:

```text
GSTIN:
- Exactly 15 characters
- Validate GSTIN structure/checksum
- Store GSTIN in normalized uppercase form
```

Do not assume GST registration status never changes. If the software supports historical compliance, maintain GST status history with effective dates.

---

# 4. Address Details

A party can have multiple addresses.

Recommended address types:

```text
REGISTERED
BILLING
SHIPPING
OFFICE
WAREHOUSE
OTHER
```

## 4.1 Address Fields

| Field | Required | Description |
|---|---|---|
| address_id | Yes | Unique address ID |
| party_id | Yes | Related party |
| address_type | Yes | Registered / Billing / Shipping / etc. |
| address_line_1 | Yes | Address |
| address_line_2 | Optional | Additional address |
| landmark | Optional | Landmark |
| city | Yes | City/town |
| district | Optional | District |
| state | Yes | State |
| state_code | Yes | GST state code |
| pincode | Yes | PIN code |
| country | Yes | Normally India for domestic parties |
| is_default | Yes | Default address flag |

---

# 5. Bank and Payment Details

Bank details should be separate because a party may have multiple bank accounts.

## 5.1 Bank Fields

| Field | Required | Description |
|---|---|---|
| bank_account_id | Yes | Unique account ID |
| party_id | Yes | Related party |
| account_holder_name | Recommended | Account holder |
| bank_name | Recommended | Bank name |
| branch_name | Optional | Branch |
| account_number | Optional | Bank account number |
| ifsc | Optional | IFSC |
| upi_id | Optional | UPI ID |
| is_primary | Yes | Primary payment account |
| status | Yes | Active / Inactive |

Sensitive bank information should be protected using appropriate access controls and encryption.

---

# 6. Credit and Payment Terms

These fields are useful for both debtors and creditors.

| Field | Description |
|---|---|
| credit_limit | Maximum permitted outstanding |
| credit_days | Allowed credit period |
| payment_terms | Cash / Advance / Credit / Custom |
| due_date_rule | Rule used to calculate due date |
| default_payment_method | Cash / Bank / UPI / Card / Other |
| default_price_list | Default sales/purchase price list |
| reminder_enabled | Enable payment reminders |
| reminder_days_before_due | Reminder threshold |

---

# 7. Sundry Debtors

## 7.1 Definition

A Sundry Debtor is normally a customer who has an amount payable to the business.

Example:

```text
Sales Invoice       ₹50,000
Receipt             ₹20,000
Credit Note          ₹5,000
--------------------------------
Outstanding         ₹25,000
```

The outstanding amount should be derived from ledger transactions rather than manually edited.

## 7.2 Debtor-Specific Information

Recommended fields:

| Field | Description |
|---|---|
| customer_category | Retail / Wholesale / Corporate / Other |
| sales_account | Default sales ledger/account |
| credit_limit | Customer credit limit |
| credit_days | Customer credit period |
| default_sales_tax_treatment | Default GST treatment |
| default_place_of_supply | Default POS where appropriate |
| collection_priority | Normal / High / Low |
| customer_notes | Internal notes |

---

# 8. Sundry Creditors

## 8.1 Definition

A Sundry Creditor is normally a supplier/vendor to whom the business owes an amount.

Example:

```text
Purchase Invoice    ₹80,000
Payment             ₹30,000
Debit Note           ₹5,000
--------------------------------
Outstanding         ₹45,000
```

## 8.2 Creditor-Specific Information

Recommended fields:

| Field | Description |
|---|---|
| supplier_category | Manufacturer / Distributor / Service Provider / Other |
| purchase_account | Default purchase ledger/account |
| credit_days | Supplier credit period |
| default_purchase_tax_treatment | Default GST treatment |
| default_expense_account | Default expense account where applicable |
| default_payment_method | Default payment method |
| supplier_notes | Internal notes |

---

# 9. Party Ledger

Do not store only a single manually editable `balance` field.

Use a transaction ledger.

## 9.1 Ledger Entry

Recommended fields:

| Field | Description |
|---|---|
| ledger_entry_id | Unique entry ID |
| party_id | Party |
| transaction_date | Transaction date |
| posting_date | Accounting posting date |
| transaction_type | Invoice / Receipt / Payment / Credit Note / Debit Note / Journal / Opening |
| reference_type | Source document type |
| reference_id | Source document ID |
| reference_number | Human-readable document number |
| debit | Debit amount |
| credit | Credit amount |
| currency | Currency |
| narration | Description |
| due_date | Due date where applicable |
| created_at | Timestamp |

---

# 10. Debtor Accounting Logic

For a normal customer account:

```text
Credit Sale Invoice
    → Debit customer

Customer Payment
    → Credit customer

Sales Credit Note
    → Credit customer

Sales Debit Note
    → Debit customer
```

Example:

```text
Invoice:
Customer A Dr.       ₹50,000
    To Sales              ₹50,000
```

Payment:

```text
Bank Dr.             ₹20,000
    To Customer A        ₹20,000
```

Outstanding:

```text
₹50,000 - ₹20,000 = ₹30,000
```

---

# 11. Creditor Accounting Logic

For a normal supplier account:

```text
Purchase Invoice
    → Credit supplier

Supplier Payment
    → Debit supplier

Purchase Debit Note
    → Debit supplier

Purchase Credit Note
    → Credit supplier
```

Example:

```text
Purchase:
Purchase/Expense Dr.  ₹80,000
    To Supplier A          ₹80,000
```

Payment:

```text
Supplier A Dr.        ₹30,000
    To Bank               ₹30,000
```

Outstanding:

```text
₹80,000 - ₹30,000 = ₹50,000
```

---

# 12. Opening Balances

The software should support opening balances.

## Debtor

```text
Customer A
Opening Balance: ₹25,000 Dr.
```

This means the customer owes the business ₹25,000.

## Creditor

```text
Supplier A
Opening Balance: ₹40,000 Cr.
```

This means the business owes the supplier ₹40,000.

The system should allow:

```text
opening_balance
opening_balance_type
opening_balance_date
opening_balance_reference
```

Opening balances should be posted through the accounting ledger rather than directly manipulating the calculated balance.

---

# 13. Invoice Party Snapshot

Historical invoices must not depend entirely on the current party master.

When an invoice is issued, save the party information used on that invoice.

Recommended snapshot fields:

```text
party_id
party_name
legal_name
trade_name
gstin
pan
billing_address
shipping_address
state
state_code
place_of_supply
gst_registration_type
```

Reason:

If a customer changes their address or GSTIN later, previously issued invoices must retain the historical information applicable when the invoice was issued.

---

# 14. Sales Invoice and Debtor Relationship

```text
Party
  │
  └── Customer / Debtor
          │
          ├── Sales Invoice
          │       ├── Invoice Items
          │       ├── GST
          │       └── Due Date
          │
          ├── Receipt
          │
          ├── Credit Note
          │
          └── Debit Note
```

---

# 15. Purchase Invoice and Creditor Relationship

```text
Party
  │
  └── Supplier / Creditor
          │
          ├── Purchase Invoice
          │       ├── Purchase Items
          │       ├── GST
          │       └── Due Date
          │
          ├── Payment
          │
          ├── Debit Note
          │
          └── Credit Note
```

---

# 16. Invoice Allocation

Payments should be capable of being allocated against specific invoices.

Example:

```text
Customer A

INV-001       ₹50,000
INV-002       ₹30,000
Receipt       ₹40,000
```

Allocation:

```text
INV-001       ₹40,000
INV-002            ₹0
```

Remaining:

```text
INV-001       ₹10,000
INV-002       ₹30,000
Total         ₹40,000
```

Recommended allocation table:

| Field | Description |
|---|---|
| allocation_id | Unique ID |
| party_id | Party |
| payment_id | Payment/receipt |
| invoice_id | Invoice |
| allocated_amount | Amount allocated |
| allocation_date | Date |

This is important for accurate outstanding and aging reports.

---

# 17. Advances

The software should support advances.

## Customer Advance

A customer pays before an invoice is generated.

```text
Bank Dr.             ₹20,000
    To Customer Advance    ₹20,000
```

Later, the advance can be adjusted against an invoice.

## Supplier Advance

The business pays a supplier before receiving the purchase invoice.

```text
Supplier Advance Dr. ₹20,000
    To Bank               ₹20,000
```

Later, it can be adjusted against the supplier invoice.

Do not force all advances into normal invoice outstanding logic.

---

# 18. Credit Notes and Debit Notes

Both debtor and creditor ledgers should support notes.

## Sales Side

```text
Sales Invoice
Credit Note
Debit Note
Receipt
```

## Purchase Side

```text
Purchase Invoice
Credit Note
Debit Note
Payment
```

Every note should reference its source document where applicable.

Recommended fields:

```text
note_id
party_id
note_number
note_date
note_type
reason
reference_invoice_id
taxable_amount
cgst
sgst
igst
cess
total_amount
```

---

# 19. Outstanding Reports

## Debtor Outstanding Report

Recommended columns:

```text
Customer
GSTIN
Invoice No.
Invoice Date
Due Date
Invoice Amount
Received
Credit Note
Debit Note
Outstanding
Days Outstanding
Ageing Bucket
```

## Creditor Outstanding Report

```text
Supplier
GSTIN
Invoice No.
Invoice Date
Due Date
Invoice Amount
Paid
Credit Note
Debit Note
Outstanding
Days Outstanding
Ageing Bucket
```

---

# 20. Aging Buckets

Recommended default buckets:

```text
Not Due
0–30 Days
31–60 Days
61–90 Days
91–180 Days
181–365 Days
Above 365 Days
```

The aging calculation should use:

```text
Days Outstanding = Current Date - Due Date
```

For overdue documents.

For invoices that are not yet due:

```text
Status = Not Due
```

---

# 21. Customer/Supplier Statement

The software should provide a ledger statement.

Example:

```text
Customer Statement
────────────────────────────────────────────
Date       Particular       Debit    Credit   Balance
01-08      Opening          25,000            25,000 Dr
05-08      INV-101          50,000            75,000 Dr
10-08      Receipt                    30,000  45,000 Dr
15-08      Credit Note                 5,000  40,000 Dr
────────────────────────────────────────────
Closing Balance                             ₹40,000 Dr
```

Supplier statements should use the corresponding creditor debit/credit logic.

---

# 22. GST-Relevant Transaction Fields

Party master should not attempt to replace invoice-level GST information.

Invoice-level GST data should include, as applicable:

```text
GSTIN
Place of Supply
Taxable Value
CGST
SGST/UTGST
IGST
CESS
GST Rate
HSN/SAC
Tax Category
Reverse Charge
ITC Eligibility
E-Invoice Details
E-Way Bill Details
```

The applicable fields and rules should be implemented according to the current GST rules and the transaction type.

---

# 23. Recommended Party Account Structure

A flexible chart-of-accounts relationship can be:

```text
Assets
└── Current Assets
    └── Sundry Debtors
        ├── Customer A
        ├── Customer B
        └── Customer C

Liabilities
└── Current Liabilities
    └── Sundry Creditors
        ├── Supplier A
        ├── Supplier B
        └── Supplier C
```

A party can be configured as:

```text
CUSTOMER
SUPPLIER
CUSTOMER_AND_SUPPLIER
```

This avoids creating duplicate party records when the same business is both a customer and supplier.

---

# 24. Recommended Database Architecture

A production implementation can use:

```text
parties
├── party_id
├── party_code
├── legal_name
├── trade_name
├── party_type
├── account_type
├── contact_person
├── mobile
├── email
├── status
└── timestamps

party_gst_details
├── party_gst_id
├── party_id
├── gstin
├── registration_type
├── gstin_status
├── pan
├── state_code
├── sez_status
├── reverse_charge_applicable
└── effective dates

party_addresses
├── address_id
├── party_id
├── address_type
├── address fields
└── state/state_code

party_bank_accounts
├── bank_account_id
├── party_id
├── account details
└── status

party_credit_terms
├── party_id
├── credit_limit
├── credit_days
├── payment_terms
└── default payment method

party_ledger_entries
├── ledger_entry_id
├── party_id
├── transaction_date
├── transaction_type
├── reference_id
├── debit
├── credit
├── due_date
└── narration

payment_allocations
├── allocation_id
├── party_id
├── payment_id
├── invoice_id
└── allocated_amount
```

---

# 25. Data Integrity Rules

The software should enforce:

1. Every party has a unique internal ID.
2. GSTIN should be normalized and validated when provided.
3. A registered GST party should have appropriate GST registration information.
4. A party may have multiple addresses.
5. A party may have multiple bank accounts.
6. Historical invoices retain their own party/GST snapshot.
7. Ledger balances are calculated from posted transactions.
8. Posted transactions should not be silently overwritten.
9. Corrections should normally be made through appropriate reversal/adjustment transactions.
10. Payments and receipts should support invoice allocation.
11. Advances should be separately identifiable.
12. Credit/debit notes should retain references to source documents where applicable.
13. Every ledger transaction should have an auditable source/reference.
14. Deleted parties should generally be soft-deleted/inactivated rather than physically deleted if they have accounting history.
15. Financial transactions should have an audit trail.

---

# 26. Minimum UI Sections

## Party Creation

```text
[ Basic Information ]

Party Code
Legal Name
Trade Name
Party Type
Customer / Supplier / Both

[ GST Information ]

GSTIN
Registration Type
PAN
State
State Code
SEZ Status
Reverse Charge

[ Address ]

Billing Address
Shipping Address

[ Contact ]

Contact Person
Mobile
Email

[ Bank ]

Bank Name
Account Number
IFSC
UPI ID

[ Accounting ]

Opening Balance
Debit / Credit
Credit Limit
Credit Days
Payment Terms

[ Save Party ]
```

---

# 27. Recommended Reports

The software should eventually provide:

### Debtor Reports

- Sundry Debtors Summary
- Customer Outstanding
- Invoice-wise Outstanding
- Customer Ledger
- Customer Statement
- Debtor Aging
- Overdue Receivables
- Customer Credit Limit Utilization
- Customer Receipts
- Customer Advances

### Creditor Reports

- Sundry Creditors Summary
- Supplier Outstanding
- Invoice-wise Payables
- Supplier Ledger
- Supplier Statement
- Creditor Aging
- Overdue Payables
- Supplier Payments
- Supplier Advances

### Combined

- Party Ledger
- Receivable/Payable Summary
- Outstanding by Due Date
- Aging Summary
- Party-wise GST transaction report
- Customer/Supplier transaction history

---

# 28. Recommended Design Principle

The most important architectural rule is:

```text
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
AGING / REPORTS
```

Do not make:

```text
Party.balance = manually editable
```

Instead:

```text
Opening Balance
+ Debit Ledger Entries
- Credit Ledger Entries
± Adjustments
= Calculated Balance
```

The exact debit/credit presentation depends on whether the party is operating as a debtor or creditor and on the accounting transaction.

---

# 29. Implementation Priority

For an initial GST billing application, implement in this order:

### Phase 1 — Party Master

- Basic details
- Customer/Supplier/Both
- GSTIN
- PAN
- Address
- Contact
- Opening balance

### Phase 2 — GST

- Registration type
- State/state code
- Place of supply
- GST validation
- GST transaction fields

### Phase 3 — Accounting

- Party ledger
- Debit/credit entries
- Opening balances
- Receipts
- Payments
- Credit notes
- Debit notes

### Phase 4 — Outstanding

- Invoice allocation
- Due dates
- Outstanding calculation
- Aging
- Customer/supplier statements

### Phase 5 — Compliance and Audit

- E-invoice integration where applicable
- E-way bill integration where applicable
- GST reports
- Audit trail
- Historical party/GST snapshots
- Financial-period controls

---

# 30. Final Recommendation

For a serious GST billing/accounting application, **Sundry Debtors and Sundry Creditors should share a common Party Master**, while their accounting behavior is determined by the party's ledger/account classification.

Use:

```text
Party
 ├── GST Details
 ├── Addresses
 ├── Contacts
 ├── Bank Accounts
 ├── Credit Terms
 ├── Accounting Classification
 └── Ledger
      ├── Invoices
      ├── Payments/Receipts
      ├── Credit/Debit Notes
      ├── Advances
      └── Adjustments
```

This structure supports GST billing now and can later be extended into a complete accounting system without redesigning the party architecture.

Yes. For your GST Billing application, I would make Phase 10 a reusable “Business Identity & GST Validation” module, rather than implementing GST validation separately on each customer, supplier, debtor, creditor, company, invoice, quotation, BOQ, etc. form.

Phase 10 — GSTIN Validation & Business Identity Module

10.1 Objective

Build one centralized, reusable GST validation component/service that can be imported anywhere in the application.

It should handle:

GSTIN structure validation

15-character restriction

GSTIN sequence/help display

GST state-code extraction

State/UT identification

PAN extraction

TAN/PAN field integration

Automatic field population

Invalid GSTIN feedback

Mobile country-code selection

Automatic country detection

Office contact number

Website

Company logo

Bank account type dropdown


The key architecture should be:

┌─────────────────────────┐
                    │ GST Identity Module     │
                    │                         │
                    │ GSTIN Validator         │
                    │ GST State Master        │
                    │ PAN Extractor            │
                    │ GSTIN Formatter         │
                    │ Validation Messages     │
                    └────────────┬────────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             │                   │                   │
       Customer Form       Supplier Form       Company Form
             │                   │                   │
             └───────────────────┼───────────────────┘
                                 │
                     Invoice / Quotation / BOQ

This prevents duplicated GST logic throughout the application.


---

10.2 Create a dedicated GST library/module

Create something similar to:

backend/
└── app/
    └── core/
        └── gst/
            ├── __init__.py
            ├── validator.py
            ├── parser.py
            ├── state_codes.py
            ├── constants.py
            ├── schemas.py
            └── exceptions.py

validator.py

Responsible for:

validate_gstin()
is_valid_gstin()
validate_gstin_checksum()
validate_gstin_structure()

parser.py

Responsible for extracting:

parse_gstin()
extract_state_code()
extract_state()
extract_pan()
extract_entity_number()

state_codes.py

Central GST state/UT master.

For example:

01 → Jammu & Kashmir
02 → Himachal Pradesh
03 → Punjab
...
29 → Karnataka
...
36 → Telangana
37 → Andhra Pradesh
38 → Ladakh

The application should never hard-code:

29 = Karnataka

in individual forms.

Instead:

GSTStateMaster.get_state("29")


---

10.3 GSTIN structure

The UI should explicitly teach the user what the number means.

Example:

GSTIN: 29ABCDE1234F1Z5

29        ABCDE1234F       1     Z     5
│         │                │     │     │
│         │                │     │     └─ Check digit
│         │                │     └────── Default character
│         │                └──────────── Entity number
│         └───────────────────────────── PAN
└─────────────────────────────────────── State code

Under the input box show:

> GSTIN format: 15 characters
Example: 29ABCDE1234F1Z5
State Code: 29 | PAN: ABCDE1234F | Entity: 1 | Default: Z | Check Digit: 5



This is useful because the user immediately understands what they are entering.


---

10.4 GSTIN input restriction

The GSTIN field should accept maximum 15 characters.

Recommended behavior:

maxlength = 15

But don't rely only on HTML.

The frontend should:

1. Remove unwanted whitespace.


2. Convert alphabetic characters to uppercase.


3. Reject characters outside the GSTIN character set.


4. Stop input after 15 characters.


5. Validate progressively.


6. Validate the complete GSTIN when 15 characters are entered.



Example:

User enters:

29abcde1234f1z5

Automatically becomes:

29ABCDE1234F1Z5

The input should display something like:

GSTIN
┌───────────────────────┐
│ 29ABCDE1234F1Z5       │
└───────────────────────┘
15 / 15
✓ Valid GSTIN


---

10.5 Progressive validation

Don't wait until form submission.

Validation should happen while entering.

0–14 characters

Show:

Enter a valid 15-character GSTIN

15 characters but invalid structure

Show:

✕ Invalid GSTIN format

Valid structure

Show:

✓ Valid GSTIN format

Valid GSTIN

Automatically populate:

State Code: 29
State: Karnataka
PAN: ABCDE1234F


---

10.6 Automatic extraction

For:

29ABCDE1234F1Z5

the parser returns:

{
  "gstin": "29ABCDE1234F1Z5",
  "state_code": "29",
  "state": "Karnataka",
  "pan": "ABCDE1234F",
  "entity_number": "1",
  "default_character": "Z",
  "check_digit": "5"
}

The frontend then automatically updates:

GSTIN
29ABCDE1234F1Z5

State Code
29

State
Karnataka

PAN/TAN
ABCDE1234F


---

10.7 PAN/TAN field

Your current form apparently doesn't have a dedicated PAN field.

Add:

PAN / TAN

However, I recommend not treating PAN and TAN as the same thing internally.

Use:

PAN
TAN

as separate database fields.

The UI can conditionally display them according to the business requirements.

For GSTIN:

GSTIN
29ABCDE1234F1Z5

↓ automatically

PAN
ABCDE1234F

Important

A GSTIN contains the PAN, not the TAN.

Therefore:

GSTIN → PAN

is automatic.

But:

GSTIN → TAN

is not possible because TAN isn't encoded in the GSTIN.

So don't label the automatically extracted value as PAN/TAN internally. It should be PAN.


---

10.8 Manual PAN behavior

If GSTIN is provided:

GSTIN = valid
        ↓
PAN = automatically extracted
        ↓
PAN field = populated
        ↓
PAN field = read-only

If GSTIN is not provided:

GSTIN = empty
        ↓
PAN field = manually editable

If GSTIN is subsequently removed:

GSTIN removed
       ↓
PAN becomes editable

This prevents users from accidentally entering a PAN that doesn't correspond to the GSTIN.


---

10.9 State field behavior

The same principle applies to State.

If GSTIN is valid:

GSTIN
   ↓
State Code
   ↓
State

Both should automatically populate.

For example:

GSTIN:       29ABCDE1234F1Z5
State Code:  29
State:       Karnataka

The state should preferably become read-only/locked while the GSTIN is valid.

This prevents:

GSTIN → Karnataka
State dropdown → Maharashtra

inconsistent data.


---

10.10 Bank Account Type dropdown

Change the current free-text account type field to a controlled dropdown.

Recommended values:

Savings Account
Current Account
Cash Credit Account
Overdraft Account
NRE Account
NRO Account
Other

Database should store a stable enum/code rather than arbitrary text.

Example:

CURRENT
SAVINGS
CASH_CREDIT
OVERDRAFT
NRE
NRO
OTHER

This will make future reporting much cleaner.


---

10.11 Mobile number country-code selector

Do not build your own country-code database.

Use an established international telephone-number library.

For the frontend, a good architecture is to use a library based on libphonenumber.

The component should provide:

🇮🇳 +91 | 9876543210

and support:

country flag

country name

dialing code

country selection

international formatting

validation

parsing

E.164 representation


Internally store the normalized number preferably as:

+919876543210

rather than storing:

country_code = +91
mobile = 9876543210

alone.

You can still store both components if your application needs them for display/search.


---

10.12 Automatic country detection

The selector can default based on the user's environment where possible.

Priority should be:

Explicit user selection
        ↓
Existing saved country
        ↓
Browser/device locale
        ↓
Application default

Don't blindly infer the country from the IP address and permanently save it.

For example, a user may be physically in India but entering a US business number.

Therefore:

Auto-detect → default suggestion
User selection → authoritative


---

10.13 Office contact number

Add:

Mobile Number *
Office Contact Number

Office contact should be optional.

Use the same international phone component/library.

Example:

Mobile
🇮🇳 +91 | 9876543210

Office Contact
🇮🇳 +91 | 08012345678


---

10.14 Website

Add:

Website

Example:

https://example.com

Validation should check that the value is a valid URL.

I would normalize:

example.com

to:

https://example.com

where appropriate, while preserving the user's actual URL in storage according to your application's policy.


---

10.15 Company logo

Add company logo upload.

Requirements:

Aspect ratio: 1:1
Display size: 1" × 1"

Important distinction:

1" × 1" is a physical print size, not a web pixel dimension.

Therefore don't store it as:

100px × 100px

alone.

Store a square image and render it at:

1 inch × 1 inch

in generated documents/PDFs.

Recommended upload requirements:

Aspect ratio: 1:1
Minimum resolution: 300 × 300 px
Recommended: 600 × 600 px
Format: PNG / JPEG / WebP

For invoices and other PDFs, a 300 DPI equivalent is preferable.

For example:

1 inch × 1 inch @ 300 DPI
=
300 × 300 pixels


---

10.16 Logo processing

Don't simply trust the uploaded dimensions.

The backend should:

Upload
  ↓
Validate MIME type
  ↓
Decode image
  ↓
Check dimensions
  ↓
Check aspect ratio
  ↓
Crop/resize if permitted
  ↓
Generate standardized square image
  ↓
Store

I recommend storing a standardized version such as:

company_logo.webp

or PNG if transparency is important.


---

10.17 Company/business master schema

The company/business profile should eventually contain something like:

Business
│
├── Legal Name
├── Trade Name
├── GSTIN
├── GST State Code
├── GST State
├── PAN
├── TAN
│
├── Mobile Number
├── Office Contact Number
├── Email
├── Website
│
├── Bank Details
│   ├── Bank Name
│   ├── Account Number
│   ├── IFSC
│   ├── Branch
│   └── Account Type
│
└── Branding
    └── Company Logo


---

10.18 Reusable frontend component

Instead of implementing this separately:

CustomerGSTInput
SupplierGSTInput
CompanyGSTInput
InvoiceGSTInput
QuotationGSTInput

create:

GSTINInput

with a reusable API.

Conceptually:

<GSTINInput
    value={gstin}
    onChange={handleGSTINChange}
    onValidated={handleGSTINValidated}
/>

Then any form can import it.

For example:

Company
Customer
Supplier
Debtor
Creditor
Quotation
BOQ
Invoice

all use the same component.


---

10.19 Reusable backend service

Likewise, don't duplicate backend validation.

Use:

GSTService

with operations conceptually like:

validate(gstin)

parse(gstin)

get_state(gstin)

extract_pan(gstin)

normalize(gstin)

Example result:

{
  "valid": true,
  "gstin": "29ABCDE1234F1Z5",
  "state_code": "29",
  "state": "Karnataka",
  "pan": "ABCDE1234F",
  "entity_number": "1"
}

Every backend module can consume this.


---

10.20 Important: structural validation vs government verification

Phase 10 should distinguish these two:

Level 1 — GSTIN structural validation

Can be performed locally:

15 characters
+
valid pattern
+
valid state code
+
PAN structure
+
entity character
+
Z position
+
checksum

Level 2 — Actual GST registration verification

This requires checking authoritative GST data/API/service.

A structurally valid GSTIN does not necessarily mean the GST registration is currently active.

Therefore the UI should eventually distinguish:

✓ Valid GSTIN format

from:

✓ GSTIN verified with GST system

Don't claim government verification merely because the checksum passes.


---

10.21 Database changes

Phase 10 should include a migration rather than modifying tables manually.

Likely fields:

gstin
gst_state_code
gst_state
pan
tan
mobile_country_code
mobile_number
office_country_code
office_contact_number
website
company_logo
bank_account_type

I would preferably normalize phone numbers into a canonical format and use a controlled enum for account type.


---

10.22 Form layout

A clean layout would be:

BUSINESS / COMPANY DETAILS

Legal Name
[________________________________________]

Trade Name
[________________________________________]

GSTIN
[ 29ABCDE1234F1Z5                 ] 15/15
✓ Valid GSTIN

29 | ABCDE1234F | 1 | Z | 5

State Code          State
[ 29 ]              [ Karnataka ]

PAN
[ ABCDE1234F ]  ← Automatically extracted

TAN
[____________]  ← Manual, if applicable


CONTACT DETAILS

Mobile Number
[ 🇮🇳 +91 ▼ ] [9876543210]

Office Contact Number (Optional)
[ 🇮🇳 +91 ▼ ] [08012345678]

Website
[ https://________________________ ]


BANK DETAILS

Bank Name
[________________________________]

Account Number
[________________________________]

IFSC
[________________]

Account Type
[ Current Account ▼ ]


BRANDING

Company Logo

       ┌─────────┐
       │         │
       │  LOGO   │  1" × 1"
       │         │
       └─────────┘

[ Upload Logo ]


---

10.23 Phase 10 implementation sequence

I recommend implementing it in this order:

10.1 — GST master

State/UT codes

State names

State/UT classification

Effective/legacy codes where necessary


10.2 — GSTIN parser

State code

PAN

entity number

default character

checksum digit


10.3 — GSTIN validator

length

character pattern

state code

PAN structure

checksum


10.4 — Reusable backend service

Create one importable GST service.

10.5 — Reusable frontend GSTIN component

Create one component used everywhere.

10.6 — GSTIN input UX

15-character limit

uppercase conversion

formatting

live validation

sequence explanation

success/error states


10.7 — Automatic extraction

GSTIN → state code → state → PAN.

10.8 — PAN/TAN

Add PAN

Add TAN

Automatically extract PAN from GSTIN

Keep TAN independent


10.9 — Bank account type

Replace free text with enum/dropdown.

10.10 — International phone component

Integrate an established libphonenumber-based library.

10.11 — Contact fields

Mobile

Office contact optional

Country selector


10.12 — Website

Add URL validation and normalization.

10.13 — Logo

Upload

1:1 validation/cropping

standardized storage

1" × 1" PDF rendering


10.14 — Database migration

Add all required fields safely.

10.15 — Integration

Use the same components/services in:

Company
Customer
Supplier
Debtor
Creditor
Invoice
Quotation
BOQ

10.16 — Testing

Test at minimum:

GSTIN < 15 characters
GSTIN > 15 characters
lowercase GSTIN
invalid state code
invalid PAN section
invalid Z position
invalid checksum
valid GSTIN
GSTIN → PAN extraction
GSTIN → state extraction
GSTIN removal
GSTIN replacement
mobile international numbers
invalid phone number
optional office number
invalid website
logo non-square
logo too small
bank account enum


---

One architectural decision I strongly recommend

Don't call this simply a GST validation feature.

Make Phase 10 a reusable:

BusinessIdentity / TaxIdentity module

with GST as its first tax identity implementation.

That gives you room later for:

GSTIN
PAN
TAN
CIN
LLPIN
Udyam Registration
IEC
FSSAI
Professional Tax

without rebuilding your business/customer/supplier forms.

For your existing GST Billing project, Phase 10 should therefore be completed before Phase 11 expands further into quotations/BOQ integrations, because quotations, BOQs, invoices, customers and suppliers will all benefit from the same centralized identity components.

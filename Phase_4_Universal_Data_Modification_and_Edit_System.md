# Phase 4 — Universal Data Modification & Edit System

## 1. Objective

Phase 4 introduces a centralized and reusable **Modification / Edit System** for all data-entry modules created in the previous phases.

The system must allow authorized users to safely modify data created in:

```text
Phase 1 → Company Account & Company Profile
Phase 2 → Units & Custom Unit Definitions
Phase 3 → Items / Products / Services / SKU
```

The modification system must be designed so that future phases can use the same architecture.

The key principle is:

```text
CREATE
   ↓
VIEW
   ↓
EDIT
   ↓
VALIDATE
   ↓
PREVIEW CHANGES
   ↓
SAVE
   ↓
AUDIT
   ↓
HISTORICAL DATA PROTECTED
```

The system must never allow a master-data modification to silently corrupt or rewrite historical accounting transactions.

---

# 2. Scope

The universal modification system covers:

```text
Company Profile
Company GST Details
Company Ownership
Company Address
Company Contact Details
Company Authorized Person
Company Logo
Company Bank Details

Units
Unit Names
Unit Symbols
Unit Codes
GST Unit Codes
Unit Categories
Conversion Factors
Conversion Formulas
Precision
Rounding Rules
Unit Aliases

Items
Item Name
Item Type
SKU
Unit
HSN/SAC
GST Applicability
GST Rate
Description
Item Status
```

It should also be extensible to:

```text
Customers
Suppliers
Invoices
Purchase Bills
Payments
Inventory
Tax Configuration
Accounting Masters
```

in future phases.

---

# 3. Universal Modification Architecture

All editable entities should follow the same lifecycle:

```text
Existing Record
      ↓
Open Edit
      ↓
Load Current Values
      ↓
User Changes Fields
      ↓
Detect Changed Fields
      ↓
Validate Changes
      ↓
Check Dependencies
      ↓
Check Historical Usage
      ↓
Show Change Preview
      ↓
User Confirms
      ↓
Save
      ↓
Create Audit Record
      ↓
Create New Version if Required
      ↓
Return Updated Record
```

---

# 4. Modification Modal

Every master-data page should provide:

```text
[ Edit ]
```

When clicked:

```text
┌───────────────────────────────────────────────────────────┐
│                 EDIT ITEM                                 │
├───────────────────────────────────────────────────────────┤
│                                                           │
│ Item Name *                                               │
│ [ 500ml Mineral Water Bottle________________________ ]    │
│                                                           │
│ Unit                                                       │
│ [ PCS ▼ ]                                                 │
│                                                           │
│ SKU                                                        │
│ [ WTR-500ML-001____________________________________ ]    │
│                                                           │
│ HSN/SAC                                                    │
│ [ XXXXXX____________________________________________ ]    │
│                                                           │
│ GST Applicable                                             │
│ [ Yes ▼ ]                                                 │
│                                                           │
│ GST Rate                                                   │
│ [ 18% ▼ ]                                                 │
│                                                           │
│ Description                                                │
│ [_______________________________________________]         │
│                                                           │
│ Changed fields: 3                                         │
│                                                           │
│                 [Cancel] [Preview Changes]                │
└───────────────────────────────────────────────────────────┘
```

The same component should be reusable for:

```text
Company
Unit
Item
Future entities
```

---

# 5. Edit vs. Update vs. Delete

The system must clearly distinguish:

```text
EDIT
```

from:

```text
DEACTIVATE
```

and:

```text
DELETE
```

and:

```text
ARCHIVE
```

Recommended behavior:

### Edit

Changes current master data.

```text
Item Name
Description
SKU
Default GST
```

### Deactivate

Prevents new transactions from using the record while preserving history.

```text
ACTIVE → INACTIVE
```

### Archive

Removes the record from normal active views while preserving history.

```text
ACTIVE → ARCHIVED
```

### Delete

Physical deletion should be restricted.

If the record has transaction references:

```text
DELETE = NOT ALLOWED
```

Use:

```text
DEACTIVATE
```

instead.

---

# 6. Changed Field Detection

The system must identify exactly what the user changed.

Example:

```text
Before

Item Name:
500ml Mineral Water Bottle

GST Rate:
18%

Description:
Packaged drinking water.
```

After:

```text
Item Name:
500ml Premium Mineral Water Bottle

GST Rate:
12%

Description:
Premium packaged drinking water.
```

Change detection:

```text
CHANGED

Item Name
18% → 12%
Description
```

The system should not create unnecessary audit entries for unchanged fields.

---

# 7. Change Preview

Before saving important modifications, display a change summary.

Example:

```text
┌────────────────────────────────────────────────────────────┐
│                    REVIEW CHANGES                         │
├────────────────────────────────────────────────────────────┤
│ Field             Previous              New                │
├────────────────────────────────────────────────────────────┤
│ Item Name         Water Bottle          Premium Water     │
│ GST Rate          18%                   12%               │
│ Description       Old description       New description   │
└────────────────────────────────────────────────────────────┘

These changes will affect future transactions only.

[Cancel]                              [Confirm Changes]
```

For changes affecting historical accounting records, the system should explain that historical transactions remain unchanged.

---

# 8. Modification Categories

Each modification should be classified.

```text
NON_CRITICAL
CONFIGURATION
TAX_RELATED
IDENTITY
FINANCIAL
SECURITY
STRUCTURAL
```

Examples:

```text
Description change
→ NON_CRITICAL

GST rate change
→ TAX_RELATED

Company GSTIN change
→ IDENTITY / TAX_RELATED

Bank account change
→ FINANCIAL

Login PIN change
→ SECURITY

Unit conversion change
→ STRUCTURAL
```

This classification determines whether additional confirmation or authorization is required.

---

# 9. Phase 1 — Company Profile Modification

Company profile fields:

```text
Company Name
Ownership Type
GSTIN
Address
Mobile Number
Office Number
Email
Authorized Person
Logo
Bank Details
```

The edit system must support modification of all these fields.

---

# 10. Company Name Modification

Example:

```text
Old:
ABC Enterprises

New:
ABC Enterprises Private Limited
```

Before saving:

```text
Confirm Company Name Change
```

The change should be recorded in the audit log.

Historical invoices should preserve the company information that was applicable when they were issued.

---

# 11. Ownership Type Modification

Supported examples:

```text
Proprietor
Sole Proprietorship
Partnership
LLP
Private Limited
Public Limited
Company
Trust
Society
Other
```

Changing ownership type may be legally significant.

Therefore:

```text
Ownership Type Change
→ Enhanced confirmation
→ Audit entry
```

The system should not automatically infer legal consequences from the selection.

---

# 12. GSTIN Modification

GSTIN is a high-impact field.

The system should not allow a simple blind overwrite.

Workflow:

```text
Edit GSTIN
      ↓
Validate 15-character format
      ↓
Extract GSTIN components
      ↓
Validate checksum
      ↓
Compare extracted PAN/state
      ↓
Show extracted information
      ↓
Confirm
      ↓
Save
```

The GSTIN should be treated as a sensitive tax-identity field.

---

# 13. GSTIN Change Protection

If the company already has:

```text
Invoices
Purchase Bills
GST Reports
Tax Transactions
```

changing GSTIN may have significant accounting implications.

The application should display:

```text
Warning

This company already contains historical tax transactions.

Changing the GSTIN will apply to future company data only.
Historical transactions will retain their original GSTIN snapshot.

Do you want to continue?
```

Recommended:

```text
Old GSTIN
New GSTIN
Effective Date
Reason
Authorized By
```

---

# 14. GSTIN Change History

Store:

```text
company_tax_identity_history
├── history_id
├── company_id
├── old_gstin
├── new_gstin
├── effective_from
├── reason
├── changed_by
├── changed_at
└── status
```

This prevents loss of historical tax identity.

---

# 15. Company Address Modification

Editable:

```text
Address Line 1
Address Line 2
City
District
State
PIN Code
Country
```

The system should support:

```text
Registered Address
Business Address
Billing Address
Shipping Address
```

in future.

Changing the address must not rewrite previously issued invoices.

---

# 16. Company Contact Modification

Editable:

```text
Mobile
Office Phone
Email
Website
```

Important contact changes should be audited.

Email format should be validated.

Phone number should be normalized according to the application's supported country/region.

---

# 17. Authorized Person Modification

Fields:

```text
Name
Designation
Contact Number
Email
```

Optional future fields:

```text
DIN
PAN
Signature
Authorization Type
```

Changing the authorized person should create an audit event.

---

# 18. Company Logo Modification

The company logo should support:

```text
Upload
Replace
Remove
Preview
```

Recommended image behavior:

```text
Preferred display:
1 inch × 1 inch

Default aspect ratio:
1:1
```

If the uploaded image is not square:

```text
Upload
 ↓
Preview
 ↓
Crop to 1:1
 ↓
Resize
 ↓
Optimize
 ↓
Save
```

Do not stretch the logo.

---

# 19. Bank Details Modification

Company bank details may include:

```text
Account Holder Name
Account Number
IFSC
Bank Name
Branch
```

Recommended additional fields:

```text
Account Type
UPI ID
SWIFT/BIC
```

future only.

---

# 20. Bank Account Security

Bank account modifications should be classified as:

```text
FINANCIAL
```

Before changing:

```text
Old Account
New Account
```

display a confirmation.

Do not expose the full account number unnecessarily in logs.

Example audit display:

```text
XXXXXX1234
→
XXXXXX7890
```

instead of storing/displaying the full number in normal audit screens.

---

# 21. Phase 2 — Unit Modification

Unit fields that may be modified:

```text
Unit Name
Symbol
Internal Code
GST Unit Code
Category
Base Unit
Conversion Factor
Conversion Formula
Precision
Rounding Mode
Aliases
Status
```

Unit modifications require special historical protection.

---

# 22. Unit Name Modification

Example:

```text
Old:
Box

New:
Carton
```

This should not change the meaning of historical invoice units.

Historical invoices should retain:

```text
Old Unit Name
Old Symbol
Old Code
```

through transaction snapshots.

---

# 23. Unit Symbol Modification

Example:

```text
Old:
BOX

New:
CTN
```

The system should check:

```text
Symbol uniqueness
Existing product usage
Invoice usage
Formula references
```

before saving.

---

# 24. Unit Conversion Modification

This is a high-impact modification.

Example:

```text
Before:

1 BOX = 12 PCS

After:

1 BOX = 24 PCS
```

The system must never silently recalculate historical inventory or invoices.

Recommended behavior:

```text
Existing Unit Version
        ↓
Close Version
        ↓
Create New Unit Version
        ↓
New Conversion Effective Date
        ↓
Future transactions use new version
```

---

# 25. Unit Formula Modification

Example:

```text
Old:
=12*PCS

New:
=24*PCS
```

Workflow:

```text
Edit Formula
      ↓
Parse
      ↓
Validate
      ↓
Dimensional Analysis
      ↓
Dependency Check
      ↓
Test Conversion
      ↓
Show Before/After
      ↓
Confirm
      ↓
Create New Unit Version
```

---

# 26. Unit Dependency Check

Before modifying a unit, identify dependencies.

Example:

```text
BOX
 │
 ├── Product A
 ├── Product B
 ├── CARTON
 └── PALLET
```

Display:

```text
This unit is referenced by:

Products: 27
Other Units: 4
Invoices: 1,245
Inventory Transactions: 4,831
```

This gives the user context before making a structural change.

---

# 27. GST Unit Code Modification

Changing a GST unit code should require validation against the configured GST unit master.

Do not permit arbitrary invalid codes where GST reporting requires a recognized code.

Workflow:

```text
New GST Unit Code
      ↓
Lookup
      ↓
Validate
      ↓
Confirm
      ↓
Version
```

---

# 28. Unit Alias Modification

Users can:

```text
Add Alias
Edit Alias
Remove Alias
```

Example:

```text
Kilogram

Aliases:
kg
kgs
kilo
kilogram
```

Removing an alias should not affect the unit itself.

---

# 29. Phase 3 — Item Modification

Item fields:

```text
Item Type
Item Name
Unit
SKU
HSN/SAC
GST Applicable
GST Rate
Description
Status
```

---

# 30. Item Name Modification

Example:

```text
Old:
Water Bottle 500ml

New:
Premium Water Bottle 500ml
```

The item ID remains unchanged.

Historical invoices preserve the old item name through invoice snapshots.

Future invoices use the new name.

---

# 31. SKU Modification

SKU changes should be checked for uniqueness.

Workflow:

```text
Enter New SKU
      ↓
Normalize
      ↓
Check Company Uniqueness
      ↓
Check Barcode / External References
      ↓
Confirm
      ↓
Save
```

Old SKU should be retained in the audit history.

Optional future feature:

```text
SKU History
```

Example:

```text
SKU History

OLD-001
2026-01-01 → 2026-08-10

NEW-001
2026-08-10 → Present
```

---

# 32. Item Unit Modification

Changing an item's unit is potentially an inventory-impacting change.

Example:

```text
Before:
PCS

After:
BOX
```

Before allowing the change, check:

```text
Current Stock
Open Orders
Open Purchase Orders
Open Sales Orders
Historical Transactions
Product Unit Conversions
```

If inventory exists, the application should require an explicit conversion or stock-adjustment workflow.

---

# 33. Item HSN/SAC Modification

Changing HSN/SAC is a tax-classification change.

Workflow:

```text
New HSN/SAC
      ↓
Validate Code
      ↓
Show Classification
      ↓
Show Current GST Rate
      ↓
Confirm
      ↓
Audit
      ↓
Future transactions use new classification
```

Historical invoices remain unchanged.

---

# 34. Item GST Rate Modification

Example:

```text
Old:
18%

New:
12%
```

The item master should treat this as:

```text
Default GST Rate Change
```

not as an instruction to rewrite historical invoices.

Workflow:

```text
Current GST Rate
      ↓
New GST Rate
      ↓
Effective Date
      ↓
Confirmation
      ↓
New Item Version
```

---

# 35. GST Rate Change Preview

Example:

```text
GST RATE CHANGE

Item:
Water Bottle

Previous:
18%

New:
12%

Effective:
01-09-2026

Historical invoices:
UNCHANGED

Future transactions:
12%
```

---

# 36. Item Description Modification

Description changes are generally low risk.

Example:

```text
Old:
500ml packaged drinking water.

New:
Premium 500ml packaged drinking water.
```

Save immediately after normal validation.

Historical invoices should preserve their original description.

---

# 37. Modification Permissions

The system should support role-based permissions.

Recommended permissions:

```text
COMPANY_VIEW
COMPANY_EDIT

COMPANY_GST_EDIT
COMPANY_BANK_EDIT
COMPANY_LOGO_EDIT

UNIT_VIEW
UNIT_CREATE
UNIT_EDIT
UNIT_DEACTIVATE

UNIT_FORMULA_EDIT
UNIT_GST_CODE_EDIT

ITEM_VIEW
ITEM_CREATE
ITEM_EDIT
ITEM_DEACTIVATE

ITEM_SKU_EDIT
ITEM_HSN_EDIT
ITEM_GST_EDIT
```

---

# 38. Sensitive Modification Authorization

Certain fields should optionally require elevated authorization:

```text
GSTIN
Bank Account
IFSC
GST Rate
HSN/SAC
Unit Conversion
Login PIN
```

Possible workflow:

```text
User Requests Change
      ↓
Permission Check
      ↓
Additional PIN / Admin Authorization
      ↓
Change Preview
      ↓
Confirm
      ↓
Audit
```

---

# 39. Maker-Checker Model — Future Extension

For higher-security deployments:

```text
Maker
  ↓
Creates Change Request
  ↓
Checker
  ↓
Reviews
  ↓
Approves / Rejects
```

Recommended for:

```text
GSTIN
Bank Account
Tax Configuration
GST Rates
High-impact Unit Conversion
```

---

# 40. Unsaved Changes Protection

If the user modifies a form and attempts to close it:

```text
┌──────────────────────────────────────────────┐
│ Unsaved Changes                              │
├──────────────────────────────────────────────┤
│ You have unsaved changes.                    │
│                                              │
│ [Discard] [Continue Editing] [Save]         │
└──────────────────────────────────────────────┘
```

Never silently discard changes.

---

# 41. Optimistic Concurrency Protection

The system should detect if another session changed the same record.

Example:

```text
User A opens Item
       ↓
User B edits Item
       ↓
User A tries to save old version
```

The system should respond:

```text
This record was modified by another session.

Current version:
Version 8

Your version:
Version 7

Review the latest changes before saving.
```

Recommended field:

```text
version_number
```

or:

```text
updated_at
```

with proper concurrency control.

---

# 42. Partial Update

The backend should support partial updates where appropriate.

Example:

```text
PATCH /api/items/{id}
```

Request:

```json
{
  "description": "Updated description"
}
```

Only the intended field should change.

The backend must still perform full authorization and validation.

---

# 43. Full Replacement

Use:

```text
PUT
```

when the API intentionally replaces the complete editable representation.

Do not use `PUT` or `PATCH` as a way to bypass field-level validation.

---

# 44. Audit Trail

Every successful modification should create an audit record.

Recommended table:

```text
audit_logs
├── audit_id
├── company_id
├── entity_type
├── entity_id
├── action
├── field_name
├── old_value
├── new_value
├── changed_by
├── changed_at
├── reason
├── source
└── metadata
```

Example:

```text
Entity:
ITEM

Entity ID:
ITEM-001

Action:
UPDATE

Field:
GST_RATE

Old:
18%

New:
12%

Changed By:
Admin

Changed At:
2026-08-10 15:30
```

---

# 45. Audit Log Rules

Audit records should be:

```text
Append-only
```

Normal users should not be able to edit or delete audit records.

Only authorized system administrators should have access to audit maintenance operations, if any are required.

---

# 46. Before/After Audit View

The UI should display:

```text
Change History

10 Aug 2026 15:30
Admin

GST Rate
18% → 12%

10 Aug 2026 15:29
Admin

Description
Old description → New description
```

For structured values:

```text
Bank Account
XXXXXX1234
→
XXXXXX7890
```

Sensitive values should be masked.

---

# 47. Reason for Modification

For high-impact changes, require a reason.

Example:

```text
Reason for Change *

[ GST rate revised according to updated tax classification. ]
```

Recommended for:

```text
GSTIN
HSN/SAC
GST Rate
Bank Details
Unit Formula
Unit Conversion
```

---

# 48. Effective Date

Some modifications should support an effective date.

Example:

```text
GST Rate:
18%

New GST Rate:
12%

Effective From:
01-09-2026
```

The system should prevent an effective date that conflicts with already finalized transaction periods unless an authorized correction process is used.

---

# 49. Future-Dated Changes

Future-dated modifications can be represented as:

```text
Current Version
      │
      ├── Valid Until: 31-08-2026
      │
      ↓
Future Version
      │
      └── Effective From: 01-09-2026
```

This is especially useful for:

```text
GST rates
Item tax classification
Unit conversion
Pricing
```

---

# 50. Versioning Strategy

Recommended general model:

```text
MASTER RECORD
      │
      ├── Version 1
      ├── Version 2
      ├── Version 3
      └── Current Version
```

Each version should contain:

```text
version_id
entity_id
version_number
valid_from
valid_to
created_by
created_at
data_snapshot
```

Not every harmless field change requires a full version table, but tax, unit, and historical-accounting-impact fields should be versioned.

---

# 51. Historical Transaction Protection

This is one of the most important requirements.

Never perform:

```text
UPDATE all historical invoices
```

when a master record changes.

Example:

```text
Item Master

GST:
18% → 12%
```

Do NOT:

```text
UPDATE invoice_lines
SET gst_rate = 12
WHERE item_id = ...
```

Instead:

```text
Item Master
    ↓
New Default GST = 12%

Historical Invoice
    ↓
GST remains 18%

New Invoice
    ↓
GST = 12%
```

---

# 52. Transaction Snapshot Principle

When a transaction is created, copy required master information into the transaction.

Example:

```text
invoice_lines

item_id
item_name_snapshot
sku_snapshot
unit_id
unit_name_snapshot
hsn_sac_snapshot
gst_rate_snapshot
description_snapshot
```

This ensures historical accuracy.

---

# 53. Modification Dependency Graph

Before saving a modification, the system should determine:

```text
Entity
  ↓
Dependencies
  ↓
Historical Usage
  ↓
Open Transactions
  ↓
Current Stock
  ↓
Tax Reports
  ↓
Impact Level
```

Example:

```text
Change Item Unit
      ↓
Products using unit
      ↓
Inventory
      ↓
Open invoices
      ↓
Purchase orders
      ↓
Impact = HIGH
```

---

# 54. Impact Levels

Every modification should be classified as:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Examples:

### LOW

```text
Description
Alias
Display name
```

### MEDIUM

```text
SKU
Logo
Contact details
```

### HIGH

```text
Unit
HSN/SAC
GST Rate
Bank Details
```

### CRITICAL

```text
GSTIN
Company identity
Login PIN
Security credentials
```

---

# 55. Modification Confirmation

For low-risk fields:

```text
[Save]
```

For high-risk fields:

```text
[Review Changes]
      ↓
[Confirm]
```

For critical fields:

```text
[Review]
      ↓
[Authorization]
      ↓
[Reason]
      ↓
[Confirm]
```

---

# 56. Modification History Page

Each entity should have:

```text
[ View History ]
```

Example:

```text
ITEM HISTORY

Version 4 — Current
10 Aug 2026

GST:
12%

HSN:
XXXX

Version 3
01 Jul 2026

GST:
18%

Version 2
01 Jan 2026

GST:
18%
```

---

# 57. Restore Previous Version

For master data, authorized users may be allowed to restore a previous version.

However:

```text
RESTORE ≠ rewrite history
```

Restoration should create a new version.

Example:

```text
Version 1
Version 2
Version 3
Version 4 Current

Restore Version 2

Result:

Version 5
= values copied from Version 2
```

Do not delete Versions 3 and 4.

---

# 58. Modification API Architecture

Generic API pattern:

```text
GET    /api/{entity}
GET    /api/{entity}/{id}
PATCH  /api/{entity}/{id}
GET    /api/{entity}/{id}/history
POST   /api/{entity}/{id}/restore
POST   /api/{entity}/{id}/deactivate
POST   /api/{entity}/{id}/activate
```

Entity-specific APIs may be used where business logic is complex.

---

# 59. Change Preview API

Recommended:

```text
POST /api/{entity}/{id}/preview-update
```

Input:

```json
{
  "changes": {
    "gst_rate_id": "gst-12",
    "description": "Updated description"
  }
}
```

Response:

```json
{
  "impact": "HIGH",
  "requires_confirmation": true,
  "requires_reason": true,
  "requires_authorization": false,
  "historical_transactions_affected": false,
  "changes": [
    {
      "field": "gst_rate",
      "old": "18%",
      "new": "12%"
    }
  ]
}
```

---

# 60. Modification Transaction

A modification should be saved atomically.

Recommended:

```text
BEGIN TRANSACTION

Validate
↓
Check Permissions
↓
Check Dependencies
↓
Update Master
↓
Create Version
↓
Create Audit Log
↓
Commit

OR

Rollback everything
```

Never allow:

```text
Master updated
but
Audit failed
```

without handling the failure appropriately.

---

# 61. Validation Error Handling

Validation errors should identify the exact field.

Example:

```text
SKU Code

This SKU already exists for this company.
```

Example:

```text
GST Rate

GST rate is required when GST is applicable.
```

Example:

```text
Unit Formula

Circular dependency detected:
BOX → CARTON → BOX
```

---

# 62. API Error Format

Use a consistent structure.

Example:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more fields are invalid.",
    "fields": {
      "sku_code": "SKU already exists.",
      "gst_rate_id": "GST rate is required."
    }
  }
}
```

Recommended error codes:

```text
VALIDATION_ERROR
PERMISSION_DENIED
NOT_FOUND
CONFLICT
VERSION_CONFLICT
DEPENDENCY_CONFLICT
HISTORICAL_USAGE
AUTHORIZATION_REQUIRED
INVALID_STATE
```

---

# 63. Concurrent Modification

Use optimistic locking.

Recommended database field:

```text
version INTEGER NOT NULL DEFAULT 1
```

Update:

```text
UPDATE items
SET ...
version = version + 1
WHERE item_id = ?
AND version = ?
```

If zero rows are updated:

```text
VERSION_CONFLICT
```

Return:

```text
The record was modified by another user/session.
Please reload the latest version.
```

---

# 64. Security Requirements

All modification APIs must:

```text
Authenticate
↓
Identify company
↓
Authorize user
↓
Validate ownership
↓
Validate input
↓
Validate dependencies
↓
Save atomically
↓
Audit
```

Never trust:

```text
company_id
user_id
role
```

provided directly by the client without server-side verification.

---

# 65. Multi-Company Isolation

A user may potentially have access to multiple companies.

Every modification must verify:

```text
authenticated_user
        ↓
company_membership
        ↓
permission
        ↓
entity.company_id
```

Example:

```text
User belongs to Company A

Request:
PATCH /api/items/ITEM-BELONGING-TO-COMPANY-B
```

Response:

```text
NOT_FOUND
```

or an appropriately non-disclosing authorization response.

Do not leak another company's records.

---

# 66. Data Entry Drafts

Future enhancement:

```text
Save as Draft
```

This is useful for large company profiles or complicated unit/item configurations.

Example:

```text
DRAFT
↓
Validate
↓
Submit
↓
ACTIVE
```

Draft data should not be used in finalized invoices.

---

# 67. Undo vs. Restore

The application should distinguish:

```text
Undo
```

from:

```text
Restore Previous Version
```

Undo is a UI-level action before saving.

Restore is a database-level creation of a new version based on historical data.

Example:

```text
Before Save:
Undo changes

After Save:
Restore previous version
```

---

# 68. Bulk Modification

Future support should allow bulk updates.

Example:

```text
Select 25 Items
      ↓
Change GST Rate
      ↓
Preview 25 Changes
      ↓
Validate
      ↓
Confirm
      ↓
Create 25 Audit Records
```

Bulk modifications should never bypass individual validation.

---

# 69. Import Modification

For Excel/CSV imports:

```text
Upload
↓
Map Columns
↓
Compare Existing Records
↓
Show:
CREATE
UPDATE
UNCHANGED
ERROR
↓
Preview
↓
Confirm
↓
Transaction
↓
Audit
```

Example:

```text
SKU      Item           GST
001      Product A      18% → UPDATE
002      Product B      12% → UNCHANGED
003      Product C      5%  → CREATE
```

---

# 70. Modification Dashboard

A future dashboard can show:

```text
Recent Changes

Today
────────────────────────────────────
GSTIN changed              1
Items modified            18
Units modified             4
GST rates changed          3
Bank details changed       1

Pending Approvals
────────────────────────────────────
GSTIN changes              1
Bank changes               1
```

---

# 71. Recommended Database Architecture

Common master fields:

```text
created_at
created_by
updated_at
updated_by
version
status
```

Company:

```text
companies
company_versions
company_tax_identity_history
company_bank_accounts
```

Units:

```text
units
unit_versions
unit_aliases
```

Items:

```text
items
item_versions
```

Audit:

```text
audit_logs
```

---

# 72. Recommended Common Edit Component

Frontend architecture should provide a reusable component:

```text
<EditEntityModal />
```

with configuration:

```text
entity
fields
validation
permissions
impactRules
dependencyCheck
preview
save
audit
```

Example:

```text
EditEntityModal
        │
        ├── Company Configuration
        ├── Unit Configuration
        ├── Item Configuration
        └── Future Entity Configuration
```

This prevents creating a separate edit implementation for every master.

---

# 73. Field Configuration Model

Example:

```json
{
  "field": "gst_rate_id",
  "label": "GST Rate",
  "type": "select",
  "required": true,
  "impact": "HIGH",
  "requires_reason": true,
  "requires_confirmation": true
}
```

Another:

```json
{
  "field": "description",
  "label": "Description",
  "type": "textarea",
  "required": false,
  "impact": "LOW"
}
```

This allows the frontend to generate consistent forms.

---

# 74. Modification Rule Engine

A reusable rule engine should determine:

```text
Can Edit?
Requires Confirmation?
Requires Reason?
Requires Authorization?
Requires Version?
Requires Dependency Check?
Requires Effective Date?
```

Example:

```text
Field:
GSTIN

Can Edit:
YES

Confirmation:
YES

Reason:
YES

Authorization:
YES

Version:
YES

Historical Check:
YES
```

---

# 75. Complete Phase 4 Workflow

```text
USER OPENS RECORD
        ↓
CLICK EDIT
        ↓
LOAD CURRENT VERSION
        ↓
USER MODIFIES DATA
        ↓
CHANGE DETECTION
        ↓
FIELD VALIDATION
        ↓
PERMISSION CHECK
        ↓
DEPENDENCY CHECK
        ↓
HISTORICAL USAGE CHECK
        ↓
IMPACT CLASSIFICATION
        ↓
CHANGE PREVIEW
        ↓
REASON / AUTHORIZATION
        ↓
CONCURRENCY CHECK
        ↓
DATABASE TRANSACTION
        ↓
UPDATE MASTER
        ↓
CREATE VERSION
        ↓
CREATE AUDIT LOG
        ↓
COMMIT
        ↓
RETURN UPDATED RECORD
```

---

# 76. Example — Complete Item GST Modification

Current:

```text
Item:
Water Bottle

SKU:
WTR-500ML-001

GST:
18%

HSN:
XXXX
```

User clicks:

```text
Edit
```

Changes:

```text
GST:
18% → 12%
```

System:

```text
1. Detect GST change
2. Classify as HIGH impact
3. Validate 12% GST rate
4. Check HSN/SAC
5. Check active transactions
6. Display impact
7. Ask reason
8. Confirm
9. Create new item version
10. Keep old version
11. Update current default
12. Create audit log
```

Result:

```text
Current Item:
GST = 12%

Historical Invoice:
GST = 18%
```

---

# 77. Example — Complete Unit Conversion Modification

Current:

```text
BOX

1 BOX = 12 PCS
```

User changes:

```text
1 BOX = 24 PCS
```

System:

```text
Validate formula
        ↓
Check dependency graph
        ↓
Check product usage
        ↓
Check inventory
        ↓
Check open transactions
        ↓
Show impact
        ↓
Require confirmation
        ↓
Create Unit Version 2
```

Result:

```text
Version 1:
1 BOX = 12 PCS

Version 2:
1 BOX = 24 PCS
```

Historical transactions remain linked to their original conversion context.

---

# 78. Example — Company Bank Change

Current:

```text
Account:
XXXXXX1234

IFSC:
OLDXXXX
```

New:

```text
Account:
XXXXXX7890

IFSC:
NEWXXXX
```

System:

```text
Impact:
CRITICAL / FINANCIAL

Require:
Authorization
Reason
Confirmation
Audit
```

Historical invoices retain their original bank/payment information snapshot where applicable.

---

# 79. Example — Company Logo Change

Current:

```text
logo-v1.png
```

User uploads:

```text
logo-v2.png
```

System:

```text
Validate file
↓
Validate MIME type
↓
Validate dimensions
↓
Crop/resize to 1:1
↓
Optimize
↓
Store
↓
Create audit record
```

Old logo can optionally remain available for historical document rendering.

---

# 80. Phase 4 Completion Criteria

Phase 4 is complete when the system supports:

```text
1. Universal Edit Modal
2. Company Profile Editing
3. Company GSTIN Editing
4. Company Address Editing
5. Company Contact Editing
6. Authorized Person Editing
7. Logo Replacement
8. Bank Detail Editing

9. Unit Editing
10. Unit Formula Editing
11. Unit Conversion Versioning
12. Unit Alias Editing
13. GST Unit Code Validation

14. Item Editing
15. SKU Editing
16. HSN/SAC Editing
17. GST Rate Editing
18. Description Editing
19. Unit Assignment Editing

20. Changed Field Detection
21. Change Preview
22. Impact Classification
23. Dependency Checking
24. Permission Checking
25. Reason for High-Impact Changes
26. Authorization Support
27. Optimistic Concurrency
28. Versioning
29. Audit Trail
30. Historical Transaction Protection
31. Deactivation
32. Archiving
33. Restore-as-New-Version
34. Consistent API Error Handling
35. Multi-Company Isolation
36. Atomic Database Transactions
```

---

# 81. Final Architecture

```text
                       MASTER DATA
                            │
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
     COMPANY              UNITS               ITEMS
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ↓
                   UNIVERSAL EDIT ENGINE
                            │
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
      Validation        Dependency          Permission
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ↓
                     Change Detection
                            ↓
                     Impact Analysis
                            ↓
                    Change Preview
                            ↓
              ┌─────────────┴─────────────┐
              ↓                           ↓
        Normal Change               High-Risk Change
              │                           │
              │                    Reason + Authorization
              │                           │
              └─────────────┬─────────────┘
                            ↓
                     Version Creation
                            ↓
                     Master Update
                            ↓
                       Audit Log
                            ↓
                    Historical Data
                       Protected
```

---

# 82. Core Design Rule

The universal modification system must follow one fundamental accounting principle:

```text
MASTER DATA CAN CHANGE.
HISTORICAL TRANSACTIONS MUST NOT CHANGE SILENTLY.
```

Therefore:

```text
Current Master
     ↓
Can be edited

Historical Transaction
     ↓
Immutable snapshot
```

For high-impact master-data changes:

```text
Old Version
     ↓
New Version
     ↓
Effective Date
     ↓
Future Transactions
```

This architecture allows the GST billing application to remain flexible while preserving the integrity, traceability, and auditability required for accounting and tax records.

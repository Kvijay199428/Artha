# Phase 3 — Item / SKU Product Entry Modal

## 1. Objective

Phase 3 introduces the **Item / SKU Product Entry** system for the GST billing and accounting application.

The purpose of this phase is to provide a dedicated modal for creating and managing products and services that can later be used in:

- Sales invoices
- Purchase bills
- Quotations
- Estimates
- Inventory
- Stock movements
- GST reporting
- Customer orders
- Supplier orders
- Reports

The item entry system should support both:

```text
GOODS / PRODUCTS
```

and

```text
SERVICES
```

The primary workflow is:

```text
Product / Service
       ↓
[ + Add Item ]
       ↓
Item Entry Modal
       ↓
Enter Item Details
       ↓
Select Unit
       ↓
Enter SKU
       ↓
Enter HSN/SAC
       ↓
Select GST Applicability
       ↓
Select GST Rate
       ↓
Add Description
       ↓
Validate
       ↓
Save Item
       ↓
Item Available in Sales/Purchase/Inventory
```

---

# 2. Item Entry Modal

The application should provide a dedicated modal for adding an item.

Example:

```text
┌─────────────────────────────────────────────────────────┐
│                    ADD ITEM                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Item Type                                               │
│ [ Product ▼ ]                                           │
│                                                         │
│ Item Name *                                              │
│ [_______________________________________________]       │
│                                                         │
│ Unit *                                                   │
│ [ PCS ▼ ]                           [ + Add Unit ]      │
│                                                         │
│ SKU Code                                                 │
│ [_______________________________________________]       │
│                                                         │
│ HSN / SAC Code                                           │
│ [_______________________________________________]       │
│                                                         │
│ GST Applicable                                           │
│ [ Yes ▼ ]                                               │
│                                                         │
│ GST Rate                                                 │
│ [ 18% ▼ ]                                               │
│                                                         │
│ Description                                              │
│ [_______________________________________________]       │
│ [_______________________________________________]       │
│                                                         │
│                         [Cancel] [Save Item]             │
└─────────────────────────────────────────────────────────┘
```

---

# 3. Item Types

The item master should distinguish between goods and services.

Recommended values:

```text
PRODUCT
SERVICE
```

Optional future values:

```text
RAW_MATERIAL
FINISHED_GOOD
PACKAGING
CONSUMABLE
ASSET
OTHER
```

For Phase 3, the minimum implementation should support:

```text
Product
Service
```

---

# 4. Item Name

## Field

```text
Item Name *
```

This is the primary display name of the product/service.

Example:

```text
500ml Mineral Water Bottle
```

or:

```text
Website Development Service
```

### Requirements

- Required
- Must not be empty
- Trim leading/trailing whitespace
- Support Unicode
- Configurable maximum length
- Duplicate-name warning recommended

The application should not necessarily prohibit duplicate names because different items can legitimately share similar names.

---

# 5. Unit

Every inventory/product item should have a unit.

Example:

```text
Unit
[ PCS ▼ ]
```

The unit selector should open the Phase 2 Unit Entry Modal.

Workflow:

```text
Item Modal
     ↓
Unit Field
     ↓
Select Unit
     ↓
Phase 2 Unit Modal
     ↓
Select Existing Unit
        OR
Create New Unit
     ↓
Return to Item Modal
     ↓
Unit Automatically Selected
```

The item should store a reference to the unit rather than only storing its display name.

Recommended:

```text
unit_id
```

---

# 6. SKU Code

## Field

```text
SKU Code
```

SKU means **Stock Keeping Unit**.

The SKU is an internal product identifier used by the business.

Example:

```text
WTR-500-001
```

or:

```text
SKU-WATER-500ML
```

### Requirements

- Optional
- Should be unique within the company where provided
- Case-normalization policy should be defined
- Should support letters, numbers, hyphens and other safe configured characters
- Should not be confused with HSN/SAC
- Should not be automatically treated as a GST code

Recommended database constraint:

```text
UNIQUE(company_id, sku_code)
```

when `sku_code` is not null.

---

# 7. Automatic SKU Generation

SKU entry can be optional.

The application may provide:

```text
[ Generate SKU ]
```

Example:

```text
Item Name:
500ml Mineral Water Bottle

Generated SKU:
WATER-500ML-001
```

The generated SKU must be editable before saving.

SKU generation should not be based solely on the item name if the generated value can create collisions.

Recommended sequence:

```text
Prefix
+
Normalized Item Identifier
+
Company/Product Sequence
```

Example:

```text
WTR-500ML-0001
WTR-500ML-0002
WTR-500ML-0003
```

Automatic SKU generation is optional for Phase 3.

---

# 8. HSN / SAC Code

The item must support a tax classification code.

The field should be:

```text
HSN / SAC Code
```

The correct classification depends on whether the item is:

```text
PRODUCT → HSN
SERVICE → SAC
```

The UI should dynamically change the label.

Example:

```text
Item Type:
Product

HSN Code:
[________________]
```

For service:

```text
Item Type:
Service

SAC Code:
[________________]
```

---

# 9. HSN/SAC Validation

The application should validate the basic structure of the entered HSN/SAC code.

Recommended behavior:

```text
User enters code
      ↓
Normalize
      ↓
Validate format
      ↓
Optional master lookup
      ↓
Display description if available
      ↓
User confirms
```

The application should maintain an extensible HSN/SAC master instead of hardcoding classifications throughout the frontend.

Example:

```text
hsn_sac_codes
├── code
├── type
├── description
├── applicable_from
├── applicable_to
├── status
└── metadata
```

The master should be kept aligned with the applicable GST classification data.

---

# 10. GST Applicable

The item must include a GST applicability field.

Example:

```text
GST Applicable
[ Yes ▼ ]
```

Recommended options:

```text
YES
NO
```

The UI can also support a more detailed tax-treatment model later.

For Phase 3:

```text
GST Applicable = YES
```

means the item has an applicable GST tax rate configured.

```text
GST Applicable = NO
```

means no GST rate should be applied by default.

---

# 11. GST Rate

If:

```text
GST Applicable = YES
```

display:

```text
GST Rate
[ Select GST Rate ▼ ]
```

The rate should be selected from a controlled dropdown rather than arbitrary free text.

Example options may include:

```text
0%
0.25%
1.5%
3%
5%
12%
18%
28%
```

The actual available rates must be maintained according to the applicable GST rules and should be configurable/versioned rather than permanently hardcoded.

---

# 12. GST Rate Master

Recommended table:

```text
gst_rates
├── gst_rate_id
├── rate
├── display_name
├── description
├── effective_from
├── effective_to
└── status
```

Example:

```text
gst_rate_id: 18
rate: 18.00
display_name: 18%
status: ACTIVE
```

The application should allow historical rates to remain available for historical transactions even if a rate becomes inactive.

---

# 13. GST Rate and Tax Calculation

The item master should provide the **default GST rate**.

It should not permanently determine the tax amount of every future invoice.

Example:

```text
Item:
Product A

Default GST:
18%
```

Invoice:

```text
Quantity: 10
Unit Price: ₹1,000
Taxable Value: ₹10,000
GST: 18%
```

Calculation:

```text
GST = ₹10,000 × 18%
    = ₹1,800
```

The invoice should snapshot the applicable GST rate used at the time of the transaction.

---

# 14. CGST / SGST / IGST

The item master should store the GST rate as the overall GST rate.

The actual invoice calculation should determine whether the tax is:

```text
CGST + SGST/UTGST
```

or:

```text
IGST
```

based on the applicable transaction rules, including place of supply and supplier/customer registration details.

Example for an intra-state transaction at 18%:

```text
CGST = 9%
SGST = 9%
```

Example for an inter-state transaction:

```text
IGST = 18%
```

Do not store:

```text
CGST = 9%
SGST = 9%
```

as the only item-level tax definition.

Store the overall GST rate and derive the applicable tax components at transaction time.

---

# 15. Description

The item should have an optional description.

Example:

```text
Description

[ Premium 500ml packaged drinking water bottle.
  Suitable for retail and institutional sales. ]
```

The description can be used as the default description on invoices.

Requirements:

- Optional
- Multi-line
- Unicode support
- Configurable maximum length
- Preserve historical invoice description separately

---

# 16. Item Master Structure

Recommended core table:

```text
items
├── item_id
├── company_id
├── item_type
├── item_name
├── sku_code
├── unit_id
├── hsn_sac_code
├── gst_applicable
├── default_gst_rate_id
├── description
├── status
├── created_by
├── created_at
├── updated_by
└── updated_at
```

---

# 17. Company Isolation

Every item must belong to a company.

```text
company_id
```

must be stored on the item record.

Example:

```text
Company A
 ├── Water Bottle
 ├── Printer
 └── Consultancy Service

Company B
 ├── Water Bottle
 └── Printer
```

The two companies may have identical item names/SKUs without data collision.

SKU uniqueness should therefore be enforced within the company:

```text
UNIQUE(company_id, sku_code)
```

---

# 18. Item Status

Recommended states:

```text
ACTIVE
INACTIVE
ARCHIVED
```

New items:

```text
ACTIVE
```

If an item is no longer sold:

```text
INACTIVE
```

If the item has historical transactions, it should generally not be physically deleted.

---

# 19. Item Code

The application should maintain an internal immutable item ID.

Example:

```text
item_id = UUID
```

The user-facing SKU is separate:

```text
item_id:
7e8c...

sku_code:
WTR-500ML-001
```

Do not use SKU as the primary database identifier.

---

# 20. Item Entry Validation

Before saving:

```text
Item Name
   ↓
Required?
   ↓
Unit
   ↓
Valid?
   ↓
SKU
   ↓
Unique?
   ↓
HSN/SAC
   ↓
Valid?
   ↓
GST Applicable
   ↓
GST Rate
   ↓
Required if GST applies
   ↓
Description
   ↓
Save
```

---

# 21. Validation Rules

## Item Name

```text
Required
Trim whitespace
Maximum configurable length
```

## Unit

```text
Required for products
Must reference an active unit
```

For services, the application may allow configurable unit requirements depending on the billing model.

## SKU

```text
Optional
Unique per company if supplied
Normalized according to configured policy
```

## HSN/SAC

```text
Optional/required according to business configuration and applicable GST requirements
Correct type based on Product/Service
Format validation
```

## GST Applicable

```text
Required
YES / NO
```

## GST Rate

If GST is applicable:

```text
Required
Must reference an active GST rate
```

If GST is not applicable:

```text
GST rate should normally be null/not applicable
```

Do not silently assign a taxable rate when the user selected GST not applicable.

---

# 22. Conditional UI

The modal should dynamically respond to the selected item type.

### Product

```text
Item Type
[ Product ▼ ]

Item Name
Unit
SKU
HSN Code
GST Applicable
GST Rate
Description
```

### Service

```text
Item Type
[ Service ▼ ]

Service Name
Unit
SKU
SAC Code
GST Applicable
GST Rate
Description
```

The field label should update automatically:

```text
HSN / SAC Code
```

or:

```text
HSN Code
```

or:

```text
SAC Code
```

depending on the selected type.

---

# 23. Example Product

```text
Item Type:
Product

Item Name:
500ml Mineral Water Bottle

Unit:
PCS

SKU:
WTR-500ML-001

HSN Code:
[Applicable HSN]

GST Applicable:
Yes

GST Rate:
18%

Description:
500ml packaged drinking water bottle.
```

---

# 24. Example Service

```text
Item Type:
Service

Item Name:
Website Development Service

Unit:
Project

SKU:
WEB-DEV-001

SAC Code:
[Applicable SAC]

GST Applicable:
Yes

GST Rate:
18%

Description:
Website design and development services.
```

---

# 25. Item Search

The item master should support search by:

```text
Item Name
SKU
HSN/SAC
Description
Unit
Item Type
```

Example:

```text
Search:
WTR
```

Results:

```text
WTR-500ML-001
500ml Mineral Water Bottle
PCS
18%
```

---

# 26. Item Selection in Invoice

Sales invoice:

```text
┌────────────────────────────────────────────────────────────┐
│ Item              Qty       Unit       Rate       GST      │
├────────────────────────────────────────────────────────────┤
│ Water Bottle      10        PCS        ₹20        18%      │
│ [Select Item ▼]                                          │
└────────────────────────────────────────────────────────────┘
```

When an item is selected:

```text
Item Name
Unit
HSN/SAC
GST Rate
Description
```

should be automatically populated from the item master.

The user may be allowed to override transaction-level fields according to the application's accounting rules and permissions.

---

# 27. Historical Invoice Snapshot

An invoice must not depend entirely on the current item master.

When an item is added to an invoice, snapshot:

```text
item_id
item_name
description
sku_code
unit_id
unit_name
unit_symbol
hsn_sac_code
gst_rate
```

Example:

```text
Invoice Line

Item:
Water Bottle

SKU:
WTR-500ML-001

Quantity:
10

Unit:
PCS

HSN:
XXXX

GST Rate:
18%
```

If the item is edited later:

```text
Water Bottle
GST: 18%
```

to:

```text
Water Bottle
GST: 12%
```

old invoices must continue to show the historical GST rate that was actually applied.

---

# 28. Item Versioning

For stronger auditability, support item versions.

```text
item_versions
├── item_version_id
├── item_id
├── version_number
├── item_name
├── unit_id
├── sku_code
├── hsn_sac_code
├── gst_rate_id
├── description
├── effective_from
└── effective_to
```

This is especially useful if:

- GST rate changes
- HSN/SAC changes
- Unit changes
- Item description changes

---

# 29. Item Master UI

The application should provide a dedicated item-management page.

Example:

```text
Items

[ Search items... ]        [ + Add Item ]

┌──────────────────────────────────────────────────────────────┐
│ Item Name              SKU             Unit     GST   Status │
├──────────────────────────────────────────────────────────────┤
│ Water Bottle            WTR-500ML-001   PCS      18%   Active │
│ Printer                 PRN-001         PCS      18%   Active │
│ Website Development     WEB-DEV-001     Project  18%   Active │
└──────────────────────────────────────────────────────────────┘
```

Actions:

```text
View
Edit
Duplicate
Deactivate
Archive
View Usage
```

---

# 30. Duplicate Item

The application should support:

```text
[ Duplicate Item ]
```

This is useful when creating similar items.

Example:

```text
500ml Water Bottle
      ↓ Duplicate
1L Water Bottle
```

The copied item should receive:

```text
New item_id
```

and the SKU should either be cleared or regenerated to prevent duplicate SKU values.

---

# 31. Item Usage

Before deactivating or deleting an item:

```text
Item Usage

Sales Invoices:     245
Purchase Bills:      63
Stock Transactions: 421
Quotations:          18
```

If historical transactions exist:

```text
This item cannot be permanently deleted because it is referenced by historical transactions.

You can deactivate the item instead.
```

---

# 32. Recommended API

## Item APIs

```text
GET    /api/items
GET    /api/items/{item_id}
POST   /api/items
PUT    /api/items/{item_id}
PATCH  /api/items/{item_id}
DELETE /api/items/{item_id}
```

## Search

```text
GET /api/items/search?q=water
```

## SKU Validation

```text
GET /api/items/check-sku?sku=WTR-500ML-001
```

## HSN/SAC

```text
GET /api/hsn-sac/search?q=...
GET /api/hsn-sac/{code}
```

---

# 33. Create Item API

Example request:

```json
{
  "item_type": "PRODUCT",
  "item_name": "500ml Mineral Water Bottle",
  "unit_id": "unit-pcs",
  "sku_code": "WTR-500ML-001",
  "hsn_sac_code": "XXXX",
  "gst_applicable": true,
  "gst_rate_id": "gst-18",
  "description": "500ml packaged drinking water bottle."
}
```

Example response:

```json
{
  "item_id": "ITEM-UUID",
  "company_id": "COMPANY-UUID",
  "item_type": "PRODUCT",
  "item_name": "500ml Mineral Water Bottle",
  "unit_id": "unit-pcs",
  "sku_code": "WTR-500ML-001",
  "hsn_sac_code": "XXXX",
  "gst_applicable": true,
  "gst_rate": 18,
  "status": "ACTIVE"
}
```

---

# 34. Database Constraints

Recommended constraints:

```text
item_id
→ PRIMARY KEY

company_id
→ NOT NULL

item_name
→ NOT NULL

unit_id
→ FOREIGN KEY

gst_rate_id
→ FOREIGN KEY when applicable

status
→ ENUM / constrained value
```

SKU:

```text
UNIQUE(company_id, normalized_sku_code)
```

if SKU is supplied.

---

# 35. Item Categories — Future Extension

Although not required for the minimum Phase 3 modal, the architecture should allow item categories.

Example:

```text
Beverages
Electronics
Stationery
Hardware
Clothing
Services
Consulting
Software
Raw Materials
Finished Goods
```

Recommended future table:

```text
item_categories
├── category_id
├── company_id
├── category_name
├── parent_category_id
└── status
```

This supports hierarchical categories.

---

# 36. Brand — Future Extension

Future versions may support:

```text
Brand
Manufacturer
Model
Variant
Color
Size
```

These should not be forced into the initial Phase 3 form unless required.

---

# 37. Barcode — Future Extension

The item model should be designed to later support:

```text
Barcode
EAN
UPC
GTIN
QR
Internal Barcode
```

Recommended future table:

```text
item_barcodes
├── barcode_id
├── item_id
├── barcode
├── barcode_type
├── is_primary
└── status
```

---

# 38. Pricing — Future Extension

Phase 3 should not unnecessarily mix item master data with pricing.

Later phases can add:

```text
purchase_price
sales_price
MRP
wholesale_price
retail_price
price_lists
effective_dates
```

A separate pricing model is recommended.

Example:

```text
Item
   ↓
Price Lists
   ├── Retail
   ├── Wholesale
   └── Distributor
```

---

# 39. Inventory — Future Extension

The item master should be designed so inventory can later use:

```text
item_id
unit_id
warehouse_id
opening_stock
stock_in
stock_out
adjustment
closing_stock
```

Do not store mutable stock balance as the only source of truth.

A future inventory ledger should calculate stock from transactions, with an optional cached balance for performance.

---

# 40. Tax Treatment

The item should have a default tax configuration:

```text
gst_applicable
default_gst_rate_id
hsn_sac_code
```

But transaction-level taxation must remain authoritative.

The invoice engine should determine the final tax treatment using:

```text
Company GST configuration
+
Customer/Supplier GST status
+
Item GST configuration
+
Place of Supply
+
Transaction type
+
Applicable GST rules
```

The item master provides defaults; it should not override mandatory transaction-level tax rules.

---

# 41. Permissions

Item management should support permissions in future multi-user environments.

Recommended permissions:

```text
ITEM_VIEW
ITEM_CREATE
ITEM_EDIT
ITEM_DEACTIVATE
ITEM_DELETE
ITEM_EXPORT
ITEM_IMPORT
```

Sensitive configuration changes such as GST classification/rates may require elevated permissions.

---

# 42. Audit Trail

Record important item events:

```text
ITEM_CREATED
ITEM_UPDATED
ITEM_DEACTIVATED
ITEM_REACTIVATED
ITEM_ARCHIVED
ITEM_DUPLICATED
SKU_CHANGED
HSN_SAC_CHANGED
GST_RATE_CHANGED
UNIT_CHANGED
```

Each event should include:

```text
event_id
company_id
item_id
event_type
actor
timestamp
old_value
new_value
```

Do not store unnecessary sensitive information in audit logs.

---

# 43. Import / Export — Future Extension

The item master should eventually support Excel/CSV import.

Example columns:

```text
Item Name
Item Type
SKU
Unit
HSN/SAC
GST Applicable
GST Rate
Description
```

Import workflow:

```text
Upload CSV/XLSX
      ↓
Column Mapping
      ↓
Validation
      ↓
Preview
      ↓
Error Report
      ↓
Confirm Import
      ↓
Create/Update Items
```

This should be implemented in a later phase if bulk item entry is required.

---

# 44. Item Entry UX Requirements

The modal should be:

- Fast
- Searchable
- Keyboard friendly
- Mobile responsive
- Accessible
- Compatible with the Phase 2 Unit Modal
- Able to create/select a unit without losing entered data
- Able to select GST rates from a controlled list
- Able to distinguish products and services
- Able to validate before saving
- Able to return the newly created item directly to the calling form

Keyboard behavior:

```text
Enter
→ Submit when form is valid

Esc
→ Close modal

Tab
→ Navigate fields
```

---

# 45. Quick Add Item From Invoice

The invoice screen should provide:

```text
Item
[ Select Item ▼ ]

[ + Add New Item ]
```

Clicking:

```text
+ Add New Item
```

opens the Phase 3 modal.

After saving:

```text
New Item Created
      ↓
Return to Invoice
      ↓
New Item Automatically Selected
```

The user should not lose the invoice draft.

---

# 46. Recommended Form Behavior

When GST is not applicable:

```text
GST Applicable:
[ No ]

GST Rate:
[ Not Applicable ]
```

When GST is applicable:

```text
GST Applicable:
[ Yes ]

GST Rate:
[ 18% ▼ ]
```

When Item Type changes:

```text
Product
→ HSN

Service
→ SAC
```

When Unit is clicked:

```text
→ Phase 2 Unit Modal
```

---

# 47. Recommended Phase 3 Data Model

```text
                         COMPANY
                            │
                            ↓
                           ITEM
                            │
       ┌────────────────────┼────────────────────┐
       ↓                    ↓                    ↓
    Item Type              Unit              SKU Code
       │                    │                    │
       ↓                    ↓                    ↓
 Product / Service    Phase 2 Unit        Internal ID
                            │
                            ↓
                      HSN / SAC Code
                            │
                            ↓
                      GST Configuration
                            │
                   ┌────────┴────────┐
                   ↓                 ↓
             GST Applicable       GST Rate
                   │
                   ↓
              Description
```

---

# 48. Complete Phase 3 Workflow

```text
User clicks:
[ + Add Item ]

        ↓

Open Item Entry Modal

        ↓

Select Item Type

        ↓

Enter Item Name

        ↓

Select Unit

        ↓

Optional SKU

        ↓

HSN/SAC

        ↓

GST Applicable

        ↓

GST Rate

        ↓

Description

        ↓

Validate

        ↓

Check SKU uniqueness

        ↓

Validate Unit

        ↓

Validate HSN/SAC

        ↓

Validate GST configuration

        ↓

Save Item

        ↓

Create Audit Event

        ↓

Return Item ID

        ↓

Item available in application
```

---

# 49. Phase 3 Completion Criteria

Phase 3 is complete when the application supports:

```text
1. Dedicated Item Entry Modal
2. Product/Service selection
3. Item name
4. Unit selection
5. Integration with Phase 2 Unit Modal
6. Optional SKU
7. SKU uniqueness per company
8. HSN/SAC field
9. Product → HSN
10. Service → SAC
11. GST applicability
12. GST rate dropdown
13. GST rate master
14. Item description
15. Item validation
16. Item status
17. Company isolation
18. Item search
19. Item management page
20. Item editing
21. Item deactivation
22. Historical transaction protection
23. Invoice item snapshot
24. Audit trail
```

---

# 50. Final Architecture

Phase 3 should build on Phase 1 and Phase 2:

```text
PHASE 1
COMPANY
   │
   ├── Company Profile
   ├── GST Details
   ├── Bank Details
   └── Authentication
          │
          ↓
PHASE 2
UNIT ENGINE
   │
   ├── Predefined Units
   ├── Custom Units
   ├── Formula Engine
   ├── Conversion
   └── GST Unit Mapping
          │
          ↓
PHASE 3
ITEM ENGINE
   │
   ├── Product
   ├── Service
   ├── SKU
   ├── Unit
   ├── HSN/SAC
   ├── GST Applicability
   ├── GST Rate
   └── Description
          │
          ↓
FUTURE
SALES / PURCHASE / INVENTORY
   │
   ├── GST Invoices
   ├── Purchase Bills
   ├── Stock
   ├── Customers
   ├── Suppliers
   └── Accounting
```

---

# 51. Key Implementation Principle

The Item Master should be treated as the **central definition of what the business sells, purchases, or bills**, while the invoice remains the authoritative historical transaction.

The architecture should therefore follow:

```text
ITEM MASTER
     │
     ├── Name
     ├── SKU
     ├── Unit
     ├── HSN/SAC
     ├── Default GST
     └── Description
             │
             ↓
       TRANSACTION
             │
       ┌─────┴─────┐
       ↓           ↓
     SALES       PURCHASE
       │           │
       ↓           ↓
   Invoice      Bill
       │           │
       └─────┬─────┘
             ↓
       Historical Snapshot
```

This ensures that changing an item's master data later does not silently alter previously issued invoices or accounting records.

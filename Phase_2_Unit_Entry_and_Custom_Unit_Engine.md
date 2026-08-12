# Phase 2 — Dedicated Unit Entry Modal & Custom Unit Definition

## 1. Objective

Phase 2 introduces a dedicated **Unit Entry Modal** for the GST billing/accounting application.

The unit system must support:

- Predefined standard units
- GST-compatible unit codes where applicable
- Common commercial units
- User-defined custom units
- Compound/sophisticated units
- Excel-style formulas for defining custom units
- Unit conversion
- Decimal quantities
- Multiple units for the same product/service where appropriate
- Unit search and selection
- Unit aliases
- Conversion validation
- Consistent units across sales, purchases, inventory, invoices, reports, and accounting

The primary user experience is:

```text
Product / Service
       ↓
Unit Field
       ↓
[ Select Unit ]
       ↓
Dedicated Unit Entry Modal
       ↓
┌──────────────────────────────────────────────┐
│ Search / Select / Create Unit                │
│                                              │
│ Predefined Units                             │
│ Custom Units                                 │
│ Unit Formula                                 │
│ Conversion                                   │
└──────────────────────────────────────────────┘
       ↓
Selected Unit
       ↓
Product / Invoice / Inventory
```

---

# 2. Design Principle

The unit system must distinguish between:

1. **Unit Name**
2. **Unit Symbol**
3. **Unit Code**
4. **Unit Category**
5. **Base Unit**
6. **Conversion Factor**
7. **Formula**
8. **Precision**
9. **Display Format**
10. **Aliases**

Do not treat the visible unit name as the conversion rule.

Example:

```text
Unit Name: Kilogram
Symbol: kg
Code: KGS
Category: Mass
Base Unit: kg
Conversion Factor: 1
```

Another:

```text
Unit Name: Gram
Symbol: g
Code: GMS
Category: Mass
Base Unit: kg
Conversion Factor: 0.001
```

Therefore:

```text
1 g = 0.001 kg
```

---

# 3. Dedicated Unit Entry Modal

Every product/service quantity field that requires a unit should provide access to the dedicated unit modal.

Example:

```text
Quantity
[ 25.50 ]

Unit
[ kg ▼ ]        [ + Manage Units ]
```

Clicking `Manage Units` or `Select Unit` opens:

```text
┌─────────────────────────────────────────────────────┐
│                 UNIT ENTRY                          │
├─────────────────────────────────────────────────────┤
│ Search units...                              [ 🔍 ] │
│                                                     │
│ [ All ] [Predefined] [Custom]                       │
│                                                     │
│ MASS                                                │
│ kg     Kilogram                                     │
│ g      Gram                                         │
│ mg     Milligram                                    │
│                                                     │
│ LENGTH                                              │
│ m      Metre                                        │
│ cm     Centimetre                                   │
│ mm     Millimetre                                   │
│                                                     │
│ AREA                                                │
│ sq m   Square Metre                                 │
│                                                     │
│ VOLUME                                              │
│ L      Litre                                        │
│ mL     Millilitre                                   │
│                                                     │
│ [ + Create Custom Unit ]                            │
│                                                     │
│                                  [Cancel] [Select]  │
└─────────────────────────────────────────────────────┘
```

---

# 4. Unit Categories

The application should maintain a unit-category master.

Recommended categories:

```text
Quantity
Mass
Length
Area
Volume
Time
Temperature
Energy
Power
Pressure
Speed
Frequency
Data
Currency
Packaging
Count
Commercial
Custom
```

Additional categories may be added later.

---

# 5. Predefined Units

The system should ship with a predefined unit library.

Examples:

## Quantity / Count

```text
Piece
Unit
Number
Set
Pair
Dozen
Gross
Pack
Box
Carton
Bundle
Lot
```

## Mass

```text
Milligram
Gram
Kilogram
Quintal
Metric Tonne
```

## Length

```text
Millimetre
Centimetre
Metre
Kilometre
Inch
Foot
Yard
Mile
```

## Area

```text
Square Millimetre
Square Centimetre
Square Metre
Square Kilometre
Square Inch
Square Foot
Square Yard
Acre
Hectare
```

## Volume

```text
Millilitre
Litre
Cubic Centimetre
Cubic Metre
Cubic Inch
Cubic Foot
Gallon
```

## Time

```text
Second
Minute
Hour
Day
Week
Month
Year
```

## Temperature

```text
Celsius
Fahrenheit
Kelvin
```

## Commercial Units

```text
Piece
Box
Carton
Packet
Bottle
Bag
Roll
Drum
Can
Container
Bundle
Pair
Set
```

The predefined library should be versioned and maintained separately from user-created units.

---

# 6. GST Unit Codes

Where GST reporting requires a recognized unit code, the application should maintain a dedicated mapping.

Example:

```text
Unit
├── Display Name
├── Symbol
├── GST Unit Code
└── Internal Unit ID
```

The GST reporting code must not be assumed to be identical to the UI symbol.

Example:

```text
Display:
Kilogram

Symbol:
kg

GST Unit Code:
KGS
```

The application should maintain an authoritative unit-code mapping according to the applicable GST reporting specification.

Do not hardcode GST unit codes in invoice components.

---

# 7. Unit Master

Recommended structure:

```text
units
├── unit_id
├── unit_name
├── symbol
├── internal_code
├── gst_unit_code
├── category_id
├── unit_type
├── base_unit_id
├── conversion_factor
├── conversion_formula
├── precision
├── rounding_mode
├── display_format
├── is_predefined
├── is_active
├── created_by
├── created_at
└── updated_at
```

---

# 8. Unit Types

Recommended:

```text
BASE
DERIVED
COMPOUND
COUNT
COMMERCIAL
CUSTOM
```

Examples:

```text
Kilogram
→ BASE

Gram
→ DERIVED

Square Metre
→ DERIVED

Kilogram per Square Metre
→ COMPOUND

Box
→ COMMERCIAL

User-defined packaging unit
→ CUSTOM
```

---

# 9. Base Units

Every dimensional unit should ultimately resolve to a base unit.

Example:

```text
Mass
└── kg
    ├── g
    ├── mg
    ├── tonne
    └── quintal
```

Length:

```text
Length
└── m
    ├── mm
    ├── cm
    ├── km
    ├── inch
    └── foot
```

Area:

```text
Area
└── m²
    ├── cm²
    ├── ft²
    └── acre
```

Volume:

```text
Volume
└── L
    ├── mL
    └── other derived units
```

---

# 10. Simple Conversion

A simple unit can use a conversion factor.

Example:

```text
Base Unit = kg

1 g = 0.001 kg
```

Store:

```text
base_unit = kg
conversion_factor = 0.001
```

Then:

```text
quantity_in_base =
quantity × conversion_factor
```

Example:

```text
500 g

500 × 0.001
= 0.5 kg
```

---

# 11. Excel-Style Formula Support

The most important feature of Phase 2 is allowing users to define sophisticated units using an **Excel-style formula interface**.

The user should not be required to write programming code.

Example:

```text
1 Box = 12 Pieces
```

The user can define:

```text
=12*PCS
```

or use a structured conversion builder.

---

# 12. Formula Syntax

The unit formula engine should support a controlled spreadsheet-like syntax.

Basic operators:

```text
+
-
*
/
^
()
```

Examples:

```text
=12*PCS
=1000*G
=2.5*KG
=10*L
=SQRT(AREA)
```

The formula engine should NOT execute arbitrary programming languages.

Never pass the user's formula directly to:

```text
eval()
exec()
shell
SQL
JavaScript execution
```

Use a safe expression parser.

---

# 13. Formula Variables

Units can be referenced by their internal symbols/codes.

Example:

```text
PCS
KG
G
M
CM
L
ML
```

Example:

```text
1 BOX = 12 PCS
```

Formula:

```text
=12*PCS
```

Another:

```text
1 CARTON = 24*BOX
```

If:

```text
1 BOX = 12 PCS
```

then:

```text
1 CARTON
= 24 × 12 PCS
= 288 PCS
```

---

# 14. Formula Examples

## Box

```text
Unit:
Box

Base:
Piece

Formula:
=12*PCS
```

Result:

```text
1 BOX = 12 PCS
```

---

## Carton

```text
Unit:
Carton

Formula:
=24*BOX
```

If:

```text
1 BOX = 12 PCS
```

then:

```text
1 CARTON = 288 PCS
```

---

## Dozen

```text
Unit:
Dozen

Formula:
=12*PCS
```

---

## Bundle

```text
Unit:
Bundle

Formula:
=10*PCS
```

---

## Half Kilogram

```text
Unit:
500G

Formula:
=0.5*KG
```

---

# 15. Compound Units

The unit system should support compound units.

Examples:

```text
kg/m²
kg/m³
L/min
₹/kg
pcs/box
m/min
km/h
```

Example:

```text
Kilogram per Square Metre
```

Formula:

```text
=KG/(M^2)
```

Another:

```text
Litre per Minute
```

Formula:

```text
=L/MIN
```

---

# 16. Dimensional Analysis

The formula engine should maintain dimensional information.

Example:

```text
KG
Dimension = MASS
```

```text
M
Dimension = LENGTH
```

```text
M^2
Dimension = AREA
```

```text
KG/M^2
Dimension = MASS / AREA
```

This allows the system to detect invalid conversions.

Example:

```text
1 KG = 1000 M
```

should be rejected because:

```text
MASS ≠ LENGTH
```

---

# 17. Formula Validation

Before saving a custom unit, validate:

```text
Syntax
Referenced Units
Unit Dimensions
Circular Dependencies
Division by Zero
Invalid Operators
Unknown Functions
Unknown Variables
Precision
Conversion Direction
```

Example:

```text
=12*PCS
```

Valid.

Example:

```text
=12*
```

Invalid.

Example:

```text
=KG+M
```

Invalid for a dimensional conversion because mass and length cannot be added.

---

# 18. Circular Dependency Protection

The system must detect:

```text
BOX → CARTON
CARTON → BOX
```

This is invalid.

Example:

```text
1 BOX = 12 PCS
1 CARTON = 24 BOX
```

Valid.

But:

```text
1 BOX = 2 CARTON
1 CARTON = 10 BOX
```

creates a circular conversion graph and should be rejected.

---

# 19. Custom Unit Creation Modal

Click:

```text
[ + Create Custom Unit ]
```

Display:

```text
┌─────────────────────────────────────────────────────┐
│             CREATE CUSTOM UNIT                     │
├─────────────────────────────────────────────────────┤
│ Unit Name *                                         │
│ [_______________________________________________]   │
│                                                     │
│ Symbol *                                            │
│ [__________]                                        │
│                                                     │
│ Category *                                          │
│ [ Commercial ▼ ]                                    │
│                                                     │
│ Base Unit                                            │
│ [ Piece ▼ ]                                         │
│                                                     │
│ Conversion Formula                                  │
│ [ =12*PCS______________________________________ ]   │
│                                                     │
│ Example                                             │
│ 1 BOX = 12 PCS                                      │
│                                                     │
│ Decimal Precision                                   │
│ [ 2 ▼ ]                                             │
│                                                     │
│ [ Test Formula ]                                    │
│                                                     │
│ Formula Result                                      │
│ ✓ Valid                                             │
│                                                     │
│              [Cancel] [Save Unit]                   │
└─────────────────────────────────────────────────────┘
```

---

# 20. Formula Builder

For non-technical users, provide an Excel-style formula builder.

Example:

```text
Formula:

[ = ] [ 12 ] [ × ] [ PCS ]

Result:

1 BOX = 12 PCS
```

Buttons:

```text
[ + ]
[ - ]
[ × ]
[ ÷ ]
[ ( ]
[ ) ]
[ ^ ]
```

Unit selector:

```text
[ Insert Unit ▼ ]
```

Functions can be offered separately if supported.

---

# 21. Excel-Style Cell Reference Support

The system may optionally support spreadsheet-like references for advanced unit definitions.

Example:

```text
A1 = 12
B1 = PCS

Formula:
=A1*B1
```

However, for the first implementation, **unit expressions are preferable to arbitrary spreadsheet cells** because unit conversion must remain deterministic and auditable.

If spreadsheet-style references are implemented later, they must be isolated within the unit-definition context.

---

# 22. Recommended Formula Language

A controlled grammar should support:

```text
NUMBER
UNIT_REFERENCE

+
-
*
/
^

(
)

MIN()
MAX()
ROUND()
ABS()
```

Example:

```text
=ROUND(12*PCS,2)
```

Do not initially support arbitrary Excel functions.

Every function should have a defined implementation and dimensional behavior.

---

# 23. Conversion Direction

The system should define a canonical direction:

```text
Custom Unit
      ↓
Base Unit
```

Example:

```text
BOX → PCS
```

If:

```text
1 BOX = 12 PCS
```

then:

```text
10 BOX = 120 PCS
```

Reverse conversion:

```text
120 PCS = 10 BOX
```

should be calculated automatically.

---

# 24. Product-Specific Units

Some units are not globally convertible.

Example:

```text
1 Box = 24 Bottles
```

may be true for one product but not another.

Therefore the system should support:

```text
Global Unit Definition
```

and:

```text
Product Unit Conversion
```

Example:

```text
Product:
Mineral Water 500 mL

Base Unit:
Piece

Product Conversion:
1 Box = 24 Pieces
```

Another product:

```text
Product:
Juice Bottle

1 Box = 12 Pieces
```

Therefore, a global `BOX` definition must not incorrectly impose the same quantity on every product.

---

# 25. Product Unit Configuration

Recommended structure:

```text
product_units
├── product_unit_id
├── product_id
├── unit_id
├── is_base_unit
├── conversion_formula
├── conversion_factor
├── barcode
├── purchase_allowed
├── sales_allowed
├── inventory_allowed
└── status
```

Example:

```text
Product:
Water Bottle

Base Unit:
PCS

Alternative:
BOX

Formula:
=24*PCS
```

---

# 26. Sales and Purchase Units

A product can have different default units for:

```text
Purchase
Sales
Inventory
```

Example:

```text
Purchase Unit:
Carton

Sales Unit:
Piece

Inventory Base Unit:
Piece
```

If:

```text
1 Carton = 24 Pieces
```

then:

```text
Purchase:
10 Cartons

Inventory:
10 × 24
= 240 Pieces
```

---

# 27. Invoice Integration

The invoice line should store:

```text
product_id
description
quantity
unit_id
unit_symbol
unit_code
unit_price
taxable_value
tax_rate
tax_amount
total_amount
```

Example:

```text
Product       Quantity     Unit      Rate
Water Bottle  10           BOX       ₹500
```

The invoice should retain the unit information used at the time of invoicing.

Do not depend solely on the current unit master for historical invoice rendering.

---

# 28. Unit Snapshot

Similar to GST/customer snapshots, invoices should preserve:

```text
unit_id
unit_name
unit_symbol
gst_unit_code
```

Example:

```text
Invoice Line

Quantity:
10

Unit:
BOX

Unit Name:
Box

GST Unit Code:
BOX
```

If the unit master is renamed later, historical invoices remain unchanged.

---

# 29. Decimal Precision

Different units require different precision.

Examples:

```text
Piece:
0 decimal places

Kilogram:
3 decimal places

Metre:
3 decimal places

Litre:
3 decimal places
```

Custom units can define:

```text
precision = 0..8
```

Example:

```text
Quantity:
12.500 KG
```

The database should use a fixed-precision numeric/decimal type rather than floating-point storage for financial and quantity calculations where exact decimal behavior is required.

---

# 30. Rounding

Unit conversion should support configurable rounding:

```text
HALF_UP
HALF_DOWN
HALF_EVEN
UP
DOWN
FLOOR
CEILING
```

The application should distinguish:

```text
Quantity Precision
```

from:

```text
Financial Amount Precision
```

Do not round intermediate calculations unnecessarily.

---

# 31. Unit Aliases

Users often type different names for the same unit.

Example:

```text
Kilogram
kg
KG
Kilo
Kgs
```

The system can map aliases to the same unit:

```text
unit_aliases
├── alias_id
├── unit_id
├── alias
└── normalized_alias
```

Search:

```text
kg
```

should return:

```text
Kilogram — kg
```

---

# 32. Unit Search

The modal should support:

```text
Search by:
- Name
- Symbol
- Internal code
- GST unit code
- Alias
- Category
```

Example:

```text
Search:
kg
```

Results:

```text
Kilogram
kg
KGS
Mass
```

---

# 33. Favorites / Recently Used Units

For better usability, the modal may provide:

```text
Recent Units
Favorite Units
Most Used Units
```

Example:

```text
Recently Used

kg
pcs
box
litre
```

This is optional but recommended.

---

# 34. Unit Status

Units should support:

```text
ACTIVE
INACTIVE
ARCHIVED
```

A unit that has been used in historical invoices should not simply be deleted.

Instead:

```text
is_active = false
```

Existing transactions remain valid.

---

# 35. Unit Versioning

If a custom unit conversion changes, historical transactions should not change.

Example:

Initially:

```text
1 BOX = 12 PCS
```

Later:

```text
1 BOX = 24 PCS
```

The system should not recalculate old invoices automatically.

Use unit-definition versioning or transaction snapshots.

Example:

```text
unit_versions
├── unit_version_id
├── unit_id
├── version_number
├── formula
├── conversion_factor
├── effective_from
└── effective_to
```

---

# 36. Formula Audit Trail

Every custom formula should be auditable.

Store:

```text
formula
normalized_formula
parsed_expression
base_unit
conversion_result
created_by
created_at
updated_by
updated_at
```

Example:

```text
Original:
=12*PCS

Normalized:
12 * PCS

Result:
1 BOX = 12 PCS
```

---

# 37. Unit Formula Examples

## Example 1 — Box

```text
Name:
Box

Symbol:
BOX

Base:
PCS

Formula:
=12*PCS
```

Result:

```text
1 BOX = 12 PCS
```

---

## Example 2 — Carton

```text
Name:
Carton

Symbol:
CTN

Base:
PCS

Formula:
=24*PCS
```

Result:

```text
1 CTN = 24 PCS
```

---

## Example 3 — Dozen

```text
Name:
Dozen

Symbol:
DOZ

Base:
PCS

Formula:
=12*PCS
```

---

## Example 4 — Half Kilogram

```text
Name:
Half Kilogram

Symbol:
0.5KG

Base:
KG

Formula:
=0.5*KG
```

---

## Example 5 — Square Metre

```text
Name:
Square Metre

Symbol:
M2

Formula:
=M^2
```

---

## Example 6 — Kilogram per Square Metre

```text
Name:
Kilogram per Square Metre

Symbol:
KG/M2

Formula:
=KG/(M^2)
```

---

## Example 7 — Production Rate

```text
Name:
Pieces per Hour

Symbol:
PCS/H

Formula:
=PCS/H
```

---

# 38. Invalid Formula Examples

```text
=12*
```

Invalid syntax.

```text
=UNKNOWN
```

Unknown unit.

```text
=KG/0
```

Division by zero.

```text
=BOX
```

Invalid if BOX has no defined conversion.

```text
=KG+M
```

Invalid dimensional operation.

```text
=BOX
```

Circular dependency if BOX eventually references itself.

---

# 39. Security

The custom formula system is an expression engine and must be treated as an input-security boundary.

Never execute formulas using:

```text
eval()
exec()
os.system()
subprocess
shell commands
dynamic SQL
```

Use:

```text
Tokenizer
   ↓
Parser
   ↓
AST
   ↓
Validator
   ↓
Dimensional Analyzer
   ↓
Safe Evaluator
   ↓
Conversion Result
```

Example:

```text
User Formula
    ↓
"=24*BOX"
    ↓
Tokenize
    ↓
Parse
    ↓
Validate
    ↓
Resolve BOX
    ↓
Calculate
    ↓
24 × BOX
    ↓
Base Unit Result
```

---

# 40. Recommended Database Tables

```text
unit_categories
├── category_id
├── name
├── code
├── dimension
└── status

units
├── unit_id
├── category_id
├── name
├── symbol
├── internal_code
├── gst_unit_code
├── unit_type
├── base_unit_id
├── conversion_factor
├── conversion_formula
├── precision
├── rounding_mode
├── is_predefined
└── status

unit_aliases
├── alias_id
├── unit_id
├── alias
└── normalized_alias

unit_versions
├── unit_version_id
├── unit_id
├── version_number
├── conversion_formula
├── conversion_factor
├── effective_from
└── effective_to

product_units
├── product_unit_id
├── product_id
├── unit_id
├── is_base_unit
├── conversion_formula
├── conversion_factor
├── purchase_allowed
├── sales_allowed
└── inventory_allowed
```

---

# 41. Unit Entry API

Recommended API structure:

```text
GET    /api/units
GET    /api/units/{unit_id}
POST   /api/units
PUT    /api/units/{unit_id}
PATCH  /api/units/{unit_id}
DELETE /api/units/{unit_id}

GET    /api/unit-categories
GET    /api/units/search?q=kg

POST   /api/units/validate-formula
POST   /api/units/test-conversion

GET    /api/products/{product_id}/units
POST   /api/products/{product_id}/units
PUT    /api/products/{product_id}/units/{unit_id}
DELETE /api/products/{product_id}/units/{unit_id}
```

Deletion should generally mean deactivation/archive rather than physical deletion where accounting history exists.

---

# 42. Formula Validation API

Example request concept:

```text
POST /api/units/validate-formula
```

Input:

```json
{
  "name": "Box",
  "symbol": "BOX",
  "base_unit": "PCS",
  "formula": "=12*PCS"
}
```

Response:

```json
{
  "valid": true,
  "normalized_formula": "12 * PCS",
  "base_unit": "PCS",
  "conversion_factor": "12"
}
```

Invalid example:

```json
{
  "valid": false,
  "error": "Unknown unit reference: XYZ"
}
```

---

# 43. Unit Conversion API

Example:

```text
POST /api/units/convert
```

Input:

```json
{
  "quantity": "10",
  "from_unit": "BOX",
  "to_unit": "PCS"
}
```

Response:

```json
{
  "quantity": "10",
  "from_unit": "BOX",
  "to_unit": "PCS",
  "converted_quantity": "120"
}
```

---

# 44. Unit Modal UX Requirements

The modal should be:

- Searchable
- Keyboard friendly
- Fast
- Categorized
- Mobile responsive
- Accessible
- Able to distinguish predefined and custom units
- Able to create a custom unit without leaving the current workflow

Recommended keyboard behavior:

```text
Ctrl/Cmd + K
→ Search

Enter
→ Select

Esc
→ Close

Tab
→ Navigate controls
```

---

# 45. Quick Unit Creation

When entering a product:

```text
Unit:
[ Box ▼ ]
```

If the required unit does not exist:

```text
[ + Create Unit ]
```

The user should be able to create it without losing the product form.

Workflow:

```text
Product Form
    ↓
Create Unit
    ↓
Unit Modal
    ↓
Save Unit
    ↓
Return to Product Form
    ↓
New Unit Automatically Selected
```

---

# 46. Unit Selection in Invoice

Example:

```text
┌────────────────────────────────────────────────────┐
│ Product           Qty       Unit       Rate        │
├────────────────────────────────────────────────────┤
│ Water Bottle      10        BOX        ₹500        │
│                  [10]       [BOX ▼]                │
└────────────────────────────────────────────────────┘
```

The application should calculate:

```text
10 BOX × ₹500
= ₹5,000
```

If the product has:

```text
1 BOX = 24 PCS
```

inventory quantity becomes:

```text
10 × 24
= 240 PCS
```

---

# 47. Unit and Price Relationship

The software should support prices defined per unit.

Example:

```text
Product:
Water Bottle

Purchase:
₹240 per BOX

Sales:
₹15 per PCS
```

If:

```text
1 BOX = 24 PCS
```

then:

```text
₹240 / 24
= ₹10 per PCS
```

The system should clearly distinguish:

```text
Price Unit
Quantity Unit
Inventory Base Unit
```

This prevents incorrect pricing when sales and purchase units differ.

---

# 48. Unit Master Screen

In addition to the modal, provide a full Unit Management page.

```text
Units

[ Search ]

Name          Symbol   Category    Type        Status
Kilogram      kg       Mass        Predefined  Active
Gram          g        Mass        Predefined  Active
Piece         pcs      Count       Predefined  Active
Box           BOX      Commercial  Custom      Active
Carton        CTN      Commercial  Custom      Active

[ + Add Unit ]
```

Actions:

```text
View
Edit
Duplicate
Deactivate
View Usage
View Formula
```

---

# 49. Unit Usage

Before deactivating a unit, show:

```text
Unit Usage

Used by:
Products: 18
Invoices: 245
Purchase Bills: 63
Stock Transactions: 421
```

If historical transactions exist:

```text
This unit cannot be permanently deleted because it is referenced by historical transactions.

You can deactivate it instead.
```

---

# 50. Phase 2 Completion Criteria

Phase 2 is complete when the application supports:

```text
1. Dedicated Unit Entry Modal
        ↓
2. Predefined Unit Library
        ↓
3. GST Unit Code Mapping
        ↓
4. Unit Search
        ↓
5. Unit Categories
        ↓
6. Custom Unit Creation
        ↓
7. Excel-style Formula Definition
        ↓
8. Formula Validation
        ↓
9. Safe Formula Evaluation
        ↓
10. Dimensional Validation
        ↓
11. Circular Dependency Detection
        ↓
12. Unit Conversion
        ↓
13. Product-specific Unit Conversion
        ↓
14. Decimal Precision
        ↓
15. Rounding Rules
        ↓
16. Unit Aliases
        ↓
17. Unit Versioning
        ↓
18. Invoice Unit Snapshot
        ↓
19. Inventory Unit Conversion
        ↓
20. Unit Management
```

---

# 51. Final Architecture

The complete Phase 2 architecture should be:

```text
                       UNIT SYSTEM
                            │
             ┌──────────────┴──────────────┐
             │                             │
      PREDEFINED UNITS              CUSTOM UNITS
             │                             │
             │                       Formula Builder
             │                             │
             │                       Safe Parser
             │                             │
             │                       Dimensional Check
             │                             │
             └──────────────┬──────────────┘
                            ↓
                       UNIT MASTER
                            │
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
          Products        Sales          Purchases
             │              │              │
             ↓              ↓              ↓
      Product Units      Invoices      Purchase Bills
             │              │              │
             └──────────────┼──────────────┘
                            ↓
                       INVENTORY
                            │
                            ↓
                       REPORTING
```

---

# 52. Key Implementation Principle

The unit system should not be limited to a static dropdown such as:

```text
kg
g
pcs
litre
meter
```

Instead, it should function as a **unit-definition engine**:

```text
Standard Unit
      +
Conversion
      +
Formula
      +
Dimension
      +
Precision
      +
GST Mapping
      +
Product Context
      =
Flexible Unit System
```

This allows users to define sophisticated commercial units without requiring a developer to add every possible unit manually.

For example:

```text
1 Box = 12 Pieces
1 Carton = 24 Boxes
1 Pallet = 40 Cartons
```

The system can resolve:

```text
1 Pallet
= 40 × 24 × 12 Pieces
= 11,520 Pieces
```

while still maintaining a clean, auditable unit hierarchy.

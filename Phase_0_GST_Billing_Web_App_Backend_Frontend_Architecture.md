# Phase 0 — GST Billing Web Application Foundation, Backend & Frontend Architecture

## 1. Purpose

Phase 0 is the **technical foundation phase** for the GST billing software.

No business module should be implemented before the Phase 0 architecture is established.

The application must provide a clean, modular foundation for:

```text
Phase 1 → Company Account Creation & PIN Login
Phase 2 → Unit Management
Phase 3 → Item / SKU Management
Phase 4 → Universal Master Data Modification
Phase 5 → GST Invoice Generation & Modification
```

The primary technology stack is:

```text
Backend:
Python

API Framework:
FastAPI

Frontend:
React.js + TypeScript

Build Tool:
Vite

Database:
SQLite

ORM:
SQLAlchemy 2.x

Database Migration:
Alembic

Validation:
Pydantic

Authentication:
Secure server-side authentication + signed/secure session mechanism

API Documentation:
OpenAPI / Swagger
```

---

# 2. Recommended Technology Stack

## Backend

Use:

```text
Python 3.12+
FastAPI
Uvicorn
SQLAlchemy 2.x
Alembic
Pydantic v2
Pydantic Settings
Argon2id password/PIN hashing
Python-Jose or PyJWT where JWT is actually required
```

Recommended backend architecture:

```text
FastAPI
   ↓
Router
   ↓
Service
   ↓
Repository / Data Access
   ↓
SQLAlchemy
   ↓
SQLite
```

Do not put business logic directly inside route functions.

---

# 3. Frontend

Recommended:

```text
React
TypeScript
Vite
React Router
TanStack Query
React Hook Form
Zod
```

Optional UI layer:

```text
Tailwind CSS
```

or a mature component library.

The frontend should be treated as a separate application from the backend.

Recommended:

```text
frontend/
backend/
```

rather than mixing Python-generated HTML throughout the project.

---

# 4. Why React + TypeScript

React is recommended because the GST billing application will eventually contain complex interactive screens:

```text
Invoice Builder
Dynamic Item Table
GST Calculation Preview
Customer Search
Item Search
Unit Formula Editor
Modals
Forms
Tables
Filters
Reports
Dashboard
PDF Preview
Audit History
```

TypeScript is strongly recommended because it catches data-model errors during development.

Example:

```typescript
type InvoiceLine = {
    itemId: string;
    quantity: number;
    unitId: string;
    rate: number;
    discount: number;
};
```

This is safer than allowing arbitrary JavaScript objects throughout the application.

---

# 5. Why FastAPI

FastAPI is recommended because the application requires:

```text
REST APIs
Strong validation
Type-safe request models
OpenAPI documentation
Async support where useful
Excellent Python integration
```

FastAPI should expose the backend as an API service.

Example:

```text
React
   ↓ HTTP/JSON
FastAPI
   ↓
Application Services
   ↓
SQLite
```

---

# 6. Database

Primary database:

```text
SQLite
```

Recommended file:

```text
data/gst_billing.db
```

Do not place the SQLite database inside:

```text
frontend/
```

or:

```text
static/
```

Recommended:

```text
project/
├── backend/
├── frontend/
├── data/
│   └── gst_billing.db
└── storage/
```

---

# 7. SQLite Design Rules

SQLite should be configured with:

```text
Foreign keys = ON
WAL mode = ON
Busy timeout = configured
```

Foreign-key enforcement is mandatory.

Conceptually:

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
```

WAL improves concurrent read behavior.

However, SQLite is still a single-file database and is not intended to become an unrestricted multi-server database cluster.

---

# 8. SQLite Deployment Strategy

Phase 0 should initially target:

```text
Single business installation
```

Possible deployment:

```text
Browser
   ↓
FastAPI
   ↓
SQLite
```

For a single-company or small-office application, SQLite is appropriate.

If the product later becomes a high-concurrency SaaS platform, the database abstraction should allow migration to:

```text
PostgreSQL
```

without rewriting the business layer.

---

# 9. Database Abstraction

Business services should not directly execute arbitrary SQL everywhere.

Prefer:

```text
Service
 ↓
Repository / SQLAlchemy
 ↓
Database
```

Example:

```python
class ItemService:
    def create_item(...):
        ...
```

rather than:

```python
@app.post("/items")
def create_item():
    cursor.execute(...)
```

Routes should remain thin.

---

# 10. Backend Directory Structure

Recommended:

```text
backend/
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   ├── exceptions.py
│   │   └── constants.py
│   │
│   ├── api/
│   │   ├── router.py
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── company.py
│   │       ├── units.py
│   │       ├── items.py
│   │       ├── customers.py
│   │       ├── invoices.py
│   │       ├── payments.py
│   │       ├── audit.py
│   │       └── health.py
│   │
│   ├── models/
│   │   ├── company.py
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── unit.py
│   │   ├── item.py
│   │   ├── customer.py
│   │   ├── invoice.py
│   │   ├── invoice_line.py
│   │   ├── payment.py
│   │   └── audit.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── company.py
│   │   ├── unit.py
│   │   ├── item.py
│   │   ├── customer.py
│   │   ├── invoice.py
│   │   ├── payment.py
│   │   └── common.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── company_service.py
│   │   ├── unit_service.py
│   │   ├── item_service.py
│   │   ├── customer_service.py
│   │   ├── invoice_service.py
│   │   ├── tax_service.py
│   │   ├── numbering_service.py
│   │   ├── pdf_service.py
│   │   └── audit_service.py
│   │
│   ├── repositories/
│   │   ├── company_repository.py
│   │   ├── unit_repository.py
│   │   ├── item_repository.py
│   │   ├── customer_repository.py
│   │   ├── invoice_repository.py
│   │   └── audit_repository.py
│   │
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── database.py
│   │
│   └── utils/
│       ├── gstin.py
│       ├── currency.py
│       ├── dates.py
│       └── files.py
│
├── migrations/
├── tests/
├── requirements.txt
└── pyproject.toml
```

---

# 11. Frontend Directory Structure

Recommended:

```text
frontend/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   │
│   ├── app/
│   │   ├── router.tsx
│   │   ├── providers.tsx
│   │   └── config.ts
│   │
│   ├── api/
│   │   ├── client.ts
│   │   ├── auth.ts
│   │   ├── company.ts
│   │   ├── units.ts
│   │   ├── items.ts
│   │   ├── customers.ts
│   │   └── invoices.ts
│   │
│   ├── components/
│   │   ├── common/
│   │   ├── forms/
│   │   ├── tables/
│   │   ├── modals/
│   │   └── invoice/
│   │
│   ├── features/
│   │   ├── auth/
│   │   ├── company/
│   │   ├── units/
│   │   ├── items/
│   │   ├── customers/
│   │   └── invoices/
│   │
│   ├── hooks/
│   ├── stores/
│   ├── types/
│   ├── utils/
│   ├── styles/
│   └── assets/
│
├── public/
├── package.json
├── tsconfig.json
├── vite.config.ts
└── index.html
```

---

# 12. Feature-Based Frontend Architecture

Each major business module should have its own feature directory.

Example:

```text
features/
└── invoices/
    ├── pages/
    ├── components/
    ├── hooks/
    ├── api.ts
    ├── types.ts
    ├── schemas.ts
    └── utils.ts
```

This prevents a huge:

```text
components/
```

folder containing unrelated business logic.

---

# 13. Application Layers

The complete system should follow:

```text
┌─────────────────────────────┐
│          Browser            │
│       React + TypeScript    │
└──────────────┬──────────────┘
               │
             HTTP
               │
               ↓
┌─────────────────────────────┐
│          FastAPI            │
│          Routers             │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│       Service Layer         │
│      Business Rules         │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ Repository / SQLAlchemy     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│           SQLite            │
└─────────────────────────────┘
```

---

# 14. Rule — Business Logic Must Live in Backend

Never trust the frontend for:

```text
GST calculation
Invoice totals
Invoice numbering
Authorization
Company ownership
Tax calculations
Finalized invoice modification
Payment confirmation
Audit events
```

The frontend is a user interface.

The backend is authoritative.

---

# 15. Frontend Responsibility

Frontend should handle:

```text
Forms
Validation feedback
Navigation
Tables
Modals
User interaction
Loading states
Error presentation
Preview
Search
Filtering
```

Backend should handle:

```text
Business rules
Database
Security
Authentication
Authorization
GST calculations
Invoice numbering
Transaction integrity
Audit
```

---

# 16. API Communication

Use a centralized HTTP client.

Example:

```text
frontend/src/api/client.ts
```

It should handle:

```text
Base URL
Authentication
JSON headers
Timeout
Error normalization
401 handling
403 handling
500 handling
```

Do not create independent raw `fetch()` implementations throughout every component.

---

# 17. API Versioning

Use:

```text
/api/v1/
```

Example:

```text
GET /api/v1/company
GET /api/v1/items
POST /api/v1/invoices
```

Future:

```text
/api/v2/
```

can coexist if the API contract changes significantly.

---

# 18. API Response Convention

Use consistent response structures.

Example:

```json
{
  "success": true,
  "data": {
    "id": "ITEM-001",
    "name": "Example Item"
  }
}
```

Error:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "GSTIN is invalid",
    "fields": {
      "gstin": "Invalid GSTIN format"
    }
  }
}
```

Do not return completely different error formats from different endpoints.

---

# 19. HTTP Status Codes

Use appropriate HTTP status codes.

```text
200 → Success
201 → Created
204 → No Content
400 → Bad Request
401 → Unauthenticated
403 → Forbidden
404 → Not Found
409 → Conflict
422 → Validation Error
500 → Server Error
```

Example:

```text
Duplicate invoice number
→ 409 Conflict
```

---

# 20. Authentication Architecture

Phase 0 should establish the authentication foundation required by Phase 1.

The application should support:

```text
Company Account
User / Owner
Authentication Session
Logout
Session Expiration
```

Phase 1 will implement the actual:

```text
Company PIN Login
```

Phase 0 only establishes the secure framework.

---

# 21. PIN Security

Company PIN must never be stored as plaintext.

If a 4-digit PIN is used:

```text
User enters PIN
       ↓
Backend
       ↓
Argon2id hash verification
       ↓
Authenticated session
```

Database:

```text
pin_hash
```

Never:

```text
pin = "1234"
```

in the database.

---

# 22. PIN Rate Limiting

Because a 4-digit PIN has only:

```text
10,000 possible combinations
```

the system must protect it from brute force.

Implement:

```text
Failed attempt counter
Rate limiting
Temporary lockout
Progressive delay
Session/IP/device controls
Audit events
```

Never rely only on frontend restrictions.

---

# 23. Session Security

Prefer secure server-controlled sessions or secure, short-lived authentication tokens.

If cookies are used:

```text
HttpOnly
Secure in HTTPS
SameSite=Lax or Strict where compatible
```

Avoid storing authentication secrets in:

```text
localStorage
```

unless there is a specific security architecture requiring it.

---

# 24. Company Isolation

Every business record must belong to a company.

Conceptually:

```text
company_id
```

on:

```text
users
units
items
customers
invoices
payments
audit_logs
```

A request authenticated for Company A must never access Company B's records.

Do not trust a client-supplied:

```text
company_id
```

as authorization.

Derive it from the authenticated principal/session.

---

# 25. Authorization

Phase 0 should support permission checks.

Future roles:

```text
OWNER
ADMIN
ACCOUNTANT
SALES
VIEWER
```

Example:

```text
OWNER
→ Everything

ACCOUNTANT
→ Invoice + Payment + Reports

SALES
→ Invoice creation

VIEWER
→ Read-only
```

Permissions should be enforced in the backend.

---

# 26. Database Base Model

Recommended common fields:

```text
id
created_at
updated_at
created_by
updated_by
```

For company-owned records:

```text
company_id
```

For soft-deletable master records:

```text
is_active
```

For versioned records:

```text
version
```

Do not automatically put every possible field on every table. Use fields based on actual lifecycle requirements.

---

# 27. IDs

Use stable primary keys.

Recommended:

```text
UUID
```

or another collision-resistant identifier.

Invoice numbers should remain separate from database IDs.

Example:

```text
Database ID:
550e8400-e29b...

Invoice Number:
INV-000123
```

Never use the invoice number as the database primary key.

---

# 28. Timestamps

Store timestamps consistently.

Recommended:

```text
UTC in database
```

Convert to:

```text
Asia/Kolkata
```

for the Indian user interface.

Do not store ambiguous local timestamps without timezone context.

---

# 29. Date vs Timestamp

Use:

```text
DATE
```

for business dates such as:

```text
invoice_date
```

Use timestamp for:

```text
created_at
updated_at
finalized_at
paid_at
```

This distinction avoids unnecessary timezone problems.

---

# 30. Money Representation

Use fixed decimal values.

Never use JavaScript floating-point arithmetic as the authoritative accounting calculation.

Frontend may display:

```text
₹10,620.00
```

Backend should calculate and persist authoritative values using suitable decimal handling.

---

# 31. SQLite Money Storage

SQLite has flexible typing, so the application should enforce money representation at the application/database boundary.

Recommended approach:

```text
Store monetary values as integer minor units
```

Example:

```text
₹10620.50
```

stored as:

```text
1062050 paise
```

or use a rigorously controlled decimal representation.

The chosen strategy must be applied consistently throughout the application.

---

# 32. GSTIN Utility

Phase 0 should create a reusable GSTIN utility.

Example:

```text
app/utils/gstin.py
```

Responsibilities:

```text
Format validation
Basic structure parsing
State code extraction
PAN extraction
Registration number extraction
Checksum validation
```

Important:

GSTIN parsing is useful for validation and UI assistance, but parsed information must not blindly overwrite authoritative GST registration data.

---

# 33. GSTIN Structure

For a GSTIN such as:

```text
29AAACG1234F1Z5
```

the system can parse:

```text
29
→ State / Union Territory code

AAACG1234F
→ PAN

1
→ Entity / registration identifier

Z
→ Default character position

5
→ Checksum character
```

The application should validate the structure and checksum according to the applicable GSTIN specification.

---

# 34. GST State Master

Create a controlled state/UT master.

Example:

```text
29 → Karnataka
10 → Bihar
07 → Delhi
27 → Maharashtra
```

Do not hardcode state names in dozens of React components.

Use one authoritative backend master/configuration.

---

# 35. File Storage

Do not store large logo/PDF files directly inside SQLite unless there is a deliberate reason.

Recommended:

```text
storage/
├── company-logos/
├── invoices/
├── attachments/
└── exports/
```

Database stores metadata:

```text
file_id
company_id
path
mime_type
size
hash
created_at
```

---

# 36. Company Logo

Phase 1 requires:

```text
1 inch × 1 inch
```

logical placeholder with:

```text
1:1 aspect ratio
```

The upload system should validate:

```text
File type
File size
Image dimensions
Aspect ratio
```

The backend may normalize/crop the image for invoice rendering.

Recommended supported formats:

```text
PNG
JPEG
WEBP
```

---

# 37. File Security

Uploaded files must be validated.

Never trust:

```text
filename
extension
Content-Type
```

alone.

Validate actual file content and impose:

```text
Maximum size
Allowed MIME types
Safe filename
Storage outside executable paths
```

---

# 38. Configuration

Use environment/configuration management.

Example:

```text
.env
.env.example
```

Configuration:

```text
APP_ENV
DATABASE_URL
SECRET_KEY
SESSION_SECRET
STORAGE_PATH
LOG_LEVEL
CORS_ORIGINS
```

Never commit production secrets.

---

# 39. Settings Object

Use a central configuration class.

Example concept:

```python
class Settings(BaseSettings):
    app_env: str
    database_url: str
    secret_key: str
    storage_path: str
```

Do not scatter:

```python
"sqlite:///..."
```

throughout the codebase.

---

# 40. Environment Profiles

Support:

```text
development
testing
production
```

Example:

```text
.env.development
.env.test
.env.production
```

Production secrets should be injected through the deployment environment rather than committed to Git.

---

# 41. Logging

Create structured application logs.

Levels:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Log useful events:

```text
Server startup
Database connection
Authentication failures
Invoice finalization
Unhandled errors
Migration execution
```

Never log:

```text
PIN
Passwords
Session tokens
Private authentication secrets
Full sensitive customer data
```

---

# 42. Error Handling

Create centralized exception handling.

Business error example:

```text
InvoiceLockedError
```

should become:

```json
{
  "success": false,
  "error": {
    "code": "INVOICE_LOCKED",
    "message": "Finalized invoices cannot be edited directly."
  }
}
```

Do not expose Python tracebacks to users in production.

---

# 43. Validation

Use Pydantic for API validation.

Example:

```text
CompanyCreate
UnitCreate
ItemCreate
CustomerCreate
InvoiceCreate
InvoiceLineCreate
```

Validation should include:

```text
Required fields
Length
Format
Range
Enum values
Cross-field rules where practical
```

Business validation belongs in services.

---

# 44. Database Migration

Use Alembic from the beginning.

Never rely on:

```text
DROP DATABASE
CREATE DATABASE
```

during normal development.

Migration:

```text
Migration 001
→ companies

Migration 002
→ users

Migration 003
→ units

Migration 004
→ items
```

Later:

```text
Migration 005
→ invoices
```

---

# 45. Migration Rules

Every schema change should be represented by a migration.

Example:

```text
Add remember_me
```

must create:

```text
Alembic migration
```

rather than manually editing SQLite columns in production.

This prevents schema mismatch problems.

---

# 46. Seed Data

Phase 0 should support controlled seed data.

Possible seed data:

```text
GST States
Default Units
Default Permissions
System Configuration
```

Seed scripts must be:

```text
Idempotent
```

Running them twice should not create duplicates.

---

# 47. Predefined Units

Phase 2 will provide the complete unit system.

Phase 0 only creates the infrastructure needed to seed default units.

Examples:

```text
PCS
BOX
KG
G
LTR
ML
MTR
CM
SQFT
SQM
```

The final list should be maintained as application data/configuration rather than hardcoded into invoice components.

---

# 48. Unit Formula Engine Preparation

Phase 2 may support formulas such as:

```text
1 BOX = 12 PCS
1 KG = 1000 G
1 LTR = 1000 ML
```

Phase 0 should therefore keep unit calculations isolated in a dedicated service:

```text
UnitConversionService
```

Do not implement unit conversion logic inside invoice React components.

---

# 49. Item Architecture Preparation

Phase 3 item fields should be supported:

```text
Item Name
Unit
SKU
HSN/SAC
GST Rate
Description
```

The database model should be designed so invoice lines can snapshot these fields.

---

# 50. Customer Architecture

Although customer management may be introduced with Phase 5, Phase 0 should reserve the architecture for:

```text
customers
customer_addresses
customer_contacts
```

Future customer fields:

```text
Name
Business Name
GSTIN
PAN
Address
State
State Code
PIN
Mobile
Phone
Email
Customer Type
Credit Limit
Payment Terms
```

---

# 51. Invoice Architecture Preparation

Phase 0 should reserve:

```text
invoices
invoice_lines
invoice_series
invoice_audit_events
```

This prevents later redesign caused by mixing invoice and master data.

---

# 52. Audit Architecture

Create a generic audit model.

Recommended:

```text
audit_logs
├── id
├── company_id
├── actor_id
├── entity_type
├── entity_id
├── action
├── before_data
├── after_data
├── reason
├── ip_address
├── user_agent
└── created_at
```

Sensitive fields should be excluded or masked.

---

# 53. Audit Event Examples

```text
COMPANY_CREATED
COMPANY_UPDATED

UNIT_CREATED
UNIT_UPDATED
UNIT_DEACTIVATED

ITEM_CREATED
ITEM_UPDATED
ITEM_DEACTIVATED

INVOICE_CREATED
INVOICE_FINALIZED
INVOICE_CANCELLED

PAYMENT_CREATED
```

---

# 54. Versioning

Master data should support optimistic concurrency.

Example:

```text
version = 4
```

Client submits:

```text
version = 4
```

but database is now:

```text
version = 5
```

Return:

```text
409 CONFLICT
```

This prevents one user from overwriting another user's recent changes.

---

# 55. Soft Delete

Master data should generally use:

```text
is_active = false
```

instead of physical deletion when referenced by historical transactions.

Example:

```text
Item:
Water Bottle

Active:
false
```

Old invoices continue referencing it.

---

# 56. Hard Delete

Hard deletion should be restricted to records that:

```text
have no dependencies
```

and:

```text
are not required for audit/history.
```

Do not hard-delete finalized invoice records.

---

# 57. Frontend State Management

Do not place the entire application state into one giant global store.

Recommended split:

```text
Server State:
TanStack Query

Form State:
React Hook Form

Local UI State:
useState

Global UI/Auth State:
small dedicated store/context where necessary
```

---

# 58. Server State

Use TanStack Query for:

```text
Company data
Items
Units
Customers
Invoices
Audit logs
```

Benefits:

```text
Caching
Refetching
Loading states
Mutation handling
Query invalidation
```

---

# 59. Form Architecture

Use:

```text
React Hook Form
+
Zod
```

for complex forms.

Example:

```text
CompanyProfileForm
UnitForm
ItemForm
CustomerForm
InvoiceForm
```

Frontend validation improves UX but backend validation remains mandatory.

---

# 60. Modal Architecture

Phase 2 and Phase 3 require modal-heavy workflows.

Create reusable:

```text
Modal
Dialog
ConfirmDialog
FormModal
```

Example:

```text
Invoice
 ↓
+ Add Item
 ↓
Item Modal
 ↓
Save
 ↓
Return to Invoice
```

Do not reload the entire page after every modal operation.

---

# 61. Routing

React Router should define:

```text
/login
/setup
/dashboard
/company
/units
/items
/customers
/invoices
/invoices/new
/invoices/:id
/settings
/audit
```

Route protection:

```text
Unauthenticated
→ /login

Authenticated
→ application routes
```

---

# 62. Protected Routes

Frontend protected routes are for UX only.

Backend must independently enforce authorization.

Do not assume:

```text
ProtectedRoute
```

means the API is secure.

---

# 63. Loading States

Every network operation should support:

```text
Loading
Success
Empty
Error
```

Example:

```text
Loading invoices...
```

instead of rendering a blank page.

---

# 64. Error UX

Display useful errors.

Bad:

```text
Error 422
```

Good:

```text
GSTIN is invalid. Please check the 15-character GSTIN.
```

For server errors:

```text
Something went wrong while saving the invoice.
Please try again.
```

Technical details belong in logs.

---

# 65. Confirmation Dialogs

Use confirmation for destructive/high-impact operations:

```text
Delete Draft
Deactivate Item
Deactivate Unit
Finalize Invoice
Cancel Invoice
Create Credit Note
```

Example:

```text
Are you sure you want to finalize this invoice?

Once finalized, normal editing will be locked.

[Cancel] [Finalize]
```

---

# 66. Accessibility

The frontend should target:

```text
Keyboard accessible
Readable contrast
Focus management
Semantic HTML
Accessible labels
Accessible modal behavior
```

Particularly important for:

```text
Invoice tables
Dropdowns
Modals
Forms
Buttons
```

---

# 67. Responsive Design

The application should support:

```text
Desktop
Laptop
Tablet
Mobile
```

Priority:

```text
Desktop-first
+
Responsive mobile support
```

Invoice entry should remain usable on smaller screens.

---

# 68. Browser Support

Target modern browsers:

```text
Chrome
Edge
Firefox
Safari
```

Do not design around obsolete browser APIs.

---

# 69. Frontend Build

Development:

```text
npm run dev
```

Production:

```text
npm run build
```

Preview:

```text
npm run preview
```

---

# 70. Backend Development

Recommended:

```text
uvicorn app.main:app --reload
```

Production:

```text
uvicorn app.main:app
```

A production deployment may later use:

```text
Nginx
+
Uvicorn
```

or another appropriate ASGI deployment architecture.

---

# 71. Local Development

Recommended development environment:

```text
Browser
   ↓
React/Vite
localhost:5173
   ↓
FastAPI
localhost:8000
   ↓
SQLite
```

Configure CORS only for known development origins.

---

# 72. Production Architecture

For a local/single-server deployment:

```text
Browser
   ↓
Nginx
   ├── React Static Files
   └── /api → FastAPI
                  ↓
                SQLite
```

Recommended:

```text
HTTPS
```

for production environments.

---

# 73. Reverse Proxy

Example routing:

```text
/
→ React application

/api/
→ FastAPI

/storage/
→ Controlled document serving
```

Do not expose:

```text
data/gst_billing.db
```

directly through the web server.

---

# 74. Database Protection

The SQLite database must never be publicly accessible.

Never configure:

```text
/static → project root
```

in a way that exposes:

```text
gst_billing.db
.env
secret files
backups
```

---

# 75. CORS

Development:

```text
http://localhost:5173
```

Production should use the actual application origin.

Never use unrestricted:

```text
allow_origins=["*"]
```

with credentialed authentication.

---

# 76. CSRF

If authentication uses cookies, implement an appropriate CSRF defense for state-changing requests.

Important operations:

```text
POST
PUT
PATCH
DELETE
```

especially:

```text
Finalize invoice
Cancel invoice
Create payment
Change PIN
```

---

# 77. Security Headers

Production reverse proxy should consider:

```text
Content-Security-Policy
X-Content-Type-Options
Referrer-Policy
Strict-Transport-Security
Frame restrictions
```

The exact policy should be tested against the application.

---

# 78. Password / PIN Secrets

Never commit:

```text
SECRET_KEY
SESSION_SECRET
Database credentials
API credentials
Payment credentials
GST integration credentials
```

to Git.

Use:

```text
Environment Variables
Secret Manager
Deployment Secrets
```

---

# 79. Git Repository

Recommended:

```text
.gitignore
```

must exclude:

```text
.env
.env.*
*.db
*.sqlite
*.sqlite3
storage/
uploads/
__pycache__/
node_modules/
dist/
.venv/
```

Do not ignore migration files.

---

# 80. Project Root

Recommended final structure:

```text
gst-billing/
├── backend/
├── frontend/
├── data/
├── storage/
├── docs/
├── scripts/
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.yml   # optional future deployment
```

---

# 81. Documentation

Create:

```text
docs/
├── architecture.md
├── database.md
├── api.md
├── security.md
├── deployment.md
├── invoice-rules.md
└── phases/
    ├── phase-0.md
    ├── phase-1.md
    ├── phase-2.md
    ├── phase-3.md
    ├── phase-4.md
    └── phase-5.md
```

---

# 82. API Documentation

FastAPI should expose:

```text
/docs
```

for Swagger UI during development.

Also:

```text
/openapi.json
```

for the OpenAPI specification.

Production access to interactive API documentation can be restricted if appropriate.

---

# 83. Health Endpoint

Create:

```text
GET /api/v1/health
```

Example:

```json
{
  "status": "ok"
}
```

Future checks:

```text
Database
Storage
Application
```

---

# 84. Readiness Endpoint

Optional:

```text
GET /api/v1/ready
```

can verify:

```text
Database reachable
Storage accessible
Required configuration available
```

Useful for deployment and monitoring.

---

# 85. Testing Strategy

Testing must start in Phase 0.

Use:

```text
pytest
pytest-asyncio
httpx
```

Backend tests:

```text
Unit Tests
Service Tests
Repository Tests
API Tests
Integration Tests
```

Frontend:

```text
Vitest
React Testing Library
```

End-to-end:

```text
Playwright
```

---

# 86. Minimum Backend Test Coverage

Before Phase 1:

```text
Database connection
Migration
Health endpoint
Validation
Authentication foundation
Company isolation
Audit logging
Error handling
```

---

# 87. Minimum Frontend Test Coverage

Before Phase 1:

```text
Application startup
Routing
Login route
Protected route
API error handling
Modal opening/closing
Form validation
```

---

# 88. Invoice Testing Preparation

Phase 0 should establish test utilities for:

```text
Money calculations
GST calculations
Date handling
Database transactions
Authentication
Company isolation
```

This becomes extremely important in Phase 5.

---

# 89. Test Database

Tests should use a separate database.

Do not run tests against:

```text
production gst_billing.db
```

Recommended:

```text
tests/test.db
```

or an isolated temporary database.

---

# 90. Transaction Testing

Test:

```text
Successful transaction
Rollback
Duplicate request
Concurrent request
Validation failure
Database failure
```

Especially for invoice finalization.

---

# 91. Backup System

Phase 0 should define a backup architecture.

SQLite backup should include:

```text
Database
```

and separately:

```text
Invoice PDFs
Company logos
Attachments
```

A database backup without document storage may be incomplete.

---

# 92. Backup Naming

Example:

```text
backup/
├── 2026-08-10/
│   ├── gst_billing.db
│   └── storage.tar
```

Backups should be timestamped and protected.

---

# 93. Backup Verification

A backup is not considered valid merely because the file exists.

Periodically test:

```text
Restore backup
Run migrations/checks
Open database
Verify invoices
Verify files
```

---

# 94. Database Integrity Check

Provide an administrative utility for:

```text
SQLite integrity check
Foreign-key check
Migration version check
```

Conceptually:

```text
PRAGMA integrity_check;
PRAGMA foreign_key_check;
```

---

# 95. Migration Safety

Before production migration:

```text
Backup database
 ↓
Run migration
 ↓
Run integrity check
 ↓
Run application smoke test
```

Never blindly apply destructive schema migrations.

---

# 96. Static Type Checking

Backend:

```text
mypy
```

or another Python type checker.

Frontend:

```text
tsc --noEmit
```

The project should not knowingly accumulate large numbers of type errors.

---

# 97. Code Formatting

Python:

```text
Ruff
Black
```

Frontend:

```text
Prettier
ESLint
```

Recommended pre-commit checks:

```text
Formatting
Linting
Type checking
Tests
```

---

# 98. Dependency Management

Python:

```text
pyproject.toml
```

Frontend:

```text
package.json
package-lock.json
```

Pin or constrain important production dependencies appropriately.

Do not randomly install packages for every small feature.

---

# 99. Recommended Python Dependencies

Conceptually:

```text
fastapi
uvicorn
sqlalchemy
alembic
pydantic
pydantic-settings
argon2-cffi
python-multipart
httpx
pytest
```

Additional packages should be introduced only when their functionality is required.

---

# 100. Recommended Frontend Dependencies

Conceptually:

```text
react
react-dom
react-router-dom
@tanstack/react-query
react-hook-form
zod
```

Optional:

```text
tailwindcss
lucide-react
date-fns
```

Do not add large UI frameworks without evaluating bundle size and maintainability.

---

# 101. Dependency Security

Regularly check:

```text
npm audit
pip audit
```

or equivalent dependency-security tooling.

Do not blindly upgrade every dependency in production.

Test upgrades before deployment.

---

# 102. API Contract

Frontend and backend must share a defined contract.

Preferred:

```text
OpenAPI
```

The frontend types can eventually be generated from the API specification where beneficial.

This reduces mismatches such as:

```text
Backend:
gst_rate

Frontend:
gstRate
```

without a defined transformation layer.

---

# 103. Naming Convention

Backend Python:

```text
snake_case
```

Example:

```python
invoice_number
```

Frontend TypeScript:

```text
camelCase
```

Example:

```typescript
invoiceNumber
```

If API uses snake_case, standardize whether frontend uses the same shape or a deliberate serialization layer.

Do not mix naming conventions randomly.

---

# 104. API Resource Naming

Use plural nouns:

```text
/api/v1/companies
/api/v1/units
/api/v1/items
/api/v1/customers
/api/v1/invoices
```

Actions can use explicit endpoints:

```text
POST /api/v1/invoices/{id}/finalize
POST /api/v1/invoices/{id}/cancel
```

---

# 105. No Business Logic in SQL Queries

Avoid encoding complex GST logic directly into SQL.

Prefer:

```text
TaxService
InvoiceCalculationService
```

Python business services should remain testable independently of SQLite.

---

# 106. No Business Logic in React

Avoid:

```typescript
if (state === "Karnataka") {
    cgst = ...
}
```

inside invoice UI components.

Instead:

```text
React
 ↓
Backend calculation API
 ↓
Authoritative result
```

The frontend may perform provisional calculations for responsiveness, but final calculations come from the backend.

---

# 107. Reusable Business Services

Recommended services:

```text
GSTINService
CompanyService
UnitService
UnitConversionService
ItemService
CustomerService
TaxService
InvoiceCalculationService
InvoiceNumberService
InvoiceService
AuditService
FileStorageService
```

Each should have one clear responsibility.

---

# 108. Dependency Injection

FastAPI dependencies should be used for:

```text
Database session
Authenticated principal
Company context
Authorization
Services
```

Example concept:

```text
get_db()
get_current_user()
get_current_company()
require_permission()
```

---

# 109. Current Company Context

After authentication, the backend should derive:

```text
current_user
current_company
```

from the authenticated session.

Do not require every frontend request to manually submit:

```text
company_id
```

for authorization.

---

# 110. Multi-Company Future Readiness

Even if Phase 1 initially supports one company per account, the database should be structured so that:

```text
Company A
Company B
```

can coexist without architectural redesign.

All company-owned data should be scoped.

---

# 111. Audit and Privacy

Audit logs should not unnecessarily store:

```text
PIN
Password
Authentication token
Full payment secrets
```

For sensitive fields:

```text
MASK
REDACT
HASH
```

as appropriate.

---

# 112. Time Zone

Application timezone:

```text
Asia/Kolkata
```

Display:

```text
IST
```

Store timestamps in UTC where practical.

Business dates remain local calendar dates.

---

# 113. Currency and Locale

Initial locale:

```text
en-IN
```

Currency:

```text
INR
```

Number formatting:

```text
₹1,00,000.00
```

The frontend should use locale-aware formatting rather than manual string concatenation.

---

# 114. PDF Architecture

PDF generation should be a backend responsibility.

Possible architecture:

```text
Invoice Data
   ↓
HTML Template
   ↓
PDF Renderer
   ↓
PDF File
```

The frontend should request:

```text
GET /api/v1/invoices/{id}/pdf
```

rather than implementing accounting PDF generation in React.

---

# 115. Browser Print

For print:

```text
Invoice Preview
 ↓
Browser Print
```

The application can use:

```text
window.print()
```

or a print-specific route/layout.

The backend remains responsible for authoritative invoice data.

---

# 116. PDF Preview

The application should support browser-native PDF viewing where practical.

Workflow:

```text
Invoice
 ↓
Generate PDF
 ↓
Browser PDF Viewer
 ↓
Print / Download
```

---

# 117. Storage Service

Create:

```text
FileStorageService
```

Responsibilities:

```text
Save
Read
Delete where permitted
Hash
Validate
Generate safe paths
```

Business modules should not manually construct arbitrary filesystem paths.

---

# 118. Path Safety

Never trust a user-supplied path.

Avoid:

```text
../../database.db
```

style path traversal.

Generate storage paths from trusted IDs.

Example:

```text
storage/company/{company_id}/logos/{file_id}.png
```

---

# 119. Database Backup vs Document Backup

These are separate:

```text
Database backup
+
File storage backup
```

Both are required for complete restoration.

---

# 120. Development Scripts

Create:

```text
scripts/
├── dev_backend.sh
├── dev_frontend.sh
├── migrate.sh
├── seed.sh
├── backup.sh
├── restore.sh
└── test.sh
```

Windows equivalents can be provided later if required.

---

# 121. One-Command Development

Optional root command:

```text
make dev
```

or:

```text
npm run dev:all
```

that starts:

```text
Frontend
+
Backend
```

This is a development convenience only.

---

# 122. Health Monitoring

Future production monitoring can check:

```text
Application health
Database health
Storage health
Disk space
Backup freshness
```

SQLite disk space is particularly important because:

```text
Database
+
WAL
+
PDF storage
```

can grow over time.

---

# 123. Disk Management

The application should not allow uncontrolled growth of:

```text
PDF files
Temporary files
Logs
Backups
Exports
```

Implement retention policies for temporary data.

Do not automatically delete legally required accounting records.

---

# 124. Temporary Files

Use a dedicated:

```text
tmp/
```

directory.

Temporary invoice PDFs should be cleaned after their lifecycle.

---

# 125. Production Error Reporting

Production errors should be logged with:

```text
request ID
timestamp
endpoint
user/company context where safe
exception type
```

Do not expose stack traces to the browser.

---

# 126. Request ID

Every API request should ideally have:

```text
X-Request-ID
```

or an equivalent correlation ID.

This makes debugging easier:

```text
Frontend Error
 ↓
Request ID
 ↓
Backend Log
 ↓
Database Event
```

---

# 127. Concurrency

SQLite can support multiple readers and limited concurrent writers, but write operations must be designed carefully.

Critical operations:

```text
Invoice finalization
Invoice numbering
Payment recording
Settings updates
```

should use proper database transactions.

---

# 128. SQLite Limit

Phase 0 should explicitly document:

```text
SQLite is the initial database.
```

It is ideal for:

```text
Local deployment
Single-server application
Small business
Low-to-moderate concurrency
```

If the application becomes:

```text
Large multi-user SaaS
Many concurrent writers
Multiple application servers
```

then PostgreSQL should be evaluated.

---

# 129. Database Portability

Use SQLAlchemy models and services so the migration path becomes:

```text
SQLite
   ↓
PostgreSQL
```

with minimal business-layer changes.

Avoid SQLite-only SQL wherever possible.

---

# 130. Phase 0 Initial Tables

Recommended initial tables:

```text
companies
users
sessions
permissions
roles
audit_logs
app_settings
```

Phase 2:

```text
units
unit_conversions
```

Phase 3:

```text
items
```

Phase 5:

```text
customers
invoices
invoice_lines
invoice_series
payments
credit_notes
debit_notes
```

---

# 131. Initial Company Table

Conceptually:

```text
companies
├── id
├── legal_name
├── trade_name
├── ownership_type
├── gstin
├── pan
├── address
├── state
├── state_code
├── pincode
├── mobile
├── office_phone
├── email
├── authorized_person
├── logo_file_id
├── status
├── created_at
├── updated_at
└── version
```

Phase 1 can expand this model.

---

# 132. User Table

Conceptually:

```text
users
├── id
├── company_id
├── name
├── mobile
├── email
├── pin_hash
├── role_id
├── is_active
├── created_at
└── updated_at
```

If one account can manage multiple companies, use a separate membership table:

```text
company_users
```

rather than duplicating users.

---

# 133. Session Table

Conceptually:

```text
sessions
├── id
├── user_id
├── company_id
├── token_hash
├── created_at
├── expires_at
├── last_seen_at
├── revoked_at
└── metadata
```

Store only what is necessary.

Authentication secrets should not be stored in plaintext.

---

# 134. App Settings

Global application settings:

```text
app_settings
├── key
├── value
├── type
├── updated_at
└── updated_by
```

Company settings should be company-scoped instead of mixing global and company-specific configuration.

---

# 135. Migration from Phase to Phase

Each phase should extend the database without breaking previous phases.

Example:

```text
Phase 0
 ↓
Base schema
 ↓
Phase 1 migration
 ↓
Phase 2 migration
 ↓
Phase 3 migration
 ↓
Phase 4 migration
 ↓
Phase 5 migration
```

Never rebuild the database manually between phases once real user data exists.

---

# 136. API Backward Compatibility

When modifying an existing API:

```text
Do not silently change response structure.
```

Use:

```text
Versioning
```

or backward-compatible fields.

Example:

```text
/api/v1/items
```

remains stable while:

```text
/api/v2/items
```

introduces breaking changes.

---

# 137. Frontend Component Rules

Components should generally follow:

```text
Presentation
↓
Props
↓
Hooks
↓
API
```

Avoid giant components such as:

```text
InvoicePage.tsx
```

containing:

```text
1,500+ lines
```

Split into:

```text
InvoiceHeader
InvoiceCustomer
InvoiceItemTable
InvoiceTotals
InvoiceActions
```

---

# 138. Custom Hooks

Examples:

```text
useCompany()
useUnits()
useItems()
useCustomers()
useInvoice()
useInvoiceCalculation()
useAuth()
usePermissions()
```

Hooks should encapsulate reusable UI/application behavior.

---

# 139. API Query Keys

Use structured query keys.

Example:

```text
["items", companyId]
["customers", companyId]
["invoice", invoiceId]
["invoices", filters]
```

This prevents stale data problems.

---

# 140. Cache Invalidation

When an item changes:

```text
Update item
 ↓
Invalidate item list
```

When invoice is finalized:

```text
Finalize
 ↓
Invalidate invoice list
 ↓
Invalidate invoice detail
```

---

# 141. Optimistic Updates

Use carefully.

Safe candidates:

```text
UI-only preferences
```

Use caution for:

```text
Invoice finalization
Payment
Cancellation
Tax changes
```

Financial operations should generally wait for authoritative backend confirmation.

---

# 142. Financial Operation UX

For:

```text
Finalize
Cancel
Credit Note
Debit Note
Payment
```

show:

```text
Submitting...
```

and disable duplicate submission.

After success:

```text
Success
 ↓
Refresh authoritative state
```

---

# 143. Phase 0 Security Checklist

```text
□ HTTPS-ready architecture
□ Secure session design
□ PIN hashing
□ PIN brute-force protection
□ Company isolation
□ Backend authorization
□ CSRF protection where cookies are used
□ CORS restricted
□ Secrets outside Git
□ File upload validation
□ Path traversal protection
□ SQL injection protection via ORM/parameterization
□ Sensitive logging disabled
□ Database not publicly accessible
□ Production error masking
```

---

# 144. Phase 0 Database Checklist

```text
□ SQLite configured
□ Foreign keys enabled
□ WAL configured
□ Migration system installed
□ Base models created
□ Timestamps standardized
□ Company scoping established
□ Audit table established
□ Index strategy established
□ Backup strategy established
□ Restore procedure documented
```

---

# 145. Phase 0 Frontend Checklist

```text
□ React + TypeScript
□ Vite
□ Router
□ API client
□ Query management
□ Form validation
□ Error handling
□ Loading states
□ Modal system
□ Protected routes
□ Responsive layout
□ Accessibility foundation
□ ESLint
□ Prettier
□ Type checking
```

---

# 146. Phase 0 Backend Checklist

```text
□ Python
□ FastAPI
□ Uvicorn
□ SQLAlchemy
□ Alembic
□ Pydantic
□ Configuration management
□ Security module
□ Authentication foundation
□ Authorization foundation
□ API versioning
□ Error handling
□ Logging
□ Health endpoint
□ Testing
```

---

# 147. Phase 0 Completion Criteria

Phase 0 is complete only when the following works:

```text
1. Backend starts successfully.

2. Frontend starts successfully.

3. Frontend can communicate with backend.

4. SQLite database is created through migrations.

5. Database foreign keys are enforced.

6. Health API responds successfully.

7. API documentation is available in development.

8. Authentication foundation exists.

9. Secure PIN hashing mechanism exists.

10. Company isolation architecture exists.

11. Audit architecture exists.

12. File storage architecture exists.

13. Frontend routing exists.

14. Protected-route architecture exists.

15. API client exists.

16. Error handling exists.

17. Loading states exist.

18. Form validation exists.

19. Automated tests execute successfully.

20. Database backup/restore process is documented.

21. Development and production configuration are separated.

22. Secrets are excluded from Git.

23. Database migrations execute successfully.

24. The project can be extended to Phase 1 without restructuring the entire codebase.
```

---

# 148. Phase 0 Development Sequence

Implement in this order:

```text
STEP 1
Create repository

STEP 2
Create backend project

STEP 3
Create FastAPI application

STEP 4
Create configuration system

STEP 5
Create SQLite connection

STEP 6
Create SQLAlchemy base

STEP 7
Create Alembic

STEP 8
Create initial migration

STEP 9
Create health endpoint

STEP 10
Create authentication foundation

STEP 11
Create company context

STEP 12
Create authorization foundation

STEP 13
Create audit framework

STEP 14
Create file storage service

STEP 15
Create React + TypeScript application

STEP 16
Create routing

STEP 17
Create API client

STEP 18
Create authentication state

STEP 19
Create protected routes

STEP 20
Create reusable UI components

STEP 21
Create testing infrastructure

STEP 22
Create backup/restore scripts

STEP 23
Run complete integration test

STEP 24
Freeze Phase 0 architecture

STEP 25
Begin Phase 1
```

---

# 149. Recommended Initial Git Commits

Suggested commits:

```text
chore: initialize project structure

feat: initialize FastAPI backend

feat: initialize React TypeScript frontend

feat: add SQLite and SQLAlchemy

feat: add Alembic migrations

feat: add configuration management

feat: add authentication foundation

feat: add company isolation

feat: add audit framework

feat: add file storage service

test: add backend test infrastructure

test: add frontend test infrastructure

docs: add Phase 0 architecture
```

---

# 150. Golden Architecture Rule

The most important Phase 0 rule is:

```text
SEPARATE UI
FROM
BUSINESS LOGIC
FROM
DATABASE ACCESS.
```

Use:

```text
React
   ↓
API
   ↓
FastAPI Router
   ↓
Service
   ↓
Repository / SQLAlchemy
   ↓
SQLite
```

Never build the application as:

```text
React
   ↓
SQL
```

or:

```text
React
   ↓
Random Python endpoint
   ↓
Business logic mixed with SQL
```

---

# 151. Final Phase 0 Architecture

```text
                           USER
                            │
                            ↓
                    ┌───────────────┐
                    │    Browser    │
                    └───────┬───────┘
                            │
                            ↓
                 ┌────────────────────┐
                 │ React + TypeScript │
                 │      + Vite       │
                 └─────────┬──────────┘
                           │
                        HTTPS
                           │
                           ↓
                 ┌────────────────────┐
                 │      Nginx         │
                 │   Production       │
                 └─────────┬──────────┘
                           │
                           ↓
                 ┌────────────────────┐
                 │      FastAPI       │
                 │      /api/v1       │
                 └─────────┬──────────┘
                           │
          ┌────────────────┼─────────────────┐
          ↓                ↓                 ↓
    Authentication      Services          Audit
          │                │                 │
          │        ┌───────┼────────┐        │
          │        ↓       ↓        ↓        │
          │      Company  GST     Invoice    │
          │      Units    Item     Payment   │
          │        │       │        │        │
          └────────┴───────┴────────┴────────┘
                           │
                           ↓
                  SQLAlchemy 2.x
                           │
                           ↓
                    ┌────────────┐
                    │   SQLite   │
                    │   WAL      │
                    └────────────┘

                           +
                           │
              ┌────────────┴────────────┐
              ↓                         ↓
        File Storage              Backup System
        ├── Logos                 ├── Database
        ├── PDFs                  └── Documents
        └── Attachments
```

---

# 152. Final Technology Decision

For this GST billing application, the recommended Phase 0 stack is:

| Layer | Technology |
|---|---|
| Frontend | React |
| Language | TypeScript |
| Build | Vite |
| Routing | React Router |
| Server State | TanStack Query |
| Forms | React Hook Form |
| Schema Validation | Zod |
| UI | Tailwind CSS or component library |
| Backend | Python |
| API | FastAPI |
| ASGI Server | Uvicorn |
| Validation | Pydantic |
| ORM | SQLAlchemy 2.x |
| Migration | Alembic |
| Database | SQLite |
| Authentication | Secure session architecture |
| PIN Hashing | Argon2id |
| PDF | Backend PDF service |
| Testing Backend | Pytest |
| Testing Frontend | Vitest + React Testing Library |
| E2E | Playwright |
| Linting Python | Ruff |
| Formatting Python | Black/Ruff formatter |
| Linting Frontend | ESLint |
| Formatting Frontend | Prettier |
| API Documentation | OpenAPI / Swagger |
| Reverse Proxy | Nginx |
| Version Control | Git |

---

# 153. Phase Dependency Map

```text
                         PHASE 0
                  Technical Foundation
                          │
        ┌─────────────────┼──────────────────┐
        ↓                 ↓                  ↓
    Backend            Frontend           Database
    Python             React/TS            SQLite
        │                 │                  │
        └─────────────────┼──────────────────┘
                          ↓
                       PHASE 1
                Company Account + PIN
                          ↓
                       PHASE 2
                    Unit Engine
                          ↓
                       PHASE 3
                  Item / SKU Master
                          ↓
                       PHASE 4
               Universal Modification
                          ↓
                       PHASE 5
              GST Invoice Generation
                          ↓
             Future Accounting Modules
```

---

# 154. Important Product Direction

The application should be developed as a **modular accounting platform**, not as a collection of independent CRUD screens.

The architecture should therefore preserve clear boundaries:

```text
MASTER DATA
    ↓
Company
Units
Items
Customers

TRANSACTION DATA
    ↓
Invoices
Payments
Credit Notes
Debit Notes

REPORTING DATA
    ↓
GST Reports
Sales Reports
Customer Statements
Tax Summaries

SYSTEM DATA
    ↓
Users
Sessions
Permissions
Audit
Settings
```

The most important architectural principle is:

```text
MASTER DATA CAN CHANGE.

HISTORICAL TRANSACTIONS MUST REMAIN HISTORICALLY CORRECT.
```

This principle must be enforced at the backend, database, API, frontend and reporting layers.

---

# 155. Phase 0 Final Deliverable

At the end of Phase 0, the repository should look approximately like:

```text
gst-billing/
│
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── tests/
│   ├── pyproject.toml
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── data/
│   └── .gitkeep
│
├── storage/
│   └── .gitkeep
│
├── docs/
│   ├── architecture.md
│   ├── database.md
│   ├── security.md
│   └── phases/
│       ├── phase-0.md
│       ├── phase-1.md
│       ├── phase-2.md
│       ├── phase-3.md
│       ├── phase-4.md
│       └── phase-5.md
│
├── scripts/
│   ├── backup.sh
│   ├── restore.sh
│   ├── migrate.sh
│   └── test.sh
│
├── .env.example
├── .gitignore
└── README.md
```

Once this foundation is stable, **Phase 1 should implement Company Account Creation, Company Profile, GSTIN parsing/validation assistance, secure 4-digit PIN authentication, company dashboard and the associated database/API/UI layers without changing the fundamental Phase 0 architecture.**

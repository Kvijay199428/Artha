Worked for 13s

I reviewed the attached artha (6).md source rather than relying only on the log excerpt. There are two separate problems here: the immediate production 400 OPTIONS failure, and several setup-flow/schema issues that should be corrected together in Phase 11.

The existing source already has a substantial GST module, PIN hashing, company logo storage, bank account type component, and company/address models, so this should be treated as a correction/refactoring phase, not a completely new implementation.  

Phase 11 — Company Setup, Authentication, Routing & Schema Stabilization

11.1 — Fix the immediate OPTIONS ... 400 Bad Request

This is the most important issue in your log:

OPTIONS /api/v1/auth/login 400 Bad Request
OPTIONS /api/v1/auth/setup 400 Bad Request

Your frontend is currently using:

VITE_API_URL
        ↓
hostname:28030/api/v1

when no environment variable is supplied. 

Meanwhile, the backend CORS configuration defaults to only:

http://localhost:5173



That is a production configuration mismatch.

Correct architecture

Production should have:

Browser
   │
   │ HTTPS/HTTP
   ▼
Nginx :28031
   │
   ├── /              → frontend
   │
   └── /api/          → backend :8000

Then the browser should preferably call:

/api/v1/auth/login
/api/v1/auth/setup
/api/v1/gst/...

rather than constructing a separate :28030 URL.

Fix frontend API base

Use environment configuration:

VITE_API_URL=/api/v1

for same-origin production.

Then:

axios baseURL = /api/v1

This removes the browser-to-different-origin CORS problem entirely.

For development:

VITE_API_URL=http://localhost:8000/api/v1

or whatever development backend is actually exposed.

Backend CORS

Keep explicit origins for development, but don't use CORS as a workaround for a badly routed production API.

For example:

Development:
http://localhost:5173

Production:
https://your-domain

If you're currently accessing the application through the IP/port shown in the logs, that exact origin must be accounted for during testing.

Do not solve this with allow_origins=["*"] while allow_credentials=True.


---

11.2 — Verify API routing

The backend routing itself is structurally correct:

/api
  └── /v1
       └── /auth
            ├── /setup
            ├── /login
            ├── /me
            ├── /pin-change
            └── /logout

The source explicitly registers /v1 and includes auth.router.  

Therefore:

POST /api/v1/auth/login
POST /api/v1/auth/setup

are the correct backend endpoints.

The 400 OPTIONS indicates the request is failing before reaching the actual POST handler, strongly pointing to the CORS/origin/preflight configuration rather than AuthService.authenticate() itself.


---

11.3 — Fix PIN validation UX

The backend already correctly detects:

Incorrect PIN

and increments failed attempts. After five failed attempts it locks the account for 15 minutes. 

The problem is that the frontend currently only displays a generic API error area.

Change it to immediate field-level feedback.

Required behavior

User enters:

1234

When four digits are entered:

PIN
┌──────────────┐
│ • • • •      │
└──────────────┘

✕ Incorrect PIN

If correct:

✓ PIN verified

Important security consideration

Do not send a request after every individual digit.

Use:

4 digits entered
       ↓
submit/verify
       ↓
incorrect
       ↓
immediately show:
"Incorrect PIN"

The server remains authoritative.

Also keep the existing server-side lockout.


---

11.4 — Login PIN field

Restrict it to:

4 digits
numeric keyboard
maxlength=4

and normalize input:

/[^\d]/g

The frontend should never allow:

12ab
12345
12-3

The backend should independently enforce the same rule.


---

11.5 — Company Setup becomes a multi-tab wizard

The current SetupPage is one large form. The source confirms everything is currently presented in one page, including basic details, address, bank and security. 

Replace this with:

Tab 1 — Business

Business Information

Fields:

Company/Legal name

Trade name

Ownership type

Authorized person

Designation



---

Tab 2 — Tax & GST

GST & Tax Identity

Fields:

GST Registered toggle

GSTIN

GST state code

State

PAN

TAN


GSTIN should automatically populate:

GSTIN
   ↓
State Code
   ↓
State
   ↓
PAN

Your existing backend already performs GST validation and extracts state/PAN. 


---

Tab 3 — Address

Registered Address

Fields:

Address line 1

Address line 2

City

State

District

Pincode

Country


Critical district behavior

Initial state:

State:   [ Select/Waiting ]
District: [ Disabled ]

After GSTIN is valid:

GSTIN
   ↓
State Code
   ↓
State automatically populated
   ↓
District ENABLED

So:

stateAutoFilled === true
        ↓
district disabled = false

Otherwise:

district disabled = true

When state changes/reset:

district = ""
district disabled = true


---

11.6 — District data should be state-aware

Don't use a free-text district field if you want reliable accounting data.

Use:

State
   ↓
District list

For example:

Karnataka
   ↓
Bengaluru Urban
Bengaluru Rural
Anekal
...

The exact administrative master should be maintained separately from the GST state master.

The current database already has district on CompanyAddress, so a schema column isn't missing. 

The missing part is primarily controlled state→district behavior in the UI/data master.


---

11.7 — Tab 4: Contact

Fields:

Required

Mobile number

Email


Optional

Office contact

Website


Mobile and office phone should use the same international phone component.

Store canonical E.164 values where possible:

+919876543210

rather than relying only on a display-formatted number.


---

11.8 — Tab 5: Security

Security

Fields:

Create PIN
Confirm PIN

Both:

4 digits

Validation:

PIN = 1234
Confirm = 1234
        ↓
✓ PINs match

Otherwise:

✕ PINs don't match

The existing schema already validates four-digit numeric PINs and matching confirmation. 


---

11.9 — Optional tab: Bank Details

Bank details should now genuinely be optional.

Currently the setup schema requires:

bank_account_holder_name
bank_account_number
bank_ifsc
bank_name
bank_branch
bank_account_type



That contradicts your requirement.

Change to:

Bank Details
────────────
Optional

All bank fields nullable/optional.

If the user doesn't want bank details:

Skip

must work.

If they provide bank details:

Account Type
[ Current Account ▼ ]

and validate them.


---

11.10 — Optional company logo

Company logo is also optional.

The existing backend already has a proper logo processing pipeline:

MIME validation

corruption validation

minimum dimensions

square crop

600×600 standardization

WebP storage. 


So do not rebuild the backend logo processor.

Only improve the UI and setup workflow.


---

11.11 — Company logo requirement

UI:

┌──────────────┐
        │              │
        │    LOGO      │
        │              │
        └──────────────┘

        1 : 1

Accept:

PNG
JPEG
WebP

Automatically crop to square.

For PDF output:

1" × 1"

The existing 600×600 standardization is suitable for the stored asset. 


---

11.12 — Light/Dark theme

Implement a centralized theme system rather than individual page colors.

Use:

Light
Dark
System

The setup/login UI should use semantic classes/tokens:

bg-background
text-foreground
bg-card
border-border
text-muted
bg-primary

rather than repeatedly using:

bg-white
text-gray-900
bg-gray-50

The current SetupPage is heavily hard-coded with light-mode colors. 

That is why dark mode will otherwise become inconsistent.


---

11.13 — Fix button visibility/alignment

Create one common button hierarchy:

Primary
Secondary
Ghost
Danger

Example:

[ Back ]              [ Save & Continue ]

instead of buttons appearing with inconsistent widths and contrast.

Mobile:

┌──────────────────────────────┐
│        Save & Continue       │
└──────────────────────────────┘

Desktop:

[Back]                    [Save & Continue]

The button should remain visually obvious in both themes.


---

11.14 — Artha navbar branding

The navbar should display the application identity as:

[logo] ARTHA

with ARTHA in uppercase.

Use a soft professional palette rather than harsh saturated colors.

For example conceptually:

ARTHA

with soft neutral/blue/teal accents.

The logo should be subtle rather than oversized.


---

11.15 — Logo wave animation

During company setup:

logo
   → → → → →
fade in/out

Animation:

left → right
+
soft opacity fade

Do not use this animation permanently throughout the dashboard.


---

11.16 — Company creation transition

When the user presses:

Complete Setup

and the backend successfully creates the company:

Setup form
    ↓
5-second transition
    ↓
center ARTHA animated logo
    ↓
"Company creation is in progress…"
    ↓
redirect/login

The screen should have:

backdrop-filter: blur(...)

with a translucent glass panel.

Example:

┌──────────────────────────────────────┐
│                                      │
│              [ ARTHA ]               │
│                                      │
│       Company creation is on         │
│                                      │
│              • • •                   │
│                                      │
└──────────────────────────────────────┘


---

11.17 — Important correction regarding the 5-second rate limit

Don't implement this as a client-only:

setTimeout(...)

and call it a security rate limit.

Separate the two concepts:

UI transition

Exactly:

5 seconds

API protection

Server-side:

company setup endpoint
       ↓
one successful company creation
       ↓
company exists
       ↓
future setup requests → reject

The current backend already prevents creating a second company by checking whether a company exists. 

You can additionally add an explicit short request throttle if required.


---

11.18 — Database schema audit

This is important because the current application is doing:

Base.metadata.create_all(bind=engine)

on startup. 

That is not a sufficient production migration strategy.

You also have Alembic configured:

script_location = migrations



Phase 11 must move schema management toward:

Alembic migration
       ↓
database revision
       ↓
upgrade
       ↓
application startup

rather than relying on:

create_all()

for production schema evolution.


---

11.19 — Current database situation

The log shows the database successfully creating:

returns
return_settlements
estimate_lines
gst_state_codes
gst_rates
unit_categories

and then starting Uvicorn successfully.

So this is not a general database startup failure.

The database seeding is also working:

Database seeding completed.

and the GST state table contains entries including:

29 → Karnataka
36 → Telangana
37 → Andhra Pradesh
38 → Ladakh

as reflected in the source/database seed behavior. 


---

11.20 — But there is a schema problem to correct

Your setup schema currently requires bank details:

bank_account_holder_name
bank_account_number
bank_ifsc
bank_name
bank_branch
bank_account_type

while you now want them optional.

That requires synchronized changes to:

Frontend Zod schema
        ↓
TypeScript SetupForm
        ↓
FastAPI CompanySetupRequest
        ↓
CompanyService
        ↓
CompanyBankAccount
        ↓
database nullability

Currently CompanyService.create_company() always creates a bank account. 

That must change to:

if bank details supplied:
    create CompanyBankAccount
else:
    don't create bank account


---

11.21 — Company creation transaction

Company creation should be atomic:

BEGIN
 │
 ├── Company
 ├── GST details
 ├── Address
 ├── Bank (if supplied)
 └── Auth/PIN
 │
 └── COMMIT

If any operation fails:

ROLLBACK

The current implementation performs all these operations before the final commit, which is good, but Phase 11 should explicitly test rollback behavior. 


---

11.22 — Schema relationship to preserve

The existing model structure is already appropriate:

Company
 │
 ├── CompanyGSTDetail
 ├── CompanyAddress
 ├── CompanyBankAccount
 ├── CompanyAuth
 ├── CompanySession
 └── CompanyAsset

The model registry already imports these company models. 

Therefore do not flatten these into one giant companies table.

Keep the separation.


---

11.23 — Fix /404 handling

There are two different 404 scenarios.

Frontend 404

For:

/setup
/login
/dashboard
/invoices
/quotations
/boq

Nginx must return the SPA entry point:

index.html

for unknown frontend routes.

Otherwise browser refresh on:

/quotations

can produce an Nginx 404.

API 404

For:

/api/v1/unknown

Nginx must not return index.html.

It should pass through to FastAPI and return:

{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Endpoint not found"
  }
}

This distinction is essential.


---

11.24 — Nginx routing model

Use:

location /api/ {
    proxy_pass http://backend:8000;
}

location / {
    try_files $uri $uri/ /index.html;
}

Conceptually:

/api/*       → backend
/assets/*    → frontend static assets
/favicon.*   → frontend
/*           → React SPA

This also eliminates the need for the frontend to know backend port 28030 in production.


---

11.25 — Health verification

Before declaring Phase 11 complete, verify:

GET /health

returns:

{
  "status": "ok"
}

The endpoint already exists. 

Then test:

GET  /api/v1/gst/states
GET  /api/v1/gst/validate/{gstin}
POST /api/v1/auth/setup
POST /api/v1/auth/login


---

11.26 — Final Phase 11 flow

The finished setup experience should be:

ARTHA
                      │
                      ▼
               Company Setup
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
   Business       GST & Tax       Address
       │              │              │
       │         GSTIN validation     │
       │              │              │
       │         State auto-fill      │
       │              │              │
       │         PAN extraction       │
       │              │              │
       └──────────────┼──────────────┘
                      ▼
                   Contact
                      │
                      ▼
                  Security
                      │
                      ▼
             Optional Bank Details
                      │
                      ▼
              Optional Company Logo
                      │
                      ▼
               Complete Setup
                      │
                      ▼
              Backend transaction
                      │
                      ▼
             ┌──────────────────┐
             │  ARTHA animation │
             │                  │
             │ Company creation │
             │    is on...      │
             └──────────────────┘
                      │
                  5 seconds
                      │
                      ▼
                    Login

Phase 11 acceptance criteria

I would not mark Phase 11 complete until all of these pass:

[ ] OPTIONS /api/v1/auth/login returns 200/204 rather than 400.

[ ] OPTIONS /api/v1/auth/setup returns 200/204 rather than 400.

[ ] Production frontend uses /api/v1, not hard-coded :28030.

[ ] Login PIN restricted to four digits.

[ ] Incorrect PIN appears immediately after verification.

[ ] Server-side PIN verification remains authoritative.

[ ] Existing five-attempt lockout remains functional.

[ ] Company setup is tabbed.

[ ] Required/optional fields are correctly separated.

[ ] GSTIN automatically populates state code/state/PAN.

[ ] District remains disabled until state is automatically populated.

[ ] District becomes enabled only after valid state.

[ ] Bank details are genuinely optional.

[ ] Logo is genuinely optional.

[ ] Logo remains square and standardized.

[ ] Mobile and office contact use international phone library.

[ ] Website validation works.

[ ] Bank account type is controlled dropdown.

[ ] Light theme works.

[ ] Dark theme works.

[ ] Buttons have sufficient contrast and consistent alignment.

[ ] ARTHA appears in uppercase in navbar.

[ ] Soft logo wave animation only appears where intended.

[ ] Company creation transition uses glass/blur effect.

[ ] Five-second creation transition works.

[ ] Duplicate company setup is rejected server-side.

[ ] Company creation rolls back completely on failure.

[ ] Alembic/database schema is synchronized.

[ ] Base.metadata.create_all() is not relied upon for production migrations.

[ ] /api/* 404s reach FastAPI.

[ ] React frontend routes don't produce Nginx 404s on refresh.

[ ] /health succeeds.

[ ] GST state master is seeded once without duplicate rows.

[ ] Existing GST, company, quotation, BOQ, estimate and invoice tables remain intact.


One particularly important finding

Your GST implementation itself is already considerably ahead of the UI. The source has the reusable GSTService, parser, state master, validation including checksum, API endpoints, and automatic PAN/state extraction already implemented.   

So I would not rebuild GST validation in Phase 11. Phase 11 should finish the integration, correct the setup state machine, fix CORS/routing, make the schema consistent with optional fields, and stabilize the production deployment.

Also, the current company logo endpoint is already /api/v1/company/logo/{company_id}, so if you're seeing a logo-related 404, that should be investigated as a routing/proxy/static-storage problem rather than creating another logo endpoint. 

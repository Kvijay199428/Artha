Worked for 16s

Yes. I examined the artha (9).md source against the production logs you provided. The deployment is partially correct, but the Credit Note/Adjustment Notes implementation is not correctly wired, and there is also a systematic trailing-slash issue causing the 307 responses.

1. What is working correctly

Production backend is starting correctly

Your logs show:

Application startup complete.
Uvicorn running on http://0.0.0.0:8000

The database initialization is also reaching all the expected tables, including:

adjustment_notes
adjustment_note_lines
note_allocations

So the database/model layer for adjustment notes is at least being loaded. The source also registers the adjustment router:

api_router.include_router(adjustments.router)



Therefore, this is not primarily an nginx/container routing problem for /adjustment-notes.


---

2. The main actual error: Credit Notes GET endpoint is missing

Your browser is requesting:

GET /api/v1/adjustment-notes?note_type=CREDIT_NOTE

and the backend returns:

404 Not Found

This is completely consistent with the source.

Your backend currently defines:

router = APIRouter(prefix="/adjustment-notes", tags=["Adjustments"])

@router.post("/credit-notes")
def create_credit_note(...):
    ...

@router.post("/debit-notes")
def create_debit_note(...):
    ...

@router.post("/{note_id}/post")
def post_adjustment_note(...):
    ...



There is no:

@router.get("/")

or:

@router.get("")

for listing adjustment notes.

Therefore:

GET /api/v1/adjustment-notes?note_type=CREDIT_NOTE

has nowhere to go → 404.

But the frontend expects that endpoint

Your frontend explicitly contains:

getAll: async (note_type?: string) => {
    const params = new URLSearchParams();
    if (note_type) params.append('note_type', note_type);

    const response =
        await apiClient.get<{items: AdjustmentNoteResponse[], total: number}>(
            `/adjustment-notes?${params.toString()}`
        );

    return response.data;
}



And AdjustmentNoteListPage calls it:

queryFn: () => adjustmentNotesApi.getAll(noteType)



So the frontend and backend are out of synchronization.


---

3. There is an even bigger API mismatch

The frontend and backend disagree on the create endpoint too.

Frontend

Frontend does:

POST /adjustment-notes



Backend

Backend only provides:

POST /adjustment-notes/credit-notes
POST /adjustment-notes/debit-notes



So after fixing the GET request, creating a credit note will likely encounter another endpoint mismatch.

The frontend API design appears to expect a generic adjustment-note API:

POST   /adjustment-notes
GET    /adjustment-notes
GET    /adjustment-notes/{id}
POST   /adjustment-notes/{id}/approve
POST   /adjustment-notes/{id}/post
POST   /adjustment-notes/{id}/cancel
POST   /adjustment-notes/{id}/reverse
GET    /adjustment-notes/{id}/pdf



But the backend currently implements only a small subset:

POST /adjustment-notes/credit-notes
POST /adjustment-notes/debit-notes
POST /adjustment-notes/{id}/post

So Adjustment Notes is incomplete, not just a broken GET request.


---

4. The 307 redirects are a separate problem

You have repeated:

GET /api/v1/units HTTP/1.1
307 Temporary Redirect

GET /api/v1/parties HTTP/1.1
307 Temporary Redirect

GET /api/v1/items HTTP/1.1
307 Temporary Redirect

GET /api/v1/invoices?transaction_type=PURCHASE HTTP/1.1
307 Temporary Redirect

This is because your backend routes are defined with trailing /.

For example:

router = APIRouter(prefix="/units")

@router.get("/")
def list_units(...):



So FastAPI expects:

/api/v1/units/

while your frontend requests:

/api/v1/units

The frontend source confirms this:

apiClient.get<Unit[]>('/units')



Same issue exists for items:

@router.get("/")



and parties:

@router.get("/")




---

5. This should be fixed rather than tolerated

The current sequence is:

Browser
   │
   │ GET /api/v1/units
   ▼
Backend
   │
   │ 307
   ▼
/api/v1/units/
   │
   ▼
Actual handler

That is unnecessary overhead.

You specifically wanted page loading to be fast and without artificial frontend delays. The 307s aren't a 5-second delay, but they are still unnecessary network round trips.

Better architecture

Make the backend routes canonical without trailing slash:

@router.get("")
def list_units(...):

instead of:

@router.get("/")

Then:

GET /api/v1/units
             ↓
         200 OK

Same for:

/items
/parties
/invoices
/adjustment-notes
/returns
/quotations
/boqs
/estimates

where applicable.


---

6. Authentication is working

This portion is good.

Your production logs show:

POST /api/v1/auth/login HTTP/1.1" 200 OK

and the backend successfully:

1. queried companies


2. queried company_auth


3. updated last_login_at


4. created a company_sessions record


5. committed it


6. returned 200 OK



The session insert is visible:

INSERT INTO company_sessions
...
status='ACTIVE'

So authentication itself is working.

The source also shows:

token = AuthService.authenticate(db, company.id, request.pin)

followed by the response. 

And the authentication service correctly resets failed attempts on successful authentication. 


---

7. The 5-second backend delay is correctly located

You previously specified that the only allowed artificial delay should be:

Company setup → 5 seconds

Login → 5 seconds

backend side

no frontend delay


The source currently has exactly:

time.sleep(5)

in company setup:

@router.post("/setup")
...
time.sleep(5)



and login:

@router.post("/login")
...
time.sleep(5)



So this requirement has been applied correctly.

I do not see evidence in the examined source of another intentional sleep(5) in ordinary page APIs.


---

8. Your lazy-loaded frontend chunks are working

The production logs are actually a good sign here.

When you visit:

/credit-notes

the browser loads:

AdjustmentNoteListPage-DXQjcj6m.js
adjustmentNotes-DceZFHf3.js
useQuery-CcE52uNG.js

When you visit:

/invoices/new

it loads:

InvoiceBuilderPage-j5qhoqJC.js
units-DARqeYHR.js
invoices-VK8lAWyt.js
items-BN1cnspH.js
parties-CM-P0ZfC.js

That is consistent with your desired route/page-level chunking.

The important point is that InvoiceBuilderPage itself calls:

useQuery(...)

for items, units and parties. 

And the production logs show those APIs only when the invoice/purchase pages are opened.

So the frontend code splitting appears to have been applied successfully.


---

9. But there is a second optimization issue inside pages

Although the route chunks are lazy-loaded, some pages immediately load multiple master datasets.

For example InvoiceBuilderPage does:

useQuery({ queryKey: ['items'], queryFn: itemsApi.getAll });
useQuery({ queryKey: ['units'], queryFn: unitsApi.getAll });
useQuery({ queryKey: ['parties'], queryFn: () => partiesApi.getAll() });



So:

Open Invoice Builder
       │
       ├── items
       ├── units
       └── parties

That may be correct if all three are needed immediately.

But it isn't truly component-level lazy data loading.

For example, if the user hasn't opened the item selector yet, you could defer items until the selector is actually opened.

That is an optimization for later—not the cause of your current 404.


---

10. Database initialization looks successful

The startup logs show all these tables being inspected:

company_contacts
company_bank_accounts
company_assets
company_auth
company_sessions
units
unit_categories
unit_aliases
unit_versions
items
item_versions
parties
party_addresses
party_bank_accounts
party_ledger_entries
payment_allocations
invoices
invoice_lines
invoice_series
payments
adjustment_notes
adjustment_note_lines
note_allocations
...

and then:

Database seeding completed.

followed by:

Application startup complete.

So there isn't an obvious database startup failure.


---

11. Important: the adjustment service itself is also incomplete

The current service has:

def create_credit_note(...):
    return self._create_note(...)

def create_debit_note(...):
    return self._create_note(...)

and:

def post_note(...):
    ...
    note.status = "POSTED"



The comment:

# Implement Ledger Posting

is particularly important.

That means the API may be able to change the note status to POSTED, but the actual accounting/ledger consequences are not implemented in this source version.

For a GST billing system, I would not consider the Credit/Debit Note module production-complete until:

Credit Note
    ↓
Note Lines
    ↓
Tax calculation
    ↓
Party ledger
    ↓
Invoice allocation
    ↓
GST effect
    ↓
Accounting posting
    ↓
Audit log

are all handled consistently.


---

12. What I conclude from your production logs

Current status

Area	Status

Docker/frontend container	✅
Nginx	✅
Backend startup	✅
DB initialization	✅
DB seeding	✅
Company login	✅
Session creation	✅
5-sec login delay backend	✅
5-sec setup delay backend	✅
Route-level frontend chunks	✅
Invoice lazy chunk	✅
Credit Note lazy chunk	✅
/units	⚠️ 307
/items	⚠️ 307
/parties	⚠️ 307
/invoices	⚠️ 307
Credit Note GET	❌ 404
Credit Note frontend/backend contract	❌ mismatch
Credit Note backend list API	❌ missing
Credit Note detail API	❌ missing
Credit Note approve API	❌ missing
Credit Note cancel API	❌ missing
Credit Note reverse API	❌ missing
Credit Note PDF API	❌ missing
Full ledger posting	❌ incomplete



---

13. The exact fix I recommend

Don't patch only this:

GET /adjustment-notes

because you'll immediately hit the next mismatch.

Bring the entire Adjustment Notes API contract into alignment.

Backend should expose

GET    /api/v1/adjustment-notes?note_type=CREDIT_NOTE

POST   /api/v1/adjustment-notes

GET    /api/v1/adjustment-notes/{id}

POST   /api/v1/adjustment-notes/{id}/approve

POST   /api/v1/adjustment-notes/{id}/post

POST   /api/v1/adjustment-notes/{id}/cancel

POST   /api/v1/adjustment-notes/{id}/reverse

GET    /api/v1/adjustment-notes/{id}/pdf

Or, if you intentionally want separate creation endpoints:

POST /api/v1/adjustment-notes/credit-notes
POST /api/v1/adjustment-notes/debit-notes

then change the frontend API to match that architecture.

I recommend the generic /adjustment-notes REST structure, because your frontend has already been designed around it.


---

14. One more thing I would fix immediately

Standardize your trailing-slash policy throughout the backend.

Currently:

@router.get("/")

is producing:

307 Temporary Redirect

for frontend calls such as:

/units
/items
/parties

Change the backend route declarations to the canonical no-slash form:

@router.get("")

and similarly for POST/list endpoints where appropriate.

Then your production logs should change from:

GET /api/v1/units 307

to:

GET /api/v1/units 200

with one request instead of two.


---

Bottom line

No, the source has not been applied completely correctly yet.

The chunking, authentication, database startup, and backend-only 5-second delays are working as intended. The production logs confirm that.

But the Credit Note module is definitively incomplete/mismatched:

> Frontend asks GET /adjustment-notes?note_type=CREDIT_NOTE, while backend has no GET route at all.



And independently:

> /units, /items, /parties, /invoices are generating unnecessary 307 redirects because frontend uses no trailing slash while backend declares @router.get("/").



Those are the two issues I would fix before considering this deployment clean.   

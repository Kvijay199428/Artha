Worked for 15s

Phase 14 — Artha Frontend Code Splitting, Lazy Loading & Zero-Delay Navigation

I checked the updated Artha source before defining this phase. The current project is partially prepared for code splitting, but Phase 14 is not complete.

The most important finding is that the current route configuration references page components directly:

element: wrap(<InvoiceBuilderPage />)
element: wrap(<QuotationBuilderPage />)
element: wrap(<AdjustmentNoteBuilderPage />)
element: wrap(<BOQListPage />)

including Credit Note, Debit Note, Supply In/Out, Returns, BOQ and Estimates. 

Therefore, merely having routes is not sufficient to guarantee one route = one asynchronously loaded chunk.

There is also an older/alternate App.tsx in the source that already uses React lazy() and Suspense, demonstrating that lazy loading has been considered, but the current Artha routing implementation needs to be standardized rather than having multiple competing routing patterns. 


---

1. Phase 14 objective

The fundamental rule will be:

> Never load an application's feature page/component bundle until the user actually navigates to that feature.



For example:

User opens Artha
        │
        ↓
Dashboard
        │
        ├── Dashboard chunk
        ├── Common shell
        └── Required dashboard API data

Nothing related to:

Credit Notes
Debit Notes
BOQ
Estimates
Quotations
Returns
Supply In
Supply Out
Invoice Builder

should be downloaded merely because the user logged in.

When the user clicks:

Credit Notes

then:

credit-notes.chunk.js

is requested.


---

2. Target loading architecture

The desired browser behavior is:

INITIAL REQUEST
│
├── index.html
├── main/app bootstrap
├── React runtime
├── router
├── authentication state
├── common UI shell
└── Dashboard chunk

Then:

Dashboard
   ↓
User clicks Credit Notes
   ↓
Browser requests credit-notes chunk
   ↓
Credit Note page renders

Not:

Login
 ↓
Download everything
 ├── Dashboard
 ├── Invoice
 ├── BOQ
 ├── Estimate
 ├── Quotation
 ├── Supply In
 ├── Supply Out
 ├── Returns
 ├── Credit Note
 ├── Debit Note
 ├── Parties
 ├── Items
 └── Units


---

3. Current dependency situation

The current frontend already has the right basic ecosystem:

React

React Router

Vite

TanStack Query

Axios

React Hook Form

Zod


The package configuration confirms React 19, React Router 7, Vite 8 and TanStack Query are already present. 

Therefore do not introduce another routing or lazy-loading framework.

Use:

React.lazy()
Suspense
React Router
Vite dynamic import()


---

4. Feature-level chunks

I recommend the following logical chunk boundaries.

Core

core

Contains:

React bootstrap
Router
AuthProvider
QueryClient
Theme
Common utilities
API client
Error boundary

Dashboard

dashboard

Contains:

DashboardPage
Dashboard widgets
Dashboard charts
Dashboard-specific hooks
Dashboard API queries

Company

company

Contains:

Company profile
Company settings
Company bank details
GST profile
Company modification

Units

units

Contains:

UnitsPage
UnitModal
Formula editor
Unit tables

Items

items

Contains:

ItemsPage
ItemForm
SKU
HSN/SAC
GST configuration

Parties

parties

Contains:

Customer
Supplier
Sundry Debtors
Sundry Creditors
Party forms

Invoice

invoices

Contains:

InvoiceList
InvoiceBuilder
InvoiceDetail
InvoicePreview
InvoiceModification

Supply In

supply-in

Contains:

Purchase Order
Purchase Quotation
Purchase Return
Purchase-related screens

Supply Out

supply-out

Contains:

Sales Order
Sales Quotation
Sales Return
Sales-related screens

Quotations

quotations

BOQ / Estimates

boq
estimates

Credit Notes

credit-notes

Debit Notes

debit-notes


---

5. Do not create one gigantic feature chunk

There are two extremes.

Bad

arthа-all-pages.js

containing everything.

Also unnecessarily granular

button.js
input.js
table.js
modal.js
icon.js
...

The second approach can create excessive network requests.

Use route/feature-level chunks.


---

6. Recommended route structure

The routing architecture should become conceptually:

const DashboardPage = lazy(() => import('./features/dashboard/pages/DashboardPage'));

const InvoiceListPage = lazy(() =>
  import('./features/invoices/pages/InvoiceListPage')
);

const InvoiceBuilderPage = lazy(() =>
  import('./features/invoices/pages/InvoiceBuilderPage')
);

const CreditNotePage = lazy(() =>
  import('./features/credit-notes/pages/CreditNotePage')
);

const DebitNotePage = lazy(() =>
  import('./features/debit-notes/pages/DebitNotePage')
);

Then:

<Route
  path="/dashboard"
  element={
    <Suspense fallback={<PageLoading />}>
      <DashboardPage />
    </Suspense>
  }
/>


---

7. Better: route-level Suspense

Do not wrap the entire application in one giant Suspense boundary if it causes the entire application shell to disappear whenever a small route chunk is loading.

Instead:

App
 ├── Router
 │
 ├── MainLayout
 │    ├── Sidebar
 │    ├── Header
 │    └── <Suspense>
 │          └── CurrentPage
 │
 └── Auth routes

Therefore when Credit Note loads:

Sidebar remains
Header remains
Main layout remains

Only content area:
    Loading Credit Note...


---

8. Dashboard loading

When user logs in:

Login successful
      ↓
Navigate /dashboard
      ↓
Load dashboard chunk
      ↓
Render dashboard
      ↓
Request dashboard API data

The dashboard API must not wait for unrelated APIs.

Don't do:

GET /dashboard
GET /invoices
GET /orders
GET /returns
GET /credit-notes
GET /debit-notes
GET /boq
GET /quotations
GET /items
GET /units
GET /parties

just because Dashboard mounted.


---

9. Dashboard API rule

Dashboard should request only data actually displayed on Dashboard.

For example:

GET /dashboard/summary
GET /dashboard/sales-summary
GET /dashboard/purchase-summary
GET /dashboard/outstanding-summary

Only if those widgets exist.


---

10. Feature API lazy loading

The same principle should apply to frontend API modules.

Don't import:

allApis.ts

containing every feature's API implementation into the initial application.

Prefer:

features/
├── dashboard/
│   └── api.ts
├── invoices/
│   └── api.ts
├── credit-notes/
│   └── api.ts
├── debit-notes/
│   └── api.ts
├── quotations/
│   └── api.ts
└── boq/
    └── api.ts


---

11. Current API architecture

The project already has a central Axios client, and authentication is injected through an interceptor. 

Keep this centralized.

For example:

api/client.ts

should remain small and always available.

But:

api/invoices.ts
api/returns.ts
api/adjustments.ts
api/boq.ts

should belong to their respective feature.


---

12. React Query behavior

The project already uses TanStack Query. 

Use it for data fetching, not page chunk loading.

These are separate concerns:

Code splitting
    ↓
React.lazy / import()

Data loading
    ↓
TanStack Query


---

13. Example: Credit Note

When the user opens:

/credit-notes

browser does:

1. Download credit-note JS chunk
2. Execute module
3. Render page
4. CreditNoteList query runs
5. API returns data

When the user never opens Credit Notes:

Credit Note JS = never downloaded
Credit Note API = never requested


---

14. Credit Note builder

Do not put:

AdjustmentNoteBuilderPage

into the initial bundle.

Instead:

/credit-notes/new

loads:

credit-note-builder chunk

only when requested.

Same for:

/debit-notes/new


---

15. Invoice builder deserves its own chunk

Invoice Builder is likely one of the largest pages because it will contain:

Items
Tax calculation UI
GST
Party selection
Unit selection
Discount
Payments
Totals
Document references
Invoice preview

Therefore:

InvoiceList
InvoiceDetail
InvoiceBuilder

should not necessarily be one huge chunk.

Recommended:

invoice-list.chunk
invoice-detail.chunk
invoice-builder.chunk
invoice-preview.chunk

But shared invoice primitives can live in:

invoice-common.chunk

if Vite determines that sharing them is beneficial.


---

16. BOQ builder

BOQ can also be heavy because it has:

hierarchical lines
quantity formulas
item selection
unit formulas
rate calculations
nested rows

So:

BOQList

and:

BOQBuilder

should be separate route chunks.

The current BOQ implementation already has quantity/formula fields such as quantity_formula, so there is a good reason not to unnecessarily load its builder on Dashboard. 


---

17. Prefetching — optional and controlled

There is one optimization I recommend after basic lazy loading works.

If the user hovers over:

Credit Notes

you may optionally prefetch:

credit-notes.chunk.js

But this is optional.

Do not prefetch every navigation item on initial load.


---

18. No artificial frontend delays

This is an explicit Phase 14 rule:

> No artificial delay is permitted anywhere in normal frontend navigation.



Remove things like:

setTimeout(() => navigate(...), 2000)

or:

await new Promise(resolve =>
  setTimeout(resolve, 1000)
);

from ordinary page loading.

The current source already contains an example of a frontend redirect delay in another project:

setTimeout(() => navigate('/login'), 2000);



That pattern should not exist in Artha's normal navigation workflow.


---

19. Allowed 5-second delay

Your requirement is:

Company Setup → 5 seconds backend delay
Login → 5 seconds backend delay

Only.

Therefore:

Operation	Artificial delay

Company setup	5 seconds backend
Company PIN login	5 seconds backend
Dashboard	0 seconds
Invoice	0 seconds
Supply In	0 seconds
Supply Out	0 seconds
Returns	0 seconds
Quotation	0 seconds
BOQ	0 seconds
Estimate	0 seconds
Credit Note	0 seconds
Debit Note	0 seconds
Items	0 seconds
Units	0 seconds
Parties	0 seconds
Company profile editing	0 seconds



---

20. The 5-second delay must be backend-only

Do not implement:

await sleep(5000);
await authApi.login();

or:

setTimeout(() => submit(), 5000);

Frontend should immediately submit:

POST /auth/login

The backend intentionally takes approximately 5 seconds before returning.


---

21. Login backend

Current login is:

POST /auth/login
       ↓
Company lookup
       ↓
AuthService.authenticate()
       ↓
token



Implement the delay inside the backend authentication service/request handling.

Conceptually:

def login(...):
    authenticate(...)
    backend_delay()
    return token

But the placement must be carefully chosen so the delay does not happen before cheap validation.


---

22. Better security implementation

Because this is PIN authentication, the 5-second delay should preferably be tied to the authentication attempt rather than simply:

sleep(5)

for every successful request.

For example:

Receive PIN
 ↓
Validate request
 ↓
Verify PIN hash
 ↓
Apply authentication delay
 ↓
Create token
 ↓
Return response

For invalid PIN:

Receive PIN
 ↓
Verify
 ↓
Failure
 ↓
Controlled delay
 ↓
Return 401

This also helps prevent obvious timing differences.


---

23. Do not block unrelated backend workers

Because Artha uses FastAPI, don't casually add:

time.sleep(5)

inside an async endpoint.

If the endpoint is synchronous, it is still important to understand worker/thread implications.

The cleaner design is an explicit authentication delay mechanism that does not unnecessarily block the application's event loop.


---

24. Company setup

Current setup endpoint calls:

CompanyService.create_company()



The 5-second delay should be implemented server-side around the setup operation.

Flow:

Frontend
   │
   │ POST /auth/setup
   ↓
FastAPI
   ↓
Validate
   ↓
Create company
   ↓
5-second backend delay
   ↓
Response

Frontend:

Submit
 ↓
Show real request progress
 ↓
Receive response
 ↓
Navigate

No setTimeout().


---

25. Loading indicator is NOT an artificial delay

This distinction is important.

Allowed:

API request is genuinely running
        ↓
Show spinner/skeleton
        ↓
Response arrives
        ↓
Render

Not allowed:

API returns in 100 ms
        ↓
wait another 4.9 seconds
        ↓
render

A loading indicator represents real work.

It must never intentionally hold the user.


---

26. Page-loading component

Create one reusable component:

components/common/PageLoading.tsx

Example behavior:

┌──────────────────────────────┐
│                              │
│          Loading...          │
│                              │
└──────────────────────────────┘

It should render immediately when a chunk is genuinely being downloaded.


---

27. Error boundary for failed chunks

Dynamic imports can fail due to:

network interruption
stale deployment
cached old index.html
server unavailable

Implement:

ChunkLoadErrorBoundary

with:

Unable to load this page.

[Retry]

Do not redirect the user to login just because a JavaScript chunk failed.


---

28. Stale chunk handling

Vite produces hashed assets such as:

assets/invoices-C7x3a9.js

When a new deployment occurs:

old browser
    ↓
requests old chunk
    ↓
404

Handle this gracefully.

Recommended:

Chunk load failure
 ↓
detect dynamic import failure
 ↓
one controlled page reload
 ↓
if still failing → show error

Do not continuously reload.


---

29. Nginx/static asset rule

The current deployment already has aggressive static asset caching:

/assets/
expires 1y
Cache-Control: public, immutable

and SPA fallback:

try_files $uri $uri/ /index.html;



That is appropriate for hashed Vite assets.

But ensure:

index.html

is not cached for a year.

Recommended:

/assets/*.js
/assets/*.css

→ immutable long-term cache.

/index.html

→ no-cache / revalidate.

This reduces stale-chunk problems after deployment.


---

30. Do not lazy-load the common shell

Keep these in the initial application:

Router
Auth
MainLayout
Sidebar
Header
Theme
Error Boundary
API client
basic UI primitives

The user should never see the entire navigation disappear because a feature chunk is loading.


---

31. Do not lazy-load tiny shared components individually

Avoid:

lazy(Button)
lazy(Input)
lazy(Modal)
lazy(Label)
lazy(Icon)

That would create unnecessary chunk fragmentation.

Keep common primitives in the shared bundle.

The project already has reusable common components, including Button/Input re-exports. 


---

32. Feature isolation

Recommended frontend structure:

frontend/src/
│
├── app/
│   ├── router.tsx
│   ├── providers.tsx
│   └── error-boundary.tsx
│
├── components/
│   ├── common/
│   └── ui/
│
├── features/
│   │
│   ├── dashboard/
│   ├── company/
│   ├── units/
│   ├── items/
│   ├── parties/
│   ├── invoices/
│   ├── supply-in/
│   ├── supply-out/
│   ├── returns/
│   ├── quotations/
│   ├── boq/
│   ├── estimates/
│   ├── credit-notes/
│   └── debit-notes/
│
└── api/
    └── client.ts


---

33. Do not import feature pages into App.tsx

Avoid:

import DashboardPage from './features/dashboard/pages/DashboardPage';
import InvoicePage from './features/invoices/pages/InvoicePage';
import CreditNotePage from './features/credit-notes/pages/CreditNotePage';

because that encourages all page modules to enter the application's dependency graph.

Instead:

const DashboardPage = lazy(
  () => import('./features/dashboard/pages/DashboardPage')
);


---

34. Route manifest

The route definitions should become declarative:

route
component importer
feature
authentication requirement

Conceptually:

{
  path: '/credit-notes',
  element: lazy(() =>
    import('../features/credit-notes/pages/CreditNoteListPage')
  ),
  protected: true
}

Then the router wrapper handles Suspense consistently.


---

35. Route groups

Group routes logically:

/auth
/dashboard
/company
/master-data
/sales
/purchases
/financial

Example:

Sales
 ├── Supply Out
 ├── Quotations
 ├── Returns
 └── Invoices

Purchases
 ├── Supply In
 ├── Quotations
 └── Returns

Financial
 ├── Credit Notes
 ├── Debit Notes
 └── Payments

This also makes future permissions easier.


---

36. Don't preload all route components

Avoid:

Promise.all([
  import(Dashboard),
  import(Invoices),
  import(CreditNotes),
  import(DebitNotes),
  import(BOQ),
  ...
])

on application startup.

That defeats Phase 14.


---

37. API data should also be demand-driven

Code splitting alone is insufficient.

This is bad:

Dashboard mounts

useQuery(invoices)
useQuery(creditNotes)
useQuery(returns)
useQuery(boq)
useQuery(quotations)

The Dashboard should only query what it displays.


---

38. Modal chunking

For very large modals, lazy-load them when opened.

Example:

Dashboard
 ↓
User clicks "Create Invoice"
 ↓
Invoice Builder chunk loads

But don't do this for tiny confirmation dialogs.

Use this selectively.


---

39. Invoice selection modal

For Phase 13's invoice-centric architecture, the reusable:

InvoiceReferenceSelector

should preferably remain in a shared financial/document module if it is used by:

Credit Note
Debit Note
Sales Return
Purchase Return
Payment

That prevents duplicating the same implementation across chunks.


---

40. Performance targets

Phase 14 should establish measurable targets.

Initial application

Should contain only:

Core
Auth
Layout
Dashboard

Feature navigation

Route change
 ↓
Dynamic import
 ↓
Render

No artificial delay

Dashboard navigation = 0 ms artificial delay
Invoice navigation = 0 ms
Credit Note = 0 ms
Debit Note = 0 ms
etc.

Only:

Company Setup = 5s backend-controlled delay
Login = 5s backend-controlled delay


---

41. Build verification

After implementation:

npm run build

Then inspect:

dist/assets/

The build should produce multiple chunks rather than one enormous application JavaScript file.

Expected conceptually:

assets/
├── index-xxxxx.js
├── dashboard-xxxxx.js
├── invoices-xxxxx.js
├── invoice-builder-xxxxx.js
├── supply-in-xxxxx.js
├── supply-out-xxxxx.js
├── quotations-xxxxx.js
├── boq-xxxxx.js
├── credit-notes-xxxxx.js
├── debit-notes-xxxxx.js
└── ...

Exact filenames are Vite-generated and should not be hard-coded.


---

42. Network verification

Use Chrome DevTools:

Network
 → JS
 → Clear
 → Disable cache

Load:

/dashboard

Verify:

dashboard chunk → loaded
credit-note chunk → NOT loaded
debit-note chunk → NOT loaded
boq chunk → NOT loaded
quotation chunk → NOT loaded

Then navigate:

Credit Notes

Verify:

credit-note chunk → loaded

Then:

Debit Notes

Verify only the missing Debit Note chunk is requested.


---

43. Navigation test matrix

Phase 14 should test every major route:

Route	Initial load?	Separate chunk?

Dashboard	Yes	Yes
Company	No	Yes
Units	No	Yes
Items	No	Yes
Parties	No	Yes
Invoice List	No	Yes
Invoice Builder	No	Yes
Invoice Detail	No	Yes
Supply In	No	Yes
Supply Out	No	Yes
Quotations	No	Yes
BOQ	No	Yes
Estimates	No	Yes
Returns	No	Yes
Credit Notes	No	Yes
Debit Notes	No	Yes



---

44. Delay audit

Search the entire frontend and backend for:

setTimeout
setInterval
sleep(
time.sleep
asyncio.sleep
Promise
delay
debounce
throttle

But don't remove legitimate functionality blindly.

Classify every occurrence:

ARTIFICIAL_PAGE_DELAY
AUTH_DELAY
UI_ANIMATION
DEBOUNCE
POLLING
RETRY
NETWORK_TIMEOUT

Only artificial page/navigation delays must be eliminated.


---

45. Specific rule for animations

CSS animation is not the same as a loading delay.

For example:

transition: background-color 0.15s;

is UI animation, not a page-loading delay.

The current source contains small UI transitions and fade-in animations. 

These don't need to be removed unless they are being used to artificially delay rendering.


---

46. Authentication UX

Correct:

PIN entered
 ↓
POST /auth/login
 ↓
Backend intentionally processes for ~5 sec
 ↓
Response
 ↓
Store token
 ↓
Navigate /dashboard
 ↓
Dashboard chunk loads immediately

Incorrect:

PIN entered
 ↓
Frontend waits 5 sec
 ↓
POST /auth/login
 ↓
Backend

Absolutely avoid the second architecture.


---

47. Company setup UX

Correct:

Submit company setup
       ↓
POST /auth/setup
       ↓
Backend processing
       ↓
5-second backend delay
       ↓
Success response
       ↓
Frontend navigates immediately

No:

setTimeout(...)

after successful setup.


---

48. Login → Dashboard should have no second artificial delay

This is especially important.

Do not implement:

Backend login = 5 seconds
+
Frontend redirect delay = 2 seconds
+
Dashboard loading delay = 1 second

That would create a terrible 8-second-plus experience.

Target:

Backend authentication = ~5 seconds
Frontend navigation = immediate
Dashboard chunk = immediate request
Dashboard rendering = immediate after chunk/data


---

49. Backend delay configuration

Don't hard-code random sleeps throughout the backend.

Create:

AUTH_ARTIFICIAL_DELAY_SECONDS=5

in configuration.

Then:

Company setup → configured delay
Login → configured delay

This gives you a controlled production setting.

But the business requirement remains:

5 seconds


---

50. Important: don't apply 5 seconds to every authentication endpoint

Only:

POST /auth/setup
POST /auth/login

should receive the intentional delay.

Do not delay:

GET /auth/me
POST /auth/logout
POST /auth/pin-change

unless there is a separate security requirement.


---

51. auth/me must remain fast

On a refresh:

Browser
 ↓
token exists
 ↓
GET /auth/me
 ↓
restore company
 ↓
Dashboard

There should be:

0-second artificial delay

Otherwise every browser refresh would become unnecessarily slow.


---

52. Cache strategy

TanStack Query should handle data caching.

For example:

Dashboard data

can be cached for a short period.

But don't cache mutable financial records indefinitely.

Invoices, payments, credit notes, debit notes and returns require appropriate invalidation after mutations.


---

53. Mutation invalidation

Example:

Create Credit Note
       ↓
Invalidate:
  invoice detail
  invoice relations
  credit-note list
  party outstanding
  dashboard financial summary

This is data-cache behavior and should not cause artificial page delays.


---

54. Loading states

Use three distinct states:

Chunk loading

Loading page...

API loading

Loading invoices...

Mutation

Saving...

Never combine them into one artificial global delay.


---

55. Don't use a fixed minimum loading time

Avoid code like:

requestStart
requestEnd

minimumLoadingTime = 500ms

If the API completes in 80 ms:

render in ~80 ms

not:

wait until 500 ms

Your requirement is explicitly zero artificial delay outside authentication/setup.


---

56. Recommended Phase 14 implementation order

Step 1 — Audit

Find:

all page imports
all route definitions
all setTimeout
all sleep
all artificial delays
all preload/prefetch logic


---

Step 2 — Standardize router

Create:

frontend/src/app/router.tsx

and eliminate duplicate/competing route implementations.

This is important because the source currently contains different routing patterns in the project snapshots.


---

Step 3 — Convert pages to lazy()

Every major feature page becomes:

lazy(() => import(...))


---

Step 4 — Add route-level Suspense

Create:

PageLoading.tsx

and:

RouteErrorBoundary.tsx


---

Step 5 — Feature isolation

Move page-specific dependencies into:

features/<feature>/


---

Step 6 — API isolation

Keep:

api/client.ts

global.

Move feature APIs into their respective feature modules.


---

Step 7 — Dashboard minimization

Dashboard should load only:

dashboard chunk
dashboard APIs
common shell


---

Step 8 — Remove frontend artificial delays

Search and eliminate:

setTimeout navigation
sleep
minimum loading timers
fake loading timers

except legitimate UI behavior.


---

Step 9 — Backend authentication delay

Implement:

AUTH_ARTIFICIAL_DELAY_SECONDS = 5

only for:

/auth/setup
/auth/login


---

Step 10 — Verify build chunks

Run:

npm run build

and inspect:

dist/assets


---

Step 11 — Network verification

Test every route using DevTools.


---

Step 12 — Performance regression testing

Verify that:

Login
 ↓
Dashboard

doesn't download:

Credit Notes
Debit Notes
BOQ
Estimates
Returns
Supply In
Supply Out


---

57. Final Phase 14 architecture

ARTHA WEB APP
                              │
                              ↓
                         CORE CHUNK
                              │
                ┌─────────────┴─────────────┐
                │                           │
             AUTH                         APP
                │                           │
        ┌───────┴───────┐             COMMON SHELL
        │               │                   │
      SETUP            LOGIN                │
        │               │                   │
        └────── 5s BACKEND ─────────────────┘
                        │
                        ↓
                    DASHBOARD
                        │
                DASHBOARD CHUNK
                        │
        ┌───────────────┼────────────────┐
        │               │                │
     Invoice        Supply Out        Supply In
        │               │                │
     CHUNK             CHUNK            CHUNK
        │
   ┌────┼──────────┐
   │    │          │
 List Builder    Detail
   │
   ↓
INVOICE-CENTRIC DOCUMENT GRAPH
   │
   ├── Returns
   ├── Credit Notes
   ├── Debit Notes
   ├── Payments
   └── Adjustments
        │
        ↓
  LOAD ONLY WHEN OPENED

Phase 14 acceptance rule

The implementation is not considered complete until all of these are true:

1. Dashboard loads without downloading unrelated feature chunks.


2. Each major feature is dynamically imported.


3. Credit Note is downloaded only when Credit Note is opened.


4. Debit Note is downloaded only when Debit Note is opened.


5. Invoice Builder is not part of the initial Dashboard bundle.


6. BOQ/Estimate builders are not initially loaded.


7. Supply In/Out and Returns are demand-loaded.


8. Feature-specific API code is not unnecessarily imported into the core bundle.


9. No artificial frontend page/navigation delay exists.


10. No artificial delay exists on ordinary API operations.


11. Exactly the requested 5-second intentional delay is server-side for Company Setup and PIN Login.


12. /auth/me, logout and PIN change remain immediate.


13. Chunk-loading failures have a retry path.


14. Vite hashed assets use long-term immutable caching.


15. index.html is revalidated rather than cached indefinitely.


16. The production build visibly produces route/feature chunks.


17. Network testing confirms unused features are not downloaded.


18. There is no duplicate/competing routing implementation left in the project.



The current source already has the correct underlying tooling—React 19, React Router 7, Vite and TanStack Query—but the actual Artha route definitions still need to be converted from eagerly referenced page components to a consistent route-level dynamic import architecture.  

One additional recommendation: because Phase 13 made the invoice the central financial/document hub, keep the invoice/document-reference primitives in the shared financial layer, but lazy-load the actual Credit Note, Debit Note, Return, Invoice Builder, BOQ, Quotation, Supply In and Supply Out screens. That gives you aggressive code splitting without duplicating the document-reference architecture across chunks.

#!/usr/bin/env python3
"""
Generate docs/BUSYWIN_DATABASE_SCHEMA.md master reference documentation.
"""

import os
import json

SCHEMA_FILE = 'd:\\VEGA\\ARTHA\\scripts\\busywin_db_schema.json'
DOCS_DIR = 'd:\\VEGA\\ARTHA\\docs'
OUTPUT_FILE = os.path.join(DOCS_DIR, 'BUSYWIN_DATABASE_SCHEMA.md')

with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
    schema = json.load(f)

db_bds = schema['db_bds']
fy_bds = schema['fy_bds']

content = """# BusyWin Database Complete Schema & Architectural Reference

> **Target Database Engine:** Microsoft Jet 4.0 / Microsoft Access 2000-2003 Engine (`.bds` extension)  
> **OLEDB Provider:** `Microsoft.ACE.OLEDB.12.0` (or `Microsoft.Jet.OLEDB.4.0`)  
> **Standard Database Password:** `ILoveMyINDIA`  
> **Company Database (`db.bds`):** 28 Tables | 1,174 Columns  
> **Financial Year Database (`db1YYYY.bds`):** 80 Tables | 2,454 Columns  
> **Total Database Surface:** **108 Tables | 3,628 Columns**

---

## 1. Executive Summary & Architecture Overview

**BusyWin** is an enterprise accounting, ERP, and statutory GST compliance system widely deployed across Indian trading, manufacturing, and distribution businesses. Built natively on Visual Basic 6.0 (`MSVBVM60.DLL`) with Microsoft Jet 4.0 database engines, BusyWin organizes its data into a **two-tier database hierarchy**:

```
C:\\BusyWin\\DATA\\
  └── COMP0001\\                 <-- Unique folder per registered enterprise
        ├── db.bds              <-- Tier 1: Global Company Database (Master configuration, users, print layouts)
        ├── db12024.bds         <-- Tier 2: FY 2024-25 Operational Database (Transactions, ledgers, vouchers)
        ├── db12025.bds         <-- Tier 2: FY 2025-26 Operational Database
        ├── db12026.bds         <-- Tier 2: FY 2026-27 Operational Database (Active FY)
        └── locks.sys           <-- Multi-user concurrency lock file
```

### Key Architectural Tenets:
1. **Physical File Decoupling by Financial Year:**  
   To prevent single-file corruption and adhere to Jet 4.0's 2 GB maximum file limit, transactions and yearly account balances are partitioned into individual `db1<YYYY>.bds` files. Global settings, multi-state profiles, user accounts, and print configurations remain in `db.bds`.
2. **Polymorphic Master Architecture (`Master1`):**  
   Rather than maintaining separate tables for accounts, vendors, customers, products, units, and tax categories, BusyWin uses a **single polymorphic table (`Master1`)** differentiated by a `MasterType` discriminator.
3. **Dual-Role Transaction Detail Engine (`Tran2`):**  
   `Tran2` serves both as an **inventory item movement ledger** (tracking items, quantities, rates, and batch details) and as the **double-entry financial accounting ledger** (tracking account debits and credits).
4. **Summary / Caching Architecture (`Folio1`, `DailySum`):**  
   To achieve high-speed reporting across massive transaction volumes without repeatedly scanning raw ledger lines, BusyWin computes running balances and aggregates into pre-computed balance registers (`Folio1` and `DailySum`).

---

## 2. Entity-Relationship & Relational Flow

The diagram below illustrates how core tables interconnect across the global company database and the annual transaction database:

```mermaid
erDiagram
    COMPANY ||--o{ STATE_COMPANY_DET : "Multi-state GST Registrations"
    COMPANY ||--o{ USER_CONTROL : "User Accounts & Security"
    COMPANY ||--o{ PRINTER_REPS : "Invoice & Report Templates"

    MASTER1 ||--o{ MASTER_ADDRESS_INFO : "Address, PAN, GSTIN"
    MASTER1 ||--o{ ITEM_DESC : "Extended Item Specs"
    MASTER1 ||--o{ ITEM_SERIAL_NO : "IMEI / Serial Numbers"
    MASTER1 ||--o{ FOLIO1 : "Running Account/Stock Balance"
    MASTER1 ||--o{ MASTER1 : "ParentGrp (Hierarchy / Groups)"

    TRAN1 ||--|{ TRAN2 : "Voucher Line Items & Ledgers"
    TRAN1 ||--o{ TRAN3 : "Bill Sundries (Freight, Discount)"
    TRAN1 ||--o{ VCH_GST_SUM_ITEM_WISE : "Item-wise GST Breakdown"
    TRAN1 ||--o{ BILLING_DET : "Consignee & Dispatch Address"
    TRAN1 ||--o{ VCH_OTHER_INFO : "Transporter & Vehicle Details"

    MASTER1 ||--o{ TRAN1 : "MasterCode1 (Party / Customer / Vendor)"
    MASTER1 ||--o{ TRAN2 : "MasterCode1 (Item or Ledger Account)"
    MASTER1 ||--o{ TRAN2 : "MasterCode2 (Godown / Material Center)"
```

---

## 3. Polymorphic Master Architecture (`Master1.MasterType`)

The `Master1` table contains **156 columns** and serves as the universal repository for all entity masters. The `MasterType` column dictates how records are interpreted:

| `MasterType` | Entity Domain | Real Record Count | Business Role & Meaning | Foreign Key Linking |
|:------------:|---------------|:-----------------:|-------------------------|---------------------|
| **1** | **Account Groups** | 29 | Standard accounting classifications: `Bank Accounts`, `Sundry Debtors`, `Sundry Creditors`, `Direct Expenses`, `Capital Account`, `Sales`, `Purchase`. | Self-referencing via `ParentGrp` |
| **2** | **Accounts / Parties** | 108 | Customer clients, vendor suppliers, bank accounts, cash ledgers, tax ledgers, and operational expense heads. | Points to `ParentGrp` (Type 1 Group); Links to `MasterAddressInfo.MasterCode` |
| **3** | **Cost Center Groups** | 1 | Organizational groupings for cost centers. | Hierarchical parent for cost centers |
| **5** | **Item Groups** | 1 | Product categories (e.g. `Raw Materials`, `Finished Goods`, `General`, `Hardware`). | Hierarchical parent for Items (Type 6) |
| **6** | **Inventory Items** | 132 | Products, SKUs, services, and raw materials traded or consumed by the business. | `ParentGrp` -> Type 5; `CM1` -> Unit (Type 8); `CM2` -> Tax Category (Type 21) |
| **7** | **Currencies** | 3 | Operating currencies (`INR ₹`, `USD $`, `EUR €`). | Used in multi-currency forex transactions |
| **8** | **Units of Measurement** | 19 | Primary measurement units: `Pcs.`, `SQFT`, `RFT`, `Box`, `Kgs.`, `CBM`, `Mtr.`. | Linked to Item `CM1` |
| **9** | **Bill Sundries** | 19 | Post-taxable voucher additions and deductions: `Trade Discount`, `Freight / Cartage`, `Insurance`, `Round Off`, `Add. Cess on GST`. | Applied in `Tran3` and voucher calculations |
| **10** | **Material Center Groups** | 3 | Groupings of storage godowns and retail stores (e.g. `Godowns`, `Stores`, `Outlets`). | Parent for Material Centers |
| **11** | **Material Centers / Godowns** | 1 | Physical storage locations and warehouses (`Main Store`, `Shop Floor`, `Transit Warehouse`). | Linked to `Tran2.MasterCode2` |
| **12** | **Price Categories** | 8 | Wholesale, Retail, Distributor, and Special customer price tier levels (`A`, `B`, `C`, etc.). | Linked to `Master1.CM1` for parties |
| **13** | **Sale Types** | 16 | Outward GST supply tax structures: `LGST 18%`, `Central-18%`, `SEZ-ZeroRated`, `Exempt`, `Composition Outward`. | Linked to `Tran1.VchSalePurcAmt` |
| **14** | **Purchase Types** | 17 | Inward GST tax structures: `LGST 18%`, `Central-18%`, `Imports-18%`, `RCM Inward`. | Linked to Purchase vouchers |
| **16** | **Alternate Units / Packaging** | 10 | Secondary unit conversion ratios: `DozenPcs.` (1 Dozen = 12 Pcs), `TonneKgs.` (1 Tonne = 1000 Kgs). | Linked to Item `CM3` |
| **21** | **Tax Categories** | 42 | Statutory GST slabs: `18% GST`, `12% GST`, `5% GST`, `28% GST`, `Exempt`, `Nil Rated`. | Linked to Item `CM2` |
| **22** | **TDS / TCS Categories** | 12 | Income Tax withholding sections: `194C Contractor`, `194J Professional`, `206C(1H) TCS on Sale`. | Applied in `TDS` and `TCS` tables |
| **25** | **GST Nature Categories** | 11 | Classification of supplies: `Regular`, `Composition`, `SEZ Developer`, `Deemed Export`. | Party tax classification |
| **28** | **Executive Groups** | 1 | Sales team departments and organizational hierarchies. | Parent for sales executives |
| **29** | **Salary Components** | 4 | Payroll pay heads: `Basic Salary`, `HRA`, `Conveyance Allowance`, `PF Deduction`. | Linked to employee ledger |
| **30** | **Discount Structures** | 15 | Automated trade discount matrices: `% of Amount`, `Absolute per unit`, `Compound Discount`. | Evaluated during voucher entry |
| **31** | **Markup Structures** | 16 | Cost-plus pricing rules and automatic markup configurations. | Evaluated during voucher entry |
| **55** | **Countries Master** | 43 | ISO country list for export/import billing: `India`, `United States`, `United Kingdom`, `Australia`, etc. | Linked to address country |
| **56** | **States Master** | 39 | Indian states and union territories with official 2-digit GST state codes (`06 Haryana`, `07 Delhi`, `09 UP`, `27 Maharashtra`). | Linked to `PartyStateCode` and place of supply |
| **60-68** | **CRM & Workflow Masters** | 28 | Lead sources, deal statuses, call types, customer stages, salutations. | Integrated CRM module |

---

## 4. Voucher Architecture (`Tran1.VchType`)

The `Tran1` table records all transaction headers. `VchType` defines the accounting nature and stock behavior of each voucher:

| `VchType` | Voucher Name | Typical Series / Prefix | Stock Effect | Accounting Ledger Effect | Real Data Example |
|:---------:|--------------|:-----------------------:|:------------:|:------------------------:|-------------------|
| **1** | **Payment Voucher** | `PMT-` | None | Credit: Cash/Bank; Debit: Expense/Creditor | Vendor dues settlements |
| **2** | **Purchase Bill** | `PUR-` | **+ Stock In** | Credit: Sundry Creditor; Debit: Purchase Account & Input GST | `PUR-1-26-27` |
| **3** | **Receipt Voucher** | `RCT-` | None | Debit: Cash/Bank; Credit: Sundry Debtor | Customer payments |
| **4** | **Journal Voucher** | `JRN-` | None | Double-entry journal adjustments | Depreciation, Accruals |
| **5** | **Contra Voucher** | `CNT-` | None | Transfer between Cash and Bank | Cash withdrawal / deposit |
| **6** | **Debit Note (Purchase Return)**| `DRN-` | **- Stock Out**| Debit: Creditor; Credit: Purchase Return & Input Tax Reversal | Return to supplier |
| **7** | **Credit Note (Sales Return)** | `CRN-` | **+ Stock In** | Debit: Sales Return & Output Tax Reversal; Credit: Debtor | `HPS  2CrN` |
| **8** | **Sales Return** | `SLR-` | **+ Stock In** | Similar to Credit Note with physical stock receipt | Goods returned by client |
| **9** | **Sales Invoice** | `HPS` / `INV-` | **- Stock Out**| Debit: Sundry Debtor; Credit: Sales Account & Output GST | `HPS00001` - `HPS00009` |
| **10** | **Purchase Return** | `PRR-` | **- Stock Out**| Goods returned to supplier | Debit Note physical entry |
| **11** | **Stock Transfer** | `STF-` | **Godown Move**| Transfers stock from Godown A (`MasterCode1`) to Godown B (`MasterCode2`)| Inter-branch / godown shift |
| **12** | **Production Voucher** | `PRD-` | **BOM Conversion**| Deducts raw materials; adds finished manufactured items | Assembly / BOM runs |
| **14** | **Receipt Voucher (Alt)** | `RCT-` | None | Fast-entry receipt voucher | Customer bank receipt |
| **16** | **Journal Voucher (Alt)** | `JRN-` | None | Multi-ledger adjustment journal | Opening balance transfers |
| **18** | **Credit Note (Post-GST)**| `CrN-` | Non-stock / Stock | Financial credit note (rate diff / discount)| Financial settlement |
| **19** | **Payment Voucher (Alt)** | `PMT-` | None | Direct payment voucher | Bank NEFT/RTGS payment |

---

## 5. Master Catalog of All 108 Tables

The tables are partitioned across 5 functional modular schema documents in `docs/busywin_schemas/`:

### [Module 1: Global Company Database (`db.bds`)](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md)
*Shared enterprise settings, multi-state profiles, user accounts, and print configurations (28 tables):*

1. [`BusyUserLog`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-busyuserlog) - Audit log recording user logins, logouts, terminal IDs, machine names, and session durations.
2. [`Company`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-company) - Master company profile (Legal name, Trade name, Address 1-4, PAN, GSTIN, FY range, Currency).
3. [`CustomScripts`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-customscripts) - User-defined VBScript or SQL event hooks.
4. [`DbImport`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-dbimport) - Legacy data import mapping definitions.
5. [`DictionarySL`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-dictionarysl) - Custom spelling dictionary and regional language translations.
6. [`FAQDatabase`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-faqdatabase) - Built-in help articles and operational FAQs.
7. [`FAQGroup`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-faqgroup) - FAQ topic categorization.
8. [`FormDetails`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-formdetails) - Continuous stationery dot matrix printing coordinates.
9. [`GSTFilingStatusDet`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-gstfilingstatusdet) - Statutory return filing history (GSTR-1, GSTR-3B ARN tracking).
10. [`GSTStatusDet`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-gststatusdet) - GST portal verification cache (Active/Suspended/Cancelled).
11. [`HSNStatusDet`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-hsnstatusdet) - HSN/SAC code validation library.
12. [`ImpNotes`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-impnotes) - System-wide important notes and company reminders.
13. [`MessageCentre`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-messagecentre) - Internal user messaging system.
14. [`MobileUser`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-mobileuser) - Registered Busy Mobile App devices and credentials.
15. [`MobileUserPreference`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-mobileuserpreference) - Permissions and menu access for mobile users.
16. [`NMCategory`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-nmcategory) - Notification categories.
17. [`NMNotes`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-nmnotes) - Notification messages and scheduled reminders.
18. [`OfflineMessage`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-offlinemessage) - Outbox queue for SMS, WhatsApp, and email alerts.
19. [`Patches`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-patches) - Version patch migration history for `db.bds`.
20. [`PrinterReps`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-printerreps) - Detailed report and invoice print format templates.
21. [`SQLQuery`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-sqlquery) - Saved user SQL queries and custom report filters.
22. [`ScreenReps`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-screenreps) - User-customized grid display layouts across screens.
23. [`StateCompanyDet`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-statecompanydet) - Multi-state GST branch registrations.
24. [`StdNar`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-stdnar) - Standard narration master library for quick voucher entry.
25. [`UserControl`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-usercontrol) - User accounts, passwords, and security roles.
26. [`UserLog`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-userlog) - Audit trail tracking user modifications and deletions.
27. [`UserPreferences`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-userpreferences) - Global company configuration flags (Inventory, Bill-by-Bill, Tax).
28. [`UserPreferences1`](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md#table-userpreferences1) - Extended parameters (E-Invoice, E-Way Bill credentials).

---

### [Module 2: Masters & Accounts (`db1YYYY.bds`)](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md)
*Polymorphic entities, parties, items, units, descriptions, and running balance caches (13 tables):*

1. [`Master1`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-master1) - Unified polymorphic master (Accounts, Parties, Items, Units, Tax Categories, Groups).
2. [`MasterAddressInfo`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-masteraddressinfo) - Extended party address, telephone, email, PAN, and GSTIN.
3. [`MasterSupport`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-mastersupport) - Secondary metadata (barcodes, custom fields, external ERP keys).
4. [`MastFootPrint`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-mastfootprint) - Audit footprint for master creation and modification.
5. [`ItemDesc`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-itemdesc) - Extended product descriptions and invoice technical specs.
6. [`ItemParamDet`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-itemparamdet) - Parameterized attributes (Size, Color, Shade, Batch).
7. [`ItemSerialNo`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-itemserialno) - Individual IMEI / Serial number lifecycle tracking.
8. [`ItemSNInstallDet`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-itemsninstalldet) - Serialized item commissioning and warranty details.
9. [`Folio1`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-folio1) - High-speed running account and inventory balance cache.
10. [`Help1`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-help1) - Auto-complete search index for UI dropdown lookups.
11. [`Help1AddnInfo`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-help1addninfo) - Secondary keyword index supporting Help1 search.
12. [`Help2`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-help2) - Lookup index for sub-entities, material centers, and cost centers.
13. [`DeletedMasters`](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md#table-deletedmasters) - Tombstone register of deleted master entities.

---

### [Module 3: Transactions & Vouchers (`db1YYYY.bds`)](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md)
*Voucher headers, dual-entry lines, bill sundries, godowns, and orders (24 tables):*

1. [`Tran1`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-tran1) - Master voucher header (VchType, VchNo, Date, Party, Net/Gross Amounts).
2. [`Tran2`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-tran2) - Double-entry transaction line items (Inventory items & Financial ledgers).
3. [`Tran3`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-tran3) - Bill sundry line items (Freight, Packing, Discounts, Round Off).
4. [`Tran4`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-tran4) - Material center / Godown location stock ledger.
5. [`Tran5`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-tran5) - Serial number and batch allocations for voucher line items.
6. [`Tran6`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-tran6) - Job work / process manufacturing ledger.
7. [`Tran7`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-tran7) - Cost center and project-level allocation records.
8. [`Tran8`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-tran8) - Pre-GST statutory sales tax declaration forms tracking.
9. [`Tran9`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-tran9) - Statutory form receipt and issuance settlement against bills.
10. [`Tran10`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-tran10) - Sales Order and Purchase Order delivery commitments.
11. [`Tran11`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-tran11) - Delivery Challan and Goods Receipt Note (GRN) linkage.
12. [`Tran12`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-tran12) - Voucher print audit log (print count, user, timestamp).
13. [`BillingDet`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-billingdet) - Consignee / Ship-to party name, address, GSTIN, and transporter.
14. [`VchOtherInfo`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-vchotherinfo) - Transporter, vehicle number, GR/LR number, payment terms.
15. [`DailySum`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-dailysum) - Daily financial and inventory aggregation cache for day-books.
16. [`DailyMessage`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-dailymessage) - Automated payment reminders and due-date notifications.
17. [`BRSOpBal`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-brsopbal) - Bank Reconciliation Statement opening uncleared cheques.
18. [`OrgSalePurc`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-orgsalepurc) - Original invoice references for Credit and Debit Notes.
19. [`POSDet`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-posdet) - Point of Sale (POS) multi-tender payment breakdown.
20. [`PackingDetails`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-packingdetails) - Packing slip, package weights, and dimensions.
21. [`JobFinishedRefs`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-jobfinishedrefs) - Finished goods batch reference generated from production BOM.
22. [`PhyStkSubDet`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-phystksubdet) - Physical stock verification audit lines and variances.
23. [`VchTemplate`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-vchtemplate) - Reusable transaction templates for recurring monthly vouchers.
24. [`VchTempTagging`](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md#table-vchtemptagging) - Tagging rules linking vouchers to transaction templates.

---

### [Module 4: GST, Statutory & Compliance (`db1YYYY.bds`)](./busywin_schemas/04_FY_GST_AND_STATUTORY.md)
*GST calculations, E-Way Bill, E-Commerce reconciliations, TDS/TCS, and VAT (25 tables):*

1. [`VchGSTSumItemWise`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-vchgstsumitemwise) - Item-level GST summary (HSN, Taxable Value, CGST/SGST/IGST, Cess).
2. [`GSTInfo`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-gstinfo) - General GST statutory register records and tax adjustments.
3. [`GSTITCPendingVchDet`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-gstitcpendingvchdet) - Input Tax Credit (ITC) reversal tracking (Rule 37, 42, 43).
4. [`GSTR1Info`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-gstr1info) - GSTR-1 return filing snapshot data (B2B, B2CL, B2CS, CDNR, EXP).
5. [`GSTR2AInfo`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-gstr2ainfo) - GSTR-2A auto-drafted inward supplies for supplier reconciliation.
6. [`GSTR2BInfo`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-gstr2binfo) - GSTR-2B static monthly ITC statements imported from GST Portal.
7. [`GSTR3BInfo`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-gstr3binfo) - GSTR-3B monthly summary return calculation register.
8. [`GetGeneratedEWayBillDet`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-getgeneratedewaybilldet) - E-Way Bill cache (EWB Number, date, validity, vehicle).
9. [`TCS`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-tcs) - Tax Collected at Source (Section 206C) register and challans.
10. [`TDS`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-tds) - Tax Deducted at Source (Section 194C, 194J, 194Q) deductions.
11. [`STDet`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-stdet) - Pre-GST Service Tax calculation details.
12. [`Excise`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-excise) - Central Excise invoice details and RG23A / PLA registers.
13. [`TradingExcise`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-tradingexcise) - First/second-stage dealer RG23D register tracking.
14. [`VATInfo`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-vatinfo) - State VAT statutory returns and annexures.
15. [`VchVATAccInfo`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-vchvataccinfo) - State VAT ledger account posting details.
16. [`VchVATSum`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-vchvatsum) - Voucher-level VAT calculation summary.
17. [`VchVATSumItemWise`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-vchvatsumitemwise) - Item-level VAT calculation breakdown.
18. [`EComOrderHeader`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-ecomorderheader) - E-commerce orders (Amazon, Flipkart) header data.
19. [`EComOrderBody`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-ecomorderbody) - E-commerce order items, marketplace SKU mapping, and returns.
20. [`EcomSettlement`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-ecomsettlement) - Marketplace payment settlement header.
21. [`EcomSettlementExp`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-ecomsettlementexp) - Marketplace commission, shipping, and promotional fees.
22. [`EcomSettlementItem`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-ecomsettlementitem) - Order-level payment reconciliation within settlement batches.
23. [`EcomSettlementItemExp`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-ecomsettlementitemexp) - Item-level fee deductions applied by marketplaces.
24. [`EmpLADet`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-empladet) - Employee Loan and Advance disbursement and payroll recovery.
25. [`AMCWarrDet`](./busywin_schemas/04_FY_GST_AND_STATUTORY.md#table-amcwarrdet) - Annual Maintenance Contract (AMC) and warranty tracking.

---

### [Module 5: System, Configuration & Audit (`db1YYYY.bds`)](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md)
*Internal configuration flags, concurrency locks, audit logs, and cloud synchronization (18 tables):*

1. [`Config`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-config) - Company FY configuration repository (180+ feature flags, numbering rules).
2. [`Locks`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-locks) - Concurrency locking table preventing multi-user collisions.
3. [`EventLog`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-eventlog) - User operation log (vouchers added, modified, deleted, printed).
4. [`DeletedInfo`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-deletedinfo) - Audit log of deleted vouchers (VchNo, date, original amount, user).
5. [`QueryLog`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-querylog) - Diagnostic SQL execution log and database errors.
6. [`DataSync`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-datasync) - Multi-branch data synchronization journal and packet status.
7. [`CloudSyncStatus`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-cloudsyncstatus) - Overall status of Busy Cloud synchronization.
8. [`CloudSyncIncr`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-cloudsyncincr) - Queue of incremental database changes pending upload.
9. [`CloudSyncIncrDet`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-cloudsyncincrdet) - XML payloads of incremental changes.
10. [`CheckList`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-checklist) - Task checklist items and workflow approval state.
11. [`CheckListNew`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-checklistnew) - Workflow approval headers for multi-level authorizations.
12. [`CheckListNewDet`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-checklistnewdet) - Workflow authorization signatures and approval payloads.
13. [`RepColSize`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-repcolsize) - User-customized report column widths and display orders.
14. [`RepOptValues`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-repoptvalues) - Saved report filter presets (date ranges, party filters).
15. [`ReportNotes`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-reportnotes) - Annotations and sticky notes attached to financial reports.
16. [`Patches`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-patches) - Version migration patches applied to `db1YYYY.bds`.
17. [`ExternalData`](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md#table-externaldata) - Integration bridge for external CRM, WMS, and ERP systems.

---

## 6. Core Tables Detailed Schema Walkthrough

The following 7 tables form the computational core of BusyWin. Full column listings and accounting semantics:

### 1. `Company` (in `db.bds`)
Primary company profile record storing corporate identity, statutory tax registrations, and accounting constraints.

| Column | Type | Role & Accounting Semantics |
|--------|------|------------------------------|
| `Name` | `VARCHAR(40)` | Registered business legal name (e.g. `HPS FURNITURE & DECORATION`). |
| `PrintName` | `VARCHAR(60)` | Trading name printed on invoices, credit notes, and quotations. |
| `Address1` - `Address4` | `VARCHAR(40)` | Registered business postal address lines 1 through 4. |
| `TelNo` | `VARCHAR(40)` | Official landline telephone number. |
| `Email` | `VARCHAR(80)` | Business communication email address. |
| `ITPAN` | `VARCHAR(20)` | 10-character Income Tax Permanent Account Number (PAN). |
| `LST` / `CST` / `TINNo` | `VARCHAR(30)` | Historical state sales tax and CST registration numbers. |
| `ExciseRegNo` | `VARCHAR(30)` | Central Excise registration number. |
| `FYBeginning` | `DATETIME` | Start date of the current financial year (e.g. `2026-04-01`). |
| `BooksBeginning` | `DATETIME` | Effective date from which computerized books are maintained. |
| `BaseCurrencySymbol` | `VARCHAR(5)` | Currency symbol (`₹`, `$`). |
| `BaseCurrencySubUnit` | `VARCHAR(10)` | Fractional currency name (`Paise`, `Cents`). |

---

### 2. `Master1` (in `db1YYYY.bds`)
The polymorphic master table holding all entities. **156 columns**, Primary Key: `Code`.

| Column | Type | Role & Accounting Semantics |
|--------|------|------------------------------|
| `Code` | `INTEGER (Long)` | **Primary Key**: Unique auto-increment master ID. |
| `MasterType` | `SMALLINT` | Entity discriminator (1=Group, 2=Account, 6=Item, 8=Unit, 21=TaxCategory). |
| `Name` | `VARCHAR(40)` | Full master name displayed in software lists and lookups. |
| `Alias` | `VARCHAR(40)` | Short lookup code or barcode shortcut. |
| `PrintName` | `VARCHAR(60)` | Name formatted for printing on customer invoices and registers. |
| `ParentGrp` | `INTEGER (Long)` | **Foreign Key**: Points to parent `Master1.Code` (Account Group or Item Group). |
| `CM1` | `INTEGER (Long)` | **Context Master 1**: For Items = Unit (`MasterType 8`); For Accounts = Price Level (`MasterType 12`). |
| `CM2` | `INTEGER (Long)` | **Context Master 2**: For Items = Tax Category (`MasterType 21`, e.g. 18% GST). |
| `CM3` | `INTEGER (Long)` | **Context Master 3**: For Items = Alternate packaging unit (`MasterType 8`). |
| `D1` | `DOUBLE` | Item Default Selling Price. |
| `D2` | `DOUBLE` | Item Default Purchase Price. |
| `D3` | `DOUBLE` | Item Maximum Retail Price (MRP). |
| `D4` | `DOUBLE` | Item Minimum Selling Price threshold. |
| `D5` | `DOUBLE` | Item Standard Cost / Self Price. |
| `D7` | `DOUBLE` | Opening Inventory Quantity. |
| `D8` | `DOUBLE` | Opening Inventory Valuation Amount. |
| `Stamp` | `INTEGER (Long)` | Modification concurrency revision sequence. |

---

### 3. `MasterAddressInfo` (in `db1YYYY.bds`)
Extended contact information table linked 1-to-1 with `Master1.Code`.

| Column | Type | Role & Accounting Semantics |
|--------|------|------------------------------|
| `MasterCode` | `INTEGER (Long)` | **Primary Key & Foreign Key**: Points to `Master1.Code`. |
| `Address1` - `Address4` | `VARCHAR(40)` | Postal address of the customer, vendor, or bank branch. |
| `TelNo` | `VARCHAR(40)` | Landline telephone number. |
| `Mobile` | `VARCHAR(255)` | Contact mobile number for SMS/WhatsApp invoice delivery. |
| `Email` | `VARCHAR(255)` | Billing email address for electronic dispatch. |
| `Contact` | `VARCHAR(40)` | Primary contact person / key account manager. |
| `ITPAN` | `VARCHAR(20)` | Party Income Tax PAN (e.g. `BPSPS2861B`). |
| `GSTNo` | `VARCHAR(20)` | 15-character GSTIN (e.g. `06BPSPS2861B1ZO`). |
| `AadharNo` | `VARCHAR(20)` | Individual Aadhaar number (for proprietary firms). |

---

### 4. `Tran1` (in `db1YYYY.bds`)
Master voucher transaction header table. **117 columns**, Primary Key: `VchCode`.

| Column | Type | Role & Accounting Semantics |
|--------|------|------------------------------|
| `VchCode` | `INTEGER (Long)` | **Primary Key**: Unique internal voucher transaction identifier. |
| `VchType` | `SMALLINT` | Voucher classification (2=Purchase, 9=Sales, 18=CreditNote, 19=Payment). |
| `Date` | `DATETIME` | Transaction / Invoice Date. |
| `VchNo` | `VARCHAR(25)` | Document sequence number (e.g. `HPS00001`, `PUR-1-26-27`). |
| `VchSeriesCode` | `INTEGER (Long)` | Foreign Key to configured voucher numbering series. |
| `MasterCode1` | `INTEGER (Long)` | **Foreign Key**: Primary Party (`Master1.Code` where `MasterType = 2`). |
| `MasterCode2` | `INTEGER (Long)` | Secondary Account (Cash/Bank ledger or Contra account). |
| `VchSalePurcAmt`| `DOUBLE` | Total net taxable supply value before bill sundries. |
| `VchAmtBaseCur` | `DOUBLE` | **Gross Invoice Total Payable** in base currency. |
| `VchCancelled` | `BOOLEAN` | Cancellation status flag (1=Cancelled, 0=Active). |
| `Nar1` / `Nar2` | `VARCHAR(100)` | Voucher narration / remarks lines. |
| `CurConRate` | `DOUBLE` | Forex currency conversion exchange rate. |

---

### 5. `Tran2` (in `db1YYYY.bds`)
Transaction line items and double-entry general ledger postings. **104 columns**.

| Column | Type | Role & Accounting Semantics |
|--------|------|------------------------------|
| `RecType` | `SMALLINT` | Record discriminator (1=Inventory Line Item, 2=Bill Sundry, 3=Ledger Debit/Credit). |
| `VchCode` | `INTEGER (Long)` | **Foreign Key**: Links to `Tran1.VchCode`. |
| `SrNo` | `SMALLINT` | Line item display order sequence. |
| `MasterCode1` | `INTEGER (Long)` | For Inventory: Item Code (`Master1.Code`, Type 6); For Ledger: Account Code (`Master1.Code`, Type 2). |
| `MasterCode2` | `INTEGER (Long)` | Storage Godown (`Master1.Code`, Type 11) or Contra ledger. |
| `Value1` | `DOUBLE` | **Quantity** (for inventory lines) or **Amount** (for financial debit/credit entries). |
| `Value2` | `DOUBLE` | **Unit Price / Rate** per measurement unit. |
| `Value3` | `DOUBLE` | **Total Line Amount** (`Value1` * `Value2`) before taxes. |
| `Balance1` | `DOUBLE` | Running stock balance after transaction execution. |
| `CashFlow` | `DOUBLE` | Net cash flow impact of this line entry. |
| `ShortNar` | `VARCHAR(40)` | Item-specific description or ledger transaction remarks. |

---

### 6. `VchGSTSumItemWise` (in `db1YYYY.bds`)
Item-level statutory GST tax calculation breakdown table. **52 columns**.

| Column | Type | Role & Accounting Semantics |
|--------|------|------------------------------|
| `VchCode` | `INTEGER (Long)` | **Foreign Key**: Links to `Tran1.VchCode`. |
| `ItemCode` | `INTEGER (Long)` | **Foreign Key**: Links to `Master1.Code` (Inventory Item). |
| `ItemSrNo` | `SMALLINT` | Corresponding line item sequence number matching `Tran2.SrNo`. |
| `PartyCode` | `INTEGER (Long)` | **Foreign Key**: Customer or Vendor party (`Master1.Code`). |
| `HSNCode` | `VARCHAR(255)` | Harmonized System of Nomenclature code (e.g. `9403`, `7606`). |
| `TaxableAmt` | `DOUBLE` | Net assessable value subject to tax. |
| `TaxRate` | `DOUBLE` | Total combined GST tax rate percentage (e.g. `18.0`). |
| `TaxAmt` | `DOUBLE` | Total GST amount calculated on this line item. |
| `CGSTRate` / `CGSTAmt` | `DOUBLE` | Central GST rate and calculated tax value (e.g. 9% / ₹90.00). |
| `SGSTRate` / `SGSTAmt` | `DOUBLE` | State GST rate and calculated tax value (e.g. 9% / ₹90.00). |
| `IGSTRate` / `IGSTAmt` | `DOUBLE` | Integrated GST rate and calculated tax value (for inter-state supplies, e.g. 18%). |
| `CessRate` / `CessAmt` | `DOUBLE` | Compensation Cess percentage and calculated cess amount. |
| `PartyStateCode` | `INTEGER (Long)`| Place of Supply state code (e.g. `6` for Haryana, `7` for Delhi). |
| `ItemMainQty` | `DOUBLE` | Billed item quantity. |

---

### 7. `BillingDet` (in `db1YYYY.bds`)
Consignee, shipping address, and transport logistics details attached to invoices. **31 columns**.

| Column | Type | Role & Accounting Semantics |
|--------|------|------------------------------|
| `VchCode` | `INTEGER (Long)` | **Foreign Key**: Links to `Tran1.VchCode`. |
| `PartyName` | `VARCHAR(60)` | Consignee / Ship-to trade name (if different from billed party). |
| `Address1` - `Address4` | `VARCHAR(40)` | Delivery destination shipping address lines. |
| `StateCode` | `INTEGER (Long)` | Destination state code for determining intra-state vs inter-state GST. |
| `MobileNo` | `VARCHAR(255)` | Delivery recipient contact phone number. |
| `Email` | `VARCHAR(255)` | Delivery recipient email address. |
| `ITPAN` | `VARCHAR(20)` | Consignee Income Tax PAN. |
| `TransporterName` | `VARCHAR(60)` | Transport carrier company name. |
| `VehicleNo` | `VARCHAR(30)` | Commercial vehicle registration number for E-Way Bill generation. |

---

## 7. Data Mapping Guide: BusyWin to ARTHA Architecture

The table below demonstrates how BusyWin's relational database maps directly into ARTHA's modern JSON-based storage engine:

| BusyWin Source Tables & Fields | ARTHA Target File & Structure | Transformation Logic & Notes |
|--------------------------------|-------------------------------|------------------------------|
| **`Company`** (`db.bds`)<br>• `Name`, `PrintName`<br>• `Address1`..`Address4`<br>• `TelNo`, `Email`, `ITPAN`<br>• `GSTStatusDet.GSTIN` | **`data/profile.json`**<br>`{ "tradeName", "legalName", "address", "phone", "email", "pan", "gstin", "state", "pincode" }` | Consolidated into a single clean enterprise profile document. State code mapped via standard 2-digit GST state dictionary. |
| **`Master1`** (`db1YYYY.bds`) where `MasterType = 8`<br>• `Name`, `Alias` | **`data/products/*.json`** (`unit`) & Unit presets | Unit codes extracted (`Pcs.`, `SQFT`, `RFT`, `Box`, `Kgs.`, `CBM`) and assigned as standard product units. |
| **`Master1`** (`db1YYYY.bds`) where `MasterType = 6`<br>• `Code`, `Name`, `D1` (Sale Price)<br>• `ItemDesc.Desc1`..`Desc5`<br>• `VchGSTSumItemWise.HSNCode` | **`data/products/<id>.json`**<br>`{ "id", "name", "rate", "hsn", "taxRate", "unit", "description" }` | Product master generated with HSN code, tax rate from linked Tax Category (`CM2`), and selling price. |
| **`Master1`** (`db1YYYY.bds`) where `MasterType = 2`<br>• `Code`, `Name`<br>• `MasterAddressInfo` (`Address1`..`4`, `TelNo`, `Mobile`, `Email`, `ITPAN`, `GSTNo`) | **`data/clients/<id>.json`**<br>`{ "id", "name", "address", "phone", "email", "pan", "gstin", "state", "pincode" }` | Customer and vendor party ledgers extracted with full postal address, contact details, PAN, and 15-digit GSTIN. |
| **`Tran1`** (`db1YYYY.bds`) where `VchType = 9` (Sales)<br>• `Tran2` (Lines: `Value1` Qty, `Value2` Rate)<br>• `VchGSTSumItemWise` (CGST, SGST, IGST)<br>• `BillingDet` (Ship-to address) | **`data/bills/<id>.json`**<br>`{ "id", "billNo", "billDate", "clientId", "items": [...], "subtotal", "cgst", "sgst", "igst", "total" }` | Outward sales invoices mapped with itemized line items, applied tax breakdowns, and shipping consignee details. |
| **`Tran1`** (`db1YYYY.bds`) where `VchType = 2` (Purchases)<br>• `Tran2` (Inward item lines)<br>• `VchGSTSumItemWise` (Input tax credit) | **`data/purchases/<id>.json`**<br>`{ "id", "billNo", "billDate", "vendorId", "items": [...], "taxableAmount", "taxAmount", "total" }` | Inward purchase bills mapped with vendor references, input tax credits, and purchase costs. |

---

## 8. Querying BusyWin via Python / ADODB

To inspect or query BusyWin Jet databases programmatically, use the following tested Python snippet:

```python
import win32com.client

PASSWORD = "ILoveMyINDIA"
DB_PATH = r"C:\BusyWin\DATA\COMP0001\db12026.bds"

# Connect via OLEDB
conn = win32com.client.Dispatch("ADODB.Connection")
connStr = f"Provider=Microsoft.ACE.OLEDB.12.0;Data Source={DB_PATH};Jet OLEDB:Database Password={PASSWORD};"
conn.Open(connStr)

# Query Sales Invoices with Party Names
sql = '''
SELECT 
    t1.VchCode,
    t1.VchNo,
    t1.[Date] AS InvoiceDate,
    m1.Name AS CustomerName,
    t1.VchSalePurcAmt AS TaxableAmount,
    t1.VchAmtBaseCur AS TotalAmount
FROM Tran1 t1
INNER JOIN Master1 m1 ON t1.MasterCode1 = m1.Code
WHERE t1.VchType = 9 AND t1.VchCancelled = 0
ORDER BY t1.[Date] DESC
'''

rs = conn.Execute(sql)[0]
while not rs.EOF:
    vch_no = rs.Fields("VchNo").Value.strip()
    customer = rs.Fields("CustomerName").Value
    total = rs.Fields("TotalAmount").Value
    print(f"Invoice {vch_no:15} | Customer: {customer:30} | Total: Rs. {total:10.2f}")
    rs.MoveNext()

rs.Close()
conn.Close()
```

---

## 9. Modular Documentation Directory Map

For the complete column-by-column schemas of all 108 tables, refer to the individual documents:

- 📄 **[Module 1: Company Database (`db.bds`)](./busywin_schemas/01_COMPANY_DATABASE_db_bds.md)** — 28 tables, 1,174 columns.
- 📄 **[Module 2: FY Masters & Accounts](./busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md)** — 13 tables, 680+ columns.
- 📄 **[Module 3: FY Transactions & Vouchers](./busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md)** — 24 tables, 590+ columns.
- 📄 **[Module 4: FY GST, Statutory & Tax](./busywin_schemas/04_FY_GST_AND_STATUTORY.md)** — 25 tables, 750+ columns.
- 📄 **[Module 5: FY System & Configuration](./busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md)** — 18 tables, 430+ columns.
"""

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Master document generated at: {OUTPUT_FILE} ({len(content)} bytes)")


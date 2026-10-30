# BusyWin Company Database Schema (`db.bds`)

> **Location:** `C:\BusyWin\DATA\COMP0001\db.bds` (or respective company folder)

> **Engine:** Microsoft Jet 4.0 / Access (`Microsoft.ACE.OLEDB.12.0`)

> **Encryption Password:** `ILoveMyINDIA`

> **Total Tables:** 28 | **Total Columns:** 1,174


The Company Database (`db.bds`) resides at the root of each company directory and stores **global company settings, multi-state GST profiles, user permissions, audit logs, printing templates, and custom scripts**. Unlike financial year databases (`db1YYYY.bds`), `db.bds` is shared across all accounting years for that enterprise.


## Table Summary Index


| # | Table Name | Columns | Active Rows | Primary Role |
|---|------------|:-------:|:-----------:|--------------|
| 1 | [`BusyUserLog`](#table-busyuserlog) | 19 | 0 | Audit log recording user logins, logouts, terminal IDs, machine names, and session durations. |
| 2 | [`Company`](#table-company) | 126 | 1 | Master company profile storing firm legal name, trade name, address lines 1-4, contact info, PAN, GSTIN, CIN, currency, financial year range, books beginning date, decimal precision, and company-level accounting mode. |
| 3 | [`CustomScripts`](#table-customscripts) | 3 | 0 | User-defined VBScript or SQL hooks executed on database events (e.g., before save, after save validation). |
| 4 | [`DbImport`](#table-dbimport) | 38 | 0 | Mapping configurations and field parameters for importing data from legacy or third-party formats. |
| 5 | [`DictionarySL`](#table-dictionarysl) | 6 | 0 | Custom spelling dictionary and regional language font translations used during voucher entry. |
| 6 | [`FAQDatabase`](#table-faqdatabase) | 5 | 0 | Built-in knowledge base articles and operational FAQs accessible from the BusyWin UI. |
| 7 | [`FAQGroup`](#table-faqgroup) | 3 | 2 | Grouping and categorization definitions for FAQ topics. |
| 8 | [`FormDetails`](#table-formdetails) | 6 | 0 | Voucher and document printing coordinate templates for continuous pre-printed stationery (dot matrix). |
| 9 | [`GSTFilingStatusDet`](#table-gstfilingstatusdet) | 11 | 0 | Filing history of statutory GST returns (GSTR-1, GSTR-3B, GSTR-9) including ARN and filing dates. |
| 10 | [`GSTStatusDet`](#table-gststatusdet) | 29 | 6 | GST portal taxpayer verification cache (Trade name, Legal name, Status: Active/Suspended/Cancelled). |
| 11 | [`HSNStatusDet`](#table-hsnstatusdet) | 12 | 0 | Harmonized System of Nomenclature (HSN) and Service Accounting Code (SAC) validation and master cache. |
| 12 | [`ImpNotes`](#table-impnotes) | 5 | 0 | System-wide important notes and critical business reminders shared across operators. |
| 13 | [`MessageCentre`](#table-messagecentre) | 15 | 0 | Internal messaging system between Busy operators within a LAN/WAN installation. |
| 14 | [`MobileUser`](#table-mobileuser) | 98 | 0 | Registered mobile devices, phone numbers, and authentication credentials for Busy Mobile App access. |
| 15 | [`MobileUserPreference`](#table-mobileuserpreference) | 98 | 0 | Permissions, menu access rights, and data visibility rules for Busy Mobile App users. |
| 16 | [`NMCategory`](#table-nmcategory) | 4 | 0 | Notification categories (e.g., Payment Alerts, Low Stock Warnings, Tax Deadlines). |
| 17 | [`NMNotes`](#table-nmnotes) | 10 | 0 | Notification message bodies, alert text, and scheduled notification tasks. |
| 18 | [`OfflineMessage`](#table-offlinemessage) | 15 | 0 | Outbox queue for SMS, WhatsApp, and email alerts waiting to be dispatched by the background worker. |
| 19 | [`Patches`](#table-patches) | 7 | 0 | Version migration patch history applied to the operational database (db1YYYY.bds). |
| 20 | [`PrinterReps`](#table-printerreps) | 149 | 607 | Detailed report and invoice print format definitions (standard / advanced layouts, headers, margins, fonts). |
| 21 | [`SQLQuery`](#table-sqlquery) | 5 | 0 | Saved user SQL queries and custom report filters created through the interactive query designer. |
| 22 | [`ScreenReps`](#table-screenreps) | 4 | 0 | User-customized grid display layouts (column order, widths, visibility) across data entry screens. |
| 23 | [`StateCompanyDet`](#table-statecompanydet) | 54 | 0 | Multi-state GST branch company registrations under the unified company umbrella. |
| 24 | [`StdNar`](#table-stdnar) | 3 | 0 | Standard narration master library for quick lookup and selection in voucher entry. |
| 25 | [`UserControl`](#table-usercontrol) | 30 | 6 | User credentials, passwords, security roles, and feature access permissions. |
| 26 | [`UserLog`](#table-userlog) | 3 | 0 | Audit trail tracking user operations (creation, modification, and deletion of masters and transactions). |
| 27 | [`UserPreferences`](#table-userpreferences) | 255 | 1 | Primary company configuration flags (Inventory, Bill-by-Bill, Multi-Currency, Batch/Expiry, Tax rules). |
| 28 | [`UserPreferences1`](#table-userpreferences1) | 161 | 1 | Extended configuration parameters (E-Invoice, E-Way Bill credentials, Cloud backup settings). |

---

## Complete Table Schemas


<a name="table-busyuserlog"></a>

### Table: `BusyUserLog`

> **Purpose:** Audit log recording user logins, logouts, terminal IDs, machine names, and session durations.

- **Row Count in Active FY:** `0`
- **Total Columns:** `19`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `UserName` | `WCHAR(20.0)` | Yes |  | Operator username who performed the action |
| 2 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 3 | `WorkedOn` | `SMALLINT` | Yes |  | Integer identifier or enum code for WorkedOn |
| 4 | `Type` | `SMALLINT` | Yes |  | Integer identifier or enum code for Type |
| 5 | `LogFor` | `SMALLINT` | Yes |  | Integer identifier or enum code for LogFor |
| 6 | `S1` | `WCHAR(255.0)` | Yes |  | Text attribute: S1 |
| 7 | `S2` | `WCHAR(255.0)` | Yes |  | Text attribute: S2 |
| 8 | `L1` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L1 |
| 9 | `L2` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L2 |
| 10 | `L3` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L3 |
| 11 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 12 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 13 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 14 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 15 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 16 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 17 | `Description` | `WCHAR` | Yes |  | Text attribute: Description |
| 18 | `ComputerName` | `WCHAR(40.0)` | Yes |  | Text attribute: ComputerName |
| 19 | `Particular` | `WCHAR(255.0)` | Yes |  | Text attribute: Particular |

---

<a name="table-company"></a>

### Table: `Company`

> **Purpose:** Master company profile storing firm legal name, trade name, address lines 1-4, contact info, PAN, GSTIN, CIN, currency, financial year range, books beginning date, decimal precision, and company-level accounting mode.

- **Row Count in Active FY:** `1`
- **Total Columns:** `126`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Name` | `WCHAR(40.0)` | Yes |  | Text attribute: Name |
| 2 | `PrintName` | `WCHAR(60.0)` | Yes |  | Text attribute: PrintName |
| 3 | `Address1` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 4 | `Address2` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 5 | `Address3` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 6 | `Address4` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 7 | `TelNo` | `WCHAR(40.0)` | Yes |  | Fixed-line landline telephone number |
| 8 | `Fax` | `WCHAR(30.0)` | Yes |  | Text attribute: Fax |
| 9 | `Email` | `WCHAR(80.0)` | Yes |  | Official email address for communication and e-invoicing |
| 10 | `ITPAN` | `WCHAR(20.0)` | Yes |  | Income Tax Permanent Account Number (PAN) |
| 11 | `ITWard` | `WCHAR(20.0)` | Yes |  | Text attribute: ITWard |
| 12 | `LST` | `WCHAR(30.0)` | Yes |  | Text attribute: LST |
| 13 | `CST` | `WCHAR(30.0)` | Yes |  | Text attribute: CST |
| 14 | `ST_37` | `WCHAR(30.0)` | Yes |  | Text attribute: ST_37 |
| 15 | `STWardNo` | `WCHAR(20.0)` | Yes |  | Text attribute: STWardNo |
| 16 | `ExciseRegNo` | `WCHAR(30.0)` | Yes |  | Text attribute: ExciseRegNo |
| 17 | `ECCCode` | `WCHAR(20.0)` | Yes |  | Text attribute: ECCCode |
| 18 | `PLANo` | `WCHAR(20.0)` | Yes |  | Text attribute: PLANo |
| 19 | `Range` | `WCHAR(80.0)` | Yes |  | Text attribute: Range |
| 20 | `Division` | `WCHAR(80.0)` | Yes |  | Text attribute: Division |
| 21 | `Collectorate` | `WCHAR(40.0)` | Yes |  | Text attribute: Collectorate |
| 22 | `TINNo` | `WCHAR(30.0)` | Yes |  | Text attribute: TINNo |
| 23 | `GSTNo` | `WCHAR(30.0)` | Yes |  | Text attribute: GSTNo |
| 24 | `C1` | `WCHAR(80.0)` | Yes |  | Text attribute: C1 |
| 25 | `C2` | `WCHAR(80.0)` | Yes |  | Text attribute: C2 |
| 26 | `OtherDet1` | `WCHAR(40.0)` | Yes |  | Text attribute: OtherDet1 |
| 27 | `OtherDet2` | `WCHAR(40.0)` | Yes |  | Text attribute: OtherDet2 |
| 28 | `OtherDet3` | `WCHAR(40.0)` | Yes |  | Text attribute: OtherDet3 |
| 29 | `TANNo` | `WCHAR(40.0)` | Yes |  | Text attribute: TANNo |
| 30 | `TDSCaption` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSCaption |
| 31 | `TDSCircle` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSCircle |
| 32 | `TDSPayerCategory` | `SMALLINT` | Yes |  | Integer identifier or enum code for TDSPayerCategory |
| 33 | `PersonName` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonName |
| 34 | `Designation` | `WCHAR(40.0)` | Yes |  | Text attribute: Designation |
| 35 | `PersonPANNo` | `WCHAR(20.0)` | Yes |  | Text attribute: PersonPANNo |
| 36 | `GuardianName` | `WCHAR(40.0)` | Yes |  | Text attribute: GuardianName |
| 37 | `PersonAddress1` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonAddress1 |
| 38 | `PersonAddress2` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonAddress2 |
| 39 | `PersonAddress3` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonAddress3 |
| 40 | `PersonAddress4` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonAddress4 |
| 41 | `PersonAddress5` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonAddress5 |
| 42 | `PersonStateCode` | `SMALLINT` | Yes |  | Integer identifier or enum code for PersonStateCode |
| 43 | `PersonPinCode` | `WCHAR(10.0)` | Yes |  | Text attribute: PersonPinCode |
| 44 | `PersonStdCode` | `WCHAR(10.0)` | Yes |  | Text attribute: PersonStdCode |
| 45 | `PersonPhoneNo` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonPhoneNo |
| 46 | `PersonEmail` | `WCHAR(80.0)` | Yes |  | Text attribute: PersonEmail |
| 47 | `PersonMobileNo` | `WCHAR(80.0)` | Yes |  | Text attribute: PersonMobileNo |
| 48 | `PersonAltStdCode` | `WCHAR(10.0)` | Yes |  | Text attribute: PersonAltStdCode |
| 49 | `PersonAltPhoneNo` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonAltPhoneNo |
| 50 | `PersonAltEmail` | `WCHAR(80.0)` | Yes |  | Text attribute: PersonAltEmail |
| 51 | `TDSAdd1` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSAdd1 |
| 52 | `TDSAdd2` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSAdd2 |
| 53 | `TDSAdd3` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSAdd3 |
| 54 | `TDSAdd4` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSAdd4 |
| 55 | `TDSAdd5` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSAdd5 |
| 56 | `TDSStateCode` | `SMALLINT` | Yes |  | Integer identifier or enum code for TDSStateCode |
| 57 | `TDSPinCode` | `WCHAR(10.0)` | Yes |  | Text attribute: TDSPinCode |
| 58 | `TDSStdCode` | `WCHAR(10.0)` | Yes |  | Text attribute: TDSStdCode |
| 59 | `TDSPhoneNo` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSPhoneNo |
| 60 | `TDSEmail` | `WCHAR(80.0)` | Yes |  | Text attribute: TDSEmail |
| 61 | `TDSAltStdCode` | `WCHAR(10.0)` | Yes |  | Text attribute: TDSAltStdCode |
| 62 | `TDSAltPhoneNo` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSAltPhoneNo |
| 63 | `TDSAltEmail` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSAltEmail |
| 64 | `VATPersonName` | `WCHAR(40.0)` | Yes |  | Text attribute: VATPersonName |
| 65 | `VATDesignation` | `WCHAR(40.0)` | Yes |  | Text attribute: VATDesignation |
| 66 | `VATGuardianName` | `WCHAR(40.0)` | Yes |  | Text attribute: VATGuardianName |
| 67 | `VATMobileNo` | `WCHAR(40.0)` | Yes |  | Text attribute: VATMobileNo |
| 68 | `VATEmail` | `WCHAR(40.0)` | Yes |  | Text attribute: VATEmail |
| 69 | `CreatedOn` | `DATETIME` | Yes |  | Timestamp / Date field for CreatedOn |
| 70 | `SerialNo` | `WCHAR(20.0)` | Yes |  | Text attribute: SerialNo |
| 71 | `BegFY` | `DATETIME` | Yes |  | Timestamp / Date field for BegFY |
| 72 | `CurFY` | `DATETIME` | Yes |  | Timestamp / Date field for CurFY |
| 73 | `BooksStart` | `DATETIME` | Yes |  | Timestamp / Date field for BooksStart |
| 74 | `FreezDate` | `DATETIME` | Yes |  | Timestamp / Date field for FreezDate |
| 75 | `ProductName` | `WCHAR(10.0)` | Yes |  | Text attribute: ProductName |
| 76 | `Major` | `SMALLINT` | Yes |  | Integer identifier or enum code for Major |
| 77 | `Minor` | `SMALLINT` | Yes |  | Integer identifier or enum code for Minor |
| 78 | `Revision` | `WCHAR(1.0)` | Yes |  | Text attribute: Revision |
| 79 | `STCNo` | `WCHAR(30.0)` | Yes |  | Text attribute: STCNo |
| 80 | `PremisesCode` | `WCHAR(20.0)` | Yes |  | Text attribute: PremisesCode |
| 81 | `TaxableService` | `WCHAR(40.0)` | Yes |  | Text attribute: TaxableService |
| 82 | `STPersonName` | `WCHAR(40.0)` | Yes |  | Text attribute: STPersonName |
| 83 | `STDesignation` | `WCHAR(40.0)` | Yes |  | Text attribute: STDesignation |
| 84 | `STGuardianName` | `WCHAR(40.0)` | Yes |  | Text attribute: STGuardianName |
| 85 | `FNIPS` | `BOOLEAN` | No |  | Boolean flag for FNIPS (True/False) |
| 86 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 87 | `FreezeType` | `SMALLINT` | Yes |  | Integer identifier or enum code for FreezeType |
| 88 | `DataFreeze` | `BOOLEAN` | No |  | Boolean flag for DataFreeze (True/False) |
| 89 | `GUID` | `WCHAR(40.0)` | Yes |  | Text attribute: GUID |
| 90 | `DLNo` | `WCHAR(255.0)` | Yes |  | Text attribute: DLNo |
| 91 | `POSZEROAMTBS` | `BOOLEAN` | No |  | Boolean flag for POSZEROAMTBS (True/False) |
| 92 | `DLNo2` | `WCHAR(255.0)` | Yes |  | Text attribute: DLNo2 |
| 93 | `ShortName` | `WCHAR(10.0)` | Yes |  | Text attribute: ShortName |
| 94 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 95 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |
| 96 | `CINNo` | `WCHAR(255.0)` | Yes |  | Text attribute: CINNo |
| 97 | `DontShowStepsToGST` | `BOOLEAN` | No |  | Boolean flag for DontShowStepsToGST (True/False) |
| 98 | `DontShowGSTHelpContents` | `BOOLEAN` | No |  | Boolean flag for DontShowGSTHelpContents (True/False) |
| 99 | `NameSL` | `WCHAR(255.0)` | Yes |  | Text attribute: NameSL |
| 100 | `AliasSL` | `WCHAR(255.0)` | Yes |  | Text attribute: AliasSL |
| 101 | `PrintNameSL` | `WCHAR(255.0)` | Yes |  | Text attribute: PrintNameSL |
| 102 | `Address1SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Address1SL |
| 103 | `Address2SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Address2SL |
| 104 | `Address3SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Address3SL |
| 105 | `Address4SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Address4SL |
| 106 | `GSTR2AUserName` | `WCHAR(255.0)` | Yes |  | Text attribute: GSTR2AUserName |
| 107 | `BDEPID` | `WCHAR(255.0)` | Yes |  | Text attribute: BDEPID |
| 108 | `BDEPPwd` | `WCHAR(255.0)` | Yes |  | Text attribute: BDEPPwd |
| 109 | `BDEPDemoCtr` | `SMALLINT` | Yes |  | Integer identifier or enum code for BDEPDemoCtr |
| 110 | `BDEPImageCtr` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for BDEPImageCtr |
| 111 | `BDEPImageLink` | `WCHAR(255.0)` | Yes |  | Text attribute: BDEPImageLink |
| 112 | `BDEPName` | `WCHAR(255.0)` | Yes |  | Text attribute: BDEPName |
| 113 | `BDEPWhatsApp` | `WCHAR(255.0)` | Yes |  | Text attribute: BDEPWhatsApp |
| 114 | `BDEPMobile` | `WCHAR(255.0)` | Yes |  | Text attribute: BDEPMobile |
| 115 | `BDEPEmailID` | `WCHAR(255.0)` | Yes |  | Text attribute: BDEPEmailID |
| 116 | `BusinessType` | `WCHAR(255.0)` | Yes |  | Text attribute: BusinessType |
| 117 | `IndustryType` | `SMALLINT` | Yes |  | Integer identifier or enum code for IndustryType |
| 118 | `NatureOfWork` | `SMALLINT` | Yes |  | Integer identifier or enum code for NatureOfWork |
| 119 | `AccountantName` | `WCHAR(255.0)` | Yes |  | Text attribute: AccountantName |
| 120 | `AccountantEmailID` | `WCHAR(255.0)` | Yes |  | Text attribute: AccountantEmailID |
| 121 | `AccountantMobile` | `WCHAR(255.0)` | Yes |  | Text attribute: AccountantMobile |
| 122 | `CAName` | `WCHAR(255.0)` | Yes |  | Text attribute: CAName |
| 123 | `CAEmailID` | `WCHAR(255.0)` | Yes |  | Text attribute: CAEmailID |
| 124 | `CAMobile` | `WCHAR(255.0)` | Yes |  | Text attribute: CAMobile |
| 125 | `City` | `WCHAR(255.0)` | Yes |  | Text attribute: City |
| 126 | `Pincode` | `WCHAR(10.0)` | Yes |  | Text attribute: Pincode |

---

<a name="table-customscripts"></a>

### Table: `CustomScripts`

> **Purpose:** User-defined VBScript or SQL hooks executed on database events (e.g., before save, after save validation).

- **Row Count in Active FY:** `0`
- **Total Columns:** `3`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 2 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 3 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |

---

<a name="table-dbimport"></a>

### Table: `DbImport`

> **Purpose:** Mapping configurations and field parameters for importing data from legacy or third-party formats.

- **Row Count in Active FY:** `0`
- **Total Columns:** `38`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `EntityType` | `SMALLINT` | Yes |  | Integer identifier or enum code for EntityType |
| 2 | `SectionID` | `SMALLINT` | Yes |  | Integer identifier or enum code for SectionID |
| 3 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 4 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 5 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 6 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 7 | `C5` | `WCHAR(255.0)` | Yes |  | Text attribute: C5 |
| 8 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 9 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 10 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 11 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 12 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 13 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 14 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 15 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 16 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 17 | `I5` | `SMALLINT` | Yes |  | Integer identifier or enum code for I5 |
| 18 | `L1` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L1 |
| 19 | `L2` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L2 |
| 20 | `L3` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L3 |
| 21 | `L4` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L4 |
| 22 | `L5` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L5 |
| 23 | `L6` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L6 |
| 24 | `L7` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L7 |
| 25 | `L8` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L8 |
| 26 | `L9` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L9 |
| 27 | `L10` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L10 |
| 28 | `L11` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L11 |
| 29 | `L12` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L12 |
| 30 | `L13` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L13 |
| 31 | `L14` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L14 |
| 32 | `L15` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L15 |
| 33 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |
| 34 | `M2` | `WCHAR` | Yes |  | Text attribute: M2 |
| 35 | `M3` | `WCHAR` | Yes |  | Text attribute: M3 |
| 36 | `M4` | `WCHAR` | Yes |  | Text attribute: M4 |
| 37 | `M5` | `WCHAR` | Yes |  | Text attribute: M5 |
| 38 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |

---

<a name="table-dictionarysl"></a>

### Table: `DictionarySL`

> **Purpose:** Custom spelling dictionary and regional language font translations used during voucher entry.

- **Row Count in Active FY:** `0`
- **Total Columns:** `6`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `SrNo` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for SrNo |
| 2 | `LocalLang` | `WCHAR(255.0)` | Yes |  | Text attribute: LocalLang |
| 3 | `SecondLang` | `WCHAR(255.0)` | Yes |  | Text attribute: SecondLang |
| 4 | `LangName` | `WCHAR(255.0)` | Yes |  | Text attribute: LangName |
| 5 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |
| 6 | `M2` | `WCHAR` | Yes |  | Text attribute: M2 |

---

<a name="table-faqdatabase"></a>

### Table: `FAQDatabase`

> **Purpose:** Built-in knowledge base articles and operational FAQs accessible from the BusyWin UI.

- **Row Count in Active FY:** `0`
- **Total Columns:** `5`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `CallType` | `SMALLINT` | Yes |  | Integer identifier or enum code for CallType |
| 2 | `FAQGrpCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for FAQGrpCode |
| 3 | `ProblemTitle` | `WCHAR(255.0)` | Yes |  | Text attribute: ProblemTitle |
| 4 | `Problem` | `WCHAR` | Yes |  | Text attribute: Problem |
| 5 | `Solution` | `WCHAR` | Yes |  | Text attribute: Solution |

---

<a name="table-faqgroup"></a>

### Table: `FAQGroup`

> **Purpose:** Grouping and categorization definitions for FAQ topics.

- **Row Count in Active FY:** `2`
- **Total Columns:** `3`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `GrpName` | `WCHAR(255.0)` | Yes |  | Text attribute: GrpName |
| 2 | `GrpCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for GrpCode |
| 3 | `GrpMasterType` | `SMALLINT` | Yes |  | Integer identifier or enum code for GrpMasterType |

---

<a name="table-formdetails"></a>

### Table: `FormDetails`

> **Purpose:** Voucher and document printing coordinate templates for continuous pre-printed stationery (dot matrix).

- **Row Count in Active FY:** `0`
- **Total Columns:** `6`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `LanguageID` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for LanguageID |
| 2 | `FormID` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for FormID |
| 3 | `FormSubID` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for FormSubID |
| 4 | `FormCaption` | `WCHAR(255.0)` | Yes |  | Text attribute: FormCaption |
| 5 | `FieldID` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for FieldID |
| 6 | `FieldCaption` | `WCHAR(255.0)` | Yes |  | Text attribute: FieldCaption |

---

<a name="table-gstfilingstatusdet"></a>

### Table: `GSTFilingStatusDet`

> **Purpose:** Filing history of statutory GST returns (GSTR-1, GSTR-3B, GSTR-9) including ARN and filing dates.

- **Row Count in Active FY:** `0`
- **Total Columns:** `11`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `GSTIN` | `WCHAR(255.0)` | Yes |  | 15-digit Goods and Services Tax Identification Number |
| 2 | `Month` | `SMALLINT` | Yes |  | Integer identifier or enum code for Month |
| 3 | `FinYr` | `SMALLINT` | Yes |  | Integer identifier or enum code for FinYr |
| 4 | `DateOfFiling` | `DATETIME` | Yes |  | Timestamp / Date field for DateOfFiling |
| 5 | `ReportName` | `WCHAR(255.0)` | Yes |  | Text attribute: ReportName |
| 6 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 7 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 8 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 9 | `Details` | `WCHAR` | Yes |  | Text attribute: Details |
| 10 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 11 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |

---

<a name="table-gststatusdet"></a>

### Table: `GSTStatusDet`

> **Purpose:** GST portal taxpayer verification cache (Trade name, Legal name, Status: Active/Suspended/Cancelled).

- **Row Count in Active FY:** `6`
- **Total Columns:** `29`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `GSTIN` | `WCHAR(255.0)` | Yes |  | 15-digit Goods and Services Tax Identification Number |
| 2 | `Status` | `SMALLINT` | Yes |  | Integer identifier or enum code for Status |
| 3 | `TradeName` | `WCHAR(255.0)` | Yes |  | Text attribute: TradeName |
| 4 | `LegalName` | `WCHAR(255.0)` | Yes |  | Text attribute: LegalName |
| 5 | `Type` | `WCHAR(255.0)` | Yes |  | Text attribute: Type |
| 6 | `Business` | `WCHAR(255.0)` | Yes |  | Text attribute: Business |
| 7 | `RegistrationDate` | `DATETIME` | Yes |  | Timestamp / Date field for RegistrationDate |
| 8 | `CancellationDate` | `DATETIME` | Yes |  | Timestamp / Date field for CancellationDate |
| 9 | `ValidatedOn` | `DATETIME` | Yes |  | Timestamp / Date field for ValidatedOn |
| 10 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 11 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 12 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 13 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 14 | `Details` | `WCHAR` | Yes |  | Text attribute: Details |
| 15 | `UpdatedInBWS` | `BOOLEAN` | No |  | Boolean flag for UpdatedInBWS (True/False) |
| 16 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 17 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 18 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 19 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 20 | `Street` | `WCHAR(255.0)` | Yes |  | Text attribute: Street |
| 21 | `State` | `WCHAR(255.0)` | Yes |  | Text attribute: State |
| 22 | `FloorNo` | `WCHAR(255.0)` | Yes |  | Text attribute: FloorNo |
| 23 | `DoorNo` | `WCHAR(255.0)` | Yes |  | Text attribute: DoorNo |
| 24 | `Pincode` | `WCHAR(255.0)` | Yes |  | Text attribute: Pincode |
| 25 | `Location` | `WCHAR(255.0)` | Yes |  | Text attribute: Location |
| 26 | `BuildingName` | `WCHAR(255.0)` | Yes |  | Text attribute: BuildingName |
| 27 | `Locality` | `WCHAR(255.0)` | Yes |  | Text attribute: Locality |
| 28 | `LandMark` | `WCHAR(255.0)` | Yes |  | Text attribute: LandMark |
| 29 | `District` | `WCHAR(255.0)` | Yes |  | Text attribute: District |

---

<a name="table-hsnstatusdet"></a>

### Table: `HSNStatusDet`

> **Purpose:** Harmonized System of Nomenclature (HSN) and Service Accounting Code (SAC) validation and master cache.

- **Row Count in Active FY:** `0`
- **Total Columns:** `12`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `HSN` | `WCHAR(255.0)` | Yes |  | Text attribute: HSN |
| 2 | `Status` | `SMALLINT` | Yes |  | Integer identifier or enum code for Status |
| 3 | `ValidatedOn` | `DATETIME` | Yes |  | Timestamp / Date field for ValidatedOn |
| 4 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 5 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 6 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 7 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 8 | `Details` | `WCHAR` | Yes |  | Text attribute: Details |
| 9 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 10 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 11 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 12 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |

---

<a name="table-impnotes"></a>

### Table: `ImpNotes`

> **Purpose:** System-wide important notes and critical business reminders shared across operators.

- **Row Count in Active FY:** `0`
- **Total Columns:** `5`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 2 | `ExecName` | `WCHAR(40.0)` | Yes |  | Text attribute: ExecName |
| 3 | `Notes` | `WCHAR` | Yes |  | Text attribute: Notes |
| 4 | `SpecifyPwd` | `BOOLEAN` | No |  | Boolean flag for SpecifyPwd (True/False) |
| 5 | `Password` | `WCHAR(100.0)` | Yes |  | Text attribute: Password |

---

<a name="table-messagecentre"></a>

### Table: `MessageCentre`

> **Purpose:** Internal messaging system between Busy operators within a LAN/WAN installation.

- **Row Count in Active FY:** `0`
- **Total Columns:** `15`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `MsgTo` | `WCHAR` | Yes |  | Text attribute: MsgTo |
| 3 | `MsgFrom` | `WCHAR(255.0)` | Yes |  | Text attribute: MsgFrom |
| 4 | `Subject` | `WCHAR` | Yes |  | Text attribute: Subject |
| 5 | `Message` | `WCHAR` | Yes |  | Text attribute: Message |
| 6 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 7 | `Time1` | `DATETIME` | Yes |  | Timestamp / Date field for Time1 |
| 8 | `Status` | `SMALLINT` | Yes |  | Integer identifier or enum code for Status |
| 9 | `AckMail` | `BOOLEAN` | No |  | Boolean flag for AckMail (True/False) |
| 10 | `CC` | `WCHAR` | Yes |  | Text attribute: CC |
| 11 | `ComputerName` | `WCHAR(100.0)` | Yes |  | Text attribute: ComputerName |
| 12 | `FolderName` | `WCHAR(255.0)` | Yes |  | Text attribute: FolderName |
| 13 | `MessageType` | `SMALLINT` | Yes |  | Integer identifier or enum code for MessageType |
| 14 | `BelongTo` | `WCHAR(20.0)` | Yes |  | Text attribute: BelongTo |
| 15 | `Added2Notes` | `BOOLEAN` | No |  | Boolean flag for Added2Notes (True/False) |

---

<a name="table-mobileuser"></a>

### Table: `MobileUser`

> **Purpose:** Registered mobile devices, phone numbers, and authentication credentials for Busy Mobile App access.

- **Row Count in Active FY:** `0`
- **Total Columns:** `98`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Name` | `WCHAR(20.0)` | Yes |  | Text attribute: Name |
| 2 | `Password` | `WCHAR(20.0)` | Yes |  | Text attribute: Password |
| 3 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 4 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 5 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 6 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 7 | `C5` | `WCHAR(255.0)` | Yes |  | Text attribute: C5 |
| 8 | `C6` | `WCHAR(255.0)` | Yes |  | Text attribute: C6 |
| 9 | `C7` | `WCHAR(255.0)` | Yes |  | Text attribute: C7 |
| 10 | `C8` | `WCHAR(255.0)` | Yes |  | Text attribute: C8 |
| 11 | `C9` | `WCHAR(255.0)` | Yes |  | Text attribute: C9 |
| 12 | `C10` | `WCHAR(255.0)` | Yes |  | Text attribute: C10 |
| 13 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 14 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 15 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 16 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 17 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 18 | `B6` | `BOOLEAN` | No |  | Boolean flag for B6 (True/False) |
| 19 | `B7` | `BOOLEAN` | No |  | Boolean flag for B7 (True/False) |
| 20 | `B8` | `BOOLEAN` | No |  | Boolean flag for B8 (True/False) |
| 21 | `B9` | `BOOLEAN` | No |  | Boolean flag for B9 (True/False) |
| 22 | `B10` | `BOOLEAN` | No |  | Boolean flag for B10 (True/False) |
| 23 | `B11` | `BOOLEAN` | No |  | Boolean flag for B11 (True/False) |
| 24 | `B12` | `BOOLEAN` | No |  | Boolean flag for B12 (True/False) |
| 25 | `B13` | `BOOLEAN` | No |  | Boolean flag for B13 (True/False) |
| 26 | `B14` | `BOOLEAN` | No |  | Boolean flag for B14 (True/False) |
| 27 | `B15` | `BOOLEAN` | No |  | Boolean flag for B15 (True/False) |
| 28 | `B16` | `BOOLEAN` | No |  | Boolean flag for B16 (True/False) |
| 29 | `B17` | `BOOLEAN` | No |  | Boolean flag for B17 (True/False) |
| 30 | `B18` | `BOOLEAN` | No |  | Boolean flag for B18 (True/False) |
| 31 | `B19` | `BOOLEAN` | No |  | Boolean flag for B19 (True/False) |
| 32 | `B20` | `BOOLEAN` | No |  | Boolean flag for B20 (True/False) |
| 33 | `B21` | `BOOLEAN` | No |  | Boolean flag for B21 (True/False) |
| 34 | `B22` | `BOOLEAN` | No |  | Boolean flag for B22 (True/False) |
| 35 | `B23` | `BOOLEAN` | No |  | Boolean flag for B23 (True/False) |
| 36 | `B24` | `BOOLEAN` | No |  | Boolean flag for B24 (True/False) |
| 37 | `B25` | `BOOLEAN` | No |  | Boolean flag for B25 (True/False) |
| 38 | `B26` | `BOOLEAN` | No |  | Boolean flag for B26 (True/False) |
| 39 | `B27` | `BOOLEAN` | No |  | Boolean flag for B27 (True/False) |
| 40 | `B28` | `BOOLEAN` | No |  | Boolean flag for B28 (True/False) |
| 41 | `B29` | `BOOLEAN` | No |  | Boolean flag for B29 (True/False) |
| 42 | `B30` | `BOOLEAN` | No |  | Boolean flag for B30 (True/False) |
| 43 | `B31` | `BOOLEAN` | No |  | Boolean flag for B31 (True/False) |
| 44 | `B32` | `BOOLEAN` | No |  | Boolean flag for B32 (True/False) |
| 45 | `B33` | `BOOLEAN` | No |  | Boolean flag for B33 (True/False) |
| 46 | `B34` | `BOOLEAN` | No |  | Boolean flag for B34 (True/False) |
| 47 | `B35` | `BOOLEAN` | No |  | Boolean flag for B35 (True/False) |
| 48 | `B36` | `BOOLEAN` | No |  | Boolean flag for B36 (True/False) |
| 49 | `B37` | `BOOLEAN` | No |  | Boolean flag for B37 (True/False) |
| 50 | `B38` | `BOOLEAN` | No |  | Boolean flag for B38 (True/False) |
| 51 | `B39` | `BOOLEAN` | No |  | Boolean flag for B39 (True/False) |
| 52 | `B40` | `BOOLEAN` | No |  | Boolean flag for B40 (True/False) |
| 53 | `B41` | `BOOLEAN` | No |  | Boolean flag for B41 (True/False) |
| 54 | `B42` | `BOOLEAN` | No |  | Boolean flag for B42 (True/False) |
| 55 | `B43` | `BOOLEAN` | No |  | Boolean flag for B43 (True/False) |
| 56 | `B44` | `BOOLEAN` | No |  | Boolean flag for B44 (True/False) |
| 57 | `B45` | `BOOLEAN` | No |  | Boolean flag for B45 (True/False) |
| 58 | `B46` | `BOOLEAN` | No |  | Boolean flag for B46 (True/False) |
| 59 | `B47` | `BOOLEAN` | No |  | Boolean flag for B47 (True/False) |
| 60 | `B48` | `BOOLEAN` | No |  | Boolean flag for B48 (True/False) |
| 61 | `B49` | `BOOLEAN` | No |  | Boolean flag for B49 (True/False) |
| 62 | `B50` | `BOOLEAN` | No |  | Boolean flag for B50 (True/False) |
| 63 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 64 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 65 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 66 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 67 | `I5` | `SMALLINT` | Yes |  | Integer identifier or enum code for I5 |
| 68 | `I6` | `SMALLINT` | Yes |  | Integer identifier or enum code for I6 |
| 69 | `I7` | `SMALLINT` | Yes |  | Integer identifier or enum code for I7 |
| 70 | `I8` | `SMALLINT` | Yes |  | Integer identifier or enum code for I8 |
| 71 | `I9` | `SMALLINT` | Yes |  | Integer identifier or enum code for I9 |
| 72 | `I10` | `SMALLINT` | Yes |  | Integer identifier or enum code for I10 |
| 73 | `I11` | `SMALLINT` | Yes |  | Integer identifier or enum code for I11 |
| 74 | `I12` | `SMALLINT` | Yes |  | Integer identifier or enum code for I12 |
| 75 | `I13` | `SMALLINT` | Yes |  | Integer identifier or enum code for I13 |
| 76 | `I14` | `SMALLINT` | Yes |  | Integer identifier or enum code for I14 |
| 77 | `I15` | `SMALLINT` | Yes |  | Integer identifier or enum code for I15 |
| 78 | `I16` | `SMALLINT` | Yes |  | Integer identifier or enum code for I16 |
| 79 | `I17` | `SMALLINT` | Yes |  | Integer identifier or enum code for I17 |
| 80 | `I18` | `SMALLINT` | Yes |  | Integer identifier or enum code for I18 |
| 81 | `I19` | `SMALLINT` | Yes |  | Integer identifier or enum code for I19 |
| 82 | `I20` | `SMALLINT` | Yes |  | Integer identifier or enum code for I20 |
| 83 | `L1` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L1 |
| 84 | `L2` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L2 |
| 85 | `L3` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L3 |
| 86 | `L4` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L4 |
| 87 | `L5` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L5 |
| 88 | `L6` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L6 |
| 89 | `L7` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L7 |
| 90 | `L8` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L8 |
| 91 | `L9` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L9 |
| 92 | `L10` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L10 |
| 93 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |
| 94 | `M2` | `WCHAR` | Yes |  | Text attribute: M2 |
| 95 | `M3` | `WCHAR` | Yes |  | Text attribute: M3 |
| 96 | `M4` | `WCHAR` | Yes |  | Text attribute: M4 |
| 97 | `M5` | `WCHAR` | Yes |  | Text attribute: M5 |
| 98 | `Rectype` | `SMALLINT` | Yes |  | Integer identifier or enum code for Rectype |

---

<a name="table-mobileuserpreference"></a>

### Table: `MobileUserPreference`

> **Purpose:** Permissions, menu access rights, and data visibility rules for Busy Mobile App users.

- **Row Count in Active FY:** `0`
- **Total Columns:** `98`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Name` | `WCHAR(20.0)` | Yes |  | Text attribute: Name |
| 2 | `FinYrs` | `DATETIME` | Yes |  | Timestamp / Date field for FinYrs |
| 3 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 4 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 5 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 6 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 7 | `C5` | `WCHAR(255.0)` | Yes |  | Text attribute: C5 |
| 8 | `C6` | `WCHAR(255.0)` | Yes |  | Text attribute: C6 |
| 9 | `C7` | `WCHAR(255.0)` | Yes |  | Text attribute: C7 |
| 10 | `C8` | `WCHAR(255.0)` | Yes |  | Text attribute: C8 |
| 11 | `C9` | `WCHAR(255.0)` | Yes |  | Text attribute: C9 |
| 12 | `C10` | `WCHAR(255.0)` | Yes |  | Text attribute: C10 |
| 13 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 14 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 15 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 16 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 17 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 18 | `B6` | `BOOLEAN` | No |  | Boolean flag for B6 (True/False) |
| 19 | `B7` | `BOOLEAN` | No |  | Boolean flag for B7 (True/False) |
| 20 | `B8` | `BOOLEAN` | No |  | Boolean flag for B8 (True/False) |
| 21 | `B9` | `BOOLEAN` | No |  | Boolean flag for B9 (True/False) |
| 22 | `B10` | `BOOLEAN` | No |  | Boolean flag for B10 (True/False) |
| 23 | `B11` | `BOOLEAN` | No |  | Boolean flag for B11 (True/False) |
| 24 | `B12` | `BOOLEAN` | No |  | Boolean flag for B12 (True/False) |
| 25 | `B13` | `BOOLEAN` | No |  | Boolean flag for B13 (True/False) |
| 26 | `B14` | `BOOLEAN` | No |  | Boolean flag for B14 (True/False) |
| 27 | `B15` | `BOOLEAN` | No |  | Boolean flag for B15 (True/False) |
| 28 | `B16` | `BOOLEAN` | No |  | Boolean flag for B16 (True/False) |
| 29 | `B17` | `BOOLEAN` | No |  | Boolean flag for B17 (True/False) |
| 30 | `B18` | `BOOLEAN` | No |  | Boolean flag for B18 (True/False) |
| 31 | `B19` | `BOOLEAN` | No |  | Boolean flag for B19 (True/False) |
| 32 | `B20` | `BOOLEAN` | No |  | Boolean flag for B20 (True/False) |
| 33 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 34 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 35 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 36 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 37 | `I5` | `SMALLINT` | Yes |  | Integer identifier or enum code for I5 |
| 38 | `I6` | `SMALLINT` | Yes |  | Integer identifier or enum code for I6 |
| 39 | `I7` | `SMALLINT` | Yes |  | Integer identifier or enum code for I7 |
| 40 | `I8` | `SMALLINT` | Yes |  | Integer identifier or enum code for I8 |
| 41 | `I9` | `SMALLINT` | Yes |  | Integer identifier or enum code for I9 |
| 42 | `I10` | `SMALLINT` | Yes |  | Integer identifier or enum code for I10 |
| 43 | `I11` | `SMALLINT` | Yes |  | Integer identifier or enum code for I11 |
| 44 | `I12` | `SMALLINT` | Yes |  | Integer identifier or enum code for I12 |
| 45 | `I13` | `SMALLINT` | Yes |  | Integer identifier or enum code for I13 |
| 46 | `I14` | `SMALLINT` | Yes |  | Integer identifier or enum code for I14 |
| 47 | `I15` | `SMALLINT` | Yes |  | Integer identifier or enum code for I15 |
| 48 | `I16` | `SMALLINT` | Yes |  | Integer identifier or enum code for I16 |
| 49 | `I17` | `SMALLINT` | Yes |  | Integer identifier or enum code for I17 |
| 50 | `I18` | `SMALLINT` | Yes |  | Integer identifier or enum code for I18 |
| 51 | `I19` | `SMALLINT` | Yes |  | Integer identifier or enum code for I19 |
| 52 | `I20` | `SMALLINT` | Yes |  | Integer identifier or enum code for I20 |
| 53 | `L1` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L1 |
| 54 | `L2` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L2 |
| 55 | `L3` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L3 |
| 56 | `L4` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L4 |
| 57 | `L5` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L5 |
| 58 | `L6` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L6 |
| 59 | `L7` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L7 |
| 60 | `L8` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L8 |
| 61 | `L9` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L9 |
| 62 | `L10` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L10 |
| 63 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |
| 64 | `M2` | `WCHAR` | Yes |  | Text attribute: M2 |
| 65 | `M3` | `WCHAR` | Yes |  | Text attribute: M3 |
| 66 | `M4` | `WCHAR` | Yes |  | Text attribute: M4 |
| 67 | `M5` | `WCHAR` | Yes |  | Text attribute: M5 |
| 68 | `Rectype` | `SMALLINT` | Yes |  | Integer identifier or enum code for Rectype |
| 69 | `B21` | `BOOLEAN` | No |  | Boolean flag for B21 (True/False) |
| 70 | `B22` | `BOOLEAN` | No |  | Boolean flag for B22 (True/False) |
| 71 | `B23` | `BOOLEAN` | No |  | Boolean flag for B23 (True/False) |
| 72 | `B24` | `BOOLEAN` | No |  | Boolean flag for B24 (True/False) |
| 73 | `B25` | `BOOLEAN` | No |  | Boolean flag for B25 (True/False) |
| 74 | `B26` | `BOOLEAN` | No |  | Boolean flag for B26 (True/False) |
| 75 | `B27` | `BOOLEAN` | No |  | Boolean flag for B27 (True/False) |
| 76 | `B28` | `BOOLEAN` | No |  | Boolean flag for B28 (True/False) |
| 77 | `B29` | `BOOLEAN` | No |  | Boolean flag for B29 (True/False) |
| 78 | `B30` | `BOOLEAN` | No |  | Boolean flag for B30 (True/False) |
| 79 | `B31` | `BOOLEAN` | No |  | Boolean flag for B31 (True/False) |
| 80 | `B32` | `BOOLEAN` | No |  | Boolean flag for B32 (True/False) |
| 81 | `B33` | `BOOLEAN` | No |  | Boolean flag for B33 (True/False) |
| 82 | `B34` | `BOOLEAN` | No |  | Boolean flag for B34 (True/False) |
| 83 | `B35` | `BOOLEAN` | No |  | Boolean flag for B35 (True/False) |
| 84 | `B36` | `BOOLEAN` | No |  | Boolean flag for B36 (True/False) |
| 85 | `B37` | `BOOLEAN` | No |  | Boolean flag for B37 (True/False) |
| 86 | `B38` | `BOOLEAN` | No |  | Boolean flag for B38 (True/False) |
| 87 | `B39` | `BOOLEAN` | No |  | Boolean flag for B39 (True/False) |
| 88 | `B40` | `BOOLEAN` | No |  | Boolean flag for B40 (True/False) |
| 89 | `B41` | `BOOLEAN` | No |  | Boolean flag for B41 (True/False) |
| 90 | `B42` | `BOOLEAN` | No |  | Boolean flag for B42 (True/False) |
| 91 | `B43` | `BOOLEAN` | No |  | Boolean flag for B43 (True/False) |
| 92 | `B44` | `BOOLEAN` | No |  | Boolean flag for B44 (True/False) |
| 93 | `B45` | `BOOLEAN` | No |  | Boolean flag for B45 (True/False) |
| 94 | `B46` | `BOOLEAN` | No |  | Boolean flag for B46 (True/False) |
| 95 | `B47` | `BOOLEAN` | No |  | Boolean flag for B47 (True/False) |
| 96 | `B48` | `BOOLEAN` | No |  | Boolean flag for B48 (True/False) |
| 97 | `B49` | `BOOLEAN` | No |  | Boolean flag for B49 (True/False) |
| 98 | `B50` | `BOOLEAN` | No |  | Boolean flag for B50 (True/False) |

---

<a name="table-nmcategory"></a>

### Table: `NMCategory`

> **Purpose:** Notification categories (e.g., Payment Alerts, Low Stock Warnings, Tax Deadlines).

- **Row Count in Active FY:** `0`
- **Total Columns:** `4`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `UserName` | `WCHAR(20.0)` | Yes |  | Operator username who performed the action |
| 2 | `CategoryName` | `WCHAR(255.0)` | Yes |  | Text attribute: CategoryName |
| 3 | `CategoryCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for CategoryCode |
| 4 | `ParentCategoryCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for ParentCategoryCode |

---

<a name="table-nmnotes"></a>

### Table: `NMNotes`

> **Purpose:** Notification message bodies, alert text, and scheduled notification tasks.

- **Row Count in Active FY:** `0`
- **Total Columns:** `10`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `UserName` | `WCHAR(20.0)` | Yes |  | Operator username who performed the action |
| 2 | `NotesCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for NotesCode |
| 3 | `NotesText` | `WCHAR` | Yes |  | Text attribute: NotesText |
| 4 | `CategoryCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for CategoryCode |
| 5 | `SpecifyDeadline` | `BOOLEAN` | No |  | Boolean flag for SpecifyDeadline (True/False) |
| 6 | `DeadlineDate` | `DATETIME` | Yes |  | Timestamp / Date field for DeadlineDate |
| 7 | `Status` | `SMALLINT` | Yes |  | Integer identifier or enum code for Status |
| 8 | `RemindNote` | `BOOLEAN` | No |  | Boolean flag for RemindNote (True/False) |
| 9 | `ReminderOccurence` | `SMALLINT` | Yes |  | Integer identifier or enum code for ReminderOccurence |
| 10 | `Counter` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for Counter |

---

<a name="table-offlinemessage"></a>

### Table: `OfflineMessage`

> **Purpose:** Outbox queue for SMS, WhatsApp, and email alerts waiting to be dispatched by the background worker.

- **Row Count in Active FY:** `0`
- **Total Columns:** `15`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Code` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for Code |
| 2 | `Type` | `SMALLINT` | Yes |  | Integer identifier or enum code for Type |
| 3 | `UserName` | `WCHAR(255.0)` | Yes |  | Operator username who performed the action |
| 4 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 5 | `Msg` | `WCHAR` | Yes |  | Text attribute: Msg |
| 6 | `WorkInBG` | `BOOLEAN` | No |  | Boolean flag for WorkInBG (True/False) |
| 7 | `CompName` | `WCHAR(255.0)` | Yes |  | Text attribute: CompName |
| 8 | `ModeOfSMS` | `SMALLINT` | Yes |  | Integer identifier or enum code for ModeOfSMS |
| 9 | `OtherUserWorking` | `BOOLEAN` | No |  | Boolean flag for OtherUserWorking (True/False) |
| 10 | `LastModified` | `DATETIME` | Yes |  | Timestamp / Date field for LastModified |
| 11 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 12 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 13 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 14 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 15 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |

---

<a name="table-patches"></a>

### Table: `Patches`

> **Purpose:** Version migration patch history applied to the operational database (db1YYYY.bds).

- **Row Count in Active FY:** `0`
- **Total Columns:** `7`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `DummyFld` | `BOOLEAN` | No |  | Boolean flag for DummyFld (True/False) |
| 2 | `MVAction` | `BOOLEAN` | No |  | Boolean flag for MVAction (True/False) |
| 3 | `DontShowStepsToGST` | `BOOLEAN` | No |  | Boolean flag for DontShowStepsToGST (True/False) |
| 4 | `ShortCut` | `BOOLEAN` | No |  | Boolean flag for ShortCut (True/False) |
| 5 | `FinalResults` | `BOOLEAN` | No |  | Boolean flag for FinalResults (True/False) |
| 6 | `UFOESA` | `BOOLEAN` | No |  | Boolean flag for UFOESA (True/False) |
| 7 | `UserRights` | `BOOLEAN` | No |  | Boolean flag for UserRights (True/False) |

---

<a name="table-printerreps"></a>

### Table: `PrinterReps`

> **Purpose:** Detailed report and invoice print format definitions (standard / advanced layouts, headers, margins, fonts).

- **Row Count in Active FY:** `607`
- **Total Columns:** `149`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RepID` | `SMALLINT` | Yes |  | Integer identifier or enum code for RepID |
| 2 | `Name` | `WCHAR(35.0)` | Yes |  | Text attribute: Name |
| 3 | `RepSubID` | `SMALLINT` | Yes |  | Integer identifier or enum code for RepSubID |
| 4 | `ScriptLine` | `WCHAR` | Yes |  | Text attribute: ScriptLine |
| 5 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 6 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 7 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 8 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 9 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 10 | `I5` | `SMALLINT` | Yes |  | Integer identifier or enum code for I5 |
| 11 | `I6` | `SMALLINT` | Yes |  | Integer identifier or enum code for I6 |
| 12 | `I7` | `SMALLINT` | Yes |  | Integer identifier or enum code for I7 |
| 13 | `I8` | `SMALLINT` | Yes |  | Integer identifier or enum code for I8 |
| 14 | `I9` | `SMALLINT` | Yes |  | Integer identifier or enum code for I9 |
| 15 | `I10` | `SMALLINT` | Yes |  | Integer identifier or enum code for I10 |
| 16 | `I11` | `SMALLINT` | Yes |  | Integer identifier or enum code for I11 |
| 17 | `I12` | `SMALLINT` | Yes |  | Integer identifier or enum code for I12 |
| 18 | `I13` | `SMALLINT` | Yes |  | Integer identifier or enum code for I13 |
| 19 | `I14` | `SMALLINT` | Yes |  | Integer identifier or enum code for I14 |
| 20 | `I15` | `SMALLINT` | Yes |  | Integer identifier or enum code for I15 |
| 21 | `I16` | `SMALLINT` | Yes |  | Integer identifier or enum code for I16 |
| 22 | `I17` | `SMALLINT` | Yes |  | Integer identifier or enum code for I17 |
| 23 | `I18` | `SMALLINT` | Yes |  | Integer identifier or enum code for I18 |
| 24 | `I19` | `SMALLINT` | Yes |  | Integer identifier or enum code for I19 |
| 25 | `I20` | `SMALLINT` | Yes |  | Integer identifier or enum code for I20 |
| 26 | `I21` | `SMALLINT` | Yes |  | Integer identifier or enum code for I21 |
| 27 | `I22` | `SMALLINT` | Yes |  | Integer identifier or enum code for I22 |
| 28 | `I23` | `SMALLINT` | Yes |  | Integer identifier or enum code for I23 |
| 29 | `I24` | `SMALLINT` | Yes |  | Integer identifier or enum code for I24 |
| 30 | `I25` | `SMALLINT` | Yes |  | Integer identifier or enum code for I25 |
| 31 | `I26` | `SMALLINT` | Yes |  | Integer identifier or enum code for I26 |
| 32 | `I27` | `SMALLINT` | Yes |  | Integer identifier or enum code for I27 |
| 33 | `I28` | `SMALLINT` | Yes |  | Integer identifier or enum code for I28 |
| 34 | `I29` | `SMALLINT` | Yes |  | Integer identifier or enum code for I29 |
| 35 | `I30` | `SMALLINT` | Yes |  | Integer identifier or enum code for I30 |
| 36 | `I31` | `SMALLINT` | Yes |  | Integer identifier or enum code for I31 |
| 37 | `I32` | `SMALLINT` | Yes |  | Integer identifier or enum code for I32 |
| 38 | `I33` | `SMALLINT` | Yes |  | Integer identifier or enum code for I33 |
| 39 | `I34` | `SMALLINT` | Yes |  | Integer identifier or enum code for I34 |
| 40 | `I35` | `SMALLINT` | Yes |  | Integer identifier or enum code for I35 |
| 41 | `I36` | `SMALLINT` | Yes |  | Integer identifier or enum code for I36 |
| 42 | `I37` | `SMALLINT` | Yes |  | Integer identifier or enum code for I37 |
| 43 | `I38` | `SMALLINT` | Yes |  | Integer identifier or enum code for I38 |
| 44 | `I39` | `SMALLINT` | Yes |  | Integer identifier or enum code for I39 |
| 45 | `I40` | `SMALLINT` | Yes |  | Integer identifier or enum code for I40 |
| 46 | `I41` | `SMALLINT` | Yes |  | Integer identifier or enum code for I41 |
| 47 | `I42` | `SMALLINT` | Yes |  | Integer identifier or enum code for I42 |
| 48 | `I43` | `SMALLINT` | Yes |  | Integer identifier or enum code for I43 |
| 49 | `I44` | `SMALLINT` | Yes |  | Integer identifier or enum code for I44 |
| 50 | `I45` | `SMALLINT` | Yes |  | Integer identifier or enum code for I45 |
| 51 | `I46` | `SMALLINT` | Yes |  | Integer identifier or enum code for I46 |
| 52 | `I47` | `SMALLINT` | Yes |  | Integer identifier or enum code for I47 |
| 53 | `I48` | `SMALLINT` | Yes |  | Integer identifier or enum code for I48 |
| 54 | `I49` | `SMALLINT` | Yes |  | Integer identifier or enum code for I49 |
| 55 | `I50` | `SMALLINT` | Yes |  | Integer identifier or enum code for I50 |
| 56 | `I51` | `SMALLINT` | Yes |  | Integer identifier or enum code for I51 |
| 57 | `I52` | `SMALLINT` | Yes |  | Integer identifier or enum code for I52 |
| 58 | `I53` | `SMALLINT` | Yes |  | Integer identifier or enum code for I53 |
| 59 | `I54` | `SMALLINT` | Yes |  | Integer identifier or enum code for I54 |
| 60 | `I55` | `SMALLINT` | Yes |  | Integer identifier or enum code for I55 |
| 61 | `I56` | `SMALLINT` | Yes |  | Integer identifier or enum code for I56 |
| 62 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 63 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 64 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 65 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 66 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 67 | `B6` | `BOOLEAN` | No |  | Boolean flag for B6 (True/False) |
| 68 | `B7` | `BOOLEAN` | No |  | Boolean flag for B7 (True/False) |
| 69 | `B8` | `BOOLEAN` | No |  | Boolean flag for B8 (True/False) |
| 70 | `B9` | `BOOLEAN` | No |  | Boolean flag for B9 (True/False) |
| 71 | `B10` | `BOOLEAN` | No |  | Boolean flag for B10 (True/False) |
| 72 | `B11` | `BOOLEAN` | No |  | Boolean flag for B11 (True/False) |
| 73 | `B12` | `BOOLEAN` | No |  | Boolean flag for B12 (True/False) |
| 74 | `B13` | `BOOLEAN` | No |  | Boolean flag for B13 (True/False) |
| 75 | `B14` | `BOOLEAN` | No |  | Boolean flag for B14 (True/False) |
| 76 | `B15` | `BOOLEAN` | No |  | Boolean flag for B15 (True/False) |
| 77 | `B16` | `BOOLEAN` | No |  | Boolean flag for B16 (True/False) |
| 78 | `B17` | `BOOLEAN` | No |  | Boolean flag for B17 (True/False) |
| 79 | `B18` | `BOOLEAN` | No |  | Boolean flag for B18 (True/False) |
| 80 | `B19` | `BOOLEAN` | No |  | Boolean flag for B19 (True/False) |
| 81 | `B20` | `BOOLEAN` | No |  | Boolean flag for B20 (True/False) |
| 82 | `B21` | `BOOLEAN` | No |  | Boolean flag for B21 (True/False) |
| 83 | `B22` | `BOOLEAN` | No |  | Boolean flag for B22 (True/False) |
| 84 | `B23` | `BOOLEAN` | No |  | Boolean flag for B23 (True/False) |
| 85 | `B24` | `BOOLEAN` | No |  | Boolean flag for B24 (True/False) |
| 86 | `B25` | `BOOLEAN` | No |  | Boolean flag for B25 (True/False) |
| 87 | `B26` | `BOOLEAN` | No |  | Boolean flag for B26 (True/False) |
| 88 | `B27` | `BOOLEAN` | No |  | Boolean flag for B27 (True/False) |
| 89 | `B28` | `BOOLEAN` | No |  | Boolean flag for B28 (True/False) |
| 90 | `B29` | `BOOLEAN` | No |  | Boolean flag for B29 (True/False) |
| 91 | `B30` | `BOOLEAN` | No |  | Boolean flag for B30 (True/False) |
| 92 | `B31` | `BOOLEAN` | No |  | Boolean flag for B31 (True/False) |
| 93 | `B32` | `BOOLEAN` | No |  | Boolean flag for B32 (True/False) |
| 94 | `B33` | `BOOLEAN` | No |  | Boolean flag for B33 (True/False) |
| 95 | `B34` | `BOOLEAN` | No |  | Boolean flag for B34 (True/False) |
| 96 | `B35` | `BOOLEAN` | No |  | Boolean flag for B35 (True/False) |
| 97 | `B36` | `BOOLEAN` | No |  | Boolean flag for B36 (True/False) |
| 98 | `B37` | `BOOLEAN` | No |  | Boolean flag for B37 (True/False) |
| 99 | `B38` | `BOOLEAN` | No |  | Boolean flag for B38 (True/False) |
| 100 | `B39` | `BOOLEAN` | No |  | Boolean flag for B39 (True/False) |
| 101 | `B40` | `BOOLEAN` | No |  | Boolean flag for B40 (True/False) |
| 102 | `B43` | `BOOLEAN` | No |  | Boolean flag for B43 (True/False) |
| 103 | `B44` | `BOOLEAN` | No |  | Boolean flag for B44 (True/False) |
| 104 | `B45` | `BOOLEAN` | No |  | Boolean flag for B45 (True/False) |
| 105 | `B46` | `BOOLEAN` | No |  | Boolean flag for B46 (True/False) |
| 106 | `B47` | `BOOLEAN` | No |  | Boolean flag for B47 (True/False) |
| 107 | `B48` | `BOOLEAN` | No |  | Boolean flag for B48 (True/False) |
| 108 | `B49` | `BOOLEAN` | No |  | Boolean flag for B49 (True/False) |
| 109 | `B50` | `BOOLEAN` | No |  | Boolean flag for B50 (True/False) |
| 110 | `B51` | `BOOLEAN` | No |  | Boolean flag for B51 (True/False) |
| 111 | `B52` | `BOOLEAN` | No |  | Boolean flag for B52 (True/False) |
| 112 | `B53` | `BOOLEAN` | No |  | Boolean flag for B53 (True/False) |
| 113 | `B54` | `BOOLEAN` | No |  | Boolean flag for B54 (True/False) |
| 114 | `B55` | `BOOLEAN` | No |  | Boolean flag for B55 (True/False) |
| 115 | `B56` | `BOOLEAN` | No |  | Boolean flag for B56 (True/False) |
| 116 | `B57` | `BOOLEAN` | No |  | Boolean flag for B57 (True/False) |
| 117 | `B58` | `BOOLEAN` | No |  | Boolean flag for B58 (True/False) |
| 118 | `B59` | `BOOLEAN` | No |  | Boolean flag for B59 (True/False) |
| 119 | `B60` | `BOOLEAN` | No |  | Boolean flag for B60 (True/False) |
| 120 | `B61` | `BOOLEAN` | No |  | Boolean flag for B61 (True/False) |
| 121 | `B62` | `BOOLEAN` | No |  | Boolean flag for B62 (True/False) |
| 122 | `B63` | `BOOLEAN` | No |  | Boolean flag for B63 (True/False) |
| 123 | `B64` | `BOOLEAN` | No |  | Boolean flag for B64 (True/False) |
| 124 | `B65` | `BOOLEAN` | No |  | Boolean flag for B65 (True/False) |
| 125 | `B66` | `BOOLEAN` | No |  | Boolean flag for B66 (True/False) |
| 126 | `B67` | `BOOLEAN` | No |  | Boolean flag for B67 (True/False) |
| 127 | `B68` | `BOOLEAN` | No |  | Boolean flag for B68 (True/False) |
| 128 | `B69` | `BOOLEAN` | No |  | Boolean flag for B69 (True/False) |
| 129 | `B70` | `BOOLEAN` | No |  | Boolean flag for B70 (True/False) |
| 130 | `B71` | `BOOLEAN` | No |  | Boolean flag for B71 (True/False) |
| 131 | `B72` | `BOOLEAN` | No |  | Boolean flag for B72 (True/False) |
| 132 | `B73` | `BOOLEAN` | No |  | Boolean flag for B73 (True/False) |
| 133 | `B74` | `BOOLEAN` | No |  | Boolean flag for B74 (True/False) |
| 134 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 135 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 136 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 137 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 138 | `D5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D5 |
| 139 | `D6` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D6 |
| 140 | `D7` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D7 |
| 141 | `C1` | `WCHAR(20.0)` | Yes |  | Text attribute: C1 |
| 142 | `C2` | `WCHAR(20.0)` | Yes |  | Text attribute: C2 |
| 143 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 144 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 145 | `TaxType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TaxType |
| 146 | `B41` | `BOOLEAN` | No |  | Boolean flag for B41 (True/False) |
| 147 | `B42` | `BOOLEAN` | No |  | Boolean flag for B42 (True/False) |
| 148 | `I57` | `SMALLINT` | Yes |  | Integer identifier or enum code for I57 |
| 149 | `I58` | `SMALLINT` | Yes |  | Integer identifier or enum code for I58 |

---

<a name="table-sqlquery"></a>

### Table: `SQLQuery`

> **Purpose:** Saved user SQL queries and custom report filters created through the interactive query designer.

- **Row Count in Active FY:** `0`
- **Total Columns:** `5`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Code` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for Code |
| 2 | `Name` | `WCHAR(255.0)` | Yes |  | Text attribute: Name |
| 3 | `Query` | `WCHAR` | Yes |  | Text attribute: Query |
| 4 | `QueryType` | `SMALLINT` | Yes |  | Integer identifier or enum code for QueryType |
| 5 | `Password` | `WCHAR(255.0)` | Yes |  | Text attribute: Password |

---

<a name="table-screenreps"></a>

### Table: `ScreenReps`

> **Purpose:** User-customized grid display layouts (column order, widths, visibility) across data entry screens.

- **Row Count in Active FY:** `0`
- **Total Columns:** `4`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RepID` | `SMALLINT` | Yes |  | Integer identifier or enum code for RepID |
| 2 | `Name` | `WCHAR(35.0)` | Yes |  | Text attribute: Name |
| 3 | `RepSubID` | `SMALLINT` | Yes |  | Integer identifier or enum code for RepSubID |
| 4 | `ScriptLine` | `WCHAR` | Yes |  | Text attribute: ScriptLine |

---

<a name="table-statecompanydet"></a>

### Table: `StateCompanyDet`

> **Purpose:** Multi-state GST branch company registrations under the unified company umbrella.

- **Row Count in Active FY:** `0`
- **Total Columns:** `54`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `StateCode` | `SMALLINT` | Yes |  | Integer identifier or enum code for StateCode |
| 2 | `Address1` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 3 | `Address2` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 4 | `Address3` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 5 | `Address4` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 6 | `TIN` | `WCHAR(30.0)` | Yes |  | Text attribute: TIN |
| 7 | `GST` | `WCHAR(30.0)` | Yes |  | Text attribute: GST |
| 8 | `CST` | `WCHAR(30.0)` | Yes |  | Text attribute: CST |
| 9 | `TelNo` | `WCHAR(40.0)` | Yes |  | Fixed-line landline telephone number |
| 10 | `Fax` | `WCHAR(30.0)` | Yes |  | Text attribute: Fax |
| 11 | `Email` | `WCHAR(80.0)` | Yes |  | Official email address for communication and e-invoicing |
| 12 | `ITPAN` | `WCHAR(20.0)` | Yes |  | Income Tax Permanent Account Number (PAN) |
| 13 | `ITWard` | `WCHAR(20.0)` | Yes |  | Text attribute: ITWard |
| 14 | `LST` | `WCHAR(30.0)` | Yes |  | Text attribute: LST |
| 15 | `ST_37` | `WCHAR(30.0)` | Yes |  | Text attribute: ST_37 |
| 16 | `STWardNo` | `WCHAR(20.0)` | Yes |  | Text attribute: STWardNo |
| 17 | `VATPersonName` | `WCHAR(40.0)` | Yes |  | Text attribute: VATPersonName |
| 18 | `VATDesignation` | `WCHAR(40.0)` | Yes |  | Text attribute: VATDesignation |
| 19 | `VATGuardianName` | `WCHAR(40.0)` | Yes |  | Text attribute: VATGuardianName |
| 20 | `ExciseRegNo` | `WCHAR(30.0)` | Yes |  | Text attribute: ExciseRegNo |
| 21 | `ECCCode` | `WCHAR(20.0)` | Yes |  | Text attribute: ECCCode |
| 22 | `PLANo` | `WCHAR(20.0)` | Yes |  | Text attribute: PLANo |
| 23 | `Range` | `WCHAR(80.0)` | Yes |  | Text attribute: Range |
| 24 | `Division` | `WCHAR(80.0)` | Yes |  | Text attribute: Division |
| 25 | `Collectorate` | `WCHAR(40.0)` | Yes |  | Text attribute: Collectorate |
| 26 | `STRegNo` | `WCHAR(30.0)` | Yes |  | Text attribute: STRegNo |
| 27 | `STCNo` | `WCHAR(30.0)` | Yes |  | Text attribute: STCNo |
| 28 | `PremisesCode` | `WCHAR(20.0)` | Yes |  | Text attribute: PremisesCode |
| 29 | `TaxableService` | `WCHAR(40.0)` | Yes |  | Text attribute: TaxableService |
| 30 | `STPersonName` | `WCHAR(40.0)` | Yes |  | Text attribute: STPersonName |
| 31 | `STDesignation` | `WCHAR(40.0)` | Yes |  | Text attribute: STDesignation |
| 32 | `STGuardianName` | `WCHAR(40.0)` | Yes |  | Text attribute: STGuardianName |
| 33 | `PersonName` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonName |
| 34 | `Designation` | `WCHAR(40.0)` | Yes |  | Text attribute: Designation |
| 35 | `GuardianName` | `WCHAR(40.0)` | Yes |  | Text attribute: GuardianName |
| 36 | `PersonAddress1` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonAddress1 |
| 37 | `PersonAddress2` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonAddress2 |
| 38 | `PersonAddress3` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonAddress3 |
| 39 | `PersonAddress4` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonAddress4 |
| 40 | `PersonAddress5` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonAddress5 |
| 41 | `PersonStateCode` | `SMALLINT` | Yes |  | Integer identifier or enum code for PersonStateCode |
| 42 | `PersonPinCode` | `WCHAR(10.0)` | Yes |  | Text attribute: PersonPinCode |
| 43 | `PersonStdCode` | `WCHAR(10.0)` | Yes |  | Text attribute: PersonStdCode |
| 44 | `PersonPhoneNo` | `WCHAR(40.0)` | Yes |  | Text attribute: PersonPhoneNo |
| 45 | `PersonEmail` | `WCHAR(80.0)` | Yes |  | Text attribute: PersonEmail |
| 46 | `TDSAdd1` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSAdd1 |
| 47 | `TDSAdd2` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSAdd2 |
| 48 | `TDSAdd3` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSAdd3 |
| 49 | `TDSAdd4` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSAdd4 |
| 50 | `TDSAdd5` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSAdd5 |
| 51 | `TDSStateCode` | `SMALLINT` | Yes |  | Integer identifier or enum code for TDSStateCode |
| 52 | `TDSPinCode` | `WCHAR(10.0)` | Yes |  | Text attribute: TDSPinCode |
| 53 | `TDSStdCode` | `WCHAR(10.0)` | Yes |  | Text attribute: TDSStdCode |
| 54 | `TDSPhoneNo` | `WCHAR(40.0)` | Yes |  | Text attribute: TDSPhoneNo |

---

<a name="table-stdnar"></a>

### Table: `StdNar`

> **Purpose:** Standard narration master library for quick lookup and selection in voucher entry.

- **Row Count in Active FY:** `0`
- **Total Columns:** `3`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 2 | `Narration1` | `WCHAR(94.0)` | Yes |  | Text attribute: Narration1 |
| 3 | `Narration2` | `WCHAR(94.0)` | Yes |  | Text attribute: Narration2 |

---

<a name="table-usercontrol"></a>

### Table: `UserControl`

> **Purpose:** User credentials, passwords, security roles, and feature access permissions.

- **Row Count in Active FY:** `6`
- **Total Columns:** `30`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Name` | `WCHAR(20.0)` | Yes |  | Text attribute: Name |
| 2 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 3 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 4 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 5 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 6 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 7 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 8 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 9 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 10 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 11 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 12 | `B6` | `BOOLEAN` | No |  | Boolean flag for B6 (True/False) |
| 13 | `B7` | `BOOLEAN` | No |  | Boolean flag for B7 (True/False) |
| 14 | `B8` | `BOOLEAN` | No |  | Boolean flag for B8 (True/False) |
| 15 | `B9` | `BOOLEAN` | No |  | Boolean flag for B9 (True/False) |
| 16 | `B10` | `BOOLEAN` | No |  | Boolean flag for B10 (True/False) |
| 17 | `B11` | `BOOLEAN` | No |  | Boolean flag for B11 (True/False) |
| 18 | `B12` | `BOOLEAN` | No |  | Boolean flag for B12 (True/False) |
| 19 | `B13` | `BOOLEAN` | No |  | Boolean flag for B13 (True/False) |
| 20 | `B14` | `BOOLEAN` | No |  | Boolean flag for B14 (True/False) |
| 21 | `B15` | `BOOLEAN` | No |  | Boolean flag for B15 (True/False) |
| 22 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 23 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 24 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 25 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 26 | `L1` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L1 |
| 27 | `L2` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L2 |
| 28 | `L3` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L3 |
| 29 | `L4` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L4 |
| 30 | `FinYrs` | `DATETIME` | Yes |  | Timestamp / Date field for FinYrs |

---

<a name="table-userlog"></a>

### Table: `UserLog`

> **Purpose:** Audit trail tracking user operations (creation, modification, and deletion of masters and transactions).

- **Row Count in Active FY:** `0`
- **Total Columns:** `3`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `ComputerName` | `WCHAR(255.0)` | Yes |  | Text attribute: ComputerName |
| 2 | `BusyUserName` | `WCHAR(255.0)` | Yes |  | Text attribute: BusyUserName |
| 3 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |

---

<a name="table-userpreferences"></a>

### Table: `UserPreferences`

> **Purpose:** Primary company configuration flags (Inventory, Bill-by-Bill, Multi-Currency, Batch/Expiry, Tax rules).

- **Row Count in Active FY:** `1`
- **Total Columns:** `255`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Name` | `WCHAR(20.0)` | Yes |  | Text attribute: Name |
| 2 | `SuperUser` | `BOOLEAN` | No |  | Boolean flag for SuperUser (True/False) |
| 3 | `CanModifyMaster` | `BOOLEAN` | No |  | Boolean flag for CanModifyMaster (True/False) |
| 4 | `CanModifyVoucher` | `BOOLEAN` | No |  | Boolean flag for CanModifyVoucher (True/False) |
| 5 | `CanEditComp` | `BOOLEAN` | No |  | Boolean flag for CanEditComp (True/False) |
| 6 | `CanBackupComp` | `BOOLEAN` | No |  | Boolean flag for CanBackupComp (True/False) |
| 7 | `CanChangePrice` | `BOOLEAN` | No |  | Boolean flag for CanChangePrice (True/False) |
| 8 | `CanChangeItemWiseDiscount` | `BOOLEAN` | No |  | Boolean flag for CanChangeItemWiseDiscount (True/False) |
| 9 | `DosDrvName` | `WCHAR(20.0)` | Yes |  | Text attribute: DosDrvName |
| 10 | `WinDrvName` | `WCHAR(255.0)` | Yes |  | Text attribute: WinDrvName |
| 11 | `PageLen` | `SMALLINT` | Yes |  | Integer identifier or enum code for PageLen |
| 12 | `LinesPerPage` | `SMALLINT` | Yes |  | Integer identifier or enum code for LinesPerPage |
| 13 | `PrintType` | `SMALLINT` | Yes |  | Integer identifier or enum code for PrintType |
| 14 | `UserPassword` | `WCHAR(100.0)` | Yes |  | Text attribute: UserPassword |
| 15 | `B1` | `BOOLEAN` | No |  | Feature toggle boolean flag B1 |
| 16 | `B2` | `BOOLEAN` | No |  | Feature toggle boolean flag B2 |
| 17 | `B3` | `BOOLEAN` | No |  | Feature toggle boolean flag B3 |
| 18 | `B4` | `BOOLEAN` | No |  | Feature toggle boolean flag B4 |
| 19 | `B5` | `BOOLEAN` | No |  | Feature toggle boolean flag B5 |
| 20 | `B6` | `BOOLEAN` | No |  | Feature toggle boolean flag B6 |
| 21 | `B7` | `BOOLEAN` | No |  | Feature toggle boolean flag B7 |
| 22 | `B8` | `BOOLEAN` | No |  | Feature toggle boolean flag B8 |
| 23 | `B9` | `BOOLEAN` | No |  | Feature toggle boolean flag B9 |
| 24 | `B10` | `BOOLEAN` | No |  | Feature toggle boolean flag B10 |
| 25 | `B11` | `BOOLEAN` | No |  | Feature toggle boolean flag B11 |
| 26 | `B12` | `BOOLEAN` | No |  | Feature toggle boolean flag B12 |
| 27 | `B13` | `BOOLEAN` | No |  | Feature toggle boolean flag B13 |
| 28 | `B14` | `BOOLEAN` | No |  | Feature toggle boolean flag B14 |
| 29 | `B15` | `BOOLEAN` | No |  | Feature toggle boolean flag B15 |
| 30 | `B16` | `BOOLEAN` | No |  | Feature toggle boolean flag B16 |
| 31 | `B17` | `BOOLEAN` | No |  | Feature toggle boolean flag B17 |
| 32 | `B18` | `BOOLEAN` | No |  | Feature toggle boolean flag B18 |
| 33 | `B19` | `BOOLEAN` | No |  | Feature toggle boolean flag B19 |
| 34 | `B20` | `BOOLEAN` | No |  | Feature toggle boolean flag B20 |
| 35 | `B21` | `BOOLEAN` | No |  | Feature toggle boolean flag B21 |
| 36 | `B22` | `BOOLEAN` | No |  | Feature toggle boolean flag B22 |
| 37 | `B23` | `BOOLEAN` | No |  | Feature toggle boolean flag B23 |
| 38 | `B24` | `BOOLEAN` | No |  | Feature toggle boolean flag B24 |
| 39 | `B25` | `BOOLEAN` | No |  | Feature toggle boolean flag B25 |
| 40 | `B26` | `BOOLEAN` | No |  | Feature toggle boolean flag B26 |
| 41 | `B27` | `BOOLEAN` | No |  | Feature toggle boolean flag B27 |
| 42 | `B28` | `BOOLEAN` | No |  | Feature toggle boolean flag B28 |
| 43 | `B29` | `BOOLEAN` | No |  | Feature toggle boolean flag B29 |
| 44 | `B30` | `BOOLEAN` | No |  | Feature toggle boolean flag B30 |
| 45 | `B31` | `BOOLEAN` | No |  | Feature toggle boolean flag B31 |
| 46 | `B32` | `BOOLEAN` | No |  | Feature toggle boolean flag B32 |
| 47 | `B33` | `BOOLEAN` | No |  | Feature toggle boolean flag B33 |
| 48 | `B34` | `BOOLEAN` | No |  | Feature toggle boolean flag B34 |
| 49 | `B35` | `BOOLEAN` | No |  | Feature toggle boolean flag B35 |
| 50 | `B36` | `BOOLEAN` | No |  | Feature toggle boolean flag B36 |
| 51 | `B37` | `BOOLEAN` | No |  | Feature toggle boolean flag B37 |
| 52 | `B38` | `BOOLEAN` | No |  | Feature toggle boolean flag B38 |
| 53 | `B39` | `BOOLEAN` | No |  | Feature toggle boolean flag B39 |
| 54 | `B40` | `BOOLEAN` | No |  | Feature toggle boolean flag B40 |
| 55 | `B41` | `BOOLEAN` | No |  | Feature toggle boolean flag B41 |
| 56 | `B42` | `BOOLEAN` | No |  | Feature toggle boolean flag B42 |
| 57 | `B43` | `BOOLEAN` | No |  | Feature toggle boolean flag B43 |
| 58 | `B44` | `BOOLEAN` | No |  | Feature toggle boolean flag B44 |
| 59 | `B45` | `BOOLEAN` | No |  | Feature toggle boolean flag B45 |
| 60 | `B46` | `BOOLEAN` | No |  | Feature toggle boolean flag B46 |
| 61 | `B47` | `BOOLEAN` | No |  | Feature toggle boolean flag B47 |
| 62 | `B48` | `BOOLEAN` | No |  | Feature toggle boolean flag B48 |
| 63 | `B49` | `BOOLEAN` | No |  | Feature toggle boolean flag B49 |
| 64 | `B50` | `BOOLEAN` | No |  | Feature toggle boolean flag B50 |
| 65 | `B51` | `BOOLEAN` | No |  | Feature toggle boolean flag B51 |
| 66 | `B52` | `BOOLEAN` | No |  | Feature toggle boolean flag B52 |
| 67 | `B53` | `BOOLEAN` | No |  | Feature toggle boolean flag B53 |
| 68 | `B54` | `BOOLEAN` | No |  | Feature toggle boolean flag B54 |
| 69 | `B55` | `BOOLEAN` | No |  | Feature toggle boolean flag B55 |
| 70 | `B56` | `BOOLEAN` | No |  | Feature toggle boolean flag B56 |
| 71 | `B57` | `BOOLEAN` | No |  | Feature toggle boolean flag B57 |
| 72 | `B58` | `BOOLEAN` | No |  | Feature toggle boolean flag B58 |
| 73 | `B59` | `BOOLEAN` | No |  | Feature toggle boolean flag B59 |
| 74 | `B60` | `BOOLEAN` | No |  | Feature toggle boolean flag B60 |
| 75 | `B61` | `BOOLEAN` | No |  | Feature toggle boolean flag B61 |
| 76 | `B62` | `BOOLEAN` | No |  | Feature toggle boolean flag B62 |
| 77 | `B63` | `BOOLEAN` | No |  | Feature toggle boolean flag B63 |
| 78 | `B64` | `BOOLEAN` | No |  | Feature toggle boolean flag B64 |
| 79 | `B65` | `BOOLEAN` | No |  | Feature toggle boolean flag B65 |
| 80 | `B66` | `BOOLEAN` | No |  | Feature toggle boolean flag B66 |
| 81 | `B67` | `BOOLEAN` | No |  | Feature toggle boolean flag B67 |
| 82 | `B68` | `BOOLEAN` | No |  | Feature toggle boolean flag B68 |
| 83 | `B69` | `BOOLEAN` | No |  | Feature toggle boolean flag B69 |
| 84 | `B70` | `BOOLEAN` | No |  | Feature toggle boolean flag B70 |
| 85 | `B71` | `BOOLEAN` | No |  | Feature toggle boolean flag B71 |
| 86 | `B72` | `BOOLEAN` | No |  | Feature toggle boolean flag B72 |
| 87 | `B73` | `BOOLEAN` | No |  | Feature toggle boolean flag B73 |
| 88 | `B74` | `BOOLEAN` | No |  | Feature toggle boolean flag B74 |
| 89 | `B75` | `BOOLEAN` | No |  | Feature toggle boolean flag B75 |
| 90 | `B76` | `BOOLEAN` | No |  | Feature toggle boolean flag B76 |
| 91 | `B77` | `BOOLEAN` | No |  | Feature toggle boolean flag B77 |
| 92 | `B78` | `BOOLEAN` | No |  | Feature toggle boolean flag B78 |
| 93 | `B79` | `BOOLEAN` | No |  | Feature toggle boolean flag B79 |
| 94 | `B80` | `BOOLEAN` | No |  | Feature toggle boolean flag B80 |
| 95 | `B81` | `BOOLEAN` | No |  | Feature toggle boolean flag B81 |
| 96 | `B82` | `BOOLEAN` | No |  | Feature toggle boolean flag B82 |
| 97 | `B83` | `BOOLEAN` | No |  | Feature toggle boolean flag B83 |
| 98 | `B84` | `BOOLEAN` | No |  | Feature toggle boolean flag B84 |
| 99 | `B85` | `BOOLEAN` | No |  | Feature toggle boolean flag B85 |
| 100 | `B86` | `BOOLEAN` | No |  | Feature toggle boolean flag B86 |
| 101 | `B87` | `BOOLEAN` | No |  | Feature toggle boolean flag B87 |
| 102 | `B88` | `BOOLEAN` | No |  | Feature toggle boolean flag B88 |
| 103 | `B89` | `BOOLEAN` | No |  | Feature toggle boolean flag B89 |
| 104 | `B90` | `BOOLEAN` | No |  | Feature toggle boolean flag B90 |
| 105 | `B91` | `BOOLEAN` | No |  | Feature toggle boolean flag B91 |
| 106 | `B92` | `BOOLEAN` | No |  | Feature toggle boolean flag B92 |
| 107 | `B93` | `BOOLEAN` | No |  | Feature toggle boolean flag B93 |
| 108 | `B94` | `BOOLEAN` | No |  | Feature toggle boolean flag B94 |
| 109 | `B95` | `BOOLEAN` | No |  | Feature toggle boolean flag B95 |
| 110 | `B96` | `BOOLEAN` | No |  | Feature toggle boolean flag B96 |
| 111 | `B97` | `BOOLEAN` | No |  | Feature toggle boolean flag B97 |
| 112 | `B98` | `BOOLEAN` | No |  | Feature toggle boolean flag B98 |
| 113 | `B99` | `BOOLEAN` | No |  | Feature toggle boolean flag B99 |
| 114 | `B100` | `BOOLEAN` | No |  | Feature toggle boolean flag B100 |
| 115 | `B101` | `BOOLEAN` | No |  | Feature toggle boolean flag B101 |
| 116 | `B102` | `BOOLEAN` | No |  | Feature toggle boolean flag B102 |
| 117 | `B103` | `BOOLEAN` | No |  | Feature toggle boolean flag B103 |
| 118 | `B104` | `BOOLEAN` | No |  | Feature toggle boolean flag B104 |
| 119 | `B105` | `BOOLEAN` | No |  | Feature toggle boolean flag B105 |
| 120 | `B106` | `BOOLEAN` | No |  | Feature toggle boolean flag B106 |
| 121 | `B107` | `BOOLEAN` | No |  | Feature toggle boolean flag B107 |
| 122 | `B108` | `BOOLEAN` | No |  | Feature toggle boolean flag B108 |
| 123 | `B109` | `BOOLEAN` | No |  | Feature toggle boolean flag B109 |
| 124 | `B110` | `BOOLEAN` | No |  | Feature toggle boolean flag B110 |
| 125 | `B111` | `BOOLEAN` | No |  | Feature toggle boolean flag B111 |
| 126 | `B112` | `BOOLEAN` | No |  | Feature toggle boolean flag B112 |
| 127 | `B113` | `BOOLEAN` | No |  | Feature toggle boolean flag B113 |
| 128 | `B114` | `BOOLEAN` | No |  | Feature toggle boolean flag B114 |
| 129 | `B115` | `BOOLEAN` | No |  | Feature toggle boolean flag B115 |
| 130 | `B116` | `BOOLEAN` | No |  | Feature toggle boolean flag B116 |
| 131 | `B117` | `BOOLEAN` | No |  | Feature toggle boolean flag B117 |
| 132 | `B118` | `BOOLEAN` | No |  | Feature toggle boolean flag B118 |
| 133 | `B119` | `BOOLEAN` | No |  | Feature toggle boolean flag B119 |
| 134 | `B120` | `BOOLEAN` | No |  | Feature toggle boolean flag B120 |
| 135 | `B121` | `BOOLEAN` | No |  | Feature toggle boolean flag B121 |
| 136 | `B122` | `BOOLEAN` | No |  | Feature toggle boolean flag B122 |
| 137 | `B123` | `BOOLEAN` | No |  | Feature toggle boolean flag B123 |
| 138 | `B124` | `BOOLEAN` | No |  | Feature toggle boolean flag B124 |
| 139 | `B125` | `BOOLEAN` | No |  | Feature toggle boolean flag B125 |
| 140 | `B126` | `BOOLEAN` | No |  | Feature toggle boolean flag B126 |
| 141 | `B127` | `BOOLEAN` | No |  | Feature toggle boolean flag B127 |
| 142 | `B128` | `BOOLEAN` | No |  | Feature toggle boolean flag B128 |
| 143 | `B129` | `BOOLEAN` | No |  | Feature toggle boolean flag B129 |
| 144 | `B130` | `BOOLEAN` | No |  | Feature toggle boolean flag B130 |
| 145 | `B131` | `BOOLEAN` | No |  | Feature toggle boolean flag B131 |
| 146 | `B132` | `BOOLEAN` | No |  | Feature toggle boolean flag B132 |
| 147 | `B133` | `BOOLEAN` | No |  | Feature toggle boolean flag B133 |
| 148 | `B134` | `BOOLEAN` | No |  | Feature toggle boolean flag B134 |
| 149 | `B135` | `BOOLEAN` | No |  | Feature toggle boolean flag B135 |
| 150 | `B136` | `BOOLEAN` | No |  | Feature toggle boolean flag B136 |
| 151 | `B137` | `BOOLEAN` | No |  | Feature toggle boolean flag B137 |
| 152 | `B138` | `BOOLEAN` | No |  | Feature toggle boolean flag B138 |
| 153 | `B139` | `BOOLEAN` | No |  | Feature toggle boolean flag B139 |
| 154 | `B140` | `BOOLEAN` | No |  | Feature toggle boolean flag B140 |
| 155 | `B141` | `BOOLEAN` | No |  | Feature toggle boolean flag B141 |
| 156 | `B142` | `BOOLEAN` | No |  | Feature toggle boolean flag B142 |
| 157 | `B143` | `BOOLEAN` | No |  | Feature toggle boolean flag B143 |
| 158 | `B144` | `BOOLEAN` | No |  | Feature toggle boolean flag B144 |
| 159 | `B145` | `BOOLEAN` | No |  | Feature toggle boolean flag B145 |
| 160 | `B146` | `BOOLEAN` | No |  | Feature toggle boolean flag B146 |
| 161 | `B147` | `BOOLEAN` | No |  | Feature toggle boolean flag B147 |
| 162 | `B148` | `BOOLEAN` | No |  | Feature toggle boolean flag B148 |
| 163 | `B149` | `BOOLEAN` | No |  | Feature toggle boolean flag B149 |
| 164 | `B150` | `BOOLEAN` | No |  | Feature toggle boolean flag B150 |
| 165 | `B151` | `BOOLEAN` | No |  | Feature toggle boolean flag B151 |
| 166 | `B152` | `BOOLEAN` | No |  | Feature toggle boolean flag B152 |
| 167 | `B153` | `BOOLEAN` | No |  | Feature toggle boolean flag B153 |
| 168 | `B154` | `BOOLEAN` | No |  | Feature toggle boolean flag B154 |
| 169 | `B155` | `BOOLEAN` | No |  | Feature toggle boolean flag B155 |
| 170 | `B156` | `BOOLEAN` | No |  | Feature toggle boolean flag B156 |
| 171 | `B157` | `BOOLEAN` | No |  | Feature toggle boolean flag B157 |
| 172 | `B158` | `BOOLEAN` | No |  | Feature toggle boolean flag B158 |
| 173 | `B159` | `BOOLEAN` | No |  | Feature toggle boolean flag B159 |
| 174 | `B160` | `BOOLEAN` | No |  | Feature toggle boolean flag B160 |
| 175 | `B161` | `BOOLEAN` | No |  | Feature toggle boolean flag B161 |
| 176 | `B162` | `BOOLEAN` | No |  | Feature toggle boolean flag B162 |
| 177 | `B163` | `BOOLEAN` | No |  | Feature toggle boolean flag B163 |
| 178 | `B164` | `BOOLEAN` | No |  | Feature toggle boolean flag B164 |
| 179 | `B165` | `BOOLEAN` | No |  | Feature toggle boolean flag B165 |
| 180 | `B166` | `BOOLEAN` | No |  | Feature toggle boolean flag B166 |
| 181 | `B167` | `BOOLEAN` | No |  | Feature toggle boolean flag B167 |
| 182 | `B168` | `BOOLEAN` | No |  | Feature toggle boolean flag B168 |
| 183 | `B169` | `BOOLEAN` | No |  | Feature toggle boolean flag B169 |
| 184 | `B170` | `BOOLEAN` | No |  | Feature toggle boolean flag B170 |
| 185 | `B171` | `BOOLEAN` | No |  | Feature toggle boolean flag B171 |
| 186 | `B172` | `BOOLEAN` | No |  | Feature toggle boolean flag B172 |
| 187 | `B173` | `BOOLEAN` | No |  | Feature toggle boolean flag B173 |
| 188 | `B174` | `BOOLEAN` | No |  | Feature toggle boolean flag B174 |
| 189 | `B175` | `BOOLEAN` | No |  | Feature toggle boolean flag B175 |
| 190 | `B176` | `BOOLEAN` | No |  | Feature toggle boolean flag B176 |
| 191 | `B177` | `BOOLEAN` | No |  | Feature toggle boolean flag B177 |
| 192 | `B178` | `BOOLEAN` | No |  | Feature toggle boolean flag B178 |
| 193 | `B179` | `BOOLEAN` | No |  | Feature toggle boolean flag B179 |
| 194 | `B180` | `BOOLEAN` | No |  | Feature toggle boolean flag B180 |
| 195 | `B181` | `BOOLEAN` | No |  | Feature toggle boolean flag B181 |
| 196 | `B182` | `BOOLEAN` | No |  | Feature toggle boolean flag B182 |
| 197 | `B183` | `BOOLEAN` | No |  | Feature toggle boolean flag B183 |
| 198 | `B184` | `BOOLEAN` | No |  | Feature toggle boolean flag B184 |
| 199 | `B185` | `BOOLEAN` | No |  | Feature toggle boolean flag B185 |
| 200 | `B186` | `BOOLEAN` | No |  | Feature toggle boolean flag B186 |
| 201 | `B187` | `BOOLEAN` | No |  | Feature toggle boolean flag B187 |
| 202 | `B188` | `BOOLEAN` | No |  | Feature toggle boolean flag B188 |
| 203 | `B189` | `BOOLEAN` | No |  | Feature toggle boolean flag B189 |
| 204 | `B190` | `BOOLEAN` | No |  | Feature toggle boolean flag B190 |
| 205 | `B191` | `BOOLEAN` | No |  | Feature toggle boolean flag B191 |
| 206 | `B192` | `BOOLEAN` | No |  | Feature toggle boolean flag B192 |
| 207 | `B193` | `BOOLEAN` | No |  | Feature toggle boolean flag B193 |
| 208 | `B194` | `BOOLEAN` | No |  | Feature toggle boolean flag B194 |
| 209 | `B195` | `BOOLEAN` | No |  | Feature toggle boolean flag B195 |
| 210 | `B196` | `BOOLEAN` | No |  | Feature toggle boolean flag B196 |
| 211 | `B197` | `BOOLEAN` | No |  | Feature toggle boolean flag B197 |
| 212 | `B198` | `BOOLEAN` | No |  | Feature toggle boolean flag B198 |
| 213 | `B199` | `BOOLEAN` | No |  | Feature toggle boolean flag B199 |
| 214 | `B200` | `BOOLEAN` | No |  | Feature toggle boolean flag B200 |
| 215 | `PI1` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI1 |
| 216 | `PI2` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI2 |
| 217 | `PI3` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI3 |
| 218 | `PI4` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI4 |
| 219 | `PI5` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI5 |
| 220 | `PI6` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI6 |
| 221 | `PI7` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI7 |
| 222 | `PI8` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI8 |
| 223 | `PI9` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI9 |
| 224 | `PI10` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI10 |
| 225 | `PI11` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI11 |
| 226 | `PI12` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI12 |
| 227 | `PI13` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI13 |
| 228 | `PI14` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI14 |
| 229 | `PI15` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI15 |
| 230 | `PI16` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI16 |
| 231 | `PI17` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI17 |
| 232 | `PI18` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI18 |
| 233 | `PI19` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI19 |
| 234 | `PI20` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI20 |
| 235 | `L1` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L1 |
| 236 | `L2` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L2 |
| 237 | `L3` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L3 |
| 238 | `L4` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L4 |
| 239 | `L5` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L5 |
| 240 | `L6` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L6 |
| 241 | `L7` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L7 |
| 242 | `L8` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L8 |
| 243 | `L9` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L9 |
| 244 | `L10` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L10 |
| 245 | `L11` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L11 |
| 246 | `L12` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L12 |
| 247 | `L13` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L13 |
| 248 | `L14` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L14 |
| 249 | `L15` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L15 |
| 250 | `L16` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L16 |
| 251 | `L17` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L17 |
| 252 | `L18` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L18 |
| 253 | `L19` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L19 |
| 254 | `L20` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L20 |
| 255 | `PI` | `SMALLINT` | Yes |  | Integer identifier or enum code for PI |

---

<a name="table-userpreferences1"></a>

### Table: `UserPreferences1`

> **Purpose:** Extended configuration parameters (E-Invoice, E-Way Bill credentials, Cloud backup settings).

- **Row Count in Active FY:** `1`
- **Total Columns:** `161`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Name` | `WCHAR(20.0)` | Yes |  | Text attribute: Name |
| 2 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 3 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 4 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 5 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 6 | `C5` | `WCHAR(255.0)` | Yes |  | Text attribute: C5 |
| 7 | `C6` | `WCHAR(255.0)` | Yes |  | Text attribute: C6 |
| 8 | `C7` | `WCHAR(255.0)` | Yes |  | Text attribute: C7 |
| 9 | `C8` | `WCHAR(255.0)` | Yes |  | Text attribute: C8 |
| 10 | `C9` | `WCHAR(255.0)` | Yes |  | Text attribute: C9 |
| 11 | `C10` | `WCHAR(255.0)` | Yes |  | Text attribute: C10 |
| 12 | `C11` | `WCHAR(255.0)` | Yes |  | Text attribute: C11 |
| 13 | `C12` | `WCHAR(255.0)` | Yes |  | Text attribute: C12 |
| 14 | `C13` | `WCHAR(255.0)` | Yes |  | Text attribute: C13 |
| 15 | `C14` | `WCHAR(255.0)` | Yes |  | Text attribute: C14 |
| 16 | `C15` | `WCHAR(255.0)` | Yes |  | Text attribute: C15 |
| 17 | `C16` | `WCHAR(255.0)` | Yes |  | Text attribute: C16 |
| 18 | `C17` | `WCHAR(255.0)` | Yes |  | Text attribute: C17 |
| 19 | `C18` | `WCHAR(255.0)` | Yes |  | Text attribute: C18 |
| 20 | `C19` | `WCHAR(255.0)` | Yes |  | Text attribute: C19 |
| 21 | `C20` | `WCHAR(255.0)` | Yes |  | Text attribute: C20 |
| 22 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 23 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 24 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 25 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 26 | `D5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D5 |
| 27 | `D6` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D6 |
| 28 | `D7` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D7 |
| 29 | `D8` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D8 |
| 30 | `D9` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D9 |
| 31 | `D10` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D10 |
| 32 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 33 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 34 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 35 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 36 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 37 | `B6` | `BOOLEAN` | No |  | Boolean flag for B6 (True/False) |
| 38 | `B7` | `BOOLEAN` | No |  | Boolean flag for B7 (True/False) |
| 39 | `B8` | `BOOLEAN` | No |  | Boolean flag for B8 (True/False) |
| 40 | `B9` | `BOOLEAN` | No |  | Boolean flag for B9 (True/False) |
| 41 | `B10` | `BOOLEAN` | No |  | Boolean flag for B10 (True/False) |
| 42 | `B11` | `BOOLEAN` | No |  | Boolean flag for B11 (True/False) |
| 43 | `B12` | `BOOLEAN` | No |  | Boolean flag for B12 (True/False) |
| 44 | `B13` | `BOOLEAN` | No |  | Boolean flag for B13 (True/False) |
| 45 | `B14` | `BOOLEAN` | No |  | Boolean flag for B14 (True/False) |
| 46 | `B15` | `BOOLEAN` | No |  | Boolean flag for B15 (True/False) |
| 47 | `B16` | `BOOLEAN` | No |  | Boolean flag for B16 (True/False) |
| 48 | `B17` | `BOOLEAN` | No |  | Boolean flag for B17 (True/False) |
| 49 | `B18` | `BOOLEAN` | No |  | Boolean flag for B18 (True/False) |
| 50 | `B19` | `BOOLEAN` | No |  | Boolean flag for B19 (True/False) |
| 51 | `B20` | `BOOLEAN` | No |  | Boolean flag for B20 (True/False) |
| 52 | `B21` | `BOOLEAN` | No |  | Boolean flag for B21 (True/False) |
| 53 | `B22` | `BOOLEAN` | No |  | Boolean flag for B22 (True/False) |
| 54 | `B23` | `BOOLEAN` | No |  | Boolean flag for B23 (True/False) |
| 55 | `B24` | `BOOLEAN` | No |  | Boolean flag for B24 (True/False) |
| 56 | `B25` | `BOOLEAN` | No |  | Boolean flag for B25 (True/False) |
| 57 | `B26` | `BOOLEAN` | No |  | Boolean flag for B26 (True/False) |
| 58 | `B27` | `BOOLEAN` | No |  | Boolean flag for B27 (True/False) |
| 59 | `B28` | `BOOLEAN` | No |  | Boolean flag for B28 (True/False) |
| 60 | `B29` | `BOOLEAN` | No |  | Boolean flag for B29 (True/False) |
| 61 | `B30` | `BOOLEAN` | No |  | Boolean flag for B30 (True/False) |
| 62 | `B31` | `BOOLEAN` | No |  | Boolean flag for B31 (True/False) |
| 63 | `B32` | `BOOLEAN` | No |  | Boolean flag for B32 (True/False) |
| 64 | `B33` | `BOOLEAN` | No |  | Boolean flag for B33 (True/False) |
| 65 | `B34` | `BOOLEAN` | No |  | Boolean flag for B34 (True/False) |
| 66 | `B35` | `BOOLEAN` | No |  | Boolean flag for B35 (True/False) |
| 67 | `B36` | `BOOLEAN` | No |  | Boolean flag for B36 (True/False) |
| 68 | `B37` | `BOOLEAN` | No |  | Boolean flag for B37 (True/False) |
| 69 | `B38` | `BOOLEAN` | No |  | Boolean flag for B38 (True/False) |
| 70 | `B39` | `BOOLEAN` | No |  | Boolean flag for B39 (True/False) |
| 71 | `B40` | `BOOLEAN` | No |  | Boolean flag for B40 (True/False) |
| 72 | `B41` | `BOOLEAN` | No |  | Boolean flag for B41 (True/False) |
| 73 | `B42` | `BOOLEAN` | No |  | Boolean flag for B42 (True/False) |
| 74 | `B43` | `BOOLEAN` | No |  | Boolean flag for B43 (True/False) |
| 75 | `B44` | `BOOLEAN` | No |  | Boolean flag for B44 (True/False) |
| 76 | `B45` | `BOOLEAN` | No |  | Boolean flag for B45 (True/False) |
| 77 | `B46` | `BOOLEAN` | No |  | Boolean flag for B46 (True/False) |
| 78 | `B47` | `BOOLEAN` | No |  | Boolean flag for B47 (True/False) |
| 79 | `B48` | `BOOLEAN` | No |  | Boolean flag for B48 (True/False) |
| 80 | `B49` | `BOOLEAN` | No |  | Boolean flag for B49 (True/False) |
| 81 | `B50` | `BOOLEAN` | No |  | Boolean flag for B50 (True/False) |
| 82 | `B51` | `BOOLEAN` | No |  | Boolean flag for B51 (True/False) |
| 83 | `B52` | `BOOLEAN` | No |  | Boolean flag for B52 (True/False) |
| 84 | `B53` | `BOOLEAN` | No |  | Boolean flag for B53 (True/False) |
| 85 | `B54` | `BOOLEAN` | No |  | Boolean flag for B54 (True/False) |
| 86 | `B55` | `BOOLEAN` | No |  | Boolean flag for B55 (True/False) |
| 87 | `B56` | `BOOLEAN` | No |  | Boolean flag for B56 (True/False) |
| 88 | `B57` | `BOOLEAN` | No |  | Boolean flag for B57 (True/False) |
| 89 | `B58` | `BOOLEAN` | No |  | Boolean flag for B58 (True/False) |
| 90 | `B59` | `BOOLEAN` | No |  | Boolean flag for B59 (True/False) |
| 91 | `B60` | `BOOLEAN` | No |  | Boolean flag for B60 (True/False) |
| 92 | `B61` | `BOOLEAN` | No |  | Boolean flag for B61 (True/False) |
| 93 | `B62` | `BOOLEAN` | No |  | Boolean flag for B62 (True/False) |
| 94 | `B63` | `BOOLEAN` | No |  | Boolean flag for B63 (True/False) |
| 95 | `B64` | `BOOLEAN` | No |  | Boolean flag for B64 (True/False) |
| 96 | `B65` | `BOOLEAN` | No |  | Boolean flag for B65 (True/False) |
| 97 | `B66` | `BOOLEAN` | No |  | Boolean flag for B66 (True/False) |
| 98 | `B67` | `BOOLEAN` | No |  | Boolean flag for B67 (True/False) |
| 99 | `B68` | `BOOLEAN` | No |  | Boolean flag for B68 (True/False) |
| 100 | `B69` | `BOOLEAN` | No |  | Boolean flag for B69 (True/False) |
| 101 | `B70` | `BOOLEAN` | No |  | Boolean flag for B70 (True/False) |
| 102 | `B71` | `BOOLEAN` | No |  | Boolean flag for B71 (True/False) |
| 103 | `B72` | `BOOLEAN` | No |  | Boolean flag for B72 (True/False) |
| 104 | `B73` | `BOOLEAN` | No |  | Boolean flag for B73 (True/False) |
| 105 | `B74` | `BOOLEAN` | No |  | Boolean flag for B74 (True/False) |
| 106 | `B75` | `BOOLEAN` | No |  | Boolean flag for B75 (True/False) |
| 107 | `B76` | `BOOLEAN` | No |  | Boolean flag for B76 (True/False) |
| 108 | `B77` | `BOOLEAN` | No |  | Boolean flag for B77 (True/False) |
| 109 | `B78` | `BOOLEAN` | No |  | Boolean flag for B78 (True/False) |
| 110 | `B79` | `BOOLEAN` | No |  | Boolean flag for B79 (True/False) |
| 111 | `B80` | `BOOLEAN` | No |  | Boolean flag for B80 (True/False) |
| 112 | `B81` | `BOOLEAN` | No |  | Boolean flag for B81 (True/False) |
| 113 | `B82` | `BOOLEAN` | No |  | Boolean flag for B82 (True/False) |
| 114 | `B83` | `BOOLEAN` | No |  | Boolean flag for B83 (True/False) |
| 115 | `B84` | `BOOLEAN` | No |  | Boolean flag for B84 (True/False) |
| 116 | `B85` | `BOOLEAN` | No |  | Boolean flag for B85 (True/False) |
| 117 | `B86` | `BOOLEAN` | No |  | Boolean flag for B86 (True/False) |
| 118 | `B87` | `BOOLEAN` | No |  | Boolean flag for B87 (True/False) |
| 119 | `B88` | `BOOLEAN` | No |  | Boolean flag for B88 (True/False) |
| 120 | `B89` | `BOOLEAN` | No |  | Boolean flag for B89 (True/False) |
| 121 | `B90` | `BOOLEAN` | No |  | Boolean flag for B90 (True/False) |
| 122 | `B91` | `BOOLEAN` | No |  | Boolean flag for B91 (True/False) |
| 123 | `B92` | `BOOLEAN` | No |  | Boolean flag for B92 (True/False) |
| 124 | `B93` | `BOOLEAN` | No |  | Boolean flag for B93 (True/False) |
| 125 | `B94` | `BOOLEAN` | No |  | Boolean flag for B94 (True/False) |
| 126 | `B95` | `BOOLEAN` | No |  | Boolean flag for B95 (True/False) |
| 127 | `B96` | `BOOLEAN` | No |  | Boolean flag for B96 (True/False) |
| 128 | `B97` | `BOOLEAN` | No |  | Boolean flag for B97 (True/False) |
| 129 | `B98` | `BOOLEAN` | No |  | Boolean flag for B98 (True/False) |
| 130 | `B99` | `BOOLEAN` | No |  | Boolean flag for B99 (True/False) |
| 131 | `B100` | `BOOLEAN` | No |  | Boolean flag for B100 (True/False) |
| 132 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 133 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 134 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 135 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 136 | `I5` | `SMALLINT` | Yes |  | Integer identifier or enum code for I5 |
| 137 | `I6` | `SMALLINT` | Yes |  | Integer identifier or enum code for I6 |
| 138 | `I7` | `SMALLINT` | Yes |  | Integer identifier or enum code for I7 |
| 139 | `I8` | `SMALLINT` | Yes |  | Integer identifier or enum code for I8 |
| 140 | `I9` | `SMALLINT` | Yes |  | Integer identifier or enum code for I9 |
| 141 | `I10` | `SMALLINT` | Yes |  | Integer identifier or enum code for I10 |
| 142 | `I11` | `SMALLINT` | Yes |  | Integer identifier or enum code for I11 |
| 143 | `I12` | `SMALLINT` | Yes |  | Integer identifier or enum code for I12 |
| 144 | `I13` | `SMALLINT` | Yes |  | Integer identifier or enum code for I13 |
| 145 | `I14` | `SMALLINT` | Yes |  | Integer identifier or enum code for I14 |
| 146 | `I15` | `SMALLINT` | Yes |  | Integer identifier or enum code for I15 |
| 147 | `I16` | `SMALLINT` | Yes |  | Integer identifier or enum code for I16 |
| 148 | `I17` | `SMALLINT` | Yes |  | Integer identifier or enum code for I17 |
| 149 | `I18` | `SMALLINT` | Yes |  | Integer identifier or enum code for I18 |
| 150 | `I19` | `SMALLINT` | Yes |  | Integer identifier or enum code for I19 |
| 151 | `I20` | `SMALLINT` | Yes |  | Integer identifier or enum code for I20 |
| 152 | `L1` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L1 |
| 153 | `MaintainNM` | `BOOLEAN` | No |  | Boolean flag for MaintainNM (True/False) |
| 154 | `PopUpNM` | `BOOLEAN` | No |  | Boolean flag for PopUpNM (True/False) |
| 155 | `LastNMCategoryCode` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for LastNMCategoryCode |
| 156 | `LastNMNotesCode` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for LastNMNotesCode |
| 157 | `LastThoughtID` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for LastThoughtID |
| 158 | `MasterVoucherAction` | `WCHAR` | Yes |  | Text attribute: MasterVoucherAction |
| 159 | `GeneralConfig` | `WCHAR` | Yes |  | Text attribute: GeneralConfig |
| 160 | `PopUpDashBoard` | `BOOLEAN` | No |  | Boolean flag for PopUpDashBoard (True/False) |
| 161 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |

---

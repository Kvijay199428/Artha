# BusyWin FY Database: Masters & Accounts Schemas

> **Database File:** `db1<YYYY>.bds` (e.g. `C:\BusyWin\DATA\COMP0001\db12026.bds`)

> **Engine:** Microsoft Jet 4.0 / Access OLEDB (`ILoveMyINDIA`)

> **Description:** Detailed table schemas and column definitions for all Master entities in db1YYYY.bds (Accounts, Parties, Items, Units, Descriptions, Balances).


## Tables in this Module


| # | Table Name | Columns | Active Rows | Primary Key | Description |
|---|------------|:-------:|:-----------:|:-----------:|-------------|
| 1 | [`Master1`](#table-master1) | 156 | 585 | `Code` | Unified polymorphic master table storing all Accounts, Parties (Customers/Vendors), Inventory Items, Units of Measurement, Bill Sundries, Tax Categories, Price Levels, and Account/Item Groups. |
| 2 | [`MasterAddressInfo`](#table-masteraddressinfo) | 75 | 108 | `MasterCode` | Extended contact information (Address lines 1-4, Phone, Mobile, Email, PAN, GSTIN, Station, Pincode) linked to Master1.Code. |
| 3 | [`MasterSupport`](#table-mastersupport) | 51 | 132 | `-` | Secondary metadata for masters including barcode mappings, custom user fields, and external ERP keys. |
| 4 | [`MastFootPrint`](#table-mastfootprint) | 6 | 245 | `-` | Audit footprint for master entities (created by user, creation timestamp, modified by, modification timestamp). |
| 5 | [`ItemDesc`](#table-itemdesc) | 30 | 7 | `-` | Extended product description lines, technical specifications, and warranty terms printed on invoices. |
| 6 | [`ItemParamDet`](#table-itemparamdet) | 42 | 0 | `-` | Parameterized stock attributes (Size, Color, Shade, Grade, Batch) for fashion/apparel/tile inventory. |
| 7 | [`ItemSerialNo`](#table-itemserialno) | 28 | 0 | `-` | Unique serial numbers / IMEI tracking for discrete inventory items with stock status (In Stock, Sold, Returned). |
| 8 | [`ItemSNInstallDet`](#table-itemsninstalldet) | 23 | 0 | `-` | Installation, commissioning, and warranty details linked to serialized equipment and appliances. |
| 9 | [`Folio1`](#table-folio1) | 164 | 276 | `MasterCode` | Fast financial and stock balance summary cache storing opening balances, monthly debits/credits, and closing balances for instantaneous report rendering without scanning raw transactions. |
| 10 | [`Help1`](#table-help1) | 14 | 1065 | `-` | High-speed auto-complete search cache indexing master names, aliases, and parent groups for UI dropdown lookups. |
| 11 | [`Help1AddnInfo`](#table-help1addninfo) | 7 | 109 | `-` | Secondary keyword index and alias search phrases supporting Help1 search acceleration. |
| 12 | [`Help2`](#table-help2) | 4 | 6 | `-` | Lookup index for sub-entities, material centers (godowns), and cost centers. |
| 13 | [`DeletedMasters`](#table-deletedmasters) | 2 | 0 | `-` | Audit tombstone register of deleted master entities preventing ID collision and maintaining audit integrity. |

---

## Detailed Column Schemas


<a name="table-master1"></a>

### Table: `Master1`

> **Purpose:** Unified polymorphic master table storing all Accounts, Parties (Customers/Vendors), Inventory Items, Units of Measurement, Bill Sundries, Tax Categories, Price Levels, and Account/Item Groups.

- **Row Count in Active FY:** `585`
- **Total Columns:** `156`
- **Primary Key:** `Code`

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Code` | `INTEGER (Long)` | Yes | **PK** | Unique Master ID (Primary Key for all accounts, items, groups, units) |
| 2 | `MasterType` | `SMALLINT` | Yes |  | Polymorphic Entity Type enum (1=AccountGroup, 2=Account, 6=Item, 8=Unit, 9=BillSundry, 21=TaxCategory) |
| 3 | `Name` | `WCHAR(40.0)` | Yes |  | Text attribute: Name |
| 4 | `Alias` | `WCHAR(40.0)` | Yes |  | Text attribute: Alias |
| 5 | `PrintName` | `WCHAR(60.0)` | Yes |  | Text attribute: PrintName |
| 6 | `ParentGrp` | `INTEGER (Long)` | Yes |  | Foreign key to parent Master1.Code (Account Group or Item Group) |
| 7 | `Stamp` | `INTEGER (Long)` | Yes |  | Internal concurrency timestamp / modification revision stamp |
| 8 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 9 | `CM2` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM2 (links to Master1.Code based on MasterType) |
| 10 | `CM3` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM3 (links to Master1.Code based on MasterType) |
| 11 | `CM4` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM4 (links to Master1.Code based on MasterType) |
| 12 | `CM5` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM5 (links to Master1.Code based on MasterType) |
| 13 | `CM6` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM6 (links to Master1.Code based on MasterType) |
| 14 | `CM7` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM7 (links to Master1.Code based on MasterType) |
| 15 | `CM8` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM8 (links to Master1.Code based on MasterType) |
| 16 | `CM9` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM9 (links to Master1.Code based on MasterType) |
| 17 | `CM10` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM10 (links to Master1.Code based on MasterType) |
| 18 | `CM11` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM11 (links to Master1.Code based on MasterType) |
| 19 | `D1` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D1 |
| 20 | `D2` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D2 |
| 21 | `D3` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D3 |
| 22 | `D4` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D4 |
| 23 | `D5` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D5 |
| 24 | `D6` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D6 |
| 25 | `D7` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D7 |
| 26 | `D8` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D8 |
| 27 | `D9` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D9 |
| 28 | `D10` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D10 |
| 29 | `D11` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D11 |
| 30 | `D12` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D12 |
| 31 | `D13` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D13 |
| 32 | `D14` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D14 |
| 33 | `D15` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D15 |
| 34 | `D16` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D16 |
| 35 | `D17` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D17 |
| 36 | `D18` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D18 |
| 37 | `D19` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D19 |
| 38 | `D20` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D20 |
| 39 | `D21` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D21 |
| 40 | `D22` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D22 |
| 41 | `D23` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D23 |
| 42 | `D24` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D24 |
| 43 | `D25` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D25 |
| 44 | `D26` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D26 |
| 45 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 46 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 47 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 48 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 49 | `I5` | `SMALLINT` | Yes |  | Integer identifier or enum code for I5 |
| 50 | `I6` | `SMALLINT` | Yes |  | Integer identifier or enum code for I6 |
| 51 | `I7` | `SMALLINT` | Yes |  | Integer identifier or enum code for I7 |
| 52 | `I8` | `SMALLINT` | Yes |  | Integer identifier or enum code for I8 |
| 53 | `I9` | `SMALLINT` | Yes |  | Integer identifier or enum code for I9 |
| 54 | `I10` | `SMALLINT` | Yes |  | Integer identifier or enum code for I10 |
| 55 | `I11` | `SMALLINT` | Yes |  | Integer identifier or enum code for I11 |
| 56 | `I12` | `SMALLINT` | Yes |  | Integer identifier or enum code for I12 |
| 57 | `I13` | `SMALLINT` | Yes |  | Integer identifier or enum code for I13 |
| 58 | `I14` | `SMALLINT` | Yes |  | Integer identifier or enum code for I14 |
| 59 | `I15` | `SMALLINT` | Yes |  | Integer identifier or enum code for I15 |
| 60 | `I16` | `SMALLINT` | Yes |  | Integer identifier or enum code for I16 |
| 61 | `I17` | `SMALLINT` | Yes |  | Integer identifier or enum code for I17 |
| 62 | `I18` | `SMALLINT` | Yes |  | Integer identifier or enum code for I18 |
| 63 | `I19` | `SMALLINT` | Yes |  | Integer identifier or enum code for I19 |
| 64 | `I20` | `SMALLINT` | Yes |  | Integer identifier or enum code for I20 |
| 65 | `I21` | `SMALLINT` | Yes |  | Integer identifier or enum code for I21 |
| 66 | `I22` | `SMALLINT` | Yes |  | Integer identifier or enum code for I22 |
| 67 | `I23` | `SMALLINT` | Yes |  | Integer identifier or enum code for I23 |
| 68 | `I24` | `SMALLINT` | Yes |  | Integer identifier or enum code for I24 |
| 69 | `I25` | `SMALLINT` | Yes |  | Integer identifier or enum code for I25 |
| 70 | `I26` | `SMALLINT` | Yes |  | Integer identifier or enum code for I26 |
| 71 | `I27` | `SMALLINT` | Yes |  | Integer identifier or enum code for I27 |
| 72 | `I28` | `SMALLINT` | Yes |  | Integer identifier or enum code for I28 |
| 73 | `Level` | `SMALLINT` | Yes |  | Integer identifier or enum code for Level |
| 74 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 75 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 76 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 77 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 78 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 79 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 80 | `B6` | `BOOLEAN` | No |  | Boolean flag for B6 (True/False) |
| 81 | `B7` | `BOOLEAN` | No |  | Boolean flag for B7 (True/False) |
| 82 | `B8` | `BOOLEAN` | No |  | Boolean flag for B8 (True/False) |
| 83 | `B9` | `BOOLEAN` | No |  | Boolean flag for B9 (True/False) |
| 84 | `B10` | `BOOLEAN` | No |  | Boolean flag for B10 (True/False) |
| 85 | `B11` | `BOOLEAN` | No |  | Boolean flag for B11 (True/False) |
| 86 | `B12` | `BOOLEAN` | No |  | Boolean flag for B12 (True/False) |
| 87 | `B13` | `BOOLEAN` | No |  | Boolean flag for B13 (True/False) |
| 88 | `B14` | `BOOLEAN` | No |  | Boolean flag for B14 (True/False) |
| 89 | `B15` | `BOOLEAN` | No |  | Boolean flag for B15 (True/False) |
| 90 | `B16` | `BOOLEAN` | No |  | Boolean flag for B16 (True/False) |
| 91 | `B17` | `BOOLEAN` | No |  | Boolean flag for B17 (True/False) |
| 92 | `B18` | `BOOLEAN` | No |  | Boolean flag for B18 (True/False) |
| 93 | `B19` | `BOOLEAN` | No |  | Boolean flag for B19 (True/False) |
| 94 | `B20` | `BOOLEAN` | No |  | Boolean flag for B20 (True/False) |
| 95 | `B21` | `BOOLEAN` | No |  | Boolean flag for B21 (True/False) |
| 96 | `B22` | `BOOLEAN` | No |  | Boolean flag for B22 (True/False) |
| 97 | `B23` | `BOOLEAN` | No |  | Boolean flag for B23 (True/False) |
| 98 | `B24` | `BOOLEAN` | No |  | Boolean flag for B24 (True/False) |
| 99 | `B25` | `BOOLEAN` | No |  | Boolean flag for B25 (True/False) |
| 100 | `B26` | `BOOLEAN` | No |  | Boolean flag for B26 (True/False) |
| 101 | `B27` | `BOOLEAN` | No |  | Boolean flag for B27 (True/False) |
| 102 | `B28` | `BOOLEAN` | No |  | Boolean flag for B28 (True/False) |
| 103 | `B29` | `BOOLEAN` | No |  | Boolean flag for B29 (True/False) |
| 104 | `B30` | `BOOLEAN` | No |  | Boolean flag for B30 (True/False) |
| 105 | `B31` | `BOOLEAN` | No |  | Boolean flag for B31 (True/False) |
| 106 | `B32` | `BOOLEAN` | No |  | Boolean flag for B32 (True/False) |
| 107 | `B33` | `BOOLEAN` | No |  | Boolean flag for B33 (True/False) |
| 108 | `B34` | `BOOLEAN` | No |  | Boolean flag for B34 (True/False) |
| 109 | `B35` | `BOOLEAN` | No |  | Boolean flag for B35 (True/False) |
| 110 | `B36` | `BOOLEAN` | No |  | Boolean flag for B36 (True/False) |
| 111 | `B37` | `BOOLEAN` | No |  | Boolean flag for B37 (True/False) |
| 112 | `B38` | `BOOLEAN` | No |  | Boolean flag for B38 (True/False) |
| 113 | `B39` | `BOOLEAN` | No |  | Boolean flag for B39 (True/False) |
| 114 | `B40` | `BOOLEAN` | No |  | Boolean flag for B40 (True/False) |
| 115 | `External` | `BOOLEAN` | No |  | Boolean flag for External (True/False) |
| 116 | `L1` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L1 |
| 117 | `L2` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L2 |
| 118 | `Notes1` | `WCHAR(80.0)` | Yes |  | Text attribute: Notes1 |
| 119 | `Notes2` | `WCHAR(80.0)` | Yes |  | Text attribute: Notes2 |
| 120 | `MasterNotes` | `WCHAR` | Yes |  | Text attribute: MasterNotes |
| 121 | `CreatedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: CreatedBy |
| 122 | `CreationTime` | `DATETIME` | Yes |  | Timestamp / Date field for CreationTime |
| 123 | `ModifiedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: ModifiedBy |
| 124 | `ModificationTime` | `DATETIME` | Yes |  | Timestamp / Date field for ModificationTime |
| 125 | `AuthorisedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: AuthorisedBy |
| 126 | `AuthorisationTime` | `DATETIME` | Yes |  | Timestamp / Date field for AuthorisationTime |
| 127 | `ApprovalStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for ApprovalStatus |
| 128 | `SyncStatus` | `BOOLEAN` | No |  | Boolean flag for SyncStatus (True/False) |
| 129 | `MasterSeriesGrp` | `WCHAR` | Yes |  | Text attribute: MasterSeriesGrp |
| 130 | `Source` | `SMALLINT` | Yes |  | Integer identifier or enum code for Source |
| 131 | `BlockedMaster` | `BOOLEAN` | No |  | Boolean flag for BlockedMaster (True/False) |
| 132 | `BlockedNotes` | `WCHAR` | Yes |  | Text attribute: BlockedNotes |
| 133 | `DeactiveMaster` | `BOOLEAN` | No |  | Pre-allocated double numeric parameter / balance accumulator DeactiveMaster |
| 134 | `C1` | `WCHAR(80.0)` | Yes |  | Text attribute: C1 |
| 135 | `C2` | `WCHAR(80.0)` | Yes |  | Text attribute: C2 |
| 136 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 137 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 138 | `C5` | `WCHAR(255.0)` | Yes |  | Text attribute: C5 |
| 139 | `C6` | `WCHAR(255.0)` | Yes |  | Text attribute: C6 |
| 140 | `HSNCode` | `WCHAR(255.0)` | Yes |  | Harmonized System of Nomenclature (HSN) or SAC code |
| 141 | `SENO` | `WCHAR(255.0)` | Yes |  | Text attribute: SENO |
| 142 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |
| 143 | `M2` | `WCHAR` | Yes |  | Text attribute: M2 |
| 144 | `BlockedVchType` | `WCHAR(255.0)` | Yes |  | Text attribute: BlockedVchType |
| 145 | `TPF1` | `BOOLEAN` | No |  | Boolean flag for TPF1 (True/False) |
| 146 | `TPF2` | `BOOLEAN` | No |  | Boolean flag for TPF2 (True/False) |
| 147 | `RejectionStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for RejectionStatus |
| 148 | `NameSL` | `WCHAR(255.0)` | Yes |  | Text attribute: NameSL |
| 149 | `AliasSL` | `WCHAR(255.0)` | Yes |  | Text attribute: AliasSL |
| 150 | `PrintNameSL` | `WCHAR(255.0)` | Yes |  | Text attribute: PrintNameSL |
| 151 | `SelfImageLink` | `WCHAR(255.0)` | Yes |  | Text attribute: SelfImageLink |
| 152 | `SelfImageName` | `WCHAR(255.0)` | Yes |  | Text attribute: SelfImageName |
| 153 | `OldIdentity` | `WCHAR` | Yes |  | Text attribute: OldIdentity |
| 154 | `C7` | `WCHAR(255.0)` | Yes |  | Text attribute: C7 |
| 155 | `I29` | `SMALLINT` | Yes |  | Integer identifier or enum code for I29 |
| 156 | `I30` | `SMALLINT` | Yes |  | Integer identifier or enum code for I30 |

---

<a name="table-masteraddressinfo"></a>

### Table: `MasterAddressInfo`

> **Purpose:** Extended contact information (Address lines 1-4, Phone, Mobile, Email, PAN, GSTIN, Station, Pincode) linked to Master1.Code.

- **Row Count in Active FY:** `108`
- **Total Columns:** `75`
- **Primary Key:** `MasterCode`

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `MasterCode` | `INTEGER (Long)` | Yes | **PK** | Integer identifier or enum code for MasterCode |
| 2 | `Address1` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 3 | `Address2` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 4 | `Address3` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 5 | `Address4` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 6 | `TelNo` | `WCHAR(40.0)` | Yes |  | Fixed-line landline telephone number |
| 7 | `Fax` | `WCHAR(30.0)` | Yes |  | Text attribute: Fax |
| 8 | `Email` | `WCHAR(255.0)` | Yes |  | Official email address for communication and e-invoicing |
| 9 | `Mobile` | `WCHAR(255.0)` | Yes |  | Primary contact mobile telephone number |
| 10 | `LST` | `WCHAR(30.0)` | Yes |  | Text attribute: LST |
| 11 | `CST` | `WCHAR(30.0)` | Yes |  | Text attribute: CST |
| 12 | `ST37` | `WCHAR(30.0)` | Yes |  | Text attribute: ST37 |
| 13 | `TINNo` | `WCHAR(30.0)` | Yes |  | Text attribute: TINNo |
| 14 | `LBTNo` | `WCHAR(255.0)` | Yes |  | Text attribute: LBTNo |
| 15 | `ITPAN` | `WCHAR(20.0)` | Yes |  | Income Tax Permanent Account Number (PAN) |
| 16 | `ITWard` | `WCHAR(20.0)` | Yes |  | Text attribute: ITWard |
| 17 | `Contact` | `WCHAR(40.0)` | Yes |  | Text attribute: Contact |
| 18 | `ExciseRegNo` | `WCHAR(30.0)` | Yes |  | Text attribute: ExciseRegNo |
| 19 | `ECCCode` | `WCHAR(20.0)` | Yes |  | Text attribute: ECCCode |
| 20 | `PLANo` | `WCHAR(20.0)` | Yes |  | Text attribute: PLANo |
| 21 | `Division` | `WCHAR(80.0)` | Yes |  | Text attribute: Division |
| 22 | `Range` | `WCHAR(80.0)` | Yes |  | Text attribute: Range |
| 23 | `Collectorate` | `WCHAR(40.0)` | Yes |  | Text attribute: Collectorate |
| 24 | `OF1` | `WCHAR(255.0)` | Yes |  | Text attribute: OF1 |
| 25 | `OF2` | `WCHAR(255.0)` | Yes |  | Text attribute: OF2 |
| 26 | `OF3` | `WCHAR(255.0)` | Yes |  | Text attribute: OF3 |
| 27 | `OF4` | `WCHAR(255.0)` | Yes |  | Text attribute: OF4 |
| 28 | `OF5` | `WCHAR(255.0)` | Yes |  | Text attribute: OF5 |
| 29 | `OF6` | `WCHAR(255.0)` | Yes |  | Text attribute: OF6 |
| 30 | `OF7` | `WCHAR(255.0)` | Yes |  | Text attribute: OF7 |
| 31 | `OF8` | `WCHAR(255.0)` | Yes |  | Text attribute: OF8 |
| 32 | `OF9` | `WCHAR(255.0)` | Yes |  | Text attribute: OF9 |
| 33 | `OF10` | `WCHAR(255.0)` | Yes |  | Text attribute: OF10 |
| 34 | `SupplierType` | `WCHAR(25.0)` | Yes |  | Text attribute: SupplierType |
| 35 | `ServiceTaxNo` | `WCHAR(30.0)` | Yes |  | Text attribute: ServiceTaxNo |
| 36 | `TelNoResi` | `WCHAR(40.0)` | Yes |  | Text attribute: TelNoResi |
| 37 | `GSTNo` | `WCHAR(30.0)` | Yes |  | Text attribute: GSTNo |
| 38 | `CountryCodeLong` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for CountryCodeLong |
| 39 | `StateCodeLong` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for StateCodeLong |
| 40 | `CityCodeLong` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for CityCodeLong |
| 41 | `RegionCodeLong` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for RegionCodeLong |
| 42 | `AreaCodeLong` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for AreaCodeLong |
| 43 | `ContDeptCodeLong` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for ContDeptCodeLong |
| 44 | `PINCode` | `WCHAR(10.0)` | Yes |  | Text attribute: PINCode |
| 45 | `DLNo` | `WCHAR(255.0)` | Yes |  | Text attribute: DLNo |
| 46 | `DLNo2` | `WCHAR(255.0)` | Yes |  | Text attribute: DLNo2 |
| 47 | `Transport` | `WCHAR(30.0)` | Yes |  | Text attribute: Transport |
| 48 | `Station` | `WCHAR(30.0)` | Yes |  | Text attribute: Station |
| 49 | `AccNo` | `WCHAR(40.0)` | Yes |  | Text attribute: AccNo |
| 50 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 51 | `Date2` | `DATETIME` | Yes |  | Timestamp / Date field for Date2 |
| 52 | `Date3` | `DATETIME` | Yes |  | Timestamp / Date field for Date3 |
| 53 | `Date4` | `DATETIME` | Yes |  | Timestamp / Date field for Date4 |
| 54 | `Date5` | `DATETIME` | Yes |  | Timestamp / Date field for Date5 |
| 55 | `Date6` | `DATETIME` | Yes |  | Timestamp / Date field for Date6 |
| 56 | `Date7` | `DATETIME` | Yes |  | Timestamp / Date field for Date7 |
| 57 | `Date8` | `DATETIME` | Yes |  | Timestamp / Date field for Date8 |
| 58 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 59 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 60 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 61 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 62 | `C5` | `WCHAR(255.0)` | Yes |  | Text attribute: C5 |
| 63 | `C6` | `WCHAR(255.0)` | Yes |  | Text attribute: C6 |
| 64 | `C7` | `WCHAR(255.0)` | Yes |  | Text attribute: C7 |
| 65 | `C8` | `WCHAR(255.0)` | Yes |  | Text attribute: C8 |
| 66 | `C9` | `WCHAR(255.0)` | Yes |  | Text attribute: C9 |
| 67 | `C10` | `WCHAR(255.0)` | Yes |  | Text attribute: C10 |
| 68 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |
| 69 | `Distance` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Distance |
| 70 | `TransportMode` | `SMALLINT` | Yes |  | Integer identifier or enum code for TransportMode |
| 71 | `Address1SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Address1SL |
| 72 | `Address2SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Address2SL |
| 73 | `Address3SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Address3SL |
| 74 | `Address4SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Address4SL |
| 75 | `WhatsAppNo` | `WCHAR(255.0)` | Yes |  | Text attribute: WhatsAppNo |

---

<a name="table-mastersupport"></a>

### Table: `MasterSupport`

> **Purpose:** Secondary metadata for masters including barcode mappings, custom user fields, and external ERP keys.

- **Row Count in Active FY:** `132`
- **Total Columns:** `51`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `MasterCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for MasterCode |
| 2 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 3 | `CM2` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM2 (links to Master1.Code based on MasterType) |
| 4 | `CM3` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM3 (links to Master1.Code based on MasterType) |
| 5 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 6 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 7 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 8 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 9 | `D5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D5 |
| 10 | `D6` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D6 |
| 11 | `D7` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D7 |
| 12 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 13 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 14 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 15 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 16 | `I5` | `SMALLINT` | Yes |  | Integer identifier or enum code for I5 |
| 17 | `I6` | `SMALLINT` | Yes |  | Integer identifier or enum code for I6 |
| 18 | `I7` | `SMALLINT` | Yes |  | Integer identifier or enum code for I7 |
| 19 | `I8` | `SMALLINT` | Yes |  | Integer identifier or enum code for I8 |
| 20 | `I9` | `SMALLINT` | Yes |  | Integer identifier or enum code for I9 |
| 21 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 22 | `MasterType` | `SMALLINT` | Yes |  | Polymorphic Entity Type enum (1=AccountGroup, 2=Account, 6=Item, 8=Unit, 9=BillSundry, 21=TaxCategory) |
| 23 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 24 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 25 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 26 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 27 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 28 | `C5` | `WCHAR(255.0)` | Yes |  | Text attribute: C5 |
| 29 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 30 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 31 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 32 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 33 | `B6` | `BOOLEAN` | No |  | Boolean flag for B6 (True/False) |
| 34 | `D8` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D8 |
| 35 | `D9` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D9 |
| 36 | `D10` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D10 |
| 37 | `D11` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D11 |
| 38 | `D12` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D12 |
| 39 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 40 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 41 | `CM4` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM4 (links to Master1.Code based on MasterType) |
| 42 | `CM5` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM5 (links to Master1.Code based on MasterType) |
| 43 | `CM6` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM6 (links to Master1.Code based on MasterType) |
| 44 | `Date2` | `DATETIME` | Yes |  | Timestamp / Date field for Date2 |
| 45 | `Date3` | `DATETIME` | Yes |  | Timestamp / Date field for Date3 |
| 46 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |
| 47 | `D13` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D13 |
| 48 | `D14` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D14 |
| 49 | `D15` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D15 |
| 50 | `D16` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D16 |
| 51 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |

---

<a name="table-mastfootprint"></a>

### Table: `MastFootPrint`

> **Purpose:** Audit footprint for master entities (created by user, creation timestamp, modified by, modification timestamp).

- **Row Count in Active FY:** `245`
- **Total Columns:** `6`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `MasterCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for MasterCode |
| 2 | `Name` | `WCHAR(40.0)` | Yes |  | Text attribute: Name |
| 3 | `MasterType` | `SMALLINT` | Yes |  | Polymorphic Entity Type enum (1=AccountGroup, 2=Account, 6=Item, 8=Unit, 9=BillSundry, 21=TaxCategory) |
| 4 | `Stamp` | `INTEGER (Long)` | Yes |  | Internal concurrency timestamp / modification revision stamp |
| 5 | `PartialFP` | `WCHAR` | Yes |  | Text attribute: PartialFP |
| 6 | `RemainFP` | `WCHAR` | Yes |  | Text attribute: RemainFP |

---

<a name="table-itemdesc"></a>

### Table: `ItemDesc`

> **Purpose:** Extended product description lines, technical specifications, and warranty terms printed on invoices.

- **Row Count in Active FY:** `7`
- **Total Columns:** `30`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 3 | `Desc1` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc1 |
| 4 | `Desc2` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc2 |
| 5 | `Desc3` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc3 |
| 6 | `Desc4` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc4 |
| 7 | `Desc5` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc5 |
| 8 | `Desc6` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc6 |
| 9 | `Desc7` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc7 |
| 10 | `Desc8` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc8 |
| 11 | `Desc9` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc9 |
| 12 | `Desc10` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc10 |
| 13 | `Desc11` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc11 |
| 14 | `Desc12` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc12 |
| 15 | `Desc13` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc13 |
| 16 | `Desc14` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc14 |
| 17 | `Desc15` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc15 |
| 18 | `Desc16` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc16 |
| 19 | `Desc17` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc17 |
| 20 | `Desc18` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc18 |
| 21 | `Desc19` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc19 |
| 22 | `Desc20` | `WCHAR(40.0)` | Yes |  | Text attribute: Desc20 |
| 23 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 24 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 25 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 26 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 27 | `Desc1SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Desc1SL |
| 28 | `Desc2SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Desc2SL |
| 29 | `Desc3SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Desc3SL |
| 30 | `Desc4SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Desc4SL |

---

<a name="table-itemparamdet"></a>

### Table: `ItemParamDet`

> **Purpose:** Parameterized stock attributes (Size, Color, Shade, Grade, Batch) for fashion/apparel/tile inventory.

- **Row Count in Active FY:** `0`
- **Total Columns:** `42`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 2 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 3 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 4 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 5 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 6 | `VchItemSN` | `SMALLINT` | Yes |  | Integer identifier or enum code for VchItemSN |
| 7 | `ItemCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Inventory Item) |
| 8 | `MCCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for MCCode |
| 9 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 10 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 11 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 12 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 13 | `C1` | `WCHAR(20.0)` | Yes |  | Text attribute: C1 |
| 14 | `C2` | `WCHAR(20.0)` | Yes |  | Text attribute: C2 |
| 15 | `C3` | `WCHAR(20.0)` | Yes |  | Text attribute: C3 |
| 16 | `C4` | `WCHAR(20.0)` | Yes |  | Text attribute: C4 |
| 17 | `C5` | `WCHAR(20.0)` | Yes |  | Text attribute: C5 |
| 18 | `C6` | `WCHAR(20.0)` | Yes |  | Text attribute: C6 |
| 19 | `C7` | `WCHAR(20.0)` | Yes |  | Text attribute: C7 |
| 20 | `C8` | `WCHAR(20.0)` | Yes |  | Text attribute: C8 |
| 21 | `C9` | `WCHAR(20.0)` | Yes |  | Text attribute: C9 |
| 22 | `C10` | `WCHAR(20.0)` | Yes |  | Text attribute: C10 |
| 23 | `C11` | `WCHAR(255.0)` | Yes |  | Text attribute: C11 |
| 24 | `C12` | `WCHAR(255.0)` | Yes |  | Text attribute: C12 |
| 25 | `C13` | `WCHAR(255.0)` | Yes |  | Text attribute: C13 |
| 26 | `Value1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value1 |
| 27 | `Value2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value2 |
| 28 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 29 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 30 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 31 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 32 | `D5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D5 |
| 33 | `D6` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D6 |
| 34 | `D7` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D7 |
| 35 | `D8` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D8 |
| 36 | `D9` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D9 |
| 37 | `D10` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D10 |
| 38 | `D11` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D11 |
| 39 | `BCN` | `WCHAR(40.0)` | Yes |  | Text attribute: BCN |
| 40 | `AutoBCN` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for AutoBCN |
| 41 | `OrgDate` | `DATETIME` | Yes |  | Timestamp / Date field for OrgDate |
| 42 | `OrgVchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for OrgVchCode |

---

<a name="table-itemserialno"></a>

### Table: `ItemSerialNo`

> **Purpose:** Unique serial numbers / IMEI tracking for discrete inventory items with stock status (In Stock, Sold, Returned).

- **Row Count in Active FY:** `0`
- **Total Columns:** `28`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 3 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 4 | `VchItemSN` | `SMALLINT` | Yes |  | Integer identifier or enum code for VchItemSN |
| 5 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 6 | `ItemCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Inventory Item) |
| 7 | `MCCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for MCCode |
| 8 | `GridSN` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for GridSN |
| 9 | `SerialNo` | `WCHAR(255.0)` | Yes |  | Text attribute: SerialNo |
| 10 | `AutoSrNo` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for AutoSrNo |
| 11 | `Value1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value1 |
| 12 | `Value2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value2 |
| 13 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 14 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 15 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 16 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 17 | `MonthVal` | `SMALLINT` | Yes |  | Integer identifier or enum code for MonthVal |
| 18 | `C1` | `WCHAR(40.0)` | Yes |  | Text attribute: C1 |
| 19 | `C2` | `WCHAR(40.0)` | Yes |  | Text attribute: C2 |
| 20 | `C3` | `WCHAR(40.0)` | Yes |  | Text attribute: C3 |
| 21 | `C4` | `WCHAR(40.0)` | Yes |  | Text attribute: C4 |
| 22 | `C5` | `WCHAR(40.0)` | Yes |  | Text attribute: C5 |
| 23 | `C6` | `WCHAR(40.0)` | Yes |  | Text attribute: C6 |
| 24 | `C7` | `WCHAR(40.0)` | Yes |  | Text attribute: C7 |
| 25 | `C8` | `WCHAR(40.0)` | Yes |  | Text attribute: C8 |
| 26 | `C9` | `WCHAR(40.0)` | Yes |  | Text attribute: C9 |
| 27 | `C10` | `WCHAR(40.0)` | Yes |  | Text attribute: C10 |
| 28 | `WarrantyMonth` | `SMALLINT` | Yes |  | Integer identifier or enum code for WarrantyMonth |

---

<a name="table-itemsninstalldet"></a>

### Table: `ItemSNInstallDet`

> **Purpose:** Installation, commissioning, and warranty details linked to serialized equipment and appliances.

- **Row Count in Active FY:** `0`
- **Total Columns:** `23`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `InstallCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for InstallCode |
| 2 | `InstallDate` | `DATETIME` | Yes |  | Timestamp / Date field for InstallDate |
| 3 | `ItemCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Inventory Item) |
| 4 | `SerialNo` | `WCHAR(255.0)` | Yes |  | Text attribute: SerialNo |
| 5 | `InvoiceNo` | `WCHAR(25.0)` | Yes |  | Text attribute: InvoiceNo |
| 6 | `InvoiceDate` | `DATETIME` | Yes |  | Timestamp / Date field for InvoiceDate |
| 7 | `PartyCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Customer or Vendor Party) |
| 8 | `Organization` | `WCHAR(40.0)` | Yes |  | Text attribute: Organization |
| 9 | `TradeDesc` | `WCHAR(40.0)` | Yes |  | Text attribute: TradeDesc |
| 10 | `ContactPerson` | `WCHAR(40.0)` | Yes |  | Text attribute: ContactPerson |
| 11 | `Designation` | `WCHAR(40.0)` | Yes |  | Text attribute: Designation |
| 12 | `Address1` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 13 | `Address2` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 14 | `CountryCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for CountryCode |
| 15 | `StateCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for StateCode |
| 16 | `CityCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for CityCode |
| 17 | `PinCode` | `WCHAR(10.0)` | Yes |  | Text attribute: PinCode |
| 18 | `MobileNo` | `WCHAR(40.0)` | Yes |  | Primary contact mobile telephone number |
| 19 | `PhoneNo` | `WCHAR(40.0)` | Yes |  | Text attribute: PhoneNo |
| 20 | `FaxNo` | `WCHAR(40.0)` | Yes |  | Text attribute: FaxNo |
| 21 | `EmailID` | `WCHAR(40.0)` | Yes |  | Text attribute: EmailID |
| 22 | `Narration` | `WCHAR(94.0)` | Yes |  | Text attribute: Narration |
| 23 | `WarrMonth` | `SMALLINT` | Yes |  | Integer identifier or enum code for WarrMonth |

---

<a name="table-folio1"></a>

### Table: `Folio1`

> **Purpose:** Fast financial and stock balance summary cache storing opening balances, monthly debits/credits, and closing balances for instantaneous report rendering without scanning raw transactions.

- **Row Count in Active FY:** `276`
- **Total Columns:** `164`
- **Primary Key:** `MasterCode`

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `MasterCode` | `INTEGER (Long)` | Yes | **PK** | Integer identifier or enum code for MasterCode |
| 2 | `MasterType` | `SMALLINT` | Yes |  | Polymorphic Entity Type enum (1=AccountGroup, 2=Account, 6=Item, 8=Unit, 9=BillSundry, 21=TaxCategory) |
| 3 | `D1` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D1 |
| 4 | `D2` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D2 |
| 5 | `D3` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D3 |
| 6 | `D4` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D4 |
| 7 | `D5` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D5 |
| 8 | `D6` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D6 |
| 9 | `D7` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D7 |
| 10 | `D8` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D8 |
| 11 | `D9` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D9 |
| 12 | `D10` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D10 |
| 13 | `D11` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D11 |
| 14 | `D12` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D12 |
| 15 | `D13` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D13 |
| 16 | `D14` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D14 |
| 17 | `D15` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D15 |
| 18 | `D16` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D16 |
| 19 | `D17` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D17 |
| 20 | `D18` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D18 |
| 21 | `D19` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D19 |
| 22 | `D20` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D20 |
| 23 | `D21` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D21 |
| 24 | `D22` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D22 |
| 25 | `D23` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D23 |
| 26 | `D24` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D24 |
| 27 | `D25` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D25 |
| 28 | `D26` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D26 |
| 29 | `D27` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D27 |
| 30 | `D28` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D28 |
| 31 | `D29` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D29 |
| 32 | `D30` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D30 |
| 33 | `D31` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D31 |
| 34 | `D32` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D32 |
| 35 | `D33` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D33 |
| 36 | `D34` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D34 |
| 37 | `D35` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D35 |
| 38 | `D36` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D36 |
| 39 | `D37` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D37 |
| 40 | `D38` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D38 |
| 41 | `D39` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D39 |
| 42 | `D40` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D40 |
| 43 | `D41` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D41 |
| 44 | `D42` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D42 |
| 45 | `D43` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D43 |
| 46 | `D44` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D44 |
| 47 | `D45` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D45 |
| 48 | `D46` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D46 |
| 49 | `D47` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D47 |
| 50 | `D48` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D48 |
| 51 | `D49` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D49 |
| 52 | `D50` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D50 |
| 53 | `D51` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D51 |
| 54 | `D52` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D52 |
| 55 | `D53` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D53 |
| 56 | `D54` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D54 |
| 57 | `D55` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D55 |
| 58 | `D56` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D56 |
| 59 | `D57` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D57 |
| 60 | `D58` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D58 |
| 61 | `D59` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D59 |
| 62 | `D60` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D60 |
| 63 | `D61` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D61 |
| 64 | `D62` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D62 |
| 65 | `D63` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D63 |
| 66 | `D64` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D64 |
| 67 | `D65` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D65 |
| 68 | `D66` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D66 |
| 69 | `D67` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D67 |
| 70 | `D68` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D68 |
| 71 | `D69` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D69 |
| 72 | `D70` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D70 |
| 73 | `D71` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D71 |
| 74 | `D72` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D72 |
| 75 | `D73` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D73 |
| 76 | `D74` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D74 |
| 77 | `D75` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D75 |
| 78 | `D76` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D76 |
| 79 | `D77` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D77 |
| 80 | `D78` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D78 |
| 81 | `D79` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D79 |
| 82 | `D80` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D80 |
| 83 | `D81` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D81 |
| 84 | `D82` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D82 |
| 85 | `D83` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D83 |
| 86 | `D84` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D84 |
| 87 | `D85` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D85 |
| 88 | `D86` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D86 |
| 89 | `D87` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D87 |
| 90 | `D88` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D88 |
| 91 | `D89` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D89 |
| 92 | `D90` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D90 |
| 93 | `D91` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D91 |
| 94 | `D92` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D92 |
| 95 | `D93` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D93 |
| 96 | `D94` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D94 |
| 97 | `D95` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D95 |
| 98 | `D96` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D96 |
| 99 | `D97` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D97 |
| 100 | `D98` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D98 |
| 101 | `D99` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D99 |
| 102 | `D100` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D100 |
| 103 | `D101` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D101 |
| 104 | `D102` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D102 |
| 105 | `D103` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D103 |
| 106 | `D104` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D104 |
| 107 | `D105` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D105 |
| 108 | `D106` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D106 |
| 109 | `D107` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D107 |
| 110 | `D108` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D108 |
| 111 | `D109` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D109 |
| 112 | `D110` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D110 |
| 113 | `D111` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D111 |
| 114 | `D112` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D112 |
| 115 | `D113` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D113 |
| 116 | `D114` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D114 |
| 117 | `D115` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D115 |
| 118 | `D116` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D116 |
| 119 | `D117` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D117 |
| 120 | `D118` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D118 |
| 121 | `D119` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D119 |
| 122 | `D120` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D120 |
| 123 | `D121` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D121 |
| 124 | `D122` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D122 |
| 125 | `D123` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D123 |
| 126 | `D124` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D124 |
| 127 | `D125` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D125 |
| 128 | `D126` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D126 |
| 129 | `D127` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D127 |
| 130 | `D128` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D128 |
| 131 | `D129` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D129 |
| 132 | `D130` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D130 |
| 133 | `D131` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D131 |
| 134 | `D132` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D132 |
| 135 | `D133` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D133 |
| 136 | `D134` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D134 |
| 137 | `D135` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D135 |
| 138 | `D136` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D136 |
| 139 | `D137` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D137 |
| 140 | `D138` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D138 |
| 141 | `D139` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D139 |
| 142 | `D140` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D140 |
| 143 | `D141` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D141 |
| 144 | `D142` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D142 |
| 145 | `D143` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D143 |
| 146 | `D144` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D144 |
| 147 | `D145` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D145 |
| 148 | `D146` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D146 |
| 149 | `D147` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D147 |
| 150 | `D148` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D148 |
| 151 | `D149` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D149 |
| 152 | `D150` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D150 |
| 153 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 154 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 155 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 156 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 157 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 158 | `B6` | `BOOLEAN` | No |  | Boolean flag for B6 (True/False) |
| 159 | `B7` | `BOOLEAN` | No |  | Boolean flag for B7 (True/False) |
| 160 | `B8` | `BOOLEAN` | No |  | Boolean flag for B8 (True/False) |
| 161 | `B9` | `BOOLEAN` | No |  | Boolean flag for B9 (True/False) |
| 162 | `B10` | `BOOLEAN` | No |  | Boolean flag for B10 (True/False) |
| 163 | `B11` | `BOOLEAN` | No |  | Boolean flag for B11 (True/False) |
| 164 | `B12` | `BOOLEAN` | No |  | Boolean flag for B12 (True/False) |

---

<a name="table-help1"></a>

### Table: `Help1`

> **Purpose:** High-speed auto-complete search cache indexing master names, aliases, and parent groups for UI dropdown lookups.

- **Row Count in Active FY:** `1065`
- **Total Columns:** `14`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 2 | `NameAlias` | `WCHAR(40.0)` | Yes |  | Text attribute: NameAlias |
| 3 | `Code` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for Code |
| 4 | `MasterType` | `SMALLINT` | Yes |  | Polymorphic Entity Type enum (1=AccountGroup, 2=Account, 6=Item, 8=Unit, 9=BillSundry, 21=TaxCategory) |
| 5 | `NameOrAlias` | `SMALLINT` | Yes |  | Integer identifier or enum code for NameOrAlias |
| 6 | `AdditionalInfo` | `WCHAR(255.0)` | Yes |  | Text attribute: AdditionalInfo |
| 7 | `ParentGroup` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for ParentGroup |
| 8 | `MasterSeries` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for MasterSeries |
| 9 | `Status` | `SMALLINT` | Yes |  | Integer identifier or enum code for Status |
| 10 | `DefaultMCCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for DefaultMCCode |
| 11 | `AddnInfoBt1` | `WCHAR(255.0)` | Yes |  | Text attribute: AddnInfoBt1 |
| 12 | `AddnInfoBt2` | `WCHAR(255.0)` | Yes |  | Text attribute: AddnInfoBt2 |
| 13 | `AddnInfoBt3` | `WCHAR(255.0)` | Yes |  | Text attribute: AddnInfoBt3 |
| 14 | `AddnInfoBt4` | `WCHAR(255.0)` | Yes |  | Text attribute: AddnInfoBt4 |

---

<a name="table-help1addninfo"></a>

### Table: `Help1AddnInfo`

> **Purpose:** Secondary keyword index and alias search phrases supporting Help1 search acceleration.

- **Row Count in Active FY:** `109`
- **Total Columns:** `7`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Code` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for Code |
| 2 | `NameAlias` | `WCHAR(40.0)` | Yes |  | Text attribute: NameAlias |
| 3 | `NameOrAlias` | `SMALLINT` | Yes |  | Integer identifier or enum code for NameOrAlias |
| 4 | `AddnInfoBt1` | `WCHAR(255.0)` | Yes |  | Text attribute: AddnInfoBt1 |
| 5 | `AddnInfoBt2` | `WCHAR(255.0)` | Yes |  | Text attribute: AddnInfoBt2 |
| 6 | `AddnInfoBt3` | `WCHAR(255.0)` | Yes |  | Text attribute: AddnInfoBt3 |
| 7 | `AddnInfoBt4` | `WCHAR(255.0)` | Yes |  | Text attribute: AddnInfoBt4 |

---

<a name="table-help2"></a>

### Table: `Help2`

> **Purpose:** Lookup index for sub-entities, material centers (godowns), and cost centers.

- **Row Count in Active FY:** `6`
- **Total Columns:** `4`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType1` | `SMALLINT` | Yes |  | Integer identifier or enum code for RecType1 |
| 2 | `RecType2` | `SMALLINT` | Yes |  | Integer identifier or enum code for RecType2 |
| 3 | `RecType3` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for RecType3 |
| 4 | `Name` | `WCHAR(255.0)` | Yes |  | Text attribute: Name |

---

<a name="table-deletedmasters"></a>

### Table: `DeletedMasters`

> **Purpose:** Audit tombstone register of deleted master entities preventing ID collision and maintaining audit integrity.

- **Row Count in Active FY:** `0`
- **Total Columns:** `2`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `MasterType` | `SMALLINT` | Yes |  | Polymorphic Entity Type enum (1=AccountGroup, 2=Account, 6=Item, 8=Unit, 9=BillSundry, 21=TaxCategory) |
| 2 | `Name` | `WCHAR(40.0)` | Yes |  | Text attribute: Name |

---

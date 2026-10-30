# BusyWin FY Database: Transactions & Vouchers Schemas

> **Database File:** `db1<YYYY>.bds` (e.g. `C:\BusyWin\DATA\COMP0001\db12026.bds`)

> **Engine:** Microsoft Jet 4.0 / Access OLEDB (`ILoveMyINDIA`)

> **Description:** Detailed table schemas and column definitions for all Voucher headers, Line items, Sundries, and Inventory journals in db1YYYY.bds.


## Tables in this Module


| # | Table Name | Columns | Active Rows | Primary Key | Description |
|---|------------|:-------:|:-----------:|:-----------:|-------------|
| 1 | [`Tran1`](#table-tran1) | 117 | 12 | `VchCode` | Voucher header table recording transaction type (Sales, Purchase, Payment, Receipt), invoice number, date, party foreign key, net/gross amounts, cancellation flag, and voucher series. |
| 2 | [`Tran2`](#table-tran2) | 104 | 73 | `-` | Double-entry transaction line items recording both inventory line items (ItemCode, Quantity, Rate, Amount) AND financial ledger debit/credit postings. |
| 3 | [`Tran3`](#table-tran3) | 33 | 0 | `-` | Bill sundry line items attached to vouchers (Freight, Packing, Insurance, Trade Discount, Round Off). |
| 4 | [`Tran4`](#table-tran4) | 8 | 10 | `-` | Material center / Godown stock ledger tracking location-level inventory additions and deductions. |
| 5 | [`Tran5`](#table-tran5) | 16 | 0 | `-` | Serial number and batch allocations linked to line items in sales and purchase vouchers. |
| 6 | [`Tran6`](#table-tran6) | 7 | 0 | `-` | Job work / process manufacturing ledger tracking raw material issued versus finished goods received. |
| 7 | [`Tran7`](#table-tran7) | 1 | 0 | `-` | Cost center and project-level expense/revenue allocation records. |
| 8 | [`Tran8`](#table-tran8) | 19 | 0 | `VchCode` | Pre-GST statutory sales tax / VAT declaration forms tracking (Form C, Form F, Form H, Form E1/E2). |
| 9 | [`Tran9`](#table-tran9) | 9 | 0 | `-` | Statutory form receipt and issuance settlement against individual sales and purchase bills. |
| 10 | [`Tran10`](#table-tran10) | 35 | 0 | `-` | Order processing linkage tracking Sales Order and Purchase Order commitments and pending delivery balances. |
| 11 | [`Tran11`](#table-tran11) | 31 | 0 | `-` | Delivery Challan and Goods Receipt Note (GRN) linkage to final sales/purchase invoices. |
| 12 | [`Tran12`](#table-tran12) | 4 | 0 | `-` | Voucher print audit log recording print count, user identity, and print timestamps. |
| 13 | [`BillingDet`](#table-billingdet) | 31 | 12 | `-` | Consignee / Ship-to party name, dispatch address, destination state, GSTIN, transporter, and vehicle details. |
| 14 | [`VchOtherInfo`](#table-vchotherinfo) | 61 | 12 | `-` | Voucher optional user-defined fields (transporter, vehicle number, GR/LR number, payment terms, delivery date). |
| 15 | [`DailySum`](#table-dailysum) | 14 | 45 | `-` | Daily financial and inventory aggregation cache for fast day-book and ledger rendering. |
| 16 | [`DailyMessage`](#table-dailymessage) | 8 | 0 | `-` | Automated notification and payment reminder messages scheduled on specific voucher due dates. |
| 17 | [`BRSOpBal`](#table-brsopbal) | 12 | 0 | `-` | Bank Reconciliation Statement (BRS) opening uncleared cheque balances carried forward from previous period. |
| 18 | [`OrgSalePurc`](#table-orgsalepurc) | 8 | 0 | `-` | Original invoice references for Credit Notes and Debit Notes (original invoice no, date, taxable value). |
| 19 | [`POSDet`](#table-posdet) | 17 | 0 | `-` | Point of Sale (POS) multi-tender payment breakdown (Cash, Credit/Debit Card, UPI, Cheque, Gift Voucher). |
| 20 | [`PackingDetails`](#table-packingdetails) | 12 | 0 | `-` | Packing slip and consignment details (box number, gross weight, net weight, dimensions, packaging unit). |
| 21 | [`JobFinishedRefs`](#table-jobfinishedrefs) | 18 | 0 | `-` | Finished goods batch reference generated from Bill of Materials (BOM) in production vouchers. |
| 22 | [`PhyStkSubDet`](#table-phystksubdet) | 39 | 0 | `-` | Physical stock verification audit lines recording counted physical quantity versus book balance variance. |
| 23 | [`VchTemplate`](#table-vchtemplate) | 2 | 0 | `-` | Reusable transaction templates for recurring monthly vouchers (Rent, Salaries, Subscriptions). |
| 24 | [`VchTempTagging`](#table-vchtemptagging) | 11 | 0 | `-` | Tagging rules and schedules linking vouchers to specific transaction templates. |

---

## Detailed Column Schemas


<a name="table-tran1"></a>

### Table: `Tran1`

> **Purpose:** Voucher header table recording transaction type (Sales, Purchase, Payment, Receipt), invoice number, date, party foreign key, net/gross amounts, cancellation flag, and voucher series.

- **Row Count in Active FY:** `12`
- **Total Columns:** `117`
- **Primary Key:** `VchCode`

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes | **PK** | Unique Voucher Transaction ID (Primary Key in Tran1, Foreign Key in others) |
| 2 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 3 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 4 | `StockUpdationDate` | `DATETIME` | Yes |  | Timestamp / Date field for StockUpdationDate |
| 5 | `Status` | `SMALLINT` | Yes |  | Integer identifier or enum code for Status |
| 6 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 7 | `VchSeriesCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchSeriesCode |
| 8 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 9 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 10 | `Stamp` | `INTEGER (Long)` | Yes |  | Internal concurrency timestamp / modification revision stamp |
| 11 | `AutoVchNo` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for AutoVchNo |
| 12 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 13 | `CM2` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM2 (links to Master1.Code based on MasterType) |
| 14 | `CM3` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM3 (links to Master1.Code based on MasterType) |
| 15 | `CM4` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM4 (links to Master1.Code based on MasterType) |
| 16 | `CM5` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM5 (links to Master1.Code based on MasterType) |
| 17 | `CM6` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM6 (links to Master1.Code based on MasterType) |
| 18 | `FormRecAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for FormRecAmt |
| 19 | `FormIssAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for FormIssAmt |
| 20 | `CurConRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CurConRate |
| 21 | `VchAmtBaseCur` | `DOUBLE` | Yes |  | Gross invoice total payable in company base currency |
| 22 | `VchSalePurcAmt` | `DOUBLE` | Yes |  | Net taxable invoice total before bill sundries |
| 23 | `ExciseApplicable` | `BOOLEAN` | No |  | Boolean flag for ExciseApplicable (True/False) |
| 24 | `ExciseDocName` | `WCHAR(20.0)` | Yes |  | Text attribute: ExciseDocName |
| 25 | `ExciseValue` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ExciseValue |
| 26 | `ExciseType` | `SMALLINT` | Yes |  | Integer identifier or enum code for ExciseType |
| 27 | `ExcisableAmount` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ExcisableAmount |
| 28 | `ExciseRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ExciseRate |
| 29 | `OrgVchAmtBaseCur` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for OrgVchAmtBaseCur |
| 30 | `TEApplicable` | `BOOLEAN` | No |  | Boolean flag for TEApplicable (True/False) |
| 31 | `TDSApplicable` | `BOOLEAN` | No |  | Boolean flag for TDSApplicable (True/False) |
| 32 | `FormRecStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for FormRecStatus |
| 33 | `FormIssStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for FormIssStatus |
| 34 | `ChallanStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for ChallanStatus |
| 35 | `STApplicable` | `BOOLEAN` | No |  | Boolean flag for STApplicable (True/False) |
| 36 | `STType` | `SMALLINT` | Yes |  | Integer identifier or enum code for STType |
| 37 | `DocPrinted` | `BOOLEAN` | No |  | Boolean flag for DocPrinted (True/False) |
| 38 | `External` | `BOOLEAN` | No |  | Boolean flag for External (True/False) |
| 39 | `CreatedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: CreatedBy |
| 40 | `CreationTime` | `DATETIME` | Yes |  | Timestamp / Date field for CreationTime |
| 41 | `AuthorisedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: AuthorisedBy |
| 42 | `AuthorisationTime` | `DATETIME` | Yes |  | Timestamp / Date field for AuthorisationTime |
| 43 | `ModifiedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: ModifiedBy |
| 44 | `ModificationTime` | `DATETIME` | Yes |  | Timestamp / Date field for ModificationTime |
| 45 | `PriceCategory` | `SMALLINT` | Yes |  | Integer identifier or enum code for PriceCategory |
| 46 | `VATInfo` | `BOOLEAN` | No |  | Boolean flag for VATInfo (True/False) |
| 47 | `POSEnabled` | `BOOLEAN` | No |  | Boolean flag for POSEnabled (True/False) |
| 48 | `AutoGeneratedType` | `SMALLINT` | Yes |  | Integer identifier or enum code for AutoGeneratedType |
| 49 | `VchCancelled` | `BOOLEAN` | No |  | Boolean flag indicating whether voucher was cancelled (1=Cancelled) |
| 50 | `BrokerageMode` | `SMALLINT` | Yes |  | Integer identifier or enum code for BrokerageMode |
| 51 | `Brokerage` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Brokerage |
| 52 | `BrokerageAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for BrokerageAmt |
| 53 | `TranType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TranType |
| 54 | `FreeQtyUsed` | `BOOLEAN` | No |  | Boolean flag for FreeQtyUsed (True/False) |
| 55 | `Cancelled` | `BOOLEAN` | No |  | Boolean flag for Cancelled (True/False) |
| 56 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 57 | `ApprovalStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for ApprovalStatus |
| 58 | `SyncStatus` | `BOOLEAN` | No |  | Boolean flag for SyncStatus (True/False) |
| 59 | `Source` | `SMALLINT` | Yes |  | Integer identifier or enum code for Source |
| 60 | `AuditStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for AuditStatus |
| 61 | `ExtraExpense` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ExtraExpense |
| 62 | `ExtraExpenseNar1` | `WCHAR(40.0)` | Yes |  | Text attribute: ExtraExpenseNar1 |
| 63 | `ExtraExpenseNar2` | `WCHAR(40.0)` | Yes |  | Text attribute: ExtraExpenseNar2 |
| 64 | `c1` | `WCHAR(255.0)` | Yes |  | Text attribute: c1 |
| 65 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 66 | `Date2` | `DATETIME` | Yes |  | Timestamp / Date field for Date2 |
| 67 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 68 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 69 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 70 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 71 | `I5` | `SMALLINT` | Yes |  | Integer identifier or enum code for I5 |
| 72 | `I6` | `SMALLINT` | Yes |  | Integer identifier or enum code for I6 |
| 73 | `I7` | `SMALLINT` | Yes |  | Integer identifier or enum code for I7 |
| 74 | `I8` | `SMALLINT` | Yes |  | Integer identifier or enum code for I8 |
| 75 | `I9` | `SMALLINT` | Yes |  | Integer identifier or enum code for I9 |
| 76 | `I10` | `SMALLINT` | Yes |  | Integer identifier or enum code for I10 |
| 77 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 78 | `TPF1` | `BOOLEAN` | No |  | Boolean flag for TPF1 (True/False) |
| 79 | `TPF2` | `BOOLEAN` | No |  | Boolean flag for TPF2 (True/False) |
| 80 | `RejectionStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for RejectionStatus |
| 81 | `L1` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L1 |
| 82 | `SourceDet` | `WCHAR(255.0)` | Yes |  | Text attribute: SourceDet |
| 83 | `NepaliDate` | `WCHAR(255.0)` | Yes |  | Text attribute: NepaliDate |
| 84 | `NepaliFY` | `WCHAR(255.0)` | Yes |  | Text attribute: NepaliFY |
| 85 | `CM7` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM7 (links to Master1.Code based on MasterType) |
| 86 | `TCSApplicable` | `BOOLEAN` | No |  | Boolean flag for TCSApplicable (True/False) |
| 87 | `ReturnStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for ReturnStatus |
| 88 | `ReturnStatusAnnual` | `SMALLINT` | Yes |  | Integer identifier or enum code for ReturnStatusAnnual |
| 89 | `GSTInfo` | `BOOLEAN` | No |  | Boolean flag for GSTInfo (True/False) |
| 90 | `GSTRecType` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTRecType |
| 91 | `InputType` | `SMALLINT` | Yes |  | Integer identifier or enum code for InputType |
| 92 | `GSTRepBasis` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTRepBasis |
| 93 | `GSTR2Status` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTR2Status |
| 94 | `CheckSum` | `WCHAR(255.0)` | Yes |  | Text attribute: CheckSum |
| 95 | `SyncWithIRD` | `BOOLEAN` | No |  | Boolean flag for SyncWithIRD (True/False) |
| 96 | `IsRealtime` | `BOOLEAN` | No |  | Boolean flag for IsRealtime (True/False) |
| 97 | `ConsignmentType` | `SMALLINT` | Yes |  | Integer identifier or enum code for ConsignmentType |
| 98 | `ITCClaimedStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for ITCClaimedStatus |
| 99 | `ITCClaimedMonth` | `SMALLINT` | Yes |  | Integer identifier or enum code for ITCClaimedMonth |
| 100 | `EInvIRN` | `WCHAR(255.0)` | Yes |  | Text attribute: EInvIRN |
| 101 | `EInvAckNo` | `WCHAR(255.0)` | Yes |  | Text attribute: EInvAckNo |
| 102 | `EInvAckDate` | `DATETIME` | Yes |  | Timestamp / Date field for EInvAckDate |
| 103 | `EInvSignedQRCode` | `WCHAR` | Yes |  | Text attribute: EInvSignedQRCode |
| 104 | `EInvSignedInvoice` | `WCHAR` | Yes |  | Text attribute: EInvSignedInvoice |
| 105 | `EInvSignedInvoice2` | `WCHAR` | Yes |  | Text attribute: EInvSignedInvoice2 |
| 106 | `EInvSignedInvoice3` | `WCHAR` | Yes |  | Text attribute: EInvSignedInvoice3 |
| 107 | `EInvSignedInvoice4` | `WCHAR` | Yes |  | Text attribute: EInvSignedInvoice4 |
| 108 | `EInvSignedInvoice5` | `WCHAR` | Yes |  | Text attribute: EInvSignedInvoice5 |
| 109 | `SelfImageLink` | `WCHAR(255.0)` | Yes |  | Text attribute: SelfImageLink |
| 110 | `BusyDocLink` | `WCHAR(255.0)` | Yes |  | Text attribute: BusyDocLink |
| 111 | `SelfImageName` | `WCHAR(255.0)` | Yes |  | Text attribute: SelfImageName |
| 112 | `BusyDocName` | `WCHAR(255.0)` | Yes |  | Text attribute: BusyDocName |
| 113 | `GSTR2BStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTR2BStatus |
| 114 | `GSTR2BMonth` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTR2BMonth |
| 115 | `GSTR2BYear` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTR2BYear |
| 116 | `OldIdentity` | `WCHAR` | Yes |  | Text attribute: OldIdentity |
| 117 | `EcomOrderID` | `WCHAR(100.0)` | Yes |  | Text attribute: EcomOrderID |

---

<a name="table-tran2"></a>

### Table: `Tran2`

> **Purpose:** Double-entry transaction line items recording both inventory line items (ItemCode, Quantity, Rate, Amount) AND financial ledger debit/credit postings.

- **Row Count in Active FY:** `73`
- **Total Columns:** `104`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 2 | `VchCode` | `INTEGER (Long)` | Yes |  | Unique Voucher Transaction ID (Primary Key in Tran1, Foreign Key in others) |
| 3 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 4 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 5 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 6 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 7 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 8 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 9 | `VchSeriesCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchSeriesCode |
| 10 | `Value1` | `DOUBLE` | Yes |  | Item Quantity (for inventory lines) or Ledger Debit Amount |
| 11 | `Value2` | `DOUBLE` | Yes |  | Unit Price / Rate per unit |
| 12 | `Value3` | `DOUBLE` | Yes |  | Total item line amount (Quantity * Rate) before taxes |
| 13 | `Balance1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance1 |
| 14 | `Balance2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance2 |
| 15 | `Balance3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance3 |
| 16 | `ItemBal1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ItemBal1 |
| 17 | `ItemBal2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ItemBal2 |
| 18 | `ItemBal3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ItemBal3 |
| 19 | `CashFlow` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CashFlow |
| 20 | `ShortNar` | `WCHAR(40.0)` | Yes |  | Brief line-item narration or ledger remark |
| 21 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 22 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 23 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 24 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 25 | `D5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D5 |
| 26 | `D6` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D6 |
| 27 | `D7` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D7 |
| 28 | `D8` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D8 |
| 29 | `D9` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D9 |
| 30 | `D10` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D10 |
| 31 | `D11` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D11 |
| 32 | `D12` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D12 |
| 33 | `D13` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D13 |
| 34 | `D14` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D14 |
| 35 | `D15` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D15 |
| 36 | `D16` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D16 |
| 37 | `D17` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D17 |
| 38 | `D18` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D18 |
| 39 | `D19` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D19 |
| 40 | `D20` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D20 |
| 41 | `D21` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D21 |
| 42 | `D22` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D22 |
| 43 | `D23` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D23 |
| 44 | `D24` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D24 |
| 45 | `D25` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D25 |
| 46 | `D26` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D26 |
| 47 | `D27` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D27 |
| 48 | `D28` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D28 |
| 49 | `D29` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D29 |
| 50 | `D30` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D30 |
| 51 | `D31` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D31 |
| 52 | `D32` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D32 |
| 53 | `D33` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D33 |
| 54 | `D34` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D34 |
| 55 | `D35` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D35 |
| 56 | `D36` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D36 |
| 57 | `D37` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D37 |
| 58 | `D38` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D38 |
| 59 | `D39` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D39 |
| 60 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 61 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 62 | `CM2` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM2 (links to Master1.Code based on MasterType) |
| 63 | `CM3` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM3 (links to Master1.Code based on MasterType) |
| 64 | `CM4` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM4 (links to Master1.Code based on MasterType) |
| 65 | `CM5` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM5 (links to Master1.Code based on MasterType) |
| 66 | `CM6` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM6 (links to Master1.Code based on MasterType) |
| 67 | `CM7` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM7 (links to Master1.Code based on MasterType) |
| 68 | `CM8` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM8 (links to Master1.Code based on MasterType) |
| 69 | `CM9` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM9 (links to Master1.Code based on MasterType) |
| 70 | `CM10` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM10 (links to Master1.Code based on MasterType) |
| 71 | `CM11` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM11 (links to Master1.Code based on MasterType) |
| 72 | `CM12` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM12 (links to Master1.Code based on MasterType) |
| 73 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 74 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 75 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 76 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 77 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 78 | `B6` | `BOOLEAN` | No |  | Boolean flag for B6 (True/False) |
| 79 | `B7` | `BOOLEAN` | No |  | Boolean flag for B7 (True/False) |
| 80 | `B8` | `BOOLEAN` | No |  | Boolean flag for B8 (True/False) |
| 81 | `ClrDate` | `DATETIME` | Yes |  | Timestamp / Date field for ClrDate |
| 82 | `PriceCategory` | `SMALLINT` | Yes |  | Integer identifier or enum code for PriceCategory |
| 83 | `CFMode` | `SMALLINT` | Yes |  | Integer identifier or enum code for CFMode |
| 84 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 85 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 86 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 87 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 88 | `TranType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TranType |
| 89 | `IsReturnQty` | `BOOLEAN` | No |  | Boolean flag for IsReturnQty (True/False) |
| 90 | `ReconStatus` | `BOOLEAN` | No |  | Boolean flag for ReconStatus (True/False) |
| 91 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 92 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 93 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 94 | `I5` | `SMALLINT` | Yes |  | Integer identifier or enum code for I5 |
| 95 | `I6` | `SMALLINT` | Yes |  | Integer identifier or enum code for I6 |
| 96 | `I7` | `SMALLINT` | Yes |  | Integer identifier or enum code for I7 |
| 97 | `I8` | `SMALLINT` | Yes |  | Integer identifier or enum code for I8 |
| 98 | `I9` | `SMALLINT` | Yes |  | Integer identifier or enum code for I9 |
| 99 | `I10` | `SMALLINT` | Yes |  | Integer identifier or enum code for I10 |
| 100 | `TrackingStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for TrackingStatus |
| 101 | `TrackingNo` | `WCHAR(255.0)` | Yes |  | Text attribute: TrackingNo |
| 102 | `ConsignmentType` | `SMALLINT` | Yes |  | Integer identifier or enum code for ConsignmentType |
| 103 | `ConsignmentCleared` | `BOOLEAN` | No |  | Boolean flag for ConsignmentCleared (True/False) |
| 104 | `EcomOrderItemID` | `WCHAR(100.0)` | Yes |  | Text attribute: EcomOrderItemID |

---

<a name="table-tran3"></a>

### Table: `Tran3`

> **Purpose:** Bill sundry line items attached to vouchers (Freight, Packing, Insurance, Trade Discount, Round Off).

- **Row Count in Active FY:** `0`
- **Total Columns:** `33`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RefCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for RefCode |
| 2 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 3 | `Method` | `SMALLINT` | Yes |  | Integer identifier or enum code for Method |
| 4 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 5 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 6 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 7 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 8 | `RefGrp` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for RefGrp |
| 9 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 10 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 11 | `DueDate` | `DATETIME` | Yes |  | Timestamp / Date field for DueDate |
| 12 | `No` | `WCHAR(25.0)` | Yes |  | Text attribute: No |
| 13 | `Status` | `SMALLINT` | Yes |  | Integer identifier or enum code for Status |
| 14 | `Type` | `SMALLINT` | Yes |  | Integer identifier or enum code for Type |
| 15 | `BrokerCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for BrokerCode |
| 16 | `Value1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value1 |
| 17 | `Value2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value2 |
| 18 | `Value3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value3 |
| 19 | `Balance1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance1 |
| 20 | `Balance2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance2 |
| 21 | `Balance3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance3 |
| 22 | `ItemSrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for ItemSrNo |
| 23 | `MfgDate` | `DATETIME` | Yes |  | Timestamp / Date field for MfgDate |
| 24 | `TranType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TranType |
| 25 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 26 | `CM2` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM2 (links to Master1.Code based on MasterType) |
| 27 | `CM3` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM3 (links to Master1.Code based on MasterType) |
| 28 | `ApprovalStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for ApprovalStatus |
| 29 | `NewRefAmount` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for NewRefAmount |
| 30 | `Narration` | `WCHAR(255.0)` | Yes |  | Text attribute: Narration |
| 31 | `BranchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for BranchCode |
| 32 | `NewRefVchType` | `SMALLINT` | Yes |  | Integer identifier or enum code for NewRefVchType |
| 33 | `NewRefVchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for NewRefVchCode |

---

<a name="table-tran4"></a>

### Table: `Tran4`

> **Purpose:** Material center / Godown stock ledger tracking location-level inventory additions and deductions.

- **Row Count in Active FY:** `10`
- **Total Columns:** `8`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `SrNo` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for SrNo |
| 2 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 3 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 4 | `D1` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D1 |
| 5 | `D2` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D2 |
| 6 | `D3` | `DOUBLE` | Yes |  | Pre-allocated double numeric parameter / balance accumulator D3 |
| 7 | `BranchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for BranchCode |
| 8 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |

---

<a name="table-tran5"></a>

### Table: `Tran5`

> **Purpose:** Serial number and batch allocations linked to line items in sales and purchase vouchers.

- **Row Count in Active FY:** `0`
- **Total Columns:** `16`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 3 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 4 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 5 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 6 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 7 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 8 | `VchSeriesCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchSeriesCode |
| 9 | `Value1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value1 |
| 10 | `Value2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value2 |
| 11 | `Balance1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance1 |
| 12 | `Balance2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance2 |
| 13 | `TranType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TranType |
| 14 | `ShortNar` | `WCHAR(40.0)` | Yes |  | Brief line-item narration or ledger remark |
| 15 | `TrackingNo` | `WCHAR(255.0)` | Yes |  | Text attribute: TrackingNo |
| 16 | `TrackingStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for TrackingStatus |

---

<a name="table-tran6"></a>

### Table: `Tran6`

> **Purpose:** Job work / process manufacturing ledger tracking raw material issued versus finished goods received.

- **Row Count in Active FY:** `0`
- **Total Columns:** `7`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `SrNo` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for SrNo |
| 2 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 3 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 4 | `StockType` | `SMALLINT` | Yes |  | Integer identifier or enum code for StockType |
| 5 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 6 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 7 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |

---

<a name="table-tran7"></a>

### Table: `Tran7`

> **Purpose:** Cost center and project-level expense/revenue allocation records.

- **Row Count in Active FY:** `0`
- **Total Columns:** `1`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `MasterCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for MasterCode |

---

<a name="table-tran8"></a>

### Table: `Tran8`

> **Purpose:** Pre-GST statutory sales tax / VAT declaration forms tracking (Form C, Form F, Form H, Form E1/E2).

- **Row Count in Active FY:** `0`
- **Total Columns:** `19`
- **Primary Key:** `VchCode`

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes | **PK** | Integer identifier or enum code for VchCode |
| 2 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 3 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 4 | `FormRecDate` | `DATETIME` | Yes |  | Timestamp / Date field for FormRecDate |
| 5 | `FormNo` | `WCHAR(25.0)` | Yes |  | Text attribute: FormNo |
| 6 | `PartyCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Customer or Vendor Party) |
| 7 | `FormCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for FormCode |
| 8 | `Stamp` | `INTEGER (Long)` | Yes |  | Internal concurrency timestamp / modification revision stamp |
| 9 | `Nar1` | `WCHAR(94.0)` | Yes |  | Voucher narration / remarks text |
| 10 | `AutoVchNo` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for AutoVchNo |
| 11 | `CreatedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: CreatedBy |
| 12 | `CreationTime` | `DATETIME` | Yes |  | Timestamp / Date field for CreationTime |
| 13 | `AuthorisedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: AuthorisedBy |
| 14 | `AuthorisationTime` | `DATETIME` | Yes |  | Timestamp / Date field for AuthorisationTime |
| 15 | `ModifiedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: ModifiedBy |
| 16 | `ModificationTime` | `DATETIME` | Yes |  | Timestamp / Date field for ModificationTime |
| 17 | `StateCode` | `SMALLINT` | Yes |  | Integer identifier or enum code for StateCode |
| 18 | `Series` | `WCHAR(255.0)` | Yes |  | Text attribute: Series |
| 19 | `IssuingOffice` | `WCHAR(255.0)` | Yes |  | Text attribute: IssuingOffice |

---

<a name="table-tran9"></a>

### Table: `Tran9`

> **Purpose:** Statutory form receipt and issuance settlement against individual sales and purchase bills.

- **Row Count in Active FY:** `0`
- **Total Columns:** `9`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `PartyCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Customer or Vendor Party) |
| 3 | `FormCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for FormCode |
| 4 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 5 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 6 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 7 | `FormNo` | `WCHAR(25.0)` | Yes |  | Text attribute: FormNo |
| 8 | `BillCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for BillCode |
| 9 | `Amount` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Amount |

---

<a name="table-tran10"></a>

### Table: `Tran10`

> **Purpose:** Order processing linkage tracking Sales Order and Purchase Order commitments and pending delivery balances.

- **Row Count in Active FY:** `0`
- **Total Columns:** `35`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 2 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 3 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 4 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 5 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 6 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 7 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 8 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 9 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 10 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 11 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 12 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 13 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 14 | `D5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D5 |
| 15 | `D6` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D6 |
| 16 | `D7` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D7 |
| 17 | `D8` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D8 |
| 18 | `D9` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D9 |
| 19 | `D10` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D10 |
| 20 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 21 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 22 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 23 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 24 | `C5` | `WCHAR(255.0)` | Yes |  | Text attribute: C5 |
| 25 | `C6` | `WCHAR(255.0)` | Yes |  | Text attribute: C6 |
| 26 | `C7` | `WCHAR(255.0)` | Yes |  | Text attribute: C7 |
| 27 | `C8` | `WCHAR(255.0)` | Yes |  | Text attribute: C8 |
| 28 | `C9` | `WCHAR(255.0)` | Yes |  | Text attribute: C9 |
| 29 | `C10` | `WCHAR(255.0)` | Yes |  | Text attribute: C10 |
| 30 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 31 | `MasterCode3` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for MasterCode3 |
| 32 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 33 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 34 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 35 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |

---

<a name="table-tran11"></a>

### Table: `Tran11`

> **Purpose:** Delivery Challan and Goods Receipt Note (GRN) linkage to final sales/purchase invoices.

- **Row Count in Active FY:** `0`
- **Total Columns:** `31`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 2 | `TranType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TranType |
| 3 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 4 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 5 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 6 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 7 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 8 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 9 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 10 | `VchSeriesCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchSeriesCode |
| 11 | `ShortNar` | `WCHAR(40.0)` | Yes |  | Brief line-item narration or ledger remark |
| 12 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 13 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 14 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 15 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 16 | `CM2` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM2 (links to Master1.Code based on MasterType) |
| 17 | `CM3` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM3 (links to Master1.Code based on MasterType) |
| 18 | `CM4` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM4 (links to Master1.Code based on MasterType) |
| 19 | `CM5` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM5 (links to Master1.Code based on MasterType) |
| 20 | `CM6` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM6 (links to Master1.Code based on MasterType) |
| 21 | `CM7` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM7 (links to Master1.Code based on MasterType) |
| 22 | `CM8` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM8 (links to Master1.Code based on MasterType) |
| 23 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 24 | `Date2` | `DATETIME` | Yes |  | Timestamp / Date field for Date2 |
| 25 | `Date3` | `DATETIME` | Yes |  | Timestamp / Date field for Date3 |
| 26 | `Date4` | `DATETIME` | Yes |  | Timestamp / Date field for Date4 |
| 27 | `Date5` | `DATETIME` | Yes |  | Timestamp / Date field for Date5 |
| 28 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 29 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 30 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |
| 31 | `M2` | `WCHAR` | Yes |  | Text attribute: M2 |

---

<a name="table-tran12"></a>

### Table: `Tran12`

> **Purpose:** Voucher print audit log recording print count, user identity, and print timestamps.

- **Row Count in Active FY:** `0`
- **Total Columns:** `4`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 3 | `UserName` | `WCHAR(40.0)` | Yes |  | Operator username who performed the action |
| 4 | `NoOfCopies` | `SMALLINT` | Yes |  | Integer identifier or enum code for NoOfCopies |

---

<a name="table-billingdet"></a>

### Table: `BillingDet`

> **Purpose:** Consignee / Ship-to party name, dispatch address, destination state, GSTIN, transporter, and vehicle details.

- **Row Count in Active FY:** `12`
- **Total Columns:** `31`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Unique Voucher Transaction ID (Primary Key in Tran1, Foreign Key in others) |
| 2 | `PartyName` | `WCHAR(60.0)` | Yes |  | Text attribute: PartyName |
| 3 | `Address1` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 4 | `Address2` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 5 | `Address3` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 6 | `Address4` | `WCHAR(40.0)` | Yes |  | Postal address line |
| 7 | `STNo` | `WCHAR(30.0)` | Yes |  | Text attribute: STNo |
| 8 | `CSTNo` | `WCHAR(30.0)` | Yes |  | Text attribute: CSTNo |
| 9 | `ECCCode` | `WCHAR(20.0)` | Yes |  | Text attribute: ECCCode |
| 10 | `ExciseRegNo` | `WCHAR(30.0)` | Yes |  | Text attribute: ExciseRegNo |
| 11 | `PLANo` | `WCHAR(20.0)` | Yes |  | Text attribute: PLANo |
| 12 | `Range` | `WCHAR(80.0)` | Yes |  | Text attribute: Range |
| 13 | `Division` | `WCHAR(80.0)` | Yes |  | Text attribute: Division |
| 14 | `Collectorate` | `WCHAR(40.0)` | Yes |  | Text attribute: Collectorate |
| 15 | `MobileNo` | `WCHAR(255.0)` | Yes |  | Primary contact mobile telephone number |
| 16 | `Email` | `WCHAR(255.0)` | Yes |  | Official email address for communication and e-invoicing |
| 17 | `DrugLicenceNo1` | `WCHAR(40.0)` | Yes |  | Text attribute: DrugLicenceNo1 |
| 18 | `DrugLicenceNo2` | `WCHAR(40.0)` | Yes |  | Text attribute: DrugLicenceNo2 |
| 19 | `ITPAN` | `WCHAR(20.0)` | Yes |  | Income Tax Permanent Account Number (PAN) |
| 20 | `StateCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for StateCode |
| 21 | `GSTNo` | `WCHAR(30.0)` | Yes |  | Text attribute: GSTNo |
| 22 | `TypeOfDealer` | `SMALLINT` | Yes |  | Integer identifier or enum code for TypeOfDealer |
| 23 | `AdharNo` | `WCHAR(255.0)` | Yes |  | Text attribute: AdharNo |
| 24 | `PartyNameSL` | `WCHAR(255.0)` | Yes |  | Text attribute: PartyNameSL |
| 25 | `Address1SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Address1SL |
| 26 | `Address2SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Address2SL |
| 27 | `Address3SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Address3SL |
| 28 | `Address4SL` | `WCHAR(255.0)` | Yes |  | Text attribute: Address4SL |
| 29 | `FSSAINo` | `WCHAR(255.0)` | Yes |  | Text attribute: FSSAINo |
| 30 | `UdyamNo` | `WCHAR(255.0)` | Yes |  | Text attribute: UdyamNo |
| 31 | `MSMEType` | `SMALLINT` | Yes |  | Integer identifier or enum code for MSMEType |

---

<a name="table-vchotherinfo"></a>

### Table: `VchOtherInfo`

> **Purpose:** Voucher optional user-defined fields (transporter, vehicle number, GR/LR number, payment terms, delivery date).

- **Row Count in Active FY:** `12`
- **Total Columns:** `61`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `OF1` | `WCHAR(30.0)` | Yes |  | Text attribute: OF1 |
| 3 | `OF2` | `WCHAR(30.0)` | Yes |  | Text attribute: OF2 |
| 4 | `OF3` | `WCHAR(30.0)` | Yes |  | Text attribute: OF3 |
| 5 | `OF4` | `WCHAR(30.0)` | Yes |  | Text attribute: OF4 |
| 6 | `OF5` | `WCHAR(30.0)` | Yes |  | Text attribute: OF5 |
| 7 | `OF6` | `WCHAR(30.0)` | Yes |  | Text attribute: OF6 |
| 8 | `OF7` | `WCHAR(30.0)` | Yes |  | Text attribute: OF7 |
| 9 | `OF8` | `WCHAR(30.0)` | Yes |  | Text attribute: OF8 |
| 10 | `OF9` | `WCHAR(30.0)` | Yes |  | Text attribute: OF9 |
| 11 | `OF10` | `WCHAR(30.0)` | Yes |  | Text attribute: OF10 |
| 12 | `Transport` | `WCHAR(30.0)` | Yes |  | Text attribute: Transport |
| 13 | `Station` | `WCHAR(30.0)` | Yes |  | Text attribute: Station |
| 14 | `GrNo` | `WCHAR(30.0)` | Yes |  | Text attribute: GrNo |
| 15 | `VehicleNo` | `WCHAR(30.0)` | Yes |  | Text attribute: VehicleNo |
| 16 | `ItemDesc` | `WCHAR(20.0)` | Yes |  | Text attribute: ItemDesc |
| 17 | `Form31No` | `WCHAR(20.0)` | Yes |  | Text attribute: Form31No |
| 18 | `Form31IssuedOn` | `WCHAR(20.0)` | Yes |  | Text attribute: Form31IssuedOn |
| 19 | `TotalQty` | `WCHAR(20.0)` | Yes |  | Text attribute: TotalQty |
| 20 | `PurchaseBillNo` | `WCHAR(25.0)` | Yes |  | Text attribute: PurchaseBillNo |
| 21 | `PurchaseBillDate` | `WCHAR(20.0)` | Yes |  | Text attribute: PurchaseBillDate |
| 22 | `Narration1` | `WCHAR(94.0)` | Yes |  | Text attribute: Narration1 |
| 23 | `Narration2` | `WCHAR(94.0)` | Yes |  | Text attribute: Narration2 |
| 24 | `InvoicePrepTime` | `WCHAR(25.0)` | Yes |  | Text attribute: InvoicePrepTime |
| 25 | `GoodsRemovalTime` | `WCHAR(25.0)` | Yes |  | Text attribute: GoodsRemovalTime |
| 26 | `GrDate` | `DATETIME` | Yes |  | Timestamp / Date field for GrDate |
| 27 | `VchNotes` | `WCHAR` | Yes |  | Text attribute: VchNotes |
| 28 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 29 | `OF11` | `WCHAR(30.0)` | Yes |  | Text attribute: OF11 |
| 30 | `OF12` | `WCHAR(30.0)` | Yes |  | Text attribute: OF12 |
| 31 | `OF13` | `WCHAR(30.0)` | Yes |  | Text attribute: OF13 |
| 32 | `OF14` | `WCHAR(30.0)` | Yes |  | Text attribute: OF14 |
| 33 | `OF15` | `WCHAR(30.0)` | Yes |  | Text attribute: OF15 |
| 34 | `OF16` | `WCHAR(30.0)` | Yes |  | Text attribute: OF16 |
| 35 | `OF17` | `WCHAR(30.0)` | Yes |  | Text attribute: OF17 |
| 36 | `OF18` | `WCHAR(30.0)` | Yes |  | Text attribute: OF18 |
| 37 | `OF19` | `WCHAR(30.0)` | Yes |  | Text attribute: OF19 |
| 38 | `OF20` | `WCHAR(30.0)` | Yes |  | Text attribute: OF20 |
| 39 | `PortCode` | `WCHAR(255.0)` | Yes |  | Text attribute: PortCode |
| 40 | `Distance` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Distance |
| 41 | `EWayBillReqd` | `BOOLEAN` | No |  | Boolean flag for EWayBillReqd (True/False) |
| 42 | `TransportMode` | `SMALLINT` | Yes |  | Integer identifier or enum code for TransportMode |
| 43 | `PinCode` | `WCHAR(255.0)` | Yes |  | Text attribute: PinCode |
| 44 | `EWayBillDate` | `DATETIME` | Yes |  | Date and time of E-Way Bill generation |
| 45 | `EWayBillPrinted` | `BOOLEAN` | No |  | Boolean flag for EWayBillPrinted (True/False) |
| 46 | `EWayBillSubType` | `SMALLINT` | Yes |  | Integer identifier or enum code for EWayBillSubType |
| 47 | `EWayBillTranType` | `SMALLINT` | Yes |  | Integer identifier or enum code for EWayBillTranType |
| 48 | `EInvoiceReq` | `BOOLEAN` | No |  | Boolean flag for EInvoiceReq (True/False) |
| 49 | `CombinedEwayBillEInvoice` | `BOOLEAN` | No |  | Boolean flag for CombinedEwayBillEInvoice (True/False) |
| 50 | `DispatchDetReq` | `BOOLEAN` | No |  | Boolean flag for DispatchDetReq (True/False) |
| 51 | `DispatcherPartyName` | `WCHAR(255.0)` | Yes |  | Text attribute: DispatcherPartyName |
| 52 | `DispatchAddr1` | `WCHAR(255.0)` | Yes |  | Text attribute: DispatchAddr1 |
| 53 | `DispatchAddr2` | `WCHAR(255.0)` | Yes |  | Text attribute: DispatchAddr2 |
| 54 | `DispatchAddr3` | `WCHAR(255.0)` | Yes |  | Text attribute: DispatchAddr3 |
| 55 | `DispatchAddr4` | `WCHAR(255.0)` | Yes |  | Text attribute: DispatchAddr4 |
| 56 | `DispatchPlace` | `WCHAR(255.0)` | Yes |  | Text attribute: DispatchPlace |
| 57 | `DispatchPIN` | `WCHAR(255.0)` | Yes |  | Text attribute: DispatchPIN |
| 58 | `DispatchStateCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for DispatchStateCode |
| 59 | `DispatchGSTIN` | `WCHAR(255.0)` | Yes |  | Text attribute: DispatchGSTIN |
| 60 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 61 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |

---

<a name="table-dailysum"></a>

### Table: `DailySum`

> **Purpose:** Daily financial and inventory aggregation cache for fast day-book and ledger rendering.

- **Row Count in Active FY:** `45`
- **Total Columns:** `14`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 2 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 3 | `MasterType` | `SMALLINT` | Yes |  | Polymorphic Entity Type enum (1=AccountGroup, 2=Account, 6=Item, 8=Unit, 9=BillSundry, 21=TaxCategory) |
| 4 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 5 | `Dr1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Dr1 |
| 6 | `Dr2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Dr2 |
| 7 | `Dr3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Dr3 |
| 8 | `Cr1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Cr1 |
| 9 | `Cr2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Cr2 |
| 10 | `Cr3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Cr3 |
| 11 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 12 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 13 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 14 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |

---

<a name="table-dailymessage"></a>

### Table: `DailyMessage`

> **Purpose:** Automated notification and payment reminder messages scheduled on specific voucher due dates.

- **Row Count in Active FY:** `0`
- **Total Columns:** `8`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 2 | `NoOfDays` | `SMALLINT` | Yes |  | Integer identifier or enum code for NoOfDays |
| 3 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 4 | `VSCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VSCode |
| 5 | `Msg1` | `WCHAR(96.0)` | Yes |  | Text attribute: Msg1 |
| 6 | `Msg2` | `WCHAR(96.0)` | Yes |  | Text attribute: Msg2 |
| 7 | `Msg3` | `WCHAR(96.0)` | Yes |  | Text attribute: Msg3 |
| 8 | `Msg4` | `WCHAR(96.0)` | Yes |  | Text attribute: Msg4 |

---

<a name="table-brsopbal"></a>

### Table: `BRSOpBal`

> **Purpose:** Bank Reconciliation Statement (BRS) opening uncleared cheque balances carried forward from previous period.

- **Row Count in Active FY:** `0`
- **Total Columns:** `12`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 2 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 3 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 4 | `OpAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for OpAmt |
| 5 | `Type` | `SMALLINT` | Yes |  | Integer identifier or enum code for Type |
| 6 | `ShortNar` | `WCHAR(40.0)` | Yes |  | Brief line-item narration or ledger remark |
| 7 | `EntryDate` | `DATETIME` | Yes |  | Timestamp / Date field for EntryDate |
| 8 | `ClrDate` | `DATETIME` | Yes |  | Timestamp / Date field for ClrDate |
| 9 | `OldVchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for OldVchCode |
| 10 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 11 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 12 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |

---

<a name="table-orgsalepurc"></a>

### Table: `OrgSalePurc`

> **Purpose:** Original invoice references for Credit Notes and Debit Notes (original invoice no, date, taxable value).

- **Row Count in Active FY:** `0`
- **Total Columns:** `8`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 3 | `VchDate` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 4 | `TaxableAmt` | `DOUBLE` | Yes |  | Taxable net amount before taxes |
| 5 | `TaxAmt` | `DOUBLE` | Yes |  | Total GST tax amount calculated |
| 6 | `TaxAmt1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TaxAmt1 |
| 7 | `SchgAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SchgAmt |
| 8 | `RegType` | `SMALLINT` | Yes |  | Integer identifier or enum code for RegType |

---

<a name="table-posdet"></a>

### Table: `POSDet`

> **Purpose:** Point of Sale (POS) multi-tender payment breakdown (Cash, Credit/Debit Card, UPI, Cheque, Gift Voucher).

- **Row Count in Active FY:** `0`
- **Total Columns:** `17`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `CashAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CashAmt |
| 3 | `ChequeAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ChequeAmt |
| 4 | `CCAmt1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CCAmt1 |
| 5 | `CCAmt2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CCAmt2 |
| 6 | `CCAmt3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CCAmt3 |
| 7 | `CashNarr` | `WCHAR(40.0)` | Yes |  | Text attribute: CashNarr |
| 8 | `ChequeNarr` | `WCHAR(40.0)` | Yes |  | Text attribute: ChequeNarr |
| 9 | `CCNarr1` | `WCHAR(40.0)` | Yes |  | Text attribute: CCNarr1 |
| 10 | `CCNarr2` | `WCHAR(40.0)` | Yes |  | Text attribute: CCNarr2 |
| 11 | `CCNarr3` | `WCHAR(40.0)` | Yes |  | Text attribute: CCNarr3 |
| 12 | `CashRecdAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CashRecdAmt |
| 13 | `CashAccCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for CashAccCode |
| 14 | `CCAccCode1` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for CCAccCode1 |
| 15 | `CCAccCode2` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for CCAccCode2 |
| 16 | `CCAccCode3` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for CCAccCode3 |
| 17 | `ChequeAccCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for ChequeAccCode |

---

<a name="table-packingdetails"></a>

### Table: `PackingDetails`

> **Purpose:** Packing slip and consignment details (box number, gross weight, net weight, dimensions, packaging unit).

- **Row Count in Active FY:** `0`
- **Total Columns:** `12`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `SrNo` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for SrNo |
| 2 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 3 | `PackageNo` | `WCHAR(255.0)` | Yes |  | Text attribute: PackageNo |
| 4 | `Weight` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Weight |
| 5 | `EstimatedValue` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for EstimatedValue |
| 6 | `Size` | `WCHAR(255.0)` | Yes |  | Text attribute: Size |
| 7 | `Description` | `WCHAR(255.0)` | Yes |  | Text attribute: Description |
| 8 | `Remarks` | `WCHAR(255.0)` | Yes |  | Text attribute: Remarks |
| 9 | `MarkaNo` | `WCHAR(255.0)` | Yes |  | Text attribute: MarkaNo |
| 10 | `Quantity` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Quantity |
| 11 | `Unit` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for Unit |
| 12 | `PackingMode` | `WCHAR(255.0)` | Yes |  | Text attribute: PackingMode |

---

<a name="table-jobfinishedrefs"></a>

### Table: `JobFinishedRefs`

> **Purpose:** Finished goods batch reference generated from Bill of Materials (BOM) in production vouchers.

- **Row Count in Active FY:** `0`
- **Total Columns:** `18`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `JobID` | `WCHAR(255.0)` | Yes |  | Text attribute: JobID |
| 2 | `TranType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TranType |
| 3 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 4 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 5 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 6 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 7 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 8 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 9 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 10 | `VchSeriesCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchSeriesCode |
| 11 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 12 | `Value1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value1 |
| 13 | `Value2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value2 |
| 14 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 15 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 16 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 17 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 18 | `Rectype` | `SMALLINT` | Yes |  | Integer identifier or enum code for Rectype |

---

<a name="table-phystksubdet"></a>

### Table: `PhyStkSubDet`

> **Purpose:** Physical stock verification audit lines recording counted physical quantity versus book balance variance.

- **Row Count in Active FY:** `0`
- **Total Columns:** `39`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 2 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 3 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 4 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 5 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 6 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 7 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 8 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 9 | `DueDate` | `DATETIME` | Yes |  | Timestamp / Date field for DueDate |
| 10 | `No` | `WCHAR(25.0)` | Yes |  | Text attribute: No |
| 11 | `Value1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value1 |
| 12 | `Value2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value2 |
| 13 | `Value3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value3 |
| 14 | `Balance1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance1 |
| 15 | `Balance2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance2 |
| 16 | `Balance3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance3 |
| 17 | `ItemSrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for ItemSrNo |
| 18 | `MfgDate` | `DATETIME` | Yes |  | Timestamp / Date field for MfgDate |
| 19 | `NewRefAmount` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for NewRefAmount |
| 20 | `MonthVal` | `SMALLINT` | Yes |  | Integer identifier or enum code for MonthVal |
| 21 | `WarrantyMonth` | `SMALLINT` | Yes |  | Integer identifier or enum code for WarrantyMonth |
| 22 | `OrgDate` | `DATETIME` | Yes |  | Timestamp / Date field for OrgDate |
| 23 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 24 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 25 | `C3` | `WCHAR(255.0)` | Yes |  | Text attribute: C3 |
| 26 | `C4` | `WCHAR(255.0)` | Yes |  | Text attribute: C4 |
| 27 | `C5` | `WCHAR(255.0)` | Yes |  | Text attribute: C5 |
| 28 | `C6` | `WCHAR(255.0)` | Yes |  | Text attribute: C6 |
| 29 | `C7` | `WCHAR(255.0)` | Yes |  | Text attribute: C7 |
| 30 | `C8` | `WCHAR(255.0)` | Yes |  | Text attribute: C8 |
| 31 | `C9` | `WCHAR(255.0)` | Yes |  | Text attribute: C9 |
| 32 | `C10` | `WCHAR(255.0)` | Yes |  | Text attribute: C10 |
| 33 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 34 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 35 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 36 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 37 | `D5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D5 |
| 38 | `D6` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D6 |
| 39 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |

---

<a name="table-vchtemplate"></a>

### Table: `VchTemplate`

> **Purpose:** Reusable transaction templates for recurring monthly vouchers (Rent, Salaries, Subscriptions).

- **Row Count in Active FY:** `0`
- **Total Columns:** `2`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `TemplateName` | `WCHAR(20.0)` | Yes |  | Text attribute: TemplateName |

---

<a name="table-vchtemptagging"></a>

### Table: `VchTempTagging`

> **Purpose:** Tagging rules and schedules linking vouchers to specific transaction templates.

- **Row Count in Active FY:** `0`
- **Total Columns:** `11`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `MasterCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for MasterCode |
| 2 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 3 | `TemplateVchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for TemplateVchCode |
| 4 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 5 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 6 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 7 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 8 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 9 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 10 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 11 | `MasterType` | `SMALLINT` | Yes |  | Polymorphic Entity Type enum (1=AccountGroup, 2=Account, 6=Item, 8=Unit, 9=BillSundry, 21=TaxCategory) |

---

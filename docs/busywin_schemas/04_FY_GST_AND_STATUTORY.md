# BusyWin FY Database: GST, Statutory & Tax Schemas

> **Database File:** `db1<YYYY>.bds` (e.g. `C:\BusyWin\DATA\COMP0001\db12026.bds`)

> **Engine:** Microsoft Jet 4.0 / Access OLEDB (`ILoveMyINDIA`)

> **Description:** Detailed table schemas and column definitions for GST calculations, E-Way Bill, E-Commerce settlement, VAT, TDS/TCS, and Payroll in db1YYYY.bds.


## Tables in this Module


| # | Table Name | Columns | Active Rows | Primary Key | Description |
|---|------------|:-------:|:-----------:|:-----------:|-------------|
| 1 | [`VchGSTSumItemWise`](#table-vchgstsumitemwise) | 52 | 15 | `-` | Item-level GST calculation summary recording HSN/SAC, taxable value, CGST/SGST/IGST rates and amounts, Cess, and place of supply state code. |
| 2 | [`GSTInfo`](#table-gstinfo) | 44 | 0 | `-` | General GST statutory register entries and manual tax adjustments (Reverse Charge Mechanism, Advance Received). |
| 3 | [`GSTITCPendingVchDet`](#table-gstitcpendingvchdet) | 53 | 0 | `-` | Input Tax Credit (ITC) pending / reversal tracking (Rule 37 180-day non-payment, Rule 42/43 capital goods reversals). |
| 4 | [`GSTR1Info`](#table-gstr1info) | 60 | 0 | `-` | GSTR-1 return filing snapshot data (B2B, B2CL, B2CS, CDNR, EXP, AT, HSN summary). |
| 5 | [`GSTR2AInfo`](#table-gstr2ainfo) | 54 | 0 | `-` | GSTR-2A auto-drafted inward supplies statement downloaded from the GST Portal for supplier reconciliation. |
| 6 | [`GSTR2BInfo`](#table-gstr2binfo) | 54 | 0 | `-` | GSTR-2B static monthly ITC statement imported from the GST Portal. |
| 7 | [`GSTR3BInfo`](#table-gstr3binfo) | 33 | 0 | `-` | GSTR-3B monthly summary return calculation table (outward taxable supplies, eligible ITC, net tax payable). |
| 8 | [`GetGeneratedEWayBillDet`](#table-getgeneratedewaybilldet) | 17 | 0 | `-` | E-Way Bill generation cache recording EWB Number, generation date, validity date, vehicle number, and status. |
| 9 | [`TCS`](#table-tcs) | 27 | 0 | `-` | Tax Collected at Source (Section 206C) register, collection rates, threshold limits, and challan details. |
| 10 | [`TDS`](#table-tds) | 30 | 0 | `-` | Tax Deducted at Source (Section 194C, 194J, 194Q) register, deduction rates, certificate numbers, and challan links. |
| 11 | [`STDet`](#table-stdet) | 8 | 0 | `-` | Pre-GST Service Tax calculation details and abatement percentages. |
| 12 | [`Excise`](#table-excise) | 31 | 0 | `-` | Central Excise invoice details, RG23A/PLA register entries, and assessable value records. |
| 13 | [`TradingExcise`](#table-tradingexcise) | 53 | 0 | `-` | First-stage and second-stage dealer excise registration and RG23D register tracking. |
| 14 | [`VATInfo`](#table-vatinfo) | 22 | 0 | `-` | State VAT statutory return information and statutory annexures (prior to GST). |
| 15 | [`VchVATAccInfo`](#table-vchvataccinfo) | 43 | 0 | `-` | State VAT ledger account posting details. |
| 16 | [`VchVATSum`](#table-vchvatsum) | 9 | 0 | `-` | Voucher-level VAT calculation summary. |
| 17 | [`VchVATSumItemWise`](#table-vchvatsumitemwise) | 11 | 0 | `-` | Item-level VAT calculation breakdown. |
| 18 | [`EComOrderHeader`](#table-ecomorderheader) | 8 | 0 | `-` | E-commerce marketplace orders (Amazon, Flipkart, Meesho) header data (Order ID, Order Date, Marketplace). |
| 19 | [`EComOrderBody`](#table-ecomorderbody) | 7 | 0 | `-` | E-commerce order line items, marketplace SKU mappings, order status, and returned quantities. |
| 20 | [`EcomSettlement`](#table-ecomsettlement) | 8 | 0 | `-` | Marketplace payment settlement reconciliation header (Settlement ID, settlement date, net amount credited). |
| 21 | [`EcomSettlementExp`](#table-ecomsettlementexp) | 6 | 0 | `-` | Marketplace platform deductions (commission fees, shipping fees, closing fees, marketing fees). |
| 22 | [`EcomSettlementItem`](#table-ecomsettlementitem) | 20 | 0 | `-` | Order-level payment settlement reconciliation within the marketplace remittance batch. |
| 23 | [`EcomSettlementItemExp`](#table-ecomsettlementitemexp) | 9 | 0 | `-` | Item-level fee deductions applied by the marketplace platform. |
| 24 | [`EmpLADet`](#table-empladet) | 8 | 0 | `-` | Employee Loan and Advance disbursement and monthly payroll installment recovery schedule. |
| 25 | [`AMCWarrDet`](#table-amcwarrdet) | 15 | 0 | `-` | Annual Maintenance Contract (AMC) and warranty tracking against sold equipment and appliances. |

---

## Detailed Column Schemas


<a name="table-vchgstsumitemwise"></a>

### Table: `VchGSTSumItemWise`

> **Purpose:** Item-level GST calculation summary recording HSN/SAC, taxable value, CGST/SGST/IGST rates and amounts, Cess, and place of supply state code.

- **Row Count in Active FY:** `15`
- **Total Columns:** `52`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Unique Voucher Transaction ID (Primary Key in Tran1, Foreign Key in others) |
| 2 | `ItemCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Inventory Item) |
| 3 | `ItemSrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for ItemSrNo |
| 4 | `PartyCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Customer or Vendor Party) |
| 5 | `TaxCatCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for TaxCatCode |
| 6 | `STPTCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for STPTCode |
| 7 | `VchNo` | `WCHAR(255.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 8 | `VchSeriesCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchSeriesCode |
| 9 | `VchDate` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 10 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 11 | `HSNCode` | `WCHAR(255.0)` | Yes |  | Harmonized System of Nomenclature (HSN) or SAC code |
| 12 | `SENo` | `WCHAR(255.0)` | Yes |  | Text attribute: SENo |
| 13 | `PartyStateTinDigit` | `WCHAR(255.0)` | Yes |  | Text attribute: PartyStateTinDigit |
| 14 | `PartyStateCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for PartyStateCode |
| 15 | `BDStateTinDigit` | `WCHAR(255.0)` | Yes |  | Text attribute: BDStateTinDigit |
| 16 | `BDStateCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for BDStateCode |
| 17 | `TaxableAmt` | `DOUBLE` | Yes |  | Taxable net amount before taxes |
| 18 | `TaxRate` | `DOUBLE` | Yes |  | GST percentage rate (e.g. 18.0 for 18%) |
| 19 | `TaxRate1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TaxRate1 |
| 20 | `TaxAmt` | `DOUBLE` | Yes |  | Total GST tax amount calculated |
| 21 | `TaxAmt1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TaxAmt1 |
| 22 | `SurchargeRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeRate |
| 23 | `SurchargeAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeAmt |
| 24 | `ACessRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ACessRate |
| 25 | `ACessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ACessAmt |
| 26 | `StateCessRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for StateCessRate |
| 27 | `StateCessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for StateCessAmt |
| 28 | `LocType` | `SMALLINT` | Yes |  | Integer identifier or enum code for LocType |
| 29 | `ZeroTaxType` | `SMALLINT` | Yes |  | Integer identifier or enum code for ZeroTaxType |
| 30 | `ActualSaleAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ActualSaleAmt |
| 31 | `TaxOnMRP` | `BOOLEAN` | No |  | Boolean flag for TaxOnMRP (True/False) |
| 32 | `ItemMainQty` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ItemMainQty |
| 33 | `ItemAltQty` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ItemAltQty |
| 34 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 35 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 36 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 37 | `OrgVchNo` | `WCHAR(255.0)` | Yes |  | Text attribute: OrgVchNo |
| 38 | `OrgVchDate` | `DATETIME` | Yes |  | Timestamp / Date field for OrgVchDate |
| 39 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 40 | `GSTRepBasis` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTRepBasis |
| 41 | `TypeOfDealer` | `SMALLINT` | Yes |  | Integer identifier or enum code for TypeOfDealer |
| 42 | `POSStateTinDigit` | `WCHAR(255.0)` | Yes |  | Text attribute: POSStateTinDigit |
| 43 | `POSStateCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for POSStateCode |
| 44 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 45 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 46 | `CM2` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM2 (links to Master1.Code based on MasterType) |
| 47 | `ITCClaimedStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for ITCClaimedStatus |
| 48 | `ITCClaimedMonth` | `SMALLINT` | Yes |  | Integer identifier or enum code for ITCClaimedMonth |
| 49 | `GSTIN` | `WCHAR(255.0)` | Yes |  | 15-digit Goods and Services Tax Identification Number |
| 50 | `GSTR2BStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTR2BStatus |
| 51 | `GSTR2BMonth` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTR2BMonth |
| 52 | `GSTR2BYear` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTR2BYear |

---

<a name="table-gstinfo"></a>

### Table: `GSTInfo`

> **Purpose:** General GST statutory register entries and manual tax adjustments (Reverse Charge Mechanism, Advance Received).

- **Row Count in Active FY:** `0`
- **Total Columns:** `44`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 2 | `Amount` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Amount |
| 3 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 4 | `Type` | `SMALLINT` | Yes |  | Integer identifier or enum code for Type |
| 5 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 6 | `Description` | `WCHAR(255.0)` | Yes |  | Text attribute: Description |
| 7 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 8 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 9 | `ChallanNo` | `WCHAR(255.0)` | Yes |  | Text attribute: ChallanNo |
| 10 | `ChallanDate` | `DATETIME` | Yes |  | Timestamp / Date field for ChallanDate |
| 11 | `ChequeNo` | `WCHAR(255.0)` | Yes |  | Text attribute: ChequeNo |
| 12 | `ChequeDate` | `DATETIME` | Yes |  | Timestamp / Date field for ChequeDate |
| 13 | `BankName` | `WCHAR(255.0)` | Yes |  | Text attribute: BankName |
| 14 | `BankCode` | `WCHAR(255.0)` | Yes |  | Text attribute: BankCode |
| 15 | `Interest` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Interest |
| 16 | `Penalty` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Penalty |
| 17 | `BankAcType` | `WCHAR(255.0)` | Yes |  | Text attribute: BankAcType |
| 18 | `BankAcNo` | `WCHAR(255.0)` | Yes |  | Text attribute: BankAcNo |
| 19 | `CGSTPercent` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CGSTPercent |
| 20 | `SGSTPercent` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SGSTPercent |
| 21 | `IGSTPercent` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for IGSTPercent |
| 22 | `CessPercent` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CessPercent |
| 23 | `ACessPercent` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ACessPercent |
| 24 | `CGSTAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CGSTAmt |
| 25 | `SGSTAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SGSTAmt |
| 26 | `IGSTAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for IGSTAmt |
| 27 | `CessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CessAmt |
| 28 | `ACessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ACessAmt |
| 29 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 30 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 31 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 32 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 33 | `D5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D5 |
| 34 | `D6` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D6 |
| 35 | `D7` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D7 |
| 36 | `D8` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D8 |
| 37 | `D9` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D9 |
| 38 | `D10` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D10 |
| 39 | `D11` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D11 |
| 40 | `D12` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D12 |
| 41 | `D13` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D13 |
| 42 | `D14` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D14 |
| 43 | `D15` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D15 |
| 44 | `LateFee` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for LateFee |

---

<a name="table-gstitcpendingvchdet"></a>

### Table: `GSTITCPendingVchDet`

> **Purpose:** Input Tax Credit (ITC) pending / reversal tracking (Rule 37 180-day non-payment, Rule 42/43 capital goods reversals).

- **Row Count in Active FY:** `0`
- **Total Columns:** `53`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `VchSeriesCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchSeriesCode |
| 3 | `ItemCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Inventory Item) |
| 4 | `ItemSrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for ItemSrNo |
| 5 | `TaxCatCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for TaxCatCode |
| 6 | `STPTCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for STPTCode |
| 7 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 8 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 9 | `LocType` | `SMALLINT` | Yes |  | Integer identifier or enum code for LocType |
| 10 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 11 | `VchDate` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 12 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 13 | `PartyName` | `WCHAR(40.0)` | Yes |  | Text attribute: PartyName |
| 14 | `GSTIN` | `WCHAR(30.0)` | Yes |  | 15-digit Goods and Services Tax Identification Number |
| 15 | `HSNCode` | `WCHAR(255.0)` | Yes |  | Harmonized System of Nomenclature (HSN) or SAC code |
| 16 | `SENo` | `WCHAR(255.0)` | Yes |  | Text attribute: SENo |
| 17 | `PartyStateTinDigit` | `WCHAR(255.0)` | Yes |  | Text attribute: PartyStateTinDigit |
| 18 | `PartyStateCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for PartyStateCode |
| 19 | `BDStateTinDigit` | `WCHAR(255.0)` | Yes |  | Text attribute: BDStateTinDigit |
| 20 | `BDStateCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for BDStateCode |
| 21 | `ActualSaleAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ActualSaleAmt |
| 22 | `TaxableAmt` | `DOUBLE` | Yes |  | Taxable net amount before taxes |
| 23 | `TaxRate` | `DOUBLE` | Yes |  | GST percentage rate (e.g. 18.0 for 18%) |
| 24 | `TaxRate1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TaxRate1 |
| 25 | `TaxAmt` | `DOUBLE` | Yes |  | Total GST tax amount calculated |
| 26 | `TaxAmt1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TaxAmt1 |
| 27 | `CessRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CessRate |
| 28 | `CessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CessAmt |
| 29 | `AddCessRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for AddCessRate |
| 30 | `AddCessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for AddCessAmt |
| 31 | `StateCessRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for StateCessRate |
| 32 | `StateCessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for StateCessAmt |
| 33 | `ZeroTaxType` | `SMALLINT` | Yes |  | Integer identifier or enum code for ZeroTaxType |
| 34 | `TaxOnMRP` | `BOOLEAN` | No |  | Boolean flag for TaxOnMRP (True/False) |
| 35 | `ItemMainQty` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ItemMainQty |
| 36 | `ItemAltQty` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ItemAltQty |
| 37 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 38 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 39 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 40 | `GSTRepBasis` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTRepBasis |
| 41 | `TypeOfDealer` | `SMALLINT` | Yes |  | Integer identifier or enum code for TypeOfDealer |
| 42 | `POSStateTinDigit` | `WCHAR(255.0)` | Yes |  | Text attribute: POSStateTinDigit |
| 43 | `POSStateCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for POSStateCode |
| 44 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 45 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 46 | `CM2` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM2 (links to Master1.Code based on MasterType) |
| 47 | `ITCClaimedStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for ITCClaimedStatus |
| 48 | `ITCClaimedMonth` | `SMALLINT` | Yes |  | Integer identifier or enum code for ITCClaimedMonth |
| 49 | `OrgVchNo` | `WCHAR(255.0)` | Yes |  | Text attribute: OrgVchNo |
| 50 | `OrgVchDate` | `DATETIME` | Yes |  | Timestamp / Date field for OrgVchDate |
| 51 | `GSTR2BStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTR2BStatus |
| 52 | `GSTR2BMonth` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTR2BMonth |
| 53 | `GSTR2BYear` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTR2BYear |

---

<a name="table-gstr1info"></a>

### Table: `GSTR1Info`

> **Purpose:** GSTR-1 return filing snapshot data (B2B, B2CL, B2CS, CDNR, EXP, AT, HSN summary).

- **Row Count in Active FY:** `0`
- **Total Columns:** `60`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 2 | `TranType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TranType |
| 3 | `Month` | `SMALLINT` | Yes |  | Integer identifier or enum code for Month |
| 4 | `Year` | `WCHAR(255.0)` | Yes |  | Text attribute: Year |
| 5 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 6 | `GSTIN` | `WCHAR(255.0)` | Yes |  | 15-digit Goods and Services Tax Identification Number |
| 7 | `CompGSTIN` | `WCHAR(255.0)` | Yes |  | 15-digit Goods and Services Tax Identification Number |
| 8 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 9 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 10 | `CrDate` | `DATETIME` | Yes |  | Timestamp / Date field for CrDate |
| 11 | `CrNo` | `WCHAR(25.0)` | Yes |  | Text attribute: CrNo |
| 12 | `InvType` | `WCHAR(255.0)` | Yes |  | Text attribute: InvType |
| 13 | `updby` | `WCHAR(255.0)` | Yes |  | Text attribute: updby |
| 14 | `CheckSum` | `WCHAR(255.0)` | Yes |  | Text attribute: CheckSum |
| 15 | `TotalAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TotalAmt |
| 16 | `TaxableAmt` | `DOUBLE` | Yes |  | Taxable net amount before taxes |
| 17 | `Rate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Rate |
| 18 | `CGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CGST |
| 19 | `SGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SGST |
| 20 | `IGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for IGST |
| 21 | `CessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CessAmt |
| 22 | `POS` | `WCHAR(25.0)` | Yes |  | Text attribute: POS |
| 23 | `cfs` | `BOOLEAN` | No |  | Boolean flag for cfs (True/False) |
| 24 | `cName` | `WCHAR(255.0)` | Yes |  | Text attribute: cName |
| 25 | `flag` | `WCHAR(10.0)` | Yes |  | Text attribute: flag |
| 26 | `rchrg` | `BOOLEAN` | No |  | Boolean flag for rchrg (True/False) |
| 27 | `cFlag` | `BOOLEAN` | No |  | Boolean flag for cFlag (True/False) |
| 28 | `uqc` | `WCHAR(10.0)` | Yes |  | Text attribute: uqc |
| 29 | `qty` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for qty |
| 30 | `hsnsc` | `WCHAR(255.0)` | Yes |  | Text attribute: hsnsc |
| 31 | `Desc` | `WCHAR(255.0)` | Yes |  | Text attribute: Desc |
| 32 | `pGST` | `BOOLEAN` | No |  | Boolean flag for pGST (True/False) |
| 33 | `SupplyType` | `WCHAR(255.0)` | Yes |  | Text attribute: SupplyType |
| 34 | `Type` | `WCHAR(255.0)` | Yes |  | Text attribute: Type |
| 35 | `Cancel` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for Cancel |
| 36 | `num` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for num |
| 37 | `totnum` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for totnum |
| 38 | `Docfrom` | `WCHAR(255.0)` | Yes |  | Text attribute: Docfrom |
| 39 | `DocTo` | `WCHAR(255.0)` | Yes |  | Text attribute: DocTo |
| 40 | `netissue` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for netissue |
| 41 | `docnum` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for docnum |
| 42 | `filDate` | `DATETIME` | Yes |  | Timestamp / Date field for filDate |
| 43 | `filType` | `WCHAR(255.0)` | Yes |  | Text attribute: filType |
| 44 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 45 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 46 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 47 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 48 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 49 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 50 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 51 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 52 | `CM2` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM2 (links to Master1.Code based on MasterType) |
| 53 | `CM3` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM3 (links to Master1.Code based on MasterType) |
| 54 | `CM4` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM4 (links to Master1.Code based on MasterType) |
| 55 | `CM5` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM5 (links to Master1.Code based on MasterType) |
| 56 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 57 | `Date2` | `DATETIME` | Yes |  | Timestamp / Date field for Date2 |
| 58 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 59 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 60 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |

---

<a name="table-gstr2ainfo"></a>

### Table: `GSTR2AInfo`

> **Purpose:** GSTR-2A auto-drafted inward supplies statement downloaded from the GST Portal for supplier reconciliation.

- **Row Count in Active FY:** `0`
- **Total Columns:** `54`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 2 | `TranType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TranType |
| 3 | `Month` | `SMALLINT` | Yes |  | Integer identifier or enum code for Month |
| 4 | `Year` | `WCHAR(255.0)` | Yes |  | Text attribute: Year |
| 5 | `SrNo` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for SrNo |
| 6 | `GSTIN` | `WCHAR(255.0)` | Yes |  | 15-digit Goods and Services Tax Identification Number |
| 7 | `CompGSTIN` | `WCHAR(255.0)` | Yes |  | 15-digit Goods and Services Tax Identification Number |
| 8 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 9 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 10 | `OrgDate` | `DATETIME` | Yes |  | Timestamp / Date field for OrgDate |
| 11 | `OrgVchNo` | `WCHAR(25.0)` | Yes |  | Text attribute: OrgVchNo |
| 12 | `InvType` | `WCHAR(255.0)` | Yes |  | Text attribute: InvType |
| 13 | `updby` | `WCHAR(255.0)` | Yes |  | Text attribute: updby |
| 14 | `CheckSum` | `WCHAR(255.0)` | Yes |  | Text attribute: CheckSum |
| 15 | `TotalAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TotalAmt |
| 16 | `TaxableAmt` | `DOUBLE` | Yes |  | Taxable net amount before taxes |
| 17 | `Rate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Rate |
| 18 | `CGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CGST |
| 19 | `SGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SGST |
| 20 | `IGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for IGST |
| 21 | `CessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CessAmt |
| 22 | `ITCCGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ITCCGST |
| 23 | `ITCSGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ITCSGST |
| 24 | `ITCIGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ITCIGST |
| 25 | `ITCCessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ITCCessAmt |
| 26 | `ITCElg` | `WCHAR(20.0)` | Yes |  | Text attribute: ITCElg |
| 27 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 28 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 29 | `POS` | `SMALLINT` | Yes |  | Integer identifier or enum code for POS |
| 30 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 31 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 32 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 33 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 34 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 35 | `CFS` | `BOOLEAN` | No |  | Boolean flag for CFS (True/False) |
| 36 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 37 | `CM2` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM2 (links to Master1.Code based on MasterType) |
| 38 | `CM3` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM3 (links to Master1.Code based on MasterType) |
| 39 | `CM4` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM4 (links to Master1.Code based on MasterType) |
| 40 | `CM5` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM5 (links to Master1.Code based on MasterType) |
| 41 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 42 | `Date2` | `DATETIME` | Yes |  | Timestamp / Date field for Date2 |
| 43 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 44 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 45 | `Reason` | `WCHAR(255.0)` | Yes |  | Text attribute: Reason |
| 46 | `Type` | `WCHAR(20.0)` | Yes |  | Text attribute: Type |
| 47 | `NoteNo` | `WCHAR(255.0)` | Yes |  | Text attribute: NoteNo |
| 48 | `NoteDate` | `DATETIME` | Yes |  | Timestamp / Date field for NoteDate |
| 49 | `DiffPercent` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for DiffPercent |
| 50 | `ITCAvl` | `BOOLEAN` | No |  | Boolean flag for ITCAvl (True/False) |
| 51 | `TradeName` | `WCHAR(255.0)` | Yes |  | Text attribute: TradeName |
| 52 | `SupplierFilDate` | `DATETIME` | Yes |  | Timestamp / Date field for SupplierFilDate |
| 53 | `SupplierPrd` | `WCHAR(25.0)` | Yes |  | Text attribute: SupplierPrd |
| 54 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |

---

<a name="table-gstr2binfo"></a>

### Table: `GSTR2BInfo`

> **Purpose:** GSTR-2B static monthly ITC statement imported from the GST Portal.

- **Row Count in Active FY:** `0`
- **Total Columns:** `54`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 2 | `TranType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TranType |
| 3 | `Month` | `SMALLINT` | Yes |  | Integer identifier or enum code for Month |
| 4 | `Year` | `WCHAR(255.0)` | Yes |  | Text attribute: Year |
| 5 | `SrNo` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for SrNo |
| 6 | `GSTIN` | `WCHAR(255.0)` | Yes |  | 15-digit Goods and Services Tax Identification Number |
| 7 | `CompGSTIN` | `WCHAR(255.0)` | Yes |  | 15-digit Goods and Services Tax Identification Number |
| 8 | `TradeName` | `WCHAR(255.0)` | Yes |  | Text attribute: TradeName |
| 9 | `SupplierFilDate` | `DATETIME` | Yes |  | Timestamp / Date field for SupplierFilDate |
| 10 | `SupplierPrd` | `WCHAR(25.0)` | Yes |  | Text attribute: SupplierPrd |
| 11 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 12 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 13 | `OrgDate` | `DATETIME` | Yes |  | Timestamp / Date field for OrgDate |
| 14 | `OrgVchNo` | `WCHAR(25.0)` | Yes |  | Text attribute: OrgVchNo |
| 15 | `InvType` | `WCHAR(255.0)` | Yes |  | Text attribute: InvType |
| 16 | `updby` | `WCHAR(255.0)` | Yes |  | Text attribute: updby |
| 17 | `CheckSum` | `WCHAR(255.0)` | Yes |  | Text attribute: CheckSum |
| 18 | `Type` | `WCHAR(20.0)` | Yes |  | Text attribute: Type |
| 19 | `TotalAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TotalAmt |
| 20 | `TaxableAmt` | `DOUBLE` | Yes |  | Taxable net amount before taxes |
| 21 | `Rate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Rate |
| 22 | `CGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CGST |
| 23 | `SGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SGST |
| 24 | `IGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for IGST |
| 25 | `CessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CessAmt |
| 26 | `ITCCGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ITCCGST |
| 27 | `ITCSGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ITCSGST |
| 28 | `ITCIGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ITCIGST |
| 29 | `ITCCessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ITCCessAmt |
| 30 | `ITCElg` | `WCHAR(20.0)` | Yes |  | Text attribute: ITCElg |
| 31 | `DiffPercent` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for DiffPercent |
| 32 | `ITCAvl` | `BOOLEAN` | No |  | Boolean flag for ITCAvl (True/False) |
| 33 | `Reason` | `WCHAR(255.0)` | Yes |  | Text attribute: Reason |
| 34 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 35 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 36 | `POS` | `SMALLINT` | Yes |  | Integer identifier or enum code for POS |
| 37 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 38 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 39 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 40 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 41 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 42 | `CFS` | `BOOLEAN` | No |  | Boolean flag for CFS (True/False) |
| 43 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 44 | `CM2` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM2 (links to Master1.Code based on MasterType) |
| 45 | `CM3` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM3 (links to Master1.Code based on MasterType) |
| 46 | `CM4` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM4 (links to Master1.Code based on MasterType) |
| 47 | `CM5` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM5 (links to Master1.Code based on MasterType) |
| 48 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 49 | `Date2` | `DATETIME` | Yes |  | Timestamp / Date field for Date2 |
| 50 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 51 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 52 | `NoteNo` | `WCHAR(255.0)` | Yes |  | Text attribute: NoteNo |
| 53 | `NoteDate` | `DATETIME` | Yes |  | Timestamp / Date field for NoteDate |
| 54 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |

---

<a name="table-gstr3binfo"></a>

### Table: `GSTR3BInfo`

> **Purpose:** GSTR-3B monthly summary return calculation table (outward taxable supplies, eligible ITC, net tax payable).

- **Row Count in Active FY:** `0`
- **Total Columns:** `33`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 2 | `TranType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TranType |
| 3 | `Month` | `SMALLINT` | Yes |  | Integer identifier or enum code for Month |
| 4 | `Year` | `WCHAR(255.0)` | Yes |  | Text attribute: Year |
| 5 | `GSTIN` | `WCHAR(255.0)` | Yes |  | 15-digit Goods and Services Tax Identification Number |
| 6 | `Type` | `WCHAR(20.0)` | Yes |  | Text attribute: Type |
| 7 | `TaxableAmt` | `DOUBLE` | Yes |  | Taxable net amount before taxes |
| 8 | `tax` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for tax |
| 9 | `CGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CGST |
| 10 | `SGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SGST |
| 11 | `IGST` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for IGST |
| 12 | `CessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CessAmt |
| 13 | `fee` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for fee |
| 14 | `Inter` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Inter |
| 15 | `Intera` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Intera |
| 16 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 17 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 18 | `POS` | `WCHAR(255.0)` | Yes |  | Text attribute: POS |
| 19 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 20 | `B2` | `BOOLEAN` | No |  | Boolean flag for B2 (True/False) |
| 21 | `B3` | `BOOLEAN` | No |  | Boolean flag for B3 (True/False) |
| 22 | `B4` | `BOOLEAN` | No |  | Boolean flag for B4 (True/False) |
| 23 | `B5` | `BOOLEAN` | No |  | Boolean flag for B5 (True/False) |
| 24 | `ldgID` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for ldgID |
| 25 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 26 | `CM2` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM2 (links to Master1.Code based on MasterType) |
| 27 | `CM3` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM3 (links to Master1.Code based on MasterType) |
| 28 | `CM4` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM4 (links to Master1.Code based on MasterType) |
| 29 | `CM5` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM5 (links to Master1.Code based on MasterType) |
| 30 | `C1` | `WCHAR(255.0)` | Yes |  | Text attribute: C1 |
| 31 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |
| 32 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 33 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |

---

<a name="table-getgeneratedewaybilldet"></a>

### Table: `GetGeneratedEWayBillDet`

> **Purpose:** E-Way Bill generation cache recording EWB Number, generation date, validity date, vehicle number, and status.

- **Row Count in Active FY:** `0`
- **Total Columns:** `17`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `GenByGSTIN` | `WCHAR(255.0)` | Yes |  | Text attribute: GenByGSTIN |
| 2 | `EWayBillNo` | `WCHAR(255.0)` | Yes |  | 12-digit government E-Way Bill Number |
| 3 | `EWayBillDate` | `DATETIME` | Yes |  | Date and time of E-Way Bill generation |
| 4 | `DocNo` | `WCHAR(255.0)` | Yes |  | Text attribute: DocNo |
| 5 | `DocDate` | `DATETIME` | Yes |  | Timestamp / Date field for DocDate |
| 6 | `FromGSTIN` | `WCHAR(255.0)` | Yes |  | Text attribute: FromGSTIN |
| 7 | `FromTradeName` | `WCHAR(255.0)` | Yes |  | Text attribute: FromTradeName |
| 8 | `ToGSTIN` | `WCHAR(255.0)` | Yes |  | Text attribute: ToGSTIN |
| 9 | `ToTradeName` | `WCHAR(255.0)` | Yes |  | Text attribute: ToTradeName |
| 10 | `InvValue` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for InvValue |
| 11 | `HSNCode` | `WCHAR(255.0)` | Yes |  | Harmonized System of Nomenclature (HSN) or SAC code |
| 12 | `HSNDesc` | `WCHAR(255.0)` | Yes |  | Text attribute: HSNDesc |
| 13 | `Date1` | `DATETIME` | Yes |  | Timestamp / Date field for Date1 |
| 14 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 15 | `DeliveryPincode` | `WCHAR(255.0)` | Yes |  | Text attribute: DeliveryPincode |
| 16 | `DeliveryPlace` | `WCHAR(255.0)` | Yes |  | Text attribute: DeliveryPlace |
| 17 | `DeliveryStateCode` | `WCHAR(255.0)` | Yes |  | Text attribute: DeliveryStateCode |

---

<a name="table-tcs"></a>

### Table: `TCS`

> **Purpose:** Tax Collected at Source (Section 206C) register, collection rates, threshold limits, and challan details.

- **Row Count in Active FY:** `0`
- **Total Columns:** `27`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Method` | `SMALLINT` | Yes |  | Integer identifier or enum code for Method |
| 2 | `RefNo` | `WCHAR(25.0)` | Yes |  | Text attribute: RefNo |
| 3 | `RefCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for RefCode |
| 4 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 5 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 6 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 7 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 8 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 9 | `EntryDate` | `DATETIME` | Yes |  | Timestamp / Date field for EntryDate |
| 10 | `DateOfCredit` | `DATETIME` | Yes |  | Timestamp / Date field for DateOfCredit |
| 11 | `VchAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for VchAmt |
| 12 | `TCSRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TCSRate |
| 13 | `TCSAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TCSAmt |
| 14 | `SurchargeRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeRate |
| 15 | `SurchargeAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeAmt |
| 16 | `Interest` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Interest |
| 17 | `OtherAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for OtherAmt |
| 18 | `LowerRate` | `BOOLEAN` | No |  | Boolean flag for LowerRate (True/False) |
| 19 | `Reason` | `WCHAR(20.0)` | Yes |  | Text attribute: Reason |
| 20 | `ChallanNo` | `WCHAR(20.0)` | Yes |  | Text attribute: ChallanNo |
| 21 | `ChequeNo` | `WCHAR(20.0)` | Yes |  | Text attribute: ChequeNo |
| 22 | `ChequeDate` | `DATETIME` | Yes |  | Timestamp / Date field for ChequeDate |
| 23 | `Quarter` | `SMALLINT` | Yes |  | Integer identifier or enum code for Quarter |
| 24 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 25 | `CategoryCode` | `WCHAR(20.0)` | Yes |  | Text attribute: CategoryCode |
| 26 | `SubCategoryCode` | `WCHAR(20.0)` | Yes |  | Text attribute: SubCategoryCode |
| 27 | `BSRCode` | `WCHAR(255.0)` | Yes |  | Text attribute: BSRCode |

---

<a name="table-tds"></a>

### Table: `TDS`

> **Purpose:** Tax Deducted at Source (Section 194C, 194J, 194Q) register, deduction rates, certificate numbers, and challan links.

- **Row Count in Active FY:** `0`
- **Total Columns:** `30`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Method` | `SMALLINT` | Yes |  | Integer identifier or enum code for Method |
| 2 | `RefNo` | `WCHAR(25.0)` | Yes |  | Text attribute: RefNo |
| 3 | `RefCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for RefCode |
| 4 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 5 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 6 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 7 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 8 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 9 | `EntryDate` | `DATETIME` | Yes |  | Timestamp / Date field for EntryDate |
| 10 | `DateOfCredit` | `DATETIME` | Yes |  | Timestamp / Date field for DateOfCredit |
| 11 | `VchAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for VchAmt |
| 12 | `TDSRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TDSRate |
| 13 | `TDSAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TDSAmt |
| 14 | `SurchargeRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeRate |
| 15 | `SurchargeAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeAmt |
| 16 | `CessRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CessRate |
| 17 | `CessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CessAmt |
| 18 | `SHECessRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SHECessRate |
| 19 | `SHECessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SHECessAmt |
| 20 | `Interest` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Interest |
| 21 | `OtherAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for OtherAmt |
| 22 | `LowerRate` | `BOOLEAN` | No |  | Boolean flag for LowerRate (True/False) |
| 23 | `Reason` | `WCHAR(20.0)` | Yes |  | Text attribute: Reason |
| 24 | `CertificateNo` | `WCHAR(255.0)` | Yes |  | Text attribute: CertificateNo |
| 25 | `ChallanNo` | `WCHAR(20.0)` | Yes |  | Text attribute: ChallanNo |
| 26 | `ChequeNo` | `WCHAR(20.0)` | Yes |  | Text attribute: ChequeNo |
| 27 | `ChequeDate` | `DATETIME` | Yes |  | Timestamp / Date field for ChequeDate |
| 28 | `Quarter` | `SMALLINT` | Yes |  | Integer identifier or enum code for Quarter |
| 29 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 30 | `BSRCode` | `WCHAR(20.0)` | Yes |  | Text attribute: BSRCode |

---

<a name="table-stdet"></a>

### Table: `STDet`

> **Purpose:** Pre-GST Service Tax calculation details and abatement percentages.

- **Row Count in Active FY:** `0`
- **Total Columns:** `8`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `STCategory` | `SMALLINT` | Yes |  | Integer identifier or enum code for STCategory |
| 3 | `STAssValue` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for STAssValue |
| 4 | `STRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for STRate |
| 5 | `SBCRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SBCRate |
| 6 | `KKCRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for KKCRate |
| 7 | `STCessRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for STCessRate |
| 8 | `STHECessRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for STHECessRate |

---

<a name="table-excise"></a>

### Table: `Excise`

> **Purpose:** Central Excise invoice details, RG23A/PLA register entries, and assessable value records.

- **Row Count in Active FY:** `0`
- **Total Columns:** `31`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 2 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 3 | `DocName` | `WCHAR(40.0)` | Yes |  | Text attribute: DocName |
| 4 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 5 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 6 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 7 | `Value` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value |
| 8 | `Balance` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance |
| 9 | `Value1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value1 |
| 10 | `Balance1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance1 |
| 11 | `Value2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value2 |
| 12 | `Balance2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance2 |
| 13 | `Value3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value3 |
| 14 | `Value4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value4 |
| 15 | `Value5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value5 |
| 16 | `ValueType` | `SMALLINT` | Yes |  | Integer identifier or enum code for ValueType |
| 17 | `SupplierType` | `SMALLINT` | Yes |  | Integer identifier or enum code for SupplierType |
| 18 | `ChallanNo` | `WCHAR(40.0)` | Yes |  | Text attribute: ChallanNo |
| 19 | `BankCode` | `WCHAR(20.0)` | Yes |  | Text attribute: BankCode |
| 20 | `DateOfDeposit` | `DATETIME` | Yes |  | Timestamp / Date field for DateOfDeposit |
| 21 | `PeriodEnding` | `DATETIME` | Yes |  | Timestamp / Date field for PeriodEnding |
| 22 | `Dummy` | `SMALLINT` | Yes |  | Integer identifier or enum code for Dummy |
| 23 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 24 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 25 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 26 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 27 | `D5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D5 |
| 28 | `BranchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for BranchCode |
| 29 | `ClearanceType` | `SMALLINT` | Yes |  | Integer identifier or enum code for ClearanceType |
| 30 | `NotificationAvailed` | `WCHAR(255.0)` | Yes |  | Text attribute: NotificationAvailed |
| 31 | `NotificationNo` | `WCHAR(255.0)` | Yes |  | Text attribute: NotificationNo |

---

<a name="table-tradingexcise"></a>

### Table: `TradingExcise`

> **Purpose:** First-stage and second-stage dealer excise registration and RG23D register tracking.

- **Row Count in Active FY:** `0`
- **Total Columns:** `53`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RefCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for RefCode |
| 2 | `Stamp` | `INTEGER (Long)` | Yes |  | Internal concurrency timestamp / modification revision stamp |
| 3 | `Method` | `SMALLINT` | Yes |  | Integer identifier or enum code for Method |
| 4 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 5 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 6 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 7 | `RefNo` | `WCHAR(25.0)` | Yes |  | Text attribute: RefNo |
| 8 | `PartyCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Customer or Vendor Party) |
| 9 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 10 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 11 | `ItemCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Inventory Item) |
| 12 | `Qty` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Qty |
| 13 | `Balance` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Balance |
| 14 | `Status` | `SMALLINT` | Yes |  | Integer identifier or enum code for Status |
| 15 | `AssValue` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for AssValue |
| 16 | `DutyRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for DutyRate |
| 17 | `DutyType` | `SMALLINT` | Yes |  | Integer identifier or enum code for DutyType |
| 18 | `DutyAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for DutyAmt |
| 19 | `DutyRate1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for DutyRate1 |
| 20 | `DutyType1` | `SMALLINT` | Yes |  | Integer identifier or enum code for DutyType1 |
| 21 | `DutyAmt1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for DutyAmt1 |
| 22 | `DutyRate2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for DutyRate2 |
| 23 | `DutyType2` | `SMALLINT` | Yes |  | Integer identifier or enum code for DutyType2 |
| 24 | `DutyAmt2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for DutyAmt2 |
| 25 | `DutyRate3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for DutyRate3 |
| 26 | `DutyType3` | `SMALLINT` | Yes |  | Integer identifier or enum code for DutyType3 |
| 27 | `DutyAmt3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for DutyAmt3 |
| 28 | `MfrQty` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for MfrQty |
| 29 | `MfrCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for MfrCode |
| 30 | `MfrBillNo` | `WCHAR(25.0)` | Yes |  | Text attribute: MfrBillNo |
| 31 | `MfrBillDate` | `DATETIME` | Yes |  | Timestamp / Date field for MfrBillDate |
| 32 | `RG23DPageNo` | `WCHAR(25.0)` | Yes |  | Text attribute: RG23DPageNo |
| 33 | `RG23DSrNo` | `WCHAR(25.0)` | Yes |  | Text attribute: RG23DSrNo |
| 34 | `AutoRG23DPageNo` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for AutoRG23DPageNo |
| 35 | `AutoRG23DSrNo` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for AutoRG23DSrNo |
| 36 | `SuppRG23DPageNo` | `WCHAR(25.0)` | Yes |  | Text attribute: SuppRG23DPageNo |
| 37 | `SuppRG23DSrNo` | `WCHAR(25.0)` | Yes |  | Text attribute: SuppRG23DSrNo |
| 38 | `MCCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for MCCode |
| 39 | `SuppAssValue` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SuppAssValue |
| 40 | `SuppDutyAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SuppDutyAmt |
| 41 | `SuppDutyAmt1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SuppDutyAmt1 |
| 42 | `SuppDutyAmt2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SuppDutyAmt2 |
| 43 | `SuppDutyAmt3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SuppDutyAmt3 |
| 44 | `CarryRefZeroQty` | `BOOLEAN` | No |  | Boolean flag for CarryRefZeroQty (True/False) |
| 45 | `MfrInvoicePrepDateTime` | `WCHAR(25.0)` | Yes |  | Text attribute: MfrInvoicePrepDateTime |
| 46 | `MfrGoodsRemovalDateTime` | `WCHAR(25.0)` | Yes |  | Text attribute: MfrGoodsRemovalDateTime |
| 47 | `ActualSuppAssValue` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ActualSuppAssValue |
| 48 | `ActualSuppDutyAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ActualSuppDutyAmt |
| 49 | `ActualSuppDutyAmt1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ActualSuppDutyAmt1 |
| 50 | `ActualSuppDutyAmt2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ActualSuppDutyAmt2 |
| 51 | `ActualSuppDutyAmt3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ActualSuppDutyAmt3 |
| 52 | `ActualSuppQty` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ActualSuppQty |
| 53 | `SuppOrgDetailsSpecified` | `BOOLEAN` | No |  | Boolean flag for SuppOrgDetailsSpecified (True/False) |

---

<a name="table-vatinfo"></a>

### Table: `VATInfo`

> **Purpose:** State VAT statutory return information and statutory annexures (prior to GST).

- **Row Count in Active FY:** `0`
- **Total Columns:** `22`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 2 | `Amount` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Amount |
| 3 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 4 | `Type` | `SMALLINT` | Yes |  | Integer identifier or enum code for Type |
| 5 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 6 | `Description` | `WCHAR(80.0)` | Yes |  | Text attribute: Description |
| 7 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 8 | `ChallanNo` | `WCHAR(40.0)` | Yes |  | Text attribute: ChallanNo |
| 9 | `ChallanDate` | `DATETIME` | Yes |  | Timestamp / Date field for ChallanDate |
| 10 | `ChequeNo` | `WCHAR(10.0)` | Yes |  | Text attribute: ChequeNo |
| 11 | `ChequeDate` | `DATETIME` | Yes |  | Timestamp / Date field for ChequeDate |
| 12 | `BankName` | `WCHAR(40.0)` | Yes |  | Text attribute: BankName |
| 13 | `BankCode` | `WCHAR(20.0)` | Yes |  | Text attribute: BankCode |
| 14 | `Interest` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Interest |
| 15 | `Penalty` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Penalty |
| 16 | `BankAcType` | `WCHAR(10.0)` | Yes |  | Text attribute: BankAcType |
| 17 | `BankAcNo` | `WCHAR(15.0)` | Yes |  | Text attribute: BankAcNo |
| 18 | `SurchargeAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeAmt |
| 19 | `SaleAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SaleAmt |
| 20 | `TaxPercent` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TaxPercent |
| 21 | `SurchargePercent` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargePercent |
| 22 | `PaymtToTaxFreePlanet` | `BOOLEAN` | No |  | Boolean flag for PaymtToTaxFreePlanet (True/False) |

---

<a name="table-vchvataccinfo"></a>

### Table: `VchVATAccInfo`

> **Purpose:** State VAT ledger account posting details.

- **Row Count in Active FY:** `0`
- **Total Columns:** `43`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `ItemCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Inventory Item) |
| 3 | `ItemSrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for ItemSrNo |
| 4 | `PartyCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Customer or Vendor Party) |
| 5 | `TaxCatCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for TaxCatCode |
| 6 | `STPTCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for STPTCode |
| 7 | `VchNo` | `WCHAR(255.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 8 | `VchSeriesCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchSeriesCode |
| 9 | `VchDate` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 10 | `VchType` | `SMALLINT` | Yes |  | Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote) |
| 11 | `HSNCode` | `WCHAR(255.0)` | Yes |  | Harmonized System of Nomenclature (HSN) or SAC code |
| 12 | `SENo` | `WCHAR(255.0)` | Yes |  | Text attribute: SENo |
| 13 | `PartyStateTinDigit` | `WCHAR(255.0)` | Yes |  | Text attribute: PartyStateTinDigit |
| 14 | `PartyStateCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for PartyStateCode |
| 15 | `BDStateTinDigit` | `WCHAR(255.0)` | Yes |  | Text attribute: BDStateTinDigit |
| 16 | `BDStateCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for BDStateCode |
| 17 | `TaxableAmt` | `DOUBLE` | Yes |  | Taxable net amount before taxes |
| 18 | `TaxRate` | `DOUBLE` | Yes |  | GST percentage rate (e.g. 18.0 for 18%) |
| 19 | `TaxRate1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TaxRate1 |
| 20 | `TaxAmt` | `DOUBLE` | Yes |  | Total GST tax amount calculated |
| 21 | `TaxAmt1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TaxAmt1 |
| 22 | `SurchargeRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeRate |
| 23 | `SurchargeAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeAmt |
| 24 | `ACessRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ACessRate |
| 25 | `ACessAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ACessAmt |
| 26 | `LocType` | `SMALLINT` | Yes |  | Integer identifier or enum code for LocType |
| 27 | `ZeroTaxType` | `SMALLINT` | Yes |  | Integer identifier or enum code for ZeroTaxType |
| 28 | `ActualSaleAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ActualSaleAmt |
| 29 | `TaxOnMRP` | `BOOLEAN` | No |  | Boolean flag for TaxOnMRP (True/False) |
| 30 | `ItemMainQty` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ItemMainQty |
| 31 | `ItemAltQty` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ItemAltQty |
| 32 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 33 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 34 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 35 | `OrgVchNo` | `WCHAR(255.0)` | Yes |  | Text attribute: OrgVchNo |
| 36 | `OrgVchDate` | `DATETIME` | Yes |  | Timestamp / Date field for OrgVchDate |
| 37 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 38 | `GSTRepBasis` | `SMALLINT` | Yes |  | Integer identifier or enum code for GSTRepBasis |
| 39 | `TypeOfDealer` | `SMALLINT` | Yes |  | Integer identifier or enum code for TypeOfDealer |
| 40 | `POSStateTinDigit` | `WCHAR(255.0)` | Yes |  | Text attribute: POSStateTinDigit |
| 41 | `POSStateCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for POSStateCode |
| 42 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 43 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |

---

<a name="table-vchvatsum"></a>

### Table: `VchVATSum`

> **Purpose:** Voucher-level VAT calculation summary.

- **Row Count in Active FY:** `0`
- **Total Columns:** `9`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `SaleAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SaleAmt |
| 3 | `TaxRate` | `DOUBLE` | Yes |  | GST percentage rate (e.g. 18.0 for 18%) |
| 4 | `TaxAmt` | `DOUBLE` | Yes |  | Total GST tax amount calculated |
| 5 | `SurchargeRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeRate |
| 6 | `SurchargeAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeAmt |
| 7 | `TaxType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TaxType |
| 8 | `ActualSaleAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ActualSaleAmt |
| 9 | `TaxOnMRP` | `BOOLEAN` | No |  | Boolean flag for TaxOnMRP (True/False) |

---

<a name="table-vchvatsumitemwise"></a>

### Table: `VchVATSumItemWise`

> **Purpose:** Item-level VAT calculation breakdown.

- **Row Count in Active FY:** `0`
- **Total Columns:** `11`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `ItemCode` | `INTEGER (Long)` | Yes |  | Foreign key to Master1.Code (Inventory Item) |
| 3 | `ItemSrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for ItemSrNo |
| 4 | `SaleAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SaleAmt |
| 5 | `TaxRate` | `DOUBLE` | Yes |  | GST percentage rate (e.g. 18.0 for 18%) |
| 6 | `TaxAmt` | `DOUBLE` | Yes |  | Total GST tax amount calculated |
| 7 | `SurchargeRate` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeRate |
| 8 | `SurchargeAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SurchargeAmt |
| 9 | `TaxType` | `SMALLINT` | Yes |  | Integer identifier or enum code for TaxType |
| 10 | `ActualSaleAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ActualSaleAmt |
| 11 | `TaxOnMRP` | `BOOLEAN` | No |  | Boolean flag for TaxOnMRP (True/False) |

---

<a name="table-ecomorderheader"></a>

### Table: `EComOrderHeader`

> **Purpose:** E-commerce marketplace orders (Amazon, Flipkart, Meesho) header data (Order ID, Order Date, Marketplace).

- **Row Count in Active FY:** `0`
- **Total Columns:** `8`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `Marketplace` | `SMALLINT` | Yes |  | Integer identifier or enum code for Marketplace |
| 3 | `EEMarketplaceID` | `SMALLINT` | Yes |  | Integer identifier or enum code for EEMarketplaceID |
| 4 | `OrderID` | `WCHAR(25.0)` | Yes |  | Text attribute: OrderID |
| 5 | `OrderDate` | `DATETIME` | Yes |  | Timestamp / Date field for OrderDate |
| 6 | `MPInvNo` | `WCHAR(25.0)` | Yes |  | Text attribute: MPInvNo |
| 7 | `MPInvDate` | `DATETIME` | Yes |  | Timestamp / Date field for MPInvDate |
| 8 | `JSONData` | `WCHAR` | Yes |  | Text attribute: JSONData |

---

<a name="table-ecomorderbody"></a>

### Table: `EComOrderBody`

> **Purpose:** E-commerce order line items, marketplace SKU mappings, order status, and returned quantities.

- **Row Count in Active FY:** `0`
- **Total Columns:** `7`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `OrderItemID` | `WCHAR(25.0)` | Yes |  | Text attribute: OrderItemID |
| 3 | `PhyQtyRcvd` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for PhyQtyRcvd |
| 4 | `PhyQtyStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for PhyQtyStatus |
| 5 | `PhyQtyRemarks` | `WCHAR(255.0)` | Yes |  | Text attribute: PhyQtyRemarks |
| 6 | `PhyQtyLastModifiedBy` | `WCHAR(255.0)` | Yes |  | Text attribute: PhyQtyLastModifiedBy |
| 7 | `PhyQtyLastModifiedDate` | `DATETIME` | Yes |  | Timestamp / Date field for PhyQtyLastModifiedDate |

---

<a name="table-ecomsettlement"></a>

### Table: `EcomSettlement`

> **Purpose:** Marketplace payment settlement reconciliation header (Settlement ID, settlement date, net amount credited).

- **Row Count in Active FY:** `0`
- **Total Columns:** `8`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `Marketplace` | `SMALLINT` | Yes |  | Integer identifier or enum code for Marketplace |
| 3 | `EEMarketplaceID` | `SMALLINT` | Yes |  | Integer identifier or enum code for EEMarketplaceID |
| 4 | `SettlementID` | `WCHAR(100.0)` | Yes |  | Text attribute: SettlementID |
| 5 | `EEPaymentID` | `WCHAR(100.0)` | Yes |  | Text attribute: EEPaymentID |
| 6 | `SettlementDate` | `DATETIME` | Yes |  | Timestamp / Date field for SettlementDate |
| 7 | `SettledAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SettledAmt |
| 8 | `jsonSum` | `WCHAR` | Yes |  | Text attribute: jsonSum |

---

<a name="table-ecomsettlementexp"></a>

### Table: `EcomSettlementExp`

> **Purpose:** Marketplace platform deductions (commission fees, shipping fees, closing fees, marketing fees).

- **Row Count in Active FY:** `0`
- **Total Columns:** `6`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Marketplace` | `SMALLINT` | Yes |  | Integer identifier or enum code for Marketplace |
| 2 | `EEMarketplaceID` | `SMALLINT` | Yes |  | Integer identifier or enum code for EEMarketplaceID |
| 3 | `SettlementID` | `WCHAR(100.0)` | Yes |  | Text attribute: SettlementID |
| 4 | `EEPaymentID` | `WCHAR(100.0)` | Yes |  | Text attribute: EEPaymentID |
| 5 | `ExpenseName` | `WCHAR(255.0)` | Yes |  | Text attribute: ExpenseName |
| 6 | `ExpenseAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ExpenseAmt |

---

<a name="table-ecomsettlementitem"></a>

### Table: `EcomSettlementItem`

> **Purpose:** Order-level payment settlement reconciliation within the marketplace remittance batch.

- **Row Count in Active FY:** `0`
- **Total Columns:** `20`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Marketplace` | `SMALLINT` | Yes |  | Integer identifier or enum code for Marketplace |
| 2 | `EEMarketplaceID` | `SMALLINT` | Yes |  | Integer identifier or enum code for EEMarketplaceID |
| 3 | `SettlementID` | `WCHAR(100.0)` | Yes |  | Text attribute: SettlementID |
| 4 | `EEPaymentID` | `WCHAR(100.0)` | Yes |  | Text attribute: EEPaymentID |
| 5 | `OrderID` | `WCHAR(100.0)` | Yes |  | Text attribute: OrderID |
| 6 | `OrderDate` | `DATETIME` | Yes |  | Timestamp / Date field for OrderDate |
| 7 | `OrderItemID` | `WCHAR(100.0)` | Yes |  | Text attribute: OrderItemID |
| 8 | `SaleAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SaleAmt |
| 9 | `RefundAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for RefundAmt |
| 10 | `Type` | `WCHAR(25.0)` | Yes |  | Text attribute: Type |
| 11 | `SettledAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SettledAmt |
| 12 | `TaxableExp` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TaxableExp |
| 13 | `CGSTAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for CGSTAmt |
| 14 | `SGSTAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for SGSTAmt |
| 15 | `IGSTAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for IGSTAmt |
| 16 | `TDSAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TDSAmt |
| 17 | `TCS_IGSTAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TCS_IGSTAmt |
| 18 | `TCS_CGSTAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TCS_CGSTAmt |
| 19 | `TCS_SGSTAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for TCS_SGSTAmt |
| 20 | `MiscInc` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for MiscInc |

---

<a name="table-ecomsettlementitemexp"></a>

### Table: `EcomSettlementItemExp`

> **Purpose:** Item-level fee deductions applied by the marketplace platform.

- **Row Count in Active FY:** `0`
- **Total Columns:** `9`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Marketplace` | `SMALLINT` | Yes |  | Integer identifier or enum code for Marketplace |
| 2 | `EEMarketplaceID` | `SMALLINT` | Yes |  | Integer identifier or enum code for EEMarketplaceID |
| 3 | `SettlementID` | `WCHAR(100.0)` | Yes |  | Text attribute: SettlementID |
| 4 | `EEPaymentID` | `WCHAR(100.0)` | Yes |  | Text attribute: EEPaymentID |
| 5 | `OrderID` | `WCHAR(100.0)` | Yes |  | Text attribute: OrderID |
| 6 | `OrderDate` | `DATETIME` | Yes |  | Timestamp / Date field for OrderDate |
| 7 | `OrderItemID` | `WCHAR(100.0)` | Yes |  | Text attribute: OrderItemID |
| 8 | `ExpenseName` | `WCHAR(255.0)` | Yes |  | Text attribute: ExpenseName |
| 9 | `ExpenseAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ExpenseAmt |

---

<a name="table-empladet"></a>

### Table: `EmpLADet`

> **Purpose:** Employee Loan and Advance disbursement and monthly payroll installment recovery schedule.

- **Row Count in Active FY:** `0`
- **Total Columns:** `8`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `EmpCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for EmpCode |
| 2 | `LAType` | `SMALLINT` | Yes |  | Integer identifier or enum code for LAType |
| 3 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 4 | `DueDate` | `DATETIME` | Yes |  | Timestamp / Date field for DueDate |
| 5 | `Amount` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Amount |
| 6 | `IntAmt` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for IntAmt |
| 7 | `Total` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Total |
| 8 | `Remarks` | `WCHAR(255.0)` | Yes |  | Text attribute: Remarks |

---

<a name="table-amcwarrdet"></a>

### Table: `AMCWarrDet`

> **Purpose:** Annual Maintenance Contract (AMC) and warranty tracking against sold equipment and appliances.

- **Row Count in Active FY:** `0`
- **Total Columns:** `15`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `VchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchCode |
| 2 | `SrNo` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for SrNo |
| 3 | `Rectype` | `SMALLINT` | Yes |  | Integer identifier or enum code for Rectype |
| 4 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 5 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 6 | `RefNo` | `WCHAR(25.0)` | Yes |  | Text attribute: RefNo |
| 7 | `ItemSerialNo` | `WCHAR(255.0)` | Yes |  | Text attribute: ItemSerialNo |
| 8 | `MasterCode1` | `INTEGER (Long)` | Yes |  | Primary Party/Account Foreign Key (Master1.Code) |
| 9 | `MasterCode2` | `INTEGER (Long)` | Yes |  | Secondary Account or Material Center Foreign Key (Master1.Code) |
| 10 | `Value1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for Value1 |
| 11 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 12 | `Narration` | `WCHAR(255.0)` | Yes |  | Text attribute: Narration |
| 13 | `ContEndDate` | `DATETIME` | Yes |  | Timestamp / Date field for ContEndDate |
| 14 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 15 | `Status` | `SMALLINT` | Yes |  | Integer identifier or enum code for Status |

---

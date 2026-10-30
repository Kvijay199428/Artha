#!/usr/bin/env python3
"""
Generate complete database schema documentation for BusyWin in d:\\VEGA\\ARTHA\\docs:
1. docs/BUSYWIN_DATABASE_SCHEMA.md (Master architecture, relationships, enums, core tables, mappings)
2. docs/busywin_schemas/01_COMPANY_DATABASE_db_bds.md (All 28 tables in db.bds)
3. docs/busywin_schemas/02_FY_MASTERS_AND_ACCOUNTS.md (13 Master tables in db1YYYY.bds)
4. docs/busywin_schemas/03_FY_TRANSACTIONS_AND_VOUCHERS.md (24 Transaction tables in db1YYYY.bds)
5. docs/busywin_schemas/04_FY_GST_AND_STATUTORY.md (25 GST & Statutory tables in db1YYYY.bds)
6. docs/busywin_schemas/05_FY_SYSTEM_AND_CONFIGURATION.md (18 System & Config tables in db1YYYY.bds)
"""

import os
import json

SCHEMA_FILE = 'd:\\VEGA\\ARTHA\\scripts\\busywin_db_schema.json'
DOCS_DIR = 'd:\\VEGA\\ARTHA\\docs'
SCHEMAS_DIR = os.path.join(DOCS_DIR, 'busywin_schemas')

os.makedirs(SCHEMAS_DIR, exist_ok=True)

with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
    schema = json.load(f)

db_bds = schema['db_bds']
fy_bds = schema['fy_bds']

# Table explanations mapping
TABLE_EXPLANATIONS = {
    # db.bds tables
    'BusyUserLog': 'Audit log recording user logins, logouts, terminal IDs, machine names, and session durations.',
    'Company': 'Master company profile storing firm legal name, trade name, address lines 1-4, contact info, PAN, GSTIN, CIN, currency, financial year range, books beginning date, decimal precision, and company-level accounting mode.',
    'CustomScripts': 'User-defined VBScript or SQL hooks executed on database events (e.g., before save, after save validation).',
    'DbImport': 'Mapping configurations and field parameters for importing data from legacy or third-party formats.',
    'DictionarySL': 'Custom spelling dictionary and regional language font translations used during voucher entry.',
    'FAQDatabase': 'Built-in knowledge base articles and operational FAQs accessible from the BusyWin UI.',
    'FAQGroup': 'Grouping and categorization definitions for FAQ topics.',
    'FormDetails': 'Voucher and document printing coordinate templates for continuous pre-printed stationery (dot matrix).',
    'GSTFilingStatusDet': 'Filing history of statutory GST returns (GSTR-1, GSTR-3B, GSTR-9) including ARN and filing dates.',
    'GSTStatusDet': 'GST portal taxpayer verification cache (Trade name, Legal name, Status: Active/Suspended/Cancelled).',
    'HSNStatusDet': 'Harmonized System of Nomenclature (HSN) and Service Accounting Code (SAC) validation and master cache.',
    'ImpNotes': 'System-wide important notes and critical business reminders shared across operators.',
    'MessageCentre': 'Internal messaging system between Busy operators within a LAN/WAN installation.',
    'MobileUser': 'Registered mobile devices, phone numbers, and authentication credentials for Busy Mobile App access.',
    'MobileUserPreference': 'Permissions, menu access rights, and data visibility rules for Busy Mobile App users.',
    'NMCategory': 'Notification categories (e.g., Payment Alerts, Low Stock Warnings, Tax Deadlines).',
    'NMNotes': 'Notification message bodies, alert text, and scheduled notification tasks.',
    'OfflineMessage': 'Outbox queue for SMS, WhatsApp, and email alerts waiting to be dispatched by the background worker.',
    'Patches': 'Version migration patch history applied to the global company database (db.bds).',
    'PrinterReps': 'Detailed report and invoice print format definitions (standard / advanced layouts, headers, margins, fonts).',
    'SQLQuery': 'Saved user SQL queries and custom report filters created through the interactive query designer.',
    'ScreenReps': 'User-customized grid display layouts (column order, widths, visibility) across data entry screens.',
    'StateCompanyDet': 'Multi-state GST branch company registrations under the unified company umbrella.',
    'StdNar': 'Standard narration master library for quick lookup and selection in voucher entry.',
    'UserControl': 'User credentials, passwords, security roles, and feature access permissions.',
    'UserLog': 'Audit trail tracking user operations (creation, modification, and deletion of masters and transactions).',
    'UserPreferences': 'Primary company configuration flags (Inventory, Bill-by-Bill, Multi-Currency, Batch/Expiry, Tax rules).',
    'UserPreferences1': 'Extended configuration parameters (E-Invoice, E-Way Bill credentials, Cloud backup settings).',

    # fy_bds tables
    # Masters & Accounts
    'Master1': 'Unified polymorphic master table storing all Accounts, Parties (Customers/Vendors), Inventory Items, Units of Measurement, Bill Sundries, Tax Categories, Price Levels, and Account/Item Groups.',
    'MasterAddressInfo': 'Extended contact information (Address lines 1-4, Phone, Mobile, Email, PAN, GSTIN, Station, Pincode) linked to Master1.Code.',
    'MasterSupport': 'Secondary metadata for masters including barcode mappings, custom user fields, and external ERP keys.',
    'MastFootPrint': 'Audit footprint for master entities (created by user, creation timestamp, modified by, modification timestamp).',
    'ItemDesc': 'Extended product description lines, technical specifications, and warranty terms printed on invoices.',
    'ItemParamDet': 'Parameterized stock attributes (Size, Color, Shade, Grade, Batch) for fashion/apparel/tile inventory.',
    'ItemSerialNo': 'Unique serial numbers / IMEI tracking for discrete inventory items with stock status (In Stock, Sold, Returned).',
    'ItemSNInstallDet': 'Installation, commissioning, and warranty details linked to serialized equipment and appliances.',
    'Folio1': 'Fast financial and stock balance summary cache storing opening balances, monthly debits/credits, and closing balances for instantaneous report rendering without scanning raw transactions.',
    'Help1': 'High-speed auto-complete search cache indexing master names, aliases, and parent groups for UI dropdown lookups.',
    'Help1AddnInfo': 'Secondary keyword index and alias search phrases supporting Help1 search acceleration.',
    'Help2': 'Lookup index for sub-entities, material centers (godowns), and cost centers.',
    'DeletedMasters': 'Audit tombstone register of deleted master entities preventing ID collision and maintaining audit integrity.',

    # Transactions & Vouchers
    'Tran1': 'Voucher header table recording transaction type (Sales, Purchase, Payment, Receipt), invoice number, date, party foreign key, net/gross amounts, cancellation flag, and voucher series.',
    'Tran2': 'Double-entry transaction line items recording both inventory line items (ItemCode, Quantity, Rate, Amount) AND financial ledger debit/credit postings.',
    'Tran3': 'Bill sundry line items attached to vouchers (Freight, Packing, Insurance, Trade Discount, Round Off).',
    'Tran4': 'Material center / Godown stock ledger tracking location-level inventory additions and deductions.',
    'Tran5': 'Serial number and batch allocations linked to line items in sales and purchase vouchers.',
    'Tran6': 'Job work / process manufacturing ledger tracking raw material issued versus finished goods received.',
    'Tran7': 'Cost center and project-level expense/revenue allocation records.',
    'Tran8': 'Pre-GST statutory sales tax / VAT declaration forms tracking (Form C, Form F, Form H, Form E1/E2).',
    'Tran9': 'Statutory form receipt and issuance settlement against individual sales and purchase bills.',
    'Tran10': 'Order processing linkage tracking Sales Order and Purchase Order commitments and pending delivery balances.',
    'Tran11': 'Delivery Challan and Goods Receipt Note (GRN) linkage to final sales/purchase invoices.',
    'Tran12': 'Voucher print audit log recording print count, user identity, and print timestamps.',
    'BillingDet': 'Consignee / Ship-to party name, dispatch address, destination state, GSTIN, transporter, and vehicle details.',
    'VchOtherInfo': 'Voucher optional user-defined fields (transporter, vehicle number, GR/LR number, payment terms, delivery date).',
    'DailySum': 'Daily financial and inventory aggregation cache for fast day-book and ledger rendering.',
    'DailyMessage': 'Automated notification and payment reminder messages scheduled on specific voucher due dates.',
    'BRSOpBal': 'Bank Reconciliation Statement (BRS) opening uncleared cheque balances carried forward from previous period.',
    'OrgSalePurc': 'Original invoice references for Credit Notes and Debit Notes (original invoice no, date, taxable value).',
    'POSDet': 'Point of Sale (POS) multi-tender payment breakdown (Cash, Credit/Debit Card, UPI, Cheque, Gift Voucher).',
    'PackingDetails': 'Packing slip and consignment details (box number, gross weight, net weight, dimensions, packaging unit).',
    'JobFinishedRefs': 'Finished goods batch reference generated from Bill of Materials (BOM) in production vouchers.',
    'PhyStkSubDet': 'Physical stock verification audit lines recording counted physical quantity versus book balance variance.',
    'VchTemplate': 'Reusable transaction templates for recurring monthly vouchers (Rent, Salaries, Subscriptions).',
    'VchTempTagging': 'Tagging rules and schedules linking vouchers to specific transaction templates.',

    # GST, Statutory & Tax
    'VchGSTSumItemWise': 'Item-level GST calculation summary recording HSN/SAC, taxable value, CGST/SGST/IGST rates and amounts, Cess, and place of supply state code.',
    'GSTInfo': 'General GST statutory register entries and manual tax adjustments (Reverse Charge Mechanism, Advance Received).',
    'GSTITCPendingVchDet': 'Input Tax Credit (ITC) pending / reversal tracking (Rule 37 180-day non-payment, Rule 42/43 capital goods reversals).',
    'GSTR1Info': 'GSTR-1 return filing snapshot data (B2B, B2CL, B2CS, CDNR, EXP, AT, HSN summary).',
    'GSTR2AInfo': 'GSTR-2A auto-drafted inward supplies statement downloaded from the GST Portal for supplier reconciliation.',
    'GSTR2BInfo': 'GSTR-2B static monthly ITC statement imported from the GST Portal.',
    'GSTR3BInfo': 'GSTR-3B monthly summary return calculation table (outward taxable supplies, eligible ITC, net tax payable).',
    'GetGeneratedEWayBillDet': 'E-Way Bill generation cache recording EWB Number, generation date, validity date, vehicle number, and status.',
    'TCS': 'Tax Collected at Source (Section 206C) register, collection rates, threshold limits, and challan details.',
    'TDS': 'Tax Deducted at Source (Section 194C, 194J, 194Q) register, deduction rates, certificate numbers, and challan links.',
    'STDet': 'Pre-GST Service Tax calculation details and abatement percentages.',
    'Excise': 'Central Excise invoice details, RG23A/PLA register entries, and assessable value records.',
    'TradingExcise': 'First-stage and second-stage dealer excise registration and RG23D register tracking.',
    'VATInfo': 'State VAT statutory return information and statutory annexures (prior to GST).',
    'VchVATAccInfo': 'State VAT ledger account posting details.',
    'VchVATSum': 'Voucher-level VAT calculation summary.',
    'VchVATSumItemWise': 'Item-level VAT calculation breakdown.',
    'EComOrderHeader': 'E-commerce marketplace orders (Amazon, Flipkart, Meesho) header data (Order ID, Order Date, Marketplace).',
    'EComOrderBody': 'E-commerce order line items, marketplace SKU mappings, order status, and returned quantities.',
    'EcomSettlement': 'Marketplace payment settlement reconciliation header (Settlement ID, settlement date, net amount credited).',
    'EcomSettlementExp': 'Marketplace platform deductions (commission fees, shipping fees, closing fees, marketing fees).',
    'EcomSettlementItem': 'Order-level payment settlement reconciliation within the marketplace remittance batch.',
    'EcomSettlementItemExp': 'Item-level fee deductions applied by the marketplace platform.',
    'EmpLADet': 'Employee Loan and Advance disbursement and monthly payroll installment recovery schedule.',
    'AMCWarrDet': 'Annual Maintenance Contract (AMC) and warranty tracking against sold equipment and appliances.',

    # System & Configuration
    'Config': 'Company financial year configuration repository (180+ feature flags, voucher numbering rules, series settings).',
    'Locks': 'Concurrency locking table preventing concurrent data corruption across multi-user network sessions.',
    'EventLog': 'System operational event log tracking voucher creation, modification, deletion, and print events with machine IP.',
    'DeletedInfo': 'Audit log of deleted transactions recording voucher number, date, original value, deleted by, and timestamp.',
    'QueryLog': 'Diagnostic SQL execution log recording slow queries and system database errors.',
    'DataSync': 'Multi-branch data synchronization journal recording packet IDs, sync timestamps, and replication status.',
    'CloudSyncStatus': 'Overall status of Busy Cloud data synchronization (bulk sync versus incremental sync state).',
    'CloudSyncIncr': 'Queue of incremental database changes pending upload to Busy Cloud.',
    'CloudSyncIncrDet': 'XML data payloads of incremental changes waiting to be replicated.',
    'CheckList': 'Task checklist items and audit approval state.',
    'CheckListNew': 'Workflow approval headers for multi-level voucher authorization hierarchies.',
    'CheckListNewDet': 'Workflow authorization signatures and approval payloads.',
    'RepColSize': 'User-customized column widths and display formats for financial statements and registers.',
    'RepOptValues': 'Saved report filter presets (date ranges, party selections, group filters).',
    'ReportNotes': 'User annotations and sticky notes attached to specific balance sheet and ledger reports.',
    'Patches': 'Version migration patch history applied to the operational database (db1YYYY.bds).',
    'ExternalData': 'Integration data bridge for external third-party software (CRM, WMS, eCommerce platforms).'
}

# Categorization for sub-documents
FY_CATEGORIES = {
    '02_FY_MASTERS_AND_ACCOUNTS.md': {
        'title': 'BusyWin FY Database: Masters & Accounts Schemas',
        'desc': 'Detailed table schemas and column definitions for all Master entities in db1YYYY.bds (Accounts, Parties, Items, Units, Descriptions, Balances).',
        'tables': ['Master1', 'MasterAddressInfo', 'MasterSupport', 'MastFootPrint', 'ItemDesc', 'ItemParamDet', 'ItemSerialNo', 'ItemSNInstallDet', 'Folio1', 'Help1', 'Help1AddnInfo', 'Help2', 'DeletedMasters']
    },
    '03_FY_TRANSACTIONS_AND_VOUCHERS.md': {
        'title': 'BusyWin FY Database: Transactions & Vouchers Schemas',
        'desc': 'Detailed table schemas and column definitions for all Voucher headers, Line items, Sundries, and Inventory journals in db1YYYY.bds.',
        'tables': ['Tran1', 'Tran2', 'Tran3', 'Tran4', 'Tran5', 'Tran6', 'Tran7', 'Tran8', 'Tran9', 'Tran10', 'Tran11', 'Tran12', 'BillingDet', 'VchOtherInfo', 'DailySum', 'DailyMessage', 'BRSOpBal', 'OrgSalePurc', 'POSDet', 'PackingDetails', 'JobFinishedRefs', 'PhyStkSubDet', 'VchTemplate', 'VchTempTagging']
    },
    '04_FY_GST_AND_STATUTORY.md': {
        'title': 'BusyWin FY Database: GST, Statutory & Tax Schemas',
        'desc': 'Detailed table schemas and column definitions for GST calculations, E-Way Bill, E-Commerce settlement, VAT, TDS/TCS, and Payroll in db1YYYY.bds.',
        'tables': ['VchGSTSumItemWise', 'GSTInfo', 'GSTITCPendingVchDet', 'GSTR1Info', 'GSTR2AInfo', 'GSTR2BInfo', 'GSTR3BInfo', 'GetGeneratedEWayBillDet', 'TCS', 'TDS', 'STDet', 'Excise', 'TradingExcise', 'VATInfo', 'VchVATAccInfo', 'VchVATSum', 'VchVATSumItemWise', 'EComOrderHeader', 'EComOrderBody', 'EcomSettlement', 'EcomSettlementExp', 'EcomSettlementItem', 'EcomSettlementItemExp', 'EmpLADet', 'AMCWarrDet']
    },
    '05_FY_SYSTEM_AND_CONFIGURATION.md': {
        'title': 'BusyWin FY Database: System & Configuration Schemas',
        'desc': 'Detailed table schemas and column definitions for internal Configuration, Concurrency Locks, Audit Logs, and Cloud Sync in db1YYYY.bds.',
        'tables': ['Config', 'Locks', 'EventLog', 'DeletedInfo', 'QueryLog', 'DataSync', 'CloudSyncStatus', 'CloudSyncIncr', 'CloudSyncIncrDet', 'CheckList', 'CheckListNew', 'CheckListNewDet', 'RepColSize', 'RepOptValues', 'ReportNotes', 'Patches', 'ExternalData']
    }
}

def format_table_markdown(tname, tinfo, explanation):
    md = []
    md.append(f"### Table: `{tname}`\n")
    md.append(f"> **Purpose:** {explanation}\n")
    md.append(f"- **Row Count in Active FY:** `{tinfo['row_count']}`")
    md.append(f"- **Total Columns:** `{len(tinfo['columns'])}`")
    pk_str = ', '.join([f"`{k}`" for k in tinfo['primary_keys']]) if tinfo['primary_keys'] else "*None defined (surrogate or multi-column indexed)*"
    md.append(f"- **Primary Key:** {pk_str}\n")
    
    md.append("| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |")
    md.append("|---|-------------|-----------|:--------:|:-----------:|-----------------------|")
    
    for c in tinfo['columns']:
        pos = int(c['pos'])
        cname = c['name']
        ctype = c['type']
        null_str = "Yes" if c['nullable'] else "No"
        pk_str = "**PK**" if c['is_pk'] else ""
        
        # Infer column description from common conventions
        desc = infer_col_desc(tname, cname, ctype)
        md.append(f"| {pos} | `{cname}` | `{ctype}` | {null_str} | {pk_str} | {desc} |")
        
    md.append("\n---\n")
    return '\n'.join(md)

def infer_col_desc(tname, cname, ctype):
    # Specialized mappings for key columns
    if cname == 'Code' and tname == 'Master1':
        return 'Unique Master ID (Primary Key for all accounts, items, groups, units)'
    if cname == 'MasterType':
        return 'Polymorphic Entity Type enum (1=AccountGroup, 2=Account, 6=Item, 8=Unit, 9=BillSundry, 21=TaxCategory)'
    if cname == 'ParentGrp':
        return 'Foreign key to parent Master1.Code (Account Group or Item Group)'
    if cname == 'VchCode' and tname in ('Tran1', 'Tran2', 'VchGSTSumItemWise', 'BillingDet'):
        return 'Unique Voucher Transaction ID (Primary Key in Tran1, Foreign Key in others)'
    if cname == 'VchType':
        return 'Voucher classification enum (1=Payment, 2=Purchase, 3=Receipt, 9=Sales, 18=CreditNote)'
    if cname == 'VchNo':
        return 'User-facing invoice / voucher series number string (e.g. HPS00001)'
    if cname == 'Date' or cname == 'VchDate':
        return 'Transaction / Voucher Date'
    if cname == 'MasterCode1':
        return 'Primary Party/Account Foreign Key (Master1.Code)'
    if cname == 'MasterCode2':
        return 'Secondary Account or Material Center Foreign Key (Master1.Code)'
    if cname == 'HSNCode':
        return 'Harmonized System of Nomenclature (HSN) or SAC code'
    if cname == 'TaxableAmt':
        return 'Taxable net amount before taxes'
    if cname == 'TaxRate':
        return 'GST percentage rate (e.g. 18.0 for 18%)'
    if cname == 'TaxAmt':
        return 'Total GST tax amount calculated'
    if cname == 'VchSalePurcAmt':
        return 'Net taxable invoice total before bill sundries'
    if cname == 'VchAmtBaseCur':
        return 'Gross invoice total payable in company base currency'
    if cname == 'VchCancelled':
        return 'Boolean flag indicating whether voucher was cancelled (1=Cancelled)'
    if cname == 'ItemCode':
        return 'Foreign key to Master1.Code (Inventory Item)'
    if cname == 'PartyCode':
        return 'Foreign key to Master1.Code (Customer or Vendor Party)'
    if cname == 'Value1' and tname == 'Tran2':
        return 'Item Quantity (for inventory lines) or Ledger Debit Amount'
    if cname == 'Value2' and tname == 'Tran2':
        return 'Unit Price / Rate per unit'
    if cname == 'Value3' and tname == 'Tran2':
        return 'Total item line amount (Quantity * Rate) before taxes'
    if cname == 'RecType':
        return 'Record discriminator enum distinguishing line types'
    if cname == 'Address1' or cname == 'Address2' or cname == 'Address3' or cname == 'Address4':
        return 'Postal address line'
    if cname == 'ITPAN':
        return 'Income Tax Permanent Account Number (PAN)'
    if cname == 'GSTIN' or cname == 'CompGSTIN':
        return '15-digit Goods and Services Tax Identification Number'
    if cname == 'Mobile' or cname == 'MobileNo':
        return 'Primary contact mobile telephone number'
    if cname == 'Email':
        return 'Official email address for communication and e-invoicing'
    if cname == 'TelNo':
        return 'Fixed-line landline telephone number'
    if cname.startswith('CM'):
        return f'Configurable master foreign key {cname} (links to Master1.Code based on MasterType)'
    if cname.startswith('D') and tname in ('Master1', 'Folio1', 'Tran4'):
        return f'Pre-allocated double numeric parameter / balance accumulator {cname}'
    if cname.startswith('B') and tname in ('UserPreferences', 'Config'):
        return f'Feature toggle boolean flag {cname}'
    if cname == 'Nar1' or cname == 'Nar2':
        return 'Voucher narration / remarks text'
    if cname == 'ShortNar':
        return 'Brief line-item narration or ledger remark'
    if cname == 'EWayBillNo':
        return '12-digit government E-Way Bill Number'
    if cname == 'EWayBillDate':
        return 'Date and time of E-Way Bill generation'
    if cname == 'Stamp':
        return 'Internal concurrency timestamp / modification revision stamp'
    if cname == 'UserName':
        return 'Operator username who performed the action'
    
    # Generic description based on column name and type
    if 'DATE' in ctype:
        return f'Timestamp / Date field for {cname}'
    elif 'BOOLEAN' in ctype:
        return f'Boolean flag for {cname} (True/False)'
    elif 'CURRENCY' in ctype or 'DOUBLE' in ctype or 'NUMERIC' in ctype:
        return f'Numeric monetary / quantity value for {cname}'
    elif 'INTEGER' in ctype or 'SMALLINT' in ctype:
        return f'Integer identifier or enum code for {cname}'
    elif 'MEMO' in ctype:
        return f'Extended multiline text or JSON/XML payload for {cname}'
    else:
        return f'Text attribute: {cname}'

# 1. Generate 01_COMPANY_DATABASE_db_bds.md
print("Generating 01_COMPANY_DATABASE_db_bds.md...")
md_comp = []
md_comp.append("# BusyWin Company Database Schema (`db.bds`)\n")
md_comp.append("> **Location:** `C:\\BusyWin\\DATA\\COMP0001\\db.bds` (or respective company folder)\n")
md_comp.append("> **Engine:** Microsoft Jet 4.0 / Access (`Microsoft.ACE.OLEDB.12.0`)\n")
md_comp.append("> **Encryption Password:** `ILoveMyINDIA`\n")
md_comp.append("> **Total Tables:** 28 | **Total Columns:** 1,174\n\n")
md_comp.append("The Company Database (`db.bds`) resides at the root of each company directory and stores **global company settings, multi-state GST profiles, user permissions, audit logs, printing templates, and custom scripts**. Unlike financial year databases (`db1YYYY.bds`), `db.bds` is shared across all accounting years for that enterprise.\n\n")
md_comp.append("## Table Summary Index\n\n")
md_comp.append("| # | Table Name | Columns | Active Rows | Primary Role |")
md_comp.append("|---|------------|:-------:|:-----------:|--------------|")

for idx, tname in enumerate(sorted(db_bds.keys()), 1):
    info = db_bds[tname]
    exp = TABLE_EXPLANATIONS.get(tname, 'Company configuration table')
    md_comp.append(f"| {idx} | [`{tname}`](#table-{tname.lower()}) | {len(info['columns'])} | {info['row_count']} | {exp} |")

md_comp.append("\n---\n\n## Complete Table Schemas\n\n")

for tname in sorted(db_bds.keys()):
    info = db_bds[tname]
    exp = TABLE_EXPLANATIONS.get(tname, 'Company configuration table')
    md_comp.append(f"<a name=\"table-{tname.lower()}\"></a>\n")
    md_comp.append(format_table_markdown(tname, info, exp))

with open(os.path.join(SCHEMAS_DIR, '01_COMPANY_DATABASE_db_bds.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_comp))

# 2. Generate FY Sub-documents
for fname, cat_info in FY_CATEGORIES.items():
    print(f"Generating {fname}...")
    md_cat = []
    md_cat.append(f"# {cat_info['title']}\n")
    md_cat.append(f"> **Database File:** `db1<YYYY>.bds` (e.g. `C:\\BusyWin\\DATA\\COMP0001\\db12026.bds`)\n")
    md_cat.append(f"> **Engine:** Microsoft Jet 4.0 / Access OLEDB (`ILoveMyINDIA`)\n")
    md_cat.append(f"> **Description:** {cat_info['desc']}\n\n")
    
    md_cat.append("## Tables in this Module\n\n")
    md_cat.append("| # | Table Name | Columns | Active Rows | Primary Key | Description |")
    md_cat.append("|---|------------|:-------:|:-----------:|:-----------:|-------------|")
    
    cat_tables = [t for t in cat_info['tables'] if t in fy_bds]
    for idx, tname in enumerate(cat_tables, 1):
        info = fy_bds[tname]
        exp = TABLE_EXPLANATIONS.get(tname, 'Operational table')
        pk_str = ', '.join(info['primary_keys']) if info['primary_keys'] else "-"
        md_cat.append(f"| {idx} | [`{tname}`](#table-{tname.lower()}) | {len(info['columns'])} | {info['row_count']} | `{pk_str}` | {exp} |")
        
    md_cat.append("\n---\n\n## Detailed Column Schemas\n\n")
    
    for tname in cat_tables:
        info = fy_bds[tname]
        exp = TABLE_EXPLANATIONS.get(tname, 'Operational table')
        md_cat.append(f"<a name=\"table-{tname.lower()}\"></a>\n")
        md_cat.append(format_table_markdown(tname, info, exp))
        
    with open(os.path.join(SCHEMAS_DIR, fname), 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_cat))

print("All modular documents generated successfully!")


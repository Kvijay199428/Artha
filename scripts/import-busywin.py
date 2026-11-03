#!/usr/bin/env python3
"""
BusyWin to ARTHA Data Importer
Extracts Company Profile, Units, Inventory Products, Clients/Parties, 
Sales Invoices, and Purchase Bills from BusyWin Jet/Access database (C:\\BusyWin\\DATA)
into ARTHA structured data directory (./data).
"""

import os
import sys
import json
import argparse
import re
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

try:
    import win32com.client
except ImportError:
    print("Error: pywin32 is required. Run 'pip install pywin32' or run with system python.")
    sys.exit(1)

PASSWORD = 'ILoveMyINDIA'

GST_STATE_CODES = {
    "01": "Jammu & Kashmir", "02": "Himachal Pradesh", "03": "Punjab", "04": "Chandigarh",
    "05": "Uttarakhand", "06": "Haryana", "07": "Delhi", "08": "Rajasthan", "09": "Uttar Pradesh",
    "10": "Bihar", "11": "Sikkim", "12": "Arunachal Pradesh", "13": "Nagaland", "14": "Manipur",
    "15": "Mizoram", "16": "Tripura", "17": "Meghalaya", "18": "Assam", "19": "West Bengal",
    "20": "Jharkhand", "21": "Odisha", "22": "Chhattisgarh", "23": "Madhya Pradesh", "24": "Gujarat",
    "26": "Dadra & Nagar Haveli and Daman & Diu", "27": "Maharashtra", "29": "Karnataka", "30": "Goa",
    "31": "Lakshadweep", "32": "Kerala", "33": "Tamil Nadu", "34": "Puducherry", "35": "Andaman & Nicobar",
    "36": "Telangana", "37": "Andhra Pradesh", "38": "Ladakh"
}

def safe_filename(name):
    return "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in str(name))

def open_db(db_path):
    conn = win32com.client.Dispatch('ADODB.Connection')
    connStr = f'Provider=Microsoft.ACE.OLEDB.12.0;Data Source={db_path};Jet OLEDB:Database Password={PASSWORD};'
    conn.Open(connStr)
    return conn

def import_busywin(busy_data_dir, artha_data_dir, comp_folder="COMP0001", dry_run=False):
    company_path = os.path.join(busy_data_dir, comp_folder)
    if not os.path.exists(company_path):
        print(f"Error: Company directory not found: {company_path}")
        return False

    main_db = os.path.join(company_path, "db.bds")
    if not os.path.exists(main_db):
        print(f"Error: Main company database not found: {main_db}")
        return False

    print("=" * 65)
    print(f"  BusyWin to ARTHA Data Importer")
    print(f"  Source Database : {company_path}")
    print(f"  Target ARTHA Dir: {artha_data_dir}")
    print(f"  Dry Run Mode    : {dry_run}")
    print("=" * 65)

    # Ensure ARTHA subdirectories exist
    for sub in ['bills', 'clients', 'products', 'purchases', 'profiles', 'templates']:
        os.makedirs(os.path.join(artha_data_dir, sub), exist_ok=True)

    # 1. Company Profile
    print("\n[1/5] Extracting Company Profile...")
    conn_main = open_db(main_db)
    rs_comp, _ = conn_main.Execute('SELECT * FROM Company')
    comp_row = {f.Name: f.Value for f in rs_comp.Fields}
    conn_main.Close()

    comp_name = (comp_row.get('Name') or '').strip()
    gstin = (comp_row.get('GSTNo') or '').strip()
    pan = (comp_row.get('ITPAN') or '').strip()
    phone = (comp_row.get('TelNo') or comp_row.get('VATMobileNo') or '').strip()
    email = (comp_row.get('Email') or comp_row.get('VATEmail') or '').strip()
    pin = (comp_row.get('Pincode') or '').strip()
    
    addr_parts = [
        (comp_row.get('Address1') or '').strip(),
        (comp_row.get('Address2') or '').strip(),
        (comp_row.get('Address3') or '').strip(),
        (comp_row.get('Address4') or '').strip()
    ]
    addr = ", ".join([p for p in addr_parts if p])
    state_code = gstin[:2] if len(gstin) >= 2 and gstin[:2].isdigit() else "06"
    state = GST_STATE_CODES.get(state_code, "Haryana")

    # Load existing profile to preserve logo/signature if present
    profile_path = os.path.join(artha_data_dir, "profile.json")
    existing_profile = {}
    if os.path.exists(profile_path):
        try:
            with open(profile_path, 'r', encoding='utf-8') as pf:
                existing_profile = json.load(pf)
        except Exception:
            pass

    profile = {
        **existing_profile,
        "businessName": comp_name,
        "address": addr or existing_profile.get("address", ""),
        "city": (comp_row.get('City') or existing_profile.get("city", "Faridabad")).strip(),
        "pin": pin or existing_profile.get("pin", ""),
        "state": state,
        "country": "India",
        "gstin": gstin,
        "pan": pan or (gstin[2:12] if len(gstin) >= 12 else ""),
        "email": email or existing_profile.get("email", ""),
        "phone": phone or existing_profile.get("phone", ""),
    }

    if not dry_run:
        with open(profile_path, 'w', encoding='utf-8') as pf:
            json.dump(profile, pf, indent=2, ensure_ascii=False)
        # Also copy to profiles/default.json
        with open(os.path.join(artha_data_dir, 'profiles', 'default.json'), 'w', encoding='utf-8') as pf:
            json.dump(profile, pf, indent=2, ensure_ascii=False)

    print(f"  [OK] Company Profile: {comp_name} (GSTIN: {gstin}, State: {state})")

    # Determine latest FY DB for master tables
    fy_files = sorted([f for f in os.listdir(company_path) if f.startswith('db1') and f.endswith('.bds')])
    latest_fy_db = os.path.join(company_path, fy_files[-1] if fy_files else "db.bds")
    print(f"  Loading master dictionaries from: {os.path.basename(latest_fy_db)}")

    conn_master = open_db(latest_fy_db)

    # 2. Units of Measurement
    print("\n[2/5] Extracting Units of Measurement...")
    units_map = {}
    rs_units, _ = conn_master.Execute('SELECT Code, Name, PrintName FROM Master1 WHERE MasterType = 8')
    while not rs_units.EOF:
        u_code = rs_units.Fields.Item('Code').Value
        u_name = (rs_units.Fields.Item('Name').Value or '').strip()
        units_map[u_code] = u_name
        rs_units.MoveNext()
    print(f"  [OK] Found {len(units_map)} units ({', '.join(list(units_map.values())[:6])}...)")

    # 3. Inventory / Products
    print("\n[3/5] Extracting Products & Inventory Items...")
    products = []
    rs_items, _ = conn_master.Execute('SELECT Code, Name, PrintName, HSNCode, CM1, D1, D3, D4 FROM Master1 WHERE MasterType = 6 ORDER BY Code')
    while not rs_items.EOF:
        code = rs_items.Fields.Item('Code').Value
        name = (rs_items.Fields.Item('Name').Value or '').strip()
        desc = (rs_items.Fields.Item('PrintName').Value or name).strip()
        hsn = (rs_items.Fields.Item('HSNCode').Value or '').strip()
        unit_code = rs_items.Fields.Item('CM1').Value
        unit = units_map.get(unit_code, 'Pcs')
        # Standardise unit labels for ARTHA
        if unit.lower() in ('pcs.', 'pcs'): unit = 'Pcs'
        elif unit.lower() in ('sqft', 'sq.ft'): unit = 'Sq.ft'
        elif unit.lower() in ('kgs.', 'kg', 'kgs'): unit = 'Kg'
        elif unit.lower() in ('gms.', 'g', 'gms'): unit = 'g'
        elif unit.lower() in ('foot', 'ft'): unit = 'Ft'
        elif unit.lower() in ('rft', 'mtr', 'metre'): unit = 'Mtr'

        selling_price = float(rs_items.Fields.Item('D3').Value or 0)
        purchase_price = float(rs_items.Fields.Item('D4').Value or 0)

        prod_id = f"prod_{code}"
        prod_obj = {
            "id": prod_id,
            "name": name,
            "description": desc,
            "hsn": hsn or "998891",
            "unit": unit,
            "sellingPrice": selling_price,
            "purchasePrice": purchase_price,
            "taxPercent": 18,
            "stock": 0
        }
        products.append(prod_obj)

        if not dry_run:
            prod_file = os.path.join(artha_data_dir, 'products', f"{safe_filename(prod_id)}.json")
            with open(prod_file, 'w', encoding='utf-8') as pf:
                json.dump(prod_obj, pf, indent=2, ensure_ascii=False)

        rs_items.MoveNext()

    print(f"  [OK] Imported {len(products)} products into ARTHA Inventory.")

    # 4. Clients / Accounts
    print("\n[4/5] Extracting Clients & Parties...")
    clients_map = {}
    clients_imported = 0
    rs_clients, _ = conn_master.Execute('''
        SELECT m.Code, m.Name, m.ParentGrp, a.Address1, a.Address2, a.Address3, a.Address4, 
               a.Mobile, a.TelNo, a.Email, a.GSTNo, a.ITPAN, a.PINCode, a.StateCodeLong
        FROM Master1 m LEFT JOIN MasterAddressInfo a ON m.Code = a.MasterCode 
        WHERE m.MasterType = 2 ORDER BY m.Code
    ''')
    while not rs_clients.EOF:
        code = rs_clients.Fields.Item('Code').Value
        name = (rs_clients.Fields.Item('Name').Value or '').strip()
        parent_grp = rs_clients.Fields.Item('ParentGrp').Value
        gstin_client = (rs_clients.Fields.Item('GSTNo').Value or '').strip()
        pan_client = (rs_clients.Fields.Item('ITPAN').Value or '').strip()
        mobile = (rs_clients.Fields.Item('Mobile').Value or rs_clients.Fields.Item('TelNo').Value or '').strip()
        email_client = (rs_clients.Fields.Item('Email').Value or '').strip()
        pincode = (rs_clients.Fields.Item('PINCode').Value or '').strip()

        addr_parts = [
            (rs_clients.Fields.Item('Address1').Value or '').strip(),
            (rs_clients.Fields.Item('Address2').Value or '').strip(),
            (rs_clients.Fields.Item('Address3').Value or '').strip(),
            (rs_clients.Fields.Item('Address4').Value or '').strip()
        ]
        addr = ", ".join([p for p in addr_parts if p])

        st_code = gstin_client[:2] if len(gstin_client) >= 2 and gstin_client[:2].isdigit() else "06"
        st_name = GST_STATE_CODES.get(st_code, "Haryana")

        client_id = f"cli_{code}"
        client_obj = {
            "id": client_id,
            "name": name,
            "address": addr,
            "city": "",
            "state": st_name,
            "stateCode": st_code,
            "pin": pincode,
            "gstin": gstin_client,
            "pan": pan_client or (gstin_client[2:12] if len(gstin_client) >= 12 else ""),
            "phone": mobile,
            "email": email_client
        }
        clients_map[code] = client_obj

        # Filter out system internal accounts like Cash, Profit & Loss, Sales, Purchase
        # System accounts generally have code <= 20 and no address/GSTIN
        if code > 20 or gstin_client or addr:
            clients_imported += 1
            if not dry_run:
                client_file = os.path.join(artha_data_dir, 'clients', f"{safe_filename(client_id)}.json")
                with open(client_file, 'w', encoding='utf-8') as cf:
                    json.dump(client_obj, cf, indent=2, ensure_ascii=False)

        rs_clients.MoveNext()

    conn_master.Close()
    print(f"  [OK] Imported {clients_imported} clients/parties into ARTHA Contacts.")

    # 5. Transactions: Sales Invoices & Purchases across all FY databases
    print("\n[5/5] Extracting Sales Invoices & Purchases...")
    sales_invoices = []
    purchase_bills = []
    seen_invoice_numbers = set()

    for fy_file in fy_files:
        fy_path = os.path.join(company_path, fy_file)
        # Determine financial year label, e.g. db12024 -> 2024-25
        fy_year = fy_file.replace("db1", "").replace(".bds", "")
        fy_label = f"{fy_year}-{str(int(fy_year)+1)[-2:]}" if fy_year.isdigit() else ""

        print(f"  Scanning {fy_file} (FY {fy_label})...")
        conn_fy = open_db(fy_path)

        # A) Sales Invoices (VchType = 9)
        rs_sales, _ = conn_fy.Execute('SELECT VchCode, VchNo, Date, MasterCode1, VchSalePurcAmt, VchAmtBaseCur, VchCancelled FROM Tran1 WHERE VchType = 9 ORDER BY Date, VchCode')
        while not rs_sales.EOF:
            vch_code = rs_sales.Fields.Item('VchCode').Value
            raw_vch_no = (rs_sales.Fields.Item('VchNo').Value or '').strip()
            date_val = rs_sales.Fields.Item('Date').Value
            iso_date = str(date_val)[:10] if date_val else "2026-04-01"
            party_code = rs_sales.Fields.Item('MasterCode1').Value
            subtotal = float(rs_sales.Fields.Item('VchSalePurcAmt').Value or 0)
            total = float(rs_sales.Fields.Item('VchAmtBaseCur').Value or 0)
            cancelled = bool(rs_sales.Fields.Item('VchCancelled').Value)

            # Skip 0 amount dummy entries
            if total <= 0 and subtotal <= 0:
                rs_sales.MoveNext()
                continue

            # Ensure unique invoice number across FYs if duplicate
            final_inv_no = raw_vch_no
            if final_inv_no in seen_invoice_numbers:
                final_inv_no = f"{raw_vch_no}/{fy_label}"
            seen_invoice_numbers.add(final_inv_no)

            # Fetch line items from VchGSTSumItemWise
            rs_items, _ = conn_fy.Execute(f'''
                SELECT ItemCode, HSNCode, TaxableAmt, TaxRate, TaxAmt, ItemMainQty, GSTIN
                FROM VchGSTSumItemWise 
                WHERE VchType = 9 AND VchCode = {vch_code}
            ''')
            line_items = []
            idx = 1
            calc_taxable = 0.0
            calc_tax = 0.0

            # Match items or fallback to Tran2
            while not rs_items.EOF:
                i_code = rs_items.Fields.Item('ItemCode').Value
                i_hsn = (rs_items.Fields.Item('HSNCode').Value or '').strip()
                i_taxable = float(rs_items.Fields.Item('TaxableAmt').Value or 0)
                i_rate = float(rs_items.Fields.Item('TaxRate').Value or 18)
                i_tax = float(rs_items.Fields.Item('TaxAmt').Value or 0)
                i_qty = float(rs_items.Fields.Item('ItemMainQty').Value or 1)
                if i_qty <= 0: i_qty = 1.0

                item_match = next((p for p in products if p['id'] == f"prod_{i_code}"), None)
                item_name = item_match['name'] if item_match else f"Item #{i_code}"
                unit = item_match['unit'] if item_match else 'Pcs'
                unit_price = round(i_taxable / i_qty, 2)

                line_items.append({
                    "id": str(idx),
                    "name": item_name,
                    "description": item_name,
                    "hsn": i_hsn or (item_match['hsn'] if item_match else "998891"),
                    "qty": i_qty,
                    "unit": unit,
                    "price": unit_price,
                    "discountPercent": 0,
                    "taxPercent": i_rate,
                    "taxAmount": i_tax,
                    "total": round(i_taxable + i_tax, 2)
                })
                calc_taxable += i_taxable
                calc_tax += i_tax
                idx += 1
                rs_items.MoveNext()

            # If no VchGSTSumItemWise rows (e.g. non-GST items), build fallback line item
            if not line_items:
                line_items.append({
                    "id": "1",
                    "name": "General Sales",
                    "description": "General Sales",
                    "hsn": "998891",
                    "qty": 1,
                    "unit": "Pcs",
                    "price": subtotal or total,
                    "discountPercent": 0,
                    "taxPercent": 18 if total > subtotal else 0,
                    "taxAmount": round(total - subtotal, 2) if total > subtotal else 0,
                    "total": total
                })
                calc_taxable = subtotal or total
                calc_tax = round(total - subtotal, 2) if total > subtotal else 0

            client_info = clients_map.get(party_code, {
                "id": f"cli_{party_code}",
                "name": "Cash",
                "address": "",
                "state": "Haryana",
                "stateCode": "06",
                "gstin": ""
            })

            # Calculate CGST/SGST vs IGST
            is_intrastate = (client_info.get("stateCode") == "06")
            cgst = round(calc_tax / 2.0, 2) if is_intrastate else 0.0
            sgst = round(calc_tax / 2.0, 2) if is_intrastate else 0.0
            igst = 0.0 if is_intrastate else round(calc_tax, 2)
            round_off = round(total - (calc_taxable + calc_tax), 2)

            bill_data = {
                "id": final_inv_no,
                "clientName": client_info.get("name"),
                "invoiceNumber": final_inv_no,
                "invoiceDate": iso_date,
                "dueDate": iso_date,
                "invoiceType": "tax-invoice",
                "currency": "INR",
                "totalAmount": total,
                "totalTaxAmount": calc_tax,
                "status": "cancelled" if cancelled else "paid",
                "paidAmount": 0 if cancelled else total,
                "payments": [] if cancelled else [{
                    "id": f"pmt_{final_inv_no}",
                    "date": iso_date,
                    "amount": total,
                    "mode": "Bank",
                    "note": "Imported from BusyWin"
                }],
                "printedCount": 1,
                "lastPrintedAt": None,
                "data": {
                    "profile": profile,
                    "client": client_info,
                    "details": {
                        "invoiceNumber": final_inv_no,
                        "invoiceDate": iso_date,
                        "dueDate": iso_date,
                        "placeOfSupply": client_info.get("state", "Haryana")
                    },
                    "items": line_items,
                    "totals": {
                        "subtotal": round(calc_taxable, 2),
                        "cgst": cgst,
                        "sgst": sgst,
                        "igst": igst,
                        "roundOff": round_off,
                        "total": total
                    },
                    "invoiceType": "tax-invoice",
                    "customTerms": "",
                    "customNotes": "Imported from BusyWin Accounting",
                    "extraSections": [],
                    "invoiceOptions": {
                        "showGST": True,
                        "showLogo": True,
                        "currency": "INR"
                    },
                    "taxInclusive": False
                }
            }
            sales_invoices.append(bill_data)

            if not dry_run:
                bill_file = os.path.join(artha_data_dir, 'bills', f"{safe_filename(final_inv_no)}.json")
                with open(bill_file, 'w', encoding='utf-8') as bf:
                    json.dump(bill_data, bf, indent=2, ensure_ascii=False)

            rs_sales.MoveNext()

        # B) Purchase Bills (VchType = 2)
        rs_purc, _ = conn_fy.Execute('SELECT VchCode, VchNo, Date, MasterCode1, VchAmtBaseCur FROM Tran1 WHERE VchType = 2 ORDER BY Date, VchCode')
        while not rs_purc.EOF:
            v_code = rs_purc.Fields.Item('VchCode').Value
            purc_no = (rs_purc.Fields.Item('VchNo').Value or '').strip()
            purc_date = rs_purc.Fields.Item('Date').Value
            purc_iso = str(purc_date)[:10] if purc_date else "2026-04-01"
            supp_code = rs_purc.Fields.Item('MasterCode1').Value
            purc_tot = float(rs_purc.Fields.Item('VchAmtBaseCur').Value or 0)

            supplier_info = clients_map.get(supp_code, {"name": f"Supplier #{supp_code}"})

            purc_obj = {
                "id": purc_no,
                "billNumber": purc_no,
                "billDate": purc_iso,
                "vendorName": supplier_info.get("name"),
                "vendorGstin": supplier_info.get("gstin", ""),
                "totalAmount": purc_tot,
                "status": "paid",
                "notes": f"Imported from BusyWin FY {fy_label}"
            }
            purchase_bills.append(purc_obj)

            if not dry_run:
                purc_file = os.path.join(artha_data_dir, 'purchases', f"{safe_filename(purc_no)}.json")
                with open(purc_file, 'w', encoding='utf-8') as pf:
                    json.dump(purc_obj, pf, indent=2, ensure_ascii=False)

            rs_purc.MoveNext()

        conn_fy.Close()

    print(f"  [OK] Imported {len(sales_invoices)} Sales Invoices across all years.")
    print(f"  [OK] Imported {len(purchase_bills)} Purchase Bills across all years.")

    # Update metadata
    if not dry_run:
        meta_path = os.path.join(artha_data_dir, "meta.json")
        meta = {}
        if os.path.exists(meta_path):
            try:
                with open(meta_path, 'r', encoding='utf-8') as mf:
                    meta = json.load(mf)
            except Exception:
                pass
        meta["lastBusyWinImport"] = {
            "at": datetime.now().isoformat(),
            "company": comp_name,
            "folder": comp_folder,
            "productsCount": len(products),
            "clientsCount": clients_imported,
            "invoicesCount": len(sales_invoices),
            "purchasesCount": len(purchase_bills)
        }
        with open(meta_path, 'w', encoding='utf-8') as mf:
            json.dump(meta, mf, indent=2, ensure_ascii=False)

    print("\n" + "=" * 65)
    print("  Import Completed Successfully!")
    print(f"  * Company Profile : {comp_name} ({gstin})")
    print(f"  * Units           : {len(units_map)} measurement units mapped")
    print(f"  * Products        : {len(products)} inventory products")
    print(f"  * Clients/Parties : {clients_imported} parties with GSTIN & addresses")
    print(f"  * Sales Invoices  : {len(sales_invoices)} invoices across all financial years")
    print(f"  * Purchase Bills  : {len(purchase_bills)} purchases")
    print("=" * 65)
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Import BusyWin data to ARTHA")
    parser.add_argument('--busy-path', default=r'C:\BusyWin\DATA', help="Path to BusyWin DATA directory")
    parser.add_argument('--artha-data', default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'), help="Path to ARTHA data directory")
    parser.add_argument('--company', default='COMP0001', help="BusyWin company folder name (e.g. COMP0001)")
    parser.add_argument('--artha-company', default='COMP0001', help="ARTHA company to import INTO (its folder is data/<id>, e.g. COMP0002). Create the company in ARTHA first.")
    parser.add_argument('--dry-run', action='store_true', help="Preview without writing files")

    args = parser.parse_args()
    # Multi-company ARTHA: every company has its own folder inside data/.
    target = args.artha_data
    if not re.match(r'^COMP\d{4,}$', os.path.basename(os.path.normpath(target))):
        target = os.path.join(target, args.artha_company)
        if not os.path.isdir(target) and not args.dry_run:
            print(f"Error: ARTHA company folder not found: {target}\n  Create the company in ARTHA first (Setup New Company), then run the import again.")
            raise SystemExit(1)
    import_busywin(args.busy_path, target, args.company, args.dry_run)

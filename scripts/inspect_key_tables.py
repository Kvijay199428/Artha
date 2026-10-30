import json
import win32com.client

with open('scripts/busywin_db_schema.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

def print_cols(db_key, tname, limit=20):
    cols = d[db_key][tname]['columns']
    print(f"\n=== {tname} ({len(cols)} cols, {d[db_key][tname]['row_count']} rows) ===")
    for c in cols[:limit]:
        pk_mark = " [PK]" if c['is_pk'] else ""
        print(f"  {c['pos']:2}. {c['name']:25} : {c['type']}{pk_mark}")

print_cols('db_bds', 'Company')
print_cols('db_bds', 'UserPreferences')
print_cols('fy_bds', 'Master1')
print_cols('fy_bds', 'MasterAddressInfo')
print_cols('fy_bds', 'Tran1')
print_cols('fy_bds', 'Tran2')
print_cols('fy_bds', 'VchGSTSumItemWise')
print_cols('fy_bds', 'BillingDet')
print_cols('fy_bds', 'Folio1')


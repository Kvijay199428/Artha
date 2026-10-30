import json

with open('scripts/busywin_db_schema.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("TOTAL TABLES IN FY BDS:", len(d['fy_bds']))
for tname, tinfo in sorted(d['fy_bds'].items()):
    col_names = [c['name'] for c in tinfo['columns'][:8]]
    pk = tinfo['primary_keys']
    print(f"{tname:25} | rows:{tinfo['row_count']:5} | cols:{len(tinfo['columns']):3} | PK:{pk} | first cols: {', '.join(col_names)}")


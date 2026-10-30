import json
import win32com.client

with open('scripts/busywin_db_schema.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('=== db.bds TABLES & ROW COUNTS ===')
for t, d in data['db_bds'].items():
    print(f"{t:25} : {d['row_count']:5} rows, {len(d['columns']):3} cols, PK: {d['primary_keys']}")

print('\n=== db12026.bds TABLES & ROW COUNTS ===')
for t, d in data['fy_bds'].items():
    print(f"{t:25} : {d['row_count']:5} rows, {len(d['columns']):3} cols, PK: {d['primary_keys']}")

conn = win32com.client.Dispatch('ADODB.Connection')
conn.Open('Provider=Microsoft.ACE.OLEDB.12.0;Data Source=C:\\BusyWin\\DATA\\COMP0001\\db12026.bds;Jet OLEDB:Database Password=ILoveMyINDIA;')

# Inspect MasterTypes in Master1
print('\n=== Master1 MasterType values ===')
rs = conn.Execute("SELECT DISTINCT MasterType FROM Master1 ORDER BY MasterType")[0]
mtypes = []
while not rs.EOF:
    mtypes.append(rs.Fields(0).Value)
    rs.MoveNext()
rs.Close()
print("MasterTypes present:", mtypes)

for mt in mtypes:
    rs2 = conn.Execute(f"SELECT COUNT(*), MIN(Name), MAX(Name) FROM Master1 WHERE MasterType = {mt}")[0]
    cnt = rs2.Fields(0).Value
    min_name = rs2.Fields(1).Value
    max_name = rs2.Fields(2).Value
    rs2.Close()
    print(f"  MasterType {mt:2}: {cnt:4} records (e.g. '{min_name}' .. '{max_name}')")

# Inspect VchType values in Tran1
print('\n=== Tran1 VchType values ===')
rs = conn.Execute("SELECT DISTINCT VchType FROM Tran1 ORDER BY VchType")[0]
vtypes = []
while not rs.EOF:
    vtypes.append(rs.Fields(0).Value)
    rs.MoveNext()
rs.Close()
print("VchTypes present:", vtypes)

for vt in vtypes:
    rs2 = conn.Execute(f"SELECT COUNT(*), MIN(VchNo), MAX(VchNo) FROM Tran1 WHERE VchType = {vt}")[0]
    cnt = rs2.Fields(0).Value
    min_vch = rs2.Fields(1).Value
    max_vch = rs2.Fields(2).Value
    rs2.Close()
    print(f"  VchType {vt:2}: {cnt:4} records (VchNo '{min_vch}' .. '{max_vch}')")

conn.Close()

import win32com.client

path = 'C:\\BusyWin\\DATA\\COMP0001\\db12026.bds'
conn = win32com.client.Dispatch('ADODB.Connection')
conn.Open(f'Provider=Microsoft.ACE.OLEDB.12.0;Data Source={path};Jet OLEDB:Database Password=ILoveMyINDIA;')

# Search Help1 for voucher names
rs = conn.Execute("SELECT * FROM Help1 WHERE [Name] LIKE '%Payment%' OR [Name] LIKE '%Receipt%' OR [Name] LIKE '%Sales%'")[0]
while not rs.EOF:
    vals = [str(rs.Fields(i).Value) for i in range(rs.Fields.Count)]
    print("Help1:", " | ".join(vals[:5]))
    rs.MoveNext()
rs.Close()

conn.Close()

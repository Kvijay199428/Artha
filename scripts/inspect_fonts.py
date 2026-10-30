import os, struct

def parse_ttf(path):
    with open(path, 'rb') as f:
        data = f.read()
    
    num_tables = struct.unpack('>H', data[4:6])[0]
    tables = {}
    for i in range(num_tables):
        offset = 12 + i * 16
        tag = data[offset:offset+4].decode('ascii', errors='ignore')
        table_offset = struct.unpack('>I', data[offset+8:offset+12])[0]
        table_len = struct.unpack('>I', data[offset+12:offset+16])[0]
        tables[tag] = (table_offset, table_len)
    
    names = {}
    if 'name' in tables:
        to, tl = tables['name']
        nr_count = struct.unpack('>H', data[to+2:to+4])[0]
        str_offset = to + struct.unpack('>H', data[to+4:to+6])[0]
        for i in range(nr_count):
            ro = to + 6 + i * 12
            pid, eid, lid, nid, length, offset = struct.unpack('>HHHHHH', data[ro:ro+12])
            sdata = data[str_offset + offset : str_offset + offset + length]
            try:
                if pid == 0 or pid == 3: # Unicode
                    val = sdata.decode('utf-16be')
                elif pid == 1: # Mac Roman
                    val = sdata.decode('latin1')
                else:
                    val = sdata.decode('utf-8', errors='ignore')
                if nid not in names:
                    names[nid] = val
            except:
                pass
    return names

font_dir = r'C:\Windows\Fonts'
files = [
    'Rupee_Foradian.ttf', 'Oloron__.TTF', 'OLORC___.TTF', 'OLORCB__.TTF',
    'OLORCI__.TTF', 'OLORCBI_.TTF', 'OLORE___.TTF', 'OLOREB__.TTF',
    'OLOREI__.TTF', 'OLOREBI_.TTF', 'OLORUC__.TTF', 'OLORUCB_.TTF',
    'OLORUCI_.TTF', 'OLORUCBI.TTF', 'micross.ttf', 'tahoma.ttf', 'calibri.ttf', 'cour.ttf'
]

for f in files:
    fp = os.path.join(font_dir, f)
    if os.path.exists(fp):
        meta = parse_ttf(fp)
        family = meta.get(1, 'Unknown')
        subfamily = meta.get(2, 'Unknown')
        fullname = meta.get(4, 'Unknown')
        print(f'{f:18} | Family: {family:20} | Subfamily: {subfamily:15} | Full: {fullname}')
    else:
        print(f'{f:18} | NOT FOUND')


#!/usr/bin/env python3
"""
Extract full schemas of BusyWin Access/Jet database files:
1. db.bds (Company Database)
2. db12026.bds (Financial Year Operational Database)
"""

import sys
import os
import json
import win32com.client

PASSWORD = 'ILoveMyINDIA'

TYPE_MAP = {
    2: 'SMALLINT',
    3: 'INTEGER (Long)',
    4: 'SINGLE',
    5: 'DOUBLE',
    6: 'CURRENCY',
    7: 'DATETIME',
    11: 'BOOLEAN',
    17: 'BYTE',
    72: 'GUID',
    128: 'BINARY',
    129: 'CHAR',
    130: 'WCHAR',
    131: 'NUMERIC/DECIMAL',
    133: 'DATE',
    134: 'TIME',
    135: 'TIMESTAMP',
    200: 'VARCHAR',
    201: 'MEMO / LONGTEXT',
    202: 'VARCHAR',
    203: 'MEMO / LONGTEXT',
    204: 'VARBINARY',
    205: 'OLE_OBJECT / BLOB'
}

def get_schema(db_path):
    conn = win32com.client.Dispatch('ADODB.Connection')
    connStr = f'Provider=Microsoft.ACE.OLEDB.12.0;Data Source={db_path};Jet OLEDB:Database Password={PASSWORD};'
    conn.Open(connStr)
    
    # 1. Tables
    rs_tables = conn.OpenSchema(20) # adSchemaTables
    table_names = []
    while not rs_tables.EOF:
        if rs_tables.Fields['TABLE_TYPE'].Value == 'TABLE':
            table_names.append(rs_tables.Fields['TABLE_NAME'].Value)
        rs_tables.MoveNext()
    rs_tables.Close()
    
    # 2. Primary Keys
    pk_map = {}
    try:
        rs_pks = conn.OpenSchema(28) # adSchemaPrimaryKeys
        while not rs_pks.EOF:
            tname = rs_pks.Fields['TABLE_NAME'].Value
            cname = rs_pks.Fields['COLUMN_NAME'].Value
            if tname not in pk_map:
                pk_map[tname] = []
            pk_map[tname].append(cname)
            rs_pks.MoveNext()
        rs_pks.Close()
    except Exception as e:
        print('PK error:', e)

    # 3. Indexes
    idx_map = {}
    try:
        rs_idx = conn.OpenSchema(12) # adSchemaIndexes
        while not rs_idx.EOF:
            tname = rs_idx.Fields['TABLE_NAME'].Value
            iname = rs_idx.Fields['INDEX_NAME'].Value
            cname = rs_idx.Fields['COLUMN_NAME'].Value
            is_unique = rs_idx.Fields['UNIQUE'].Value
            is_pk = rs_idx.Fields['PRIMARY_KEY'].Value
            if tname not in idx_map:
                idx_map[tname] = {}
            if iname not in idx_map[tname]:
                idx_map[tname][iname] = {'unique': bool(is_unique), 'primary_key': bool(is_pk), 'columns': []}
            idx_map[tname][iname]['columns'].append(cname)
            rs_idx.MoveNext()
        rs_idx.Close()
    except Exception as e:
        print('Index error:', e)
        
    # 4. Tables Data
    tables_data = {}
    for tname in sorted(table_names):
        count = 0
        try:
            rs_res = conn.Execute(f'SELECT COUNT(*) FROM [{tname}]')
            rs_cnt = rs_res[0] if isinstance(rs_res, tuple) else rs_res
            count = rs_cnt.Fields(0).Value
            rs_cnt.Close()
        except Exception as e:
            count = -1
            
        tables_data[tname] = {
            'row_count': count,
            'primary_keys': pk_map.get(tname, []),
            'indexes': idx_map.get(tname, {}),
            'columns': []
        }
        
    # 5. Columns via adSchemaColumns
    rs_cols = conn.OpenSchema(4) # adSchemaColumns
    while not rs_cols.EOF:
        tname = rs_cols.Fields['TABLE_NAME'].Value
        if tname in tables_data:
            cname = rs_cols.Fields['COLUMN_NAME'].Value
            dtype_num = rs_cols.Fields['DATA_TYPE'].Value
            dtype_str = TYPE_MAP.get(dtype_num, f'TYPE_{dtype_num}')
            char_len = rs_cols.Fields['CHARACTER_MAXIMUM_LENGTH'].Value
            num_prec = rs_cols.Fields['NUMERIC_PRECISION'].Value
            num_scale = rs_cols.Fields['NUMERIC_SCALE'].Value
            is_nullable = rs_cols.Fields['IS_NULLABLE'].Value
            ord_pos = rs_cols.Fields['ORDINAL_POSITION'].Value
            
            # format type nicely
            if 'VARCHAR' in dtype_str or 'CHAR' in dtype_str:
                if char_len and char_len > 0:
                    dtype_str = f'{dtype_str}({char_len})'
            elif 'NUMERIC' in dtype_str and num_prec:
                dtype_str = f'{dtype_str}({num_prec},{num_scale})'
                
            tables_data[tname]['columns'].append({
                'name': cname,
                'pos': ord_pos,
                'type': dtype_str,
                'nullable': bool(is_nullable),
                'is_pk': cname in tables_data[tname]['primary_keys']
            })
        rs_cols.MoveNext()
    rs_cols.Close()
    
    # Sort columns by ordinal position
    for tname in tables_data:
        tables_data[tname]['columns'].sort(key=lambda c: c['pos'])
        
    conn.Close()
    return tables_data

if __name__ == '__main__':
    db_path = 'C:\\BusyWin\\DATA\\COMP0001\\db.bds'
    fy_path = 'C:\\BusyWin\\DATA\\COMP0001\\db12026.bds'
    
    db_bds_data = get_schema(db_path)
    fy_bds_data = get_schema(fy_path)
    
    out_file = 'd:\\VEGA\\ARTHA\\scripts\\busywin_db_schema.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump({'db_bds': db_bds_data, 'fy_bds': fy_bds_data}, f, indent=2)
        
    total_db_cols = sum(len(t['columns']) for t in db_bds_data.values())
    total_fy_cols = sum(len(t['columns']) for t in fy_bds_data.values())
    print(f'Done! db.bds tables: {len(db_bds_data)}, Total cols: {total_db_cols}')
    print(f'Done! db12026.bds tables: {len(fy_bds_data)}, Total cols: {total_fy_cols}')

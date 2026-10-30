# BusyWin FY Database: System & Configuration Schemas

> **Database File:** `db1<YYYY>.bds` (e.g. `C:\BusyWin\DATA\COMP0001\db12026.bds`)

> **Engine:** Microsoft Jet 4.0 / Access OLEDB (`ILoveMyINDIA`)

> **Description:** Detailed table schemas and column definitions for internal Configuration, Concurrency Locks, Audit Logs, and Cloud Sync in db1YYYY.bds.


## Tables in this Module


| # | Table Name | Columns | Active Rows | Primary Key | Description |
|---|------------|:-------:|:-----------:|:-----------:|-------------|
| 1 | [`Config`](#table-config) | 255 | 180 | `-` | Company financial year configuration repository (180+ feature flags, voucher numbering rules, series settings). |
| 2 | [`Locks`](#table-locks) | 59 | 1 | `-` | Concurrency locking table preventing concurrent data corruption across multi-user network sessions. |
| 3 | [`EventLog`](#table-eventlog) | 9 | 9 | `-` | System operational event log tracking voucher creation, modification, deletion, and print events with machine IP. |
| 4 | [`DeletedInfo`](#table-deletedinfo) | 8 | 0 | `-` | Audit log of deleted transactions recording voucher number, date, original value, deleted by, and timestamp. |
| 5 | [`QueryLog`](#table-querylog) | 5 | 0 | `-` | Diagnostic SQL execution log recording slow queries and system database errors. |
| 6 | [`DataSync`](#table-datasync) | 37 | 0 | `-` | Multi-branch data synchronization journal recording packet IDs, sync timestamps, and replication status. |
| 7 | [`CloudSyncStatus`](#table-cloudsyncstatus) | 10 | 0 | `-` | Overall status of Busy Cloud data synchronization (bulk sync versus incremental sync state). |
| 8 | [`CloudSyncIncr`](#table-cloudsyncincr) | 12 | 0 | `-` | Queue of incremental database changes pending upload to Busy Cloud. |
| 9 | [`CloudSyncIncrDet`](#table-cloudsyncincrdet) | 3 | 0 | `-` | XML data payloads of incremental changes waiting to be replicated. |
| 10 | [`CheckList`](#table-checklist) | 12 | 0 | `-` | Task checklist items and audit approval state. |
| 11 | [`CheckListNew`](#table-checklistnew) | 10 | 0 | `-` | Workflow approval headers for multi-level voucher authorization hierarchies. |
| 12 | [`CheckListNewDet`](#table-checklistnewdet) | 3 | 0 | `-` | Workflow authorization signatures and approval payloads. |
| 13 | [`RepColSize`](#table-repcolsize) | 7 | 38 | `-` | User-customized column widths and display formats for financial statements and registers. |
| 14 | [`RepOptValues`](#table-repoptvalues) | 9 | 40 | `-` | Saved report filter presets (date ranges, party selections, group filters). |
| 15 | [`ReportNotes`](#table-reportnotes) | 10 | 0 | `-` | User annotations and sticky notes attached to specific balance sheet and ledger reports. |
| 16 | [`Patches`](#table-patches) | 79 | 0 | `-` | Version migration patch history applied to the operational database (db1YYYY.bds). |
| 17 | [`ExternalData`](#table-externaldata) | 15 | 0 | `-` | Integration data bridge for external third-party software (CRM, WMS, eCommerce platforms). |

---

## Detailed Column Schemas


<a name="table-config"></a>

### Table: `Config`

> **Purpose:** Company financial year configuration repository (180+ feature flags, voucher numbering rules, series settings).

- **Row Count in Active FY:** `180`
- **Total Columns:** `255`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 2 | `Type` | `SMALLINT` | Yes |  | Integer identifier or enum code for Type |
| 3 | `C1` | `WCHAR(20.0)` | Yes |  | Text attribute: C1 |
| 4 | `C2` | `WCHAR(20.0)` | Yes |  | Text attribute: C2 |
| 5 | `C3` | `WCHAR(20.0)` | Yes |  | Text attribute: C3 |
| 6 | `C4` | `WCHAR(20.0)` | Yes |  | Text attribute: C4 |
| 7 | `C5` | `WCHAR(20.0)` | Yes |  | Text attribute: C5 |
| 8 | `C6` | `WCHAR(20.0)` | Yes |  | Text attribute: C6 |
| 9 | `C7` | `WCHAR(20.0)` | Yes |  | Text attribute: C7 |
| 10 | `C8` | `WCHAR(20.0)` | Yes |  | Text attribute: C8 |
| 11 | `C9` | `WCHAR(20.0)` | Yes |  | Text attribute: C9 |
| 12 | `C10` | `WCHAR(20.0)` | Yes |  | Text attribute: C10 |
| 13 | `C11` | `WCHAR(20.0)` | Yes |  | Text attribute: C11 |
| 14 | `C12` | `WCHAR(20.0)` | Yes |  | Text attribute: C12 |
| 15 | `C13` | `WCHAR(20.0)` | Yes |  | Text attribute: C13 |
| 16 | `C14` | `WCHAR(20.0)` | Yes |  | Text attribute: C14 |
| 17 | `C15` | `WCHAR(20.0)` | Yes |  | Text attribute: C15 |
| 18 | `C16` | `WCHAR(20.0)` | Yes |  | Text attribute: C16 |
| 19 | `C17` | `WCHAR(20.0)` | Yes |  | Text attribute: C17 |
| 20 | `C18` | `WCHAR(20.0)` | Yes |  | Text attribute: C18 |
| 21 | `C19` | `WCHAR(20.0)` | Yes |  | Text attribute: C19 |
| 22 | `C20` | `WCHAR(20.0)` | Yes |  | Text attribute: C20 |
| 23 | `C21` | `WCHAR(255.0)` | Yes |  | Text attribute: C21 |
| 24 | `C22` | `WCHAR(255.0)` | Yes |  | Text attribute: C22 |
| 25 | `C23` | `WCHAR(255.0)` | Yes |  | Text attribute: C23 |
| 26 | `C24` | `WCHAR(255.0)` | Yes |  | Text attribute: C24 |
| 27 | `C25` | `WCHAR(255.0)` | Yes |  | Text attribute: C25 |
| 28 | `C26` | `WCHAR(255.0)` | Yes |  | Text attribute: C26 |
| 29 | `C27` | `WCHAR(255.0)` | Yes |  | Text attribute: C27 |
| 30 | `C28` | `WCHAR(255.0)` | Yes |  | Text attribute: C28 |
| 31 | `C29` | `WCHAR(255.0)` | Yes |  | Text attribute: C29 |
| 32 | `C30` | `WCHAR(255.0)` | Yes |  | Text attribute: C30 |
| 33 | `DocName` | `WCHAR(35.0)` | Yes |  | Text attribute: DocName |
| 34 | `InvVchName` | `WCHAR(35.0)` | Yes |  | Text attribute: InvVchName |
| 35 | `FaVchName` | `WCHAR(35.0)` | Yes |  | Text attribute: FaVchName |
| 36 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 37 | `I2` | `SMALLINT` | Yes |  | Integer identifier or enum code for I2 |
| 38 | `I3` | `SMALLINT` | Yes |  | Integer identifier or enum code for I3 |
| 39 | `I4` | `SMALLINT` | Yes |  | Integer identifier or enum code for I4 |
| 40 | `I5` | `SMALLINT` | Yes |  | Integer identifier or enum code for I5 |
| 41 | `I6` | `SMALLINT` | Yes |  | Integer identifier or enum code for I6 |
| 42 | `I7` | `SMALLINT` | Yes |  | Integer identifier or enum code for I7 |
| 43 | `I8` | `SMALLINT` | Yes |  | Integer identifier or enum code for I8 |
| 44 | `I9` | `SMALLINT` | Yes |  | Integer identifier or enum code for I9 |
| 45 | `I10` | `SMALLINT` | Yes |  | Integer identifier or enum code for I10 |
| 46 | `I11` | `SMALLINT` | Yes |  | Integer identifier or enum code for I11 |
| 47 | `I12` | `SMALLINT` | Yes |  | Integer identifier or enum code for I12 |
| 48 | `I13` | `SMALLINT` | Yes |  | Integer identifier or enum code for I13 |
| 49 | `I14` | `SMALLINT` | Yes |  | Integer identifier or enum code for I14 |
| 50 | `I15` | `SMALLINT` | Yes |  | Integer identifier or enum code for I15 |
| 51 | `I16` | `SMALLINT` | Yes |  | Integer identifier or enum code for I16 |
| 52 | `I17` | `SMALLINT` | Yes |  | Integer identifier or enum code for I17 |
| 53 | `I18` | `SMALLINT` | Yes |  | Integer identifier or enum code for I18 |
| 54 | `I19` | `SMALLINT` | Yes |  | Integer identifier or enum code for I19 |
| 55 | `I20` | `SMALLINT` | Yes |  | Integer identifier or enum code for I20 |
| 56 | `I21` | `SMALLINT` | Yes |  | Integer identifier or enum code for I21 |
| 57 | `I22` | `SMALLINT` | Yes |  | Integer identifier or enum code for I22 |
| 58 | `I23` | `SMALLINT` | Yes |  | Integer identifier or enum code for I23 |
| 59 | `I24` | `SMALLINT` | Yes |  | Integer identifier or enum code for I24 |
| 60 | `I25` | `SMALLINT` | Yes |  | Integer identifier or enum code for I25 |
| 61 | `I26` | `SMALLINT` | Yes |  | Integer identifier or enum code for I26 |
| 62 | `I27` | `SMALLINT` | Yes |  | Integer identifier or enum code for I27 |
| 63 | `I28` | `SMALLINT` | Yes |  | Integer identifier or enum code for I28 |
| 64 | `I29` | `SMALLINT` | Yes |  | Integer identifier or enum code for I29 |
| 65 | `I30` | `SMALLINT` | Yes |  | Integer identifier or enum code for I30 |
| 66 | `I31` | `SMALLINT` | Yes |  | Integer identifier or enum code for I31 |
| 67 | `I32` | `SMALLINT` | Yes |  | Integer identifier or enum code for I32 |
| 68 | `I33` | `SMALLINT` | Yes |  | Integer identifier or enum code for I33 |
| 69 | `I34` | `SMALLINT` | Yes |  | Integer identifier or enum code for I34 |
| 70 | `I35` | `SMALLINT` | Yes |  | Integer identifier or enum code for I35 |
| 71 | `NoOfFld` | `SMALLINT` | Yes |  | Integer identifier or enum code for NoOfFld |
| 72 | `B1` | `BOOLEAN` | No |  | Feature toggle boolean flag B1 |
| 73 | `B2` | `BOOLEAN` | No |  | Feature toggle boolean flag B2 |
| 74 | `B3` | `BOOLEAN` | No |  | Feature toggle boolean flag B3 |
| 75 | `B4` | `BOOLEAN` | No |  | Feature toggle boolean flag B4 |
| 76 | `B5` | `BOOLEAN` | No |  | Feature toggle boolean flag B5 |
| 77 | `B6` | `BOOLEAN` | No |  | Feature toggle boolean flag B6 |
| 78 | `B7` | `BOOLEAN` | No |  | Feature toggle boolean flag B7 |
| 79 | `B8` | `BOOLEAN` | No |  | Feature toggle boolean flag B8 |
| 80 | `B9` | `BOOLEAN` | No |  | Feature toggle boolean flag B9 |
| 81 | `B10` | `BOOLEAN` | No |  | Feature toggle boolean flag B10 |
| 82 | `B11` | `BOOLEAN` | No |  | Feature toggle boolean flag B11 |
| 83 | `B12` | `BOOLEAN` | No |  | Feature toggle boolean flag B12 |
| 84 | `B13` | `BOOLEAN` | No |  | Feature toggle boolean flag B13 |
| 85 | `B14` | `BOOLEAN` | No |  | Feature toggle boolean flag B14 |
| 86 | `B15` | `BOOLEAN` | No |  | Feature toggle boolean flag B15 |
| 87 | `B16` | `BOOLEAN` | No |  | Feature toggle boolean flag B16 |
| 88 | `B17` | `BOOLEAN` | No |  | Feature toggle boolean flag B17 |
| 89 | `B18` | `BOOLEAN` | No |  | Feature toggle boolean flag B18 |
| 90 | `B19` | `BOOLEAN` | No |  | Feature toggle boolean flag B19 |
| 91 | `B20` | `BOOLEAN` | No |  | Feature toggle boolean flag B20 |
| 92 | `B21` | `BOOLEAN` | No |  | Feature toggle boolean flag B21 |
| 93 | `B22` | `BOOLEAN` | No |  | Feature toggle boolean flag B22 |
| 94 | `B23` | `BOOLEAN` | No |  | Feature toggle boolean flag B23 |
| 95 | `B24` | `BOOLEAN` | No |  | Feature toggle boolean flag B24 |
| 96 | `B25` | `BOOLEAN` | No |  | Feature toggle boolean flag B25 |
| 97 | `B26` | `BOOLEAN` | No |  | Feature toggle boolean flag B26 |
| 98 | `B27` | `BOOLEAN` | No |  | Feature toggle boolean flag B27 |
| 99 | `B28` | `BOOLEAN` | No |  | Feature toggle boolean flag B28 |
| 100 | `B29` | `BOOLEAN` | No |  | Feature toggle boolean flag B29 |
| 101 | `B30` | `BOOLEAN` | No |  | Feature toggle boolean flag B30 |
| 102 | `B31` | `BOOLEAN` | No |  | Feature toggle boolean flag B31 |
| 103 | `B32` | `BOOLEAN` | No |  | Feature toggle boolean flag B32 |
| 104 | `B33` | `BOOLEAN` | No |  | Feature toggle boolean flag B33 |
| 105 | `B34` | `BOOLEAN` | No |  | Feature toggle boolean flag B34 |
| 106 | `B35` | `BOOLEAN` | No |  | Feature toggle boolean flag B35 |
| 107 | `B36` | `BOOLEAN` | No |  | Feature toggle boolean flag B36 |
| 108 | `B37` | `BOOLEAN` | No |  | Feature toggle boolean flag B37 |
| 109 | `B38` | `BOOLEAN` | No |  | Feature toggle boolean flag B38 |
| 110 | `B39` | `BOOLEAN` | No |  | Feature toggle boolean flag B39 |
| 111 | `B40` | `BOOLEAN` | No |  | Feature toggle boolean flag B40 |
| 112 | `B41` | `BOOLEAN` | No |  | Feature toggle boolean flag B41 |
| 113 | `B42` | `BOOLEAN` | No |  | Feature toggle boolean flag B42 |
| 114 | `B43` | `BOOLEAN` | No |  | Feature toggle boolean flag B43 |
| 115 | `B44` | `BOOLEAN` | No |  | Feature toggle boolean flag B44 |
| 116 | `B45` | `BOOLEAN` | No |  | Feature toggle boolean flag B45 |
| 117 | `B46` | `BOOLEAN` | No |  | Feature toggle boolean flag B46 |
| 118 | `B47` | `BOOLEAN` | No |  | Feature toggle boolean flag B47 |
| 119 | `B48` | `BOOLEAN` | No |  | Feature toggle boolean flag B48 |
| 120 | `B49` | `BOOLEAN` | No |  | Feature toggle boolean flag B49 |
| 121 | `B50` | `BOOLEAN` | No |  | Feature toggle boolean flag B50 |
| 122 | `B51` | `BOOLEAN` | No |  | Feature toggle boolean flag B51 |
| 123 | `B52` | `BOOLEAN` | No |  | Feature toggle boolean flag B52 |
| 124 | `B53` | `BOOLEAN` | No |  | Feature toggle boolean flag B53 |
| 125 | `B54` | `BOOLEAN` | No |  | Feature toggle boolean flag B54 |
| 126 | `B55` | `BOOLEAN` | No |  | Feature toggle boolean flag B55 |
| 127 | `B56` | `BOOLEAN` | No |  | Feature toggle boolean flag B56 |
| 128 | `B57` | `BOOLEAN` | No |  | Feature toggle boolean flag B57 |
| 129 | `B58` | `BOOLEAN` | No |  | Feature toggle boolean flag B58 |
| 130 | `B59` | `BOOLEAN` | No |  | Feature toggle boolean flag B59 |
| 131 | `B60` | `BOOLEAN` | No |  | Feature toggle boolean flag B60 |
| 132 | `B61` | `BOOLEAN` | No |  | Feature toggle boolean flag B61 |
| 133 | `B62` | `BOOLEAN` | No |  | Feature toggle boolean flag B62 |
| 134 | `B63` | `BOOLEAN` | No |  | Feature toggle boolean flag B63 |
| 135 | `B64` | `BOOLEAN` | No |  | Feature toggle boolean flag B64 |
| 136 | `B65` | `BOOLEAN` | No |  | Feature toggle boolean flag B65 |
| 137 | `B66` | `BOOLEAN` | No |  | Feature toggle boolean flag B66 |
| 138 | `B67` | `BOOLEAN` | No |  | Feature toggle boolean flag B67 |
| 139 | `B68` | `BOOLEAN` | No |  | Feature toggle boolean flag B68 |
| 140 | `B69` | `BOOLEAN` | No |  | Feature toggle boolean flag B69 |
| 141 | `B70` | `BOOLEAN` | No |  | Feature toggle boolean flag B70 |
| 142 | `B71` | `BOOLEAN` | No |  | Feature toggle boolean flag B71 |
| 143 | `B72` | `BOOLEAN` | No |  | Feature toggle boolean flag B72 |
| 144 | `B73` | `BOOLEAN` | No |  | Feature toggle boolean flag B73 |
| 145 | `B74` | `BOOLEAN` | No |  | Feature toggle boolean flag B74 |
| 146 | `B75` | `BOOLEAN` | No |  | Feature toggle boolean flag B75 |
| 147 | `B76` | `BOOLEAN` | No |  | Feature toggle boolean flag B76 |
| 148 | `B77` | `BOOLEAN` | No |  | Feature toggle boolean flag B77 |
| 149 | `B78` | `BOOLEAN` | No |  | Feature toggle boolean flag B78 |
| 150 | `B79` | `BOOLEAN` | No |  | Feature toggle boolean flag B79 |
| 151 | `B80` | `BOOLEAN` | No |  | Feature toggle boolean flag B80 |
| 152 | `B81` | `BOOLEAN` | No |  | Feature toggle boolean flag B81 |
| 153 | `B82` | `BOOLEAN` | No |  | Feature toggle boolean flag B82 |
| 154 | `B83` | `BOOLEAN` | No |  | Feature toggle boolean flag B83 |
| 155 | `B84` | `BOOLEAN` | No |  | Feature toggle boolean flag B84 |
| 156 | `B85` | `BOOLEAN` | No |  | Feature toggle boolean flag B85 |
| 157 | `B86` | `BOOLEAN` | No |  | Feature toggle boolean flag B86 |
| 158 | `B87` | `BOOLEAN` | No |  | Feature toggle boolean flag B87 |
| 159 | `B88` | `BOOLEAN` | No |  | Feature toggle boolean flag B88 |
| 160 | `B89` | `BOOLEAN` | No |  | Feature toggle boolean flag B89 |
| 161 | `B90` | `BOOLEAN` | No |  | Feature toggle boolean flag B90 |
| 162 | `B91` | `BOOLEAN` | No |  | Feature toggle boolean flag B91 |
| 163 | `B92` | `BOOLEAN` | No |  | Feature toggle boolean flag B92 |
| 164 | `B93` | `BOOLEAN` | No |  | Feature toggle boolean flag B93 |
| 165 | `B94` | `BOOLEAN` | No |  | Feature toggle boolean flag B94 |
| 166 | `B95` | `BOOLEAN` | No |  | Feature toggle boolean flag B95 |
| 167 | `B96` | `BOOLEAN` | No |  | Feature toggle boolean flag B96 |
| 168 | `B97` | `BOOLEAN` | No |  | Feature toggle boolean flag B97 |
| 169 | `B98` | `BOOLEAN` | No |  | Feature toggle boolean flag B98 |
| 170 | `B99` | `BOOLEAN` | No |  | Feature toggle boolean flag B99 |
| 171 | `B100` | `BOOLEAN` | No |  | Feature toggle boolean flag B100 |
| 172 | `B101` | `BOOLEAN` | No |  | Feature toggle boolean flag B101 |
| 173 | `B102` | `BOOLEAN` | No |  | Feature toggle boolean flag B102 |
| 174 | `B103` | `BOOLEAN` | No |  | Feature toggle boolean flag B103 |
| 175 | `B104` | `BOOLEAN` | No |  | Feature toggle boolean flag B104 |
| 176 | `B105` | `BOOLEAN` | No |  | Feature toggle boolean flag B105 |
| 177 | `B106` | `BOOLEAN` | No |  | Feature toggle boolean flag B106 |
| 178 | `B107` | `BOOLEAN` | No |  | Feature toggle boolean flag B107 |
| 179 | `B108` | `BOOLEAN` | No |  | Feature toggle boolean flag B108 |
| 180 | `B109` | `BOOLEAN` | No |  | Feature toggle boolean flag B109 |
| 181 | `B110` | `BOOLEAN` | No |  | Feature toggle boolean flag B110 |
| 182 | `B111` | `BOOLEAN` | No |  | Feature toggle boolean flag B111 |
| 183 | `B112` | `BOOLEAN` | No |  | Feature toggle boolean flag B112 |
| 184 | `B113` | `BOOLEAN` | No |  | Feature toggle boolean flag B113 |
| 185 | `B114` | `BOOLEAN` | No |  | Feature toggle boolean flag B114 |
| 186 | `B115` | `BOOLEAN` | No |  | Feature toggle boolean flag B115 |
| 187 | `B116` | `BOOLEAN` | No |  | Feature toggle boolean flag B116 |
| 188 | `B117` | `BOOLEAN` | No |  | Feature toggle boolean flag B117 |
| 189 | `B118` | `BOOLEAN` | No |  | Feature toggle boolean flag B118 |
| 190 | `B119` | `BOOLEAN` | No |  | Feature toggle boolean flag B119 |
| 191 | `B120` | `BOOLEAN` | No |  | Feature toggle boolean flag B120 |
| 192 | `B121` | `BOOLEAN` | No |  | Feature toggle boolean flag B121 |
| 193 | `B122` | `BOOLEAN` | No |  | Feature toggle boolean flag B122 |
| 194 | `B123` | `BOOLEAN` | No |  | Feature toggle boolean flag B123 |
| 195 | `B124` | `BOOLEAN` | No |  | Feature toggle boolean flag B124 |
| 196 | `B125` | `BOOLEAN` | No |  | Feature toggle boolean flag B125 |
| 197 | `B126` | `BOOLEAN` | No |  | Feature toggle boolean flag B126 |
| 198 | `B127` | `BOOLEAN` | No |  | Feature toggle boolean flag B127 |
| 199 | `B128` | `BOOLEAN` | No |  | Feature toggle boolean flag B128 |
| 200 | `B129` | `BOOLEAN` | No |  | Feature toggle boolean flag B129 |
| 201 | `B130` | `BOOLEAN` | No |  | Feature toggle boolean flag B130 |
| 202 | `B131` | `BOOLEAN` | No |  | Feature toggle boolean flag B131 |
| 203 | `B132` | `BOOLEAN` | No |  | Feature toggle boolean flag B132 |
| 204 | `B133` | `BOOLEAN` | No |  | Feature toggle boolean flag B133 |
| 205 | `B134` | `BOOLEAN` | No |  | Feature toggle boolean flag B134 |
| 206 | `B135` | `BOOLEAN` | No |  | Feature toggle boolean flag B135 |
| 207 | `B136` | `BOOLEAN` | No |  | Feature toggle boolean flag B136 |
| 208 | `B137` | `BOOLEAN` | No |  | Feature toggle boolean flag B137 |
| 209 | `B138` | `BOOLEAN` | No |  | Feature toggle boolean flag B138 |
| 210 | `B139` | `BOOLEAN` | No |  | Feature toggle boolean flag B139 |
| 211 | `B140` | `BOOLEAN` | No |  | Feature toggle boolean flag B140 |
| 212 | `B141` | `BOOLEAN` | No |  | Feature toggle boolean flag B141 |
| 213 | `B142` | `BOOLEAN` | No |  | Feature toggle boolean flag B142 |
| 214 | `L1` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L1 |
| 215 | `L2` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L2 |
| 216 | `L3` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L3 |
| 217 | `L4` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L4 |
| 218 | `L5` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L5 |
| 219 | `L6` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L6 |
| 220 | `L7` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L7 |
| 221 | `L8` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L8 |
| 222 | `L9` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L9 |
| 223 | `L10` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L10 |
| 224 | `L11` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L11 |
| 225 | `L12` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L12 |
| 226 | `L13` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L13 |
| 227 | `L14` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L14 |
| 228 | `L15` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L15 |
| 229 | `L16` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L16 |
| 230 | `L17` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L17 |
| 231 | `L18` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L18 |
| 232 | `L19` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L19 |
| 233 | `L20` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L20 |
| 234 | `CM1` | `INTEGER (Long)` | Yes |  | Configurable master foreign key CM1 (links to Master1.Code based on MasterType) |
| 235 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 236 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 237 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 238 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 239 | `D5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D5 |
| 240 | `D6` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D6 |
| 241 | `D7` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D7 |
| 242 | `D8` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D8 |
| 243 | `D9` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D9 |
| 244 | `D10` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D10 |
| 245 | `D11` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D11 |
| 246 | `D12` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D12 |
| 247 | `D13` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D13 |
| 248 | `D14` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D14 |
| 249 | `D15` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D15 |
| 250 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 251 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |
| 252 | `PricingMode` | `SMALLINT` | Yes |  | Integer identifier or enum code for PricingMode |
| 253 | `PricingModeForPurc` | `SMALLINT` | Yes |  | Integer identifier or enum code for PricingModeForPurc |
| 254 | `M2` | `WCHAR` | Yes |  | Text attribute: M2 |
| 255 | `Stamp` | `INTEGER (Long)` | Yes |  | Internal concurrency timestamp / modification revision stamp |

---

<a name="table-locks"></a>

### Table: `Locks`

> **Purpose:** Concurrency locking table preventing concurrent data corruption across multi-user network sessions.

- **Row Count in Active FY:** `1`
- **Total Columns:** `59`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Type` | `DATETIME` | Yes |  | Timestamp / Date field for Type |
| 2 | `IBR` | `BOOLEAN` | No |  | Boolean flag for IBR (True/False) |
| 3 | `MBU` | `BOOLEAN` | No |  | Boolean flag for MBU (True/False) |
| 4 | `CSU` | `BOOLEAN` | No |  | Boolean flag for CSU (True/False) |
| 5 | `STU` | `BOOLEAN` | No |  | Boolean flag for STU (True/False) |
| 6 | `Working` | `BOOLEAN` | No |  | Boolean flag for Working (True/False) |
| 7 | `BSSTD` | `BOOLEAN` | No |  | Boolean flag for BSSTD (True/False) |
| 8 | `TERBR` | `BOOLEAN` | No |  | Boolean flag for TERBR (True/False) |
| 9 | `BRS` | `BOOLEAN` | No |  | Boolean flag for BRS (True/False) |
| 10 | `CCCF` | `BOOLEAN` | No |  | Boolean flag for CCCF (True/False) |
| 11 | `SuppTypeF` | `BOOLEAN` | No |  | Boolean flag for SuppTypeF (True/False) |
| 12 | `BSNF` | `BOOLEAN` | No |  | Boolean flag for BSNF (True/False) |
| 13 | `BST` | `BOOLEAN` | No |  | Boolean flag for BST (True/False) |
| 14 | `OSPO` | `BOOLEAN` | No |  | Boolean flag for OSPO (True/False) |
| 15 | `OBAMC` | `BOOLEAN` | No |  | Boolean flag for OBAMC (True/False) |
| 16 | `TDSSHE` | `BOOLEAN` | No |  | Boolean flag for TDSSHE (True/False) |
| 17 | `TESRNO` | `BOOLEAN` | No |  | Boolean flag for TESRNO (True/False) |
| 18 | `MAJOR` | `SMALLINT` | Yes |  | Integer identifier or enum code for MAJOR |
| 19 | `MINOR` | `SMALLINT` | Yes |  | Integer identifier or enum code for MINOR |
| 20 | `RW35` | `BOOLEAN` | No |  | Boolean flag for RW35 (True/False) |
| 21 | `MEBR` | `BOOLEAN` | No |  | Boolean flag for MEBR (True/False) |
| 22 | `MEBR1` | `BOOLEAN` | No |  | Boolean flag for MEBR1 (True/False) |
| 23 | `MFFSA` | `BOOLEAN` | No |  | Boolean flag for MFFSA (True/False) |
| 24 | `SMPL` | `BOOLEAN` | No |  | Boolean flag for SMPL (True/False) |
| 25 | `GSTU` | `BOOLEAN` | No |  | Boolean flag for GSTU (True/False) |
| 26 | `MUSPO` | `BOOLEAN` | No |  | Boolean flag for MUSPO (True/False) |
| 27 | `DFYW` | `BOOLEAN` | No |  | Boolean flag for DFYW (True/False) |
| 28 | `BATCH` | `BOOLEAN` | No |  | Boolean flag for BATCH (True/False) |
| 29 | `BATCHMRPSRNOPARAM` | `BOOLEAN` | No |  | Boolean flag for BATCHMRPSRNOPARAM (True/False) |
| 30 | `ENTRYTAXRATE` | `BOOLEAN` | No |  | Boolean flag for ENTRYTAXRATE (True/False) |
| 31 | `STPTMC` | `BOOLEAN` | No |  | Boolean flag for STPTMC (True/False) |
| 32 | `CHALLANNO` | `BOOLEAN` | No |  | Boolean flag for CHALLANNO (True/False) |
| 33 | `PARAMDET` | `BOOLEAN` | No |  | Boolean flag for PARAMDET (True/False) |
| 34 | `MASTFP` | `BOOLEAN` | No |  | Boolean flag for MASTFP (True/False) |
| 35 | `MASTFP1` | `BOOLEAN` | No |  | Boolean flag for MASTFP1 (True/False) |
| 36 | `RMVLOCDB` | `BOOLEAN` | No |  | Boolean flag for RMVLOCDB (True/False) |
| 37 | `POSSERIESFTBSNAME` | `BOOLEAN` | No |  | Boolean flag for POSSERIESFTBSNAME (True/False) |
| 38 | `STSCGUPDT` | `BOOLEAN` | No |  | Boolean flag for STSCGUPDT (True/False) |
| 39 | `ItemSrNoLen` | `BOOLEAN` | No |  | Boolean flag for ItemSrNoLen (True/False) |
| 40 | `RGMAST` | `BOOLEAN` | No |  | Boolean flag for RGMAST (True/False) |
| 41 | `MainDbVer` | `SMALLINT` | Yes |  | Integer identifier or enum code for MainDbVer |
| 42 | `PartialDbVer` | `SMALLINT` | Yes |  | Integer identifier or enum code for PartialDbVer |
| 43 | `COMPEGRPMAST` | `BOOLEAN` | No |  | Boolean flag for COMPEGRPMAST (True/False) |
| 44 | `COMPCONTGRPMAST` | `BOOLEAN` | No |  | Boolean flag for COMPCONTGRPMAST (True/False) |
| 45 | `AREAMAST` | `BOOLEAN` | No |  | Boolean flag for AREAMAST (True/False) |
| 46 | `CONTDEPTMAST` | `BOOLEAN` | No |  | Boolean flag for CONTDEPTMAST (True/False) |
| 47 | `SOURCEMAST` | `BOOLEAN` | No |  | Boolean flag for SOURCEMAST (True/False) |
| 48 | `SUBSTATUSMAST` | `BOOLEAN` | No |  | Boolean flag for SUBSTATUSMAST (True/False) |
| 49 | `NXTACTIONMAST` | `BOOLEAN` | No |  | Boolean flag for NXTACTIONMAST (True/False) |
| 50 | `TRADEMAST` | `BOOLEAN` | No |  | Boolean flag for TRADEMAST (True/False) |
| 51 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 52 | `FAQGRPMAST` | `BOOLEAN` | No |  | Boolean flag for FAQGRPMAST (True/False) |
| 53 | `PENDSUBSTATUSMAST` | `BOOLEAN` | No |  | Boolean flag for PENDSUBSTATUSMAST (True/False) |
| 54 | `TRACKINGNO` | `BOOLEAN` | No |  | Boolean flag for TRACKINGNO (True/False) |
| 55 | `WinUser` | `WCHAR(255.0)` | Yes |  | Text attribute: WinUser |
| 56 | `PIIPD` | `WCHAR(255.0)` | Yes |  | Text attribute: PIIPD |
| 57 | `TOFQ` | `BOOLEAN` | No |  | Boolean flag for TOFQ (True/False) |
| 58 | `CompanyName` | `WCHAR(255.0)` | Yes |  | Text attribute: CompanyName |
| 59 | `URefBal` | `BOOLEAN` | No |  | Boolean flag for URefBal (True/False) |

---

<a name="table-eventlog"></a>

### Table: `EventLog`

> **Purpose:** System operational event log tracking voucher creation, modification, deletion, and print events with machine IP.

- **Row Count in Active FY:** `9`
- **Total Columns:** `9`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `UserName` | `WCHAR(20.0)` | Yes |  | Operator username who performed the action |
| 2 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 3 | `WorkedOn` | `SMALLINT` | Yes |  | Integer identifier or enum code for WorkedOn |
| 4 | `Description` | `WCHAR` | Yes |  | Text attribute: Description |
| 5 | `UID` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for UID |
| 6 | `ComputerName` | `WCHAR(40.0)` | Yes |  | Text attribute: ComputerName |
| 7 | `VersionNo` | `WCHAR(40.0)` | Yes |  | Text attribute: VersionNo |
| 8 | `S1` | `WCHAR(255.0)` | Yes |  | Text attribute: S1 |
| 9 | `SessionId` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for SessionId |

---

<a name="table-deletedinfo"></a>

### Table: `DeletedInfo`

> **Purpose:** Audit log of deleted transactions recording voucher number, date, original value, deleted by, and timestamp.

- **Row Count in Active FY:** `0`
- **Total Columns:** `8`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Type` | `SMALLINT` | Yes |  | Integer identifier or enum code for Type |
| 2 | `VchMastType` | `SMALLINT` | Yes |  | Integer identifier or enum code for VchMastType |
| 3 | `Identity` | `WCHAR(50.0)` | Yes |  | Text attribute: Identity |
| 4 | `DeletedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: DeletedBy |
| 5 | `DeletionTime` | `DATETIME` | Yes |  | Timestamp / Date field for DeletionTime |
| 6 | `OrgVchAmtBaseCur` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for OrgVchAmtBaseCur |
| 7 | `ModVchAmtBaseCur` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for ModVchAmtBaseCur |
| 8 | `ComputerName` | `WCHAR(25.0)` | Yes |  | Text attribute: ComputerName |

---

<a name="table-querylog"></a>

### Table: `QueryLog`

> **Purpose:** Diagnostic SQL execution log recording slow queries and system database errors.

- **Row Count in Active FY:** `0`
- **Total Columns:** `5`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `UserName` | `WCHAR(20.0)` | Yes |  | Operator username who performed the action |
| 2 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 3 | `Qry` | `WCHAR` | Yes |  | Text attribute: Qry |
| 4 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 5 | `ErrStr` | `WCHAR` | Yes |  | Text attribute: ErrStr |

---

<a name="table-datasync"></a>

### Table: `DataSync`

> **Purpose:** Multi-branch data synchronization journal recording packet IDs, sync timestamps, and replication status.

- **Row Count in Active FY:** `0`
- **Total Columns:** `37`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `UID` | `INTEGER (Long)` | No |  | Integer identifier or enum code for UID |
| 2 | `BranchCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for BranchCode |
| 3 | `RecType` | `SMALLINT` | Yes |  | Record discriminator enum distinguishing line types |
| 4 | `Type` | `SMALLINT` | Yes |  | Integer identifier or enum code for Type |
| 5 | `VMType` | `SMALLINT` | Yes |  | Integer identifier or enum code for VMType |
| 6 | `MasterName` | `WCHAR(40.0)` | Yes |  | Text attribute: MasterName |
| 7 | `VchNo` | `WCHAR(25.0)` | Yes |  | User-facing invoice / voucher series number string (e.g. HPS00001) |
| 8 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 9 | `VchSrCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchSrCode |
| 10 | `CreatedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: CreatedBy |
| 11 | `CreationTime` | `DATETIME` | Yes |  | Timestamp / Date field for CreationTime |
| 12 | `LastModifiedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: LastModifiedBy |
| 13 | `LastModificationTime` | `DATETIME` | Yes |  | Timestamp / Date field for LastModificationTime |
| 14 | `ApprovedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: ApprovedBy |
| 15 | `ApprovalTime` | `DATETIME` | Yes |  | Timestamp / Date field for ApprovalTime |
| 16 | `ServerInTime` | `DATETIME` | Yes |  | Timestamp / Date field for ServerInTime |
| 17 | `M1` | `WCHAR` | Yes |  | Text attribute: M1 |
| 18 | `M2` | `WCHAR` | Yes |  | Text attribute: M2 |
| 19 | `MasterName1` | `WCHAR(40.0)` | Yes |  | Text attribute: MasterName1 |
| 20 | `ComputerName` | `WCHAR(255.0)` | Yes |  | Text attribute: ComputerName |
| 21 | `OldVchSrName` | `WCHAR(10.0)` | Yes |  | Text attribute: OldVchSrName |
| 22 | `OldVchType` | `SMALLINT` | Yes |  | Integer identifier or enum code for OldVchType |
| 23 | `VchSrName` | `WCHAR(10.0)` | Yes |  | Text attribute: VchSrName |
| 24 | `DeletedBy` | `WCHAR(20.0)` | Yes |  | Text attribute: DeletedBy |
| 25 | `DeletionTime` | `DATETIME` | Yes |  | Timestamp / Date field for DeletionTime |
| 26 | `Srno` | `SMALLINT` | Yes |  | Integer identifier or enum code for Srno |
| 27 | `CheckType` | `SMALLINT` | Yes |  | Integer identifier or enum code for CheckType |
| 28 | `ClearFullVch` | `BOOLEAN` | No |  | Boolean flag for ClearFullVch (True/False) |
| 29 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 30 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 31 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 32 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 33 | `D5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D5 |
| 34 | `OldMasterName` | `WCHAR(40.0)` | Yes |  | Text attribute: OldMasterName |
| 35 | `OldDate` | `DATETIME` | Yes |  | Timestamp / Date field for OldDate |
| 36 | `OldVchNo` | `WCHAR(25.0)` | Yes |  | Text attribute: OldVchNo |
| 37 | `OldIdentity` | `WCHAR` | Yes |  | Text attribute: OldIdentity |

---

<a name="table-cloudsyncstatus"></a>

### Table: `CloudSyncStatus`

> **Purpose:** Overall status of Busy Cloud data synchronization (bulk sync versus incremental sync state).

- **Row Count in Active FY:** `0`
- **Total Columns:** `10`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `BulkStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for BulkStatus |
| 2 | `BulkStatusDet` | `WCHAR` | Yes |  | Text attribute: BulkStatusDet |
| 3 | `BulkDateTime` | `DATETIME` | Yes |  | Timestamp / Date field for BulkDateTime |
| 4 | `BulkComputerName` | `WCHAR(255.0)` | Yes |  | Text attribute: BulkComputerName |
| 5 | `BulkIP` | `WCHAR(255.0)` | Yes |  | Text attribute: BulkIP |
| 6 | `IncrStatus` | `SMALLINT` | Yes |  | Integer identifier or enum code for IncrStatus |
| 7 | `IncrStatusDet` | `WCHAR` | Yes |  | Text attribute: IncrStatusDet |
| 8 | `IncrDateTime` | `DATETIME` | Yes |  | Timestamp / Date field for IncrDateTime |
| 9 | `IncrComputerName` | `WCHAR(255.0)` | Yes |  | Text attribute: IncrComputerName |
| 10 | `IncrIP` | `WCHAR(255.0)` | Yes |  | Text attribute: IncrIP |

---

<a name="table-cloudsyncincr"></a>

### Table: `CloudSyncIncr`

> **Purpose:** Queue of incremental database changes pending upload to Busy Cloud.

- **Row Count in Active FY:** `0`
- **Total Columns:** `12`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Code` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for Code |
| 2 | `Type` | `SMALLINT` | Yes |  | Integer identifier or enum code for Type |
| 3 | `SubType` | `SMALLINT` | Yes |  | Integer identifier or enum code for SubType |
| 4 | `Action` | `SMALLINT` | Yes |  | Integer identifier or enum code for Action |
| 5 | `VchMastCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for VchMastCode |
| 6 | `EntryDateTime` | `DATETIME` | Yes |  | Timestamp / Date field for EntryDateTime |
| 7 | `Error` | `WCHAR(255.0)` | Yes |  | Text attribute: Error |
| 8 | `Status` | `SMALLINT` | Yes |  | Integer identifier or enum code for Status |
| 9 | `SelfImageLink` | `WCHAR(255.0)` | Yes |  | Text attribute: SelfImageLink |
| 10 | `BusyDocLink` | `WCHAR(255.0)` | Yes |  | Text attribute: BusyDocLink |
| 11 | `FormatType` | `SMALLINT` | Yes |  | Integer identifier or enum code for FormatType |
| 12 | `Description` | `WCHAR(255.0)` | Yes |  | Text attribute: Description |

---

<a name="table-cloudsyncincrdet"></a>

### Table: `CloudSyncIncrDet`

> **Purpose:** XML data payloads of incremental changes waiting to be replicated.

- **Row Count in Active FY:** `0`
- **Total Columns:** `3`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Code` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for Code |
| 2 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 3 | `XMLStr` | `WCHAR` | Yes |  | Text attribute: XMLStr |

---

<a name="table-checklist"></a>

### Table: `CheckList`

> **Purpose:** Task checklist items and audit approval state.

- **Row Count in Active FY:** `0`
- **Total Columns:** `12`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `Type` | `SMALLINT` | Yes |  | Integer identifier or enum code for Type |
| 2 | `Code` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for Code |
| 3 | `Action` | `SMALLINT` | Yes |  | Integer identifier or enum code for Action |
| 4 | `ActionTime` | `DATETIME` | Yes |  | Timestamp / Date field for ActionTime |
| 5 | `UserName` | `WCHAR(20.0)` | Yes |  | Operator username who performed the action |
| 6 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 7 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 8 | `D3` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D3 |
| 9 | `D4` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D4 |
| 10 | `D5` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D5 |
| 11 | `Notes` | `WCHAR` | Yes |  | Text attribute: Notes |
| 12 | `ComputerName` | `WCHAR(25.0)` | Yes |  | Text attribute: ComputerName |

---

<a name="table-checklistnew"></a>

### Table: `CheckListNew`

> **Purpose:** Workflow approval headers for multi-level voucher authorization hierarchies.

- **Row Count in Active FY:** `0`
- **Total Columns:** `10`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `UID` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for UID |
| 2 | `Type` | `SMALLINT` | Yes |  | Integer identifier or enum code for Type |
| 3 | `Code` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for Code |
| 4 | `Action` | `SMALLINT` | Yes |  | Integer identifier or enum code for Action |
| 5 | `ActionTime` | `DATETIME` | Yes |  | Timestamp / Date field for ActionTime |
| 6 | `UserName` | `WCHAR(20.0)` | Yes |  | Operator username who performed the action |
| 7 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 8 | `D2` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D2 |
| 9 | `ComputerName` | `WCHAR(100.0)` | Yes |  | Text attribute: ComputerName |
| 10 | `Remarks` | `WCHAR(100.0)` | Yes |  | Text attribute: Remarks |

---

<a name="table-checklistnewdet"></a>

### Table: `CheckListNewDet`

> **Purpose:** Workflow authorization signatures and approval payloads.

- **Row Count in Active FY:** `0`
- **Total Columns:** `3`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `UID` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for UID |
| 2 | `SrNo` | `SMALLINT` | Yes |  | Integer identifier or enum code for SrNo |
| 3 | `XMLStr` | `WCHAR` | Yes |  | Text attribute: XMLStr |

---

<a name="table-repcolsize"></a>

### Table: `RepColSize`

> **Purpose:** User-customized column widths and display formats for financial statements and registers.

- **Row Count in Active FY:** `38`
- **Total Columns:** `7`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RepID` | `SMALLINT` | Yes |  | Integer identifier or enum code for RepID |
| 2 | `SubID` | `SMALLINT` | Yes |  | Integer identifier or enum code for SubID |
| 3 | `ColID` | `SMALLINT` | Yes |  | Integer identifier or enum code for ColID |
| 4 | `ColSize` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for ColSize |
| 5 | `FormatName` | `WCHAR(35.0)` | Yes |  | Text attribute: FormatName |
| 6 | `CustomRepFormatName` | `WCHAR(255.0)` | Yes |  | Text attribute: CustomRepFormatName |
| 7 | `WideScreen` | `BOOLEAN` | No |  | Boolean flag for WideScreen (True/False) |

---

<a name="table-repoptvalues"></a>

### Table: `RepOptValues`

> **Purpose:** Saved report filter presets (date ranges, party selections, group filters).

- **Row Count in Active FY:** `40`
- **Total Columns:** `9`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `RepID` | `SMALLINT` | Yes |  | Integer identifier or enum code for RepID |
| 2 | `ReportType` | `SMALLINT` | Yes |  | Integer identifier or enum code for ReportType |
| 3 | `ValueType` | `SMALLINT` | Yes |  | Integer identifier or enum code for ValueType |
| 4 | `Value` | `WCHAR(255.0)` | Yes |  | Text attribute: Value |
| 5 | `MasterType` | `SMALLINT` | Yes |  | Polymorphic Entity Type enum (1=AccountGroup, 2=Account, 6=Item, 8=Unit, 9=BillSundry, 21=TaxCategory) |
| 6 | `FieldID` | `SMALLINT` | Yes |  | Integer identifier or enum code for FieldID |
| 7 | `FieldValue` | `WCHAR` | Yes |  | Text attribute: FieldValue |
| 8 | `SubRepID` | `SMALLINT` | Yes |  | Integer identifier or enum code for SubRepID |
| 9 | `FormatName` | `WCHAR(40.0)` | Yes |  | Text attribute: FormatName |

---

<a name="table-reportnotes"></a>

### Table: `ReportNotes`

> **Purpose:** User annotations and sticky notes attached to specific balance sheet and ledger reports.

- **Row Count in Active FY:** `0`
- **Total Columns:** `10`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `NoteID` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for NoteID |
| 2 | `RepID` | `SMALLINT` | Yes |  | Integer identifier or enum code for RepID |
| 3 | `SubRepID` | `SMALLINT` | Yes |  | Integer identifier or enum code for SubRepID |
| 4 | `NoteRepID` | `SMALLINT` | Yes |  | Integer identifier or enum code for NoteRepID |
| 5 | `MasterCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for MasterCode |
| 6 | `UserName` | `WCHAR(255.0)` | Yes |  | Operator username who performed the action |
| 7 | `Date` | `DATETIME` | Yes |  | Transaction / Voucher Date |
| 8 | `Description` | `WCHAR` | Yes |  | Text attribute: Description |
| 9 | `NotesCarried` | `BOOLEAN` | No |  | Boolean flag for NotesCarried (True/False) |
| 10 | `FinYear` | `DATETIME` | Yes |  | Timestamp / Date field for FinYear |

---

<a name="table-patches"></a>

### Table: `Patches`

> **Purpose:** Version migration patch history applied to the operational database (db1YYYY.bds).

- **Row Count in Active FY:** `0`
- **Total Columns:** `79`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `DummyFld` | `BOOLEAN` | No |  | Boolean flag for DummyFld (True/False) |
| 2 | `MasterNotes` | `BOOLEAN` | No |  | Boolean flag for MasterNotes (True/False) |
| 3 | `MBO` | `BOOLEAN` | No |  | Boolean flag for MBO (True/False) |
| 4 | `UFSU` | `BOOLEAN` | No |  | Boolean flag for UFSU (True/False) |
| 5 | `DUFITC` | `BOOLEAN` | No |  | Boolean flag for DUFITC (True/False) |
| 6 | `CheckList` | `BOOLEAN` | No |  | Boolean flag for CheckList (True/False) |
| 7 | `SPACC` | `BOOLEAN` | No |  | Boolean flag for SPACC (True/False) |
| 8 | `UMBDB1` | `BOOLEAN` | No |  | Boolean flag for UMBDB1 (True/False) |
| 9 | `BCNAltQty` | `BOOLEAN` | No |  | Boolean flag for BCNAltQty (True/False) |
| 10 | `UMB1` | `BOOLEAN` | No |  | Boolean flag for UMB1 (True/False) |
| 11 | `ExpBatch` | `BOOLEAN` | No |  | Boolean flag for ExpBatch (True/False) |
| 12 | `QuoteDefaultSeries` | `BOOLEAN` | No |  | Boolean flag for QuoteDefaultSeries (True/False) |
| 13 | `BatchStkTfr` | `BOOLEAN` | No |  | Boolean flag for BatchStkTfr (True/False) |
| 14 | `ImpactBSSalePurc` | `BOOLEAN` | No |  | Boolean flag for ImpactBSSalePurc (True/False) |
| 15 | `DiscMarkupConfig` | `BOOLEAN` | No |  | Boolean flag for DiscMarkupConfig (True/False) |
| 16 | `PickQtnAltQty` | `BOOLEAN` | No |  | Boolean flag for PickQtnAltQty (True/False) |
| 17 | `VchAudit` | `BOOLEAN` | No |  | Boolean flag for VchAudit (True/False) |
| 18 | `DiscHelpData` | `BOOLEAN` | No |  | Boolean flag for DiscHelpData (True/False) |
| 19 | `ItemSrNoLen` | `BOOLEAN` | No |  | Boolean flag for ItemSrNoLen (True/False) |
| 20 | `SalaryDefaultSeries` | `BOOLEAN` | No |  | Boolean flag for SalaryDefaultSeries (True/False) |
| 21 | `FinalResults` | `BOOLEAN` | No |  | Boolean flag for FinalResults (True/False) |
| 22 | `PDCT3` | `BOOLEAN` | No |  | Boolean flag for PDCT3 (True/False) |
| 23 | `PaidDays` | `BOOLEAN` | No |  | Boolean flag for PaidDays (True/False) |
| 24 | `PUSJMC` | `BOOLEAN` | No |  | Boolean flag for PUSJMC (True/False) |
| 25 | `CRSalesDefaultSeries` | `BOOLEAN` | No |  | Boolean flag for CRSalesDefaultSeries (True/False) |
| 26 | `UFRD` | `BOOLEAN` | No |  | Boolean flag for UFRD (True/False) |
| 27 | `DefaultSettlementMode` | `BOOLEAN` | No |  | Boolean flag for DefaultSettlementMode (True/False) |
| 28 | `DefaultExciseType` | `BOOLEAN` | No |  | Boolean flag for DefaultExciseType (True/False) |
| 29 | `BatchDate` | `SMALLINT` | Yes |  | Integer identifier or enum code for BatchDate |
| 30 | `IndentDefaultSeries` | `BOOLEAN` | No |  | Boolean flag for IndentDefaultSeries (True/False) |
| 31 | `UserRights` | `BOOLEAN` | No |  | Boolean flag for UserRights (True/False) |
| 32 | `AccCodes` | `BOOLEAN` | No |  | Boolean flag for AccCodes (True/False) |
| 33 | `ItemMastDefaultPrice` | `BOOLEAN` | No |  | Boolean flag for ItemMastDefaultPrice (True/False) |
| 34 | `ItemMastTreatMRPAsSP` | `BOOLEAN` | No |  | Boolean flag for ItemMastTreatMRPAsSP (True/False) |
| 35 | `Help1AddnInfo` | `BOOLEAN` | No |  | Boolean flag for Help1AddnInfo (True/False) |
| 36 | `ItemParamNettAmt` | `BOOLEAN` | No |  | Boolean flag for ItemParamNettAmt (True/False) |
| 37 | `PricingModeDiscConfig` | `BOOLEAN` | No |  | Boolean flag for PricingModeDiscConfig (True/False) |
| 38 | `PIRDiscAmt` | `BOOLEAN` | No |  | Boolean flag for PIRDiscAmt (True/False) |
| 39 | `UpgradeForSchemeMast` | `BOOLEAN` | No |  | Boolean flag for UpgradeForSchemeMast (True/False) |
| 40 | `UpgradeForTaxCategory` | `BOOLEAN` | No |  | Boolean flag for UpgradeForTaxCategory (True/False) |
| 41 | `UpgradeForSTPTinHelp1` | `BOOLEAN` | No |  | Boolean flag for UpgradeForSTPTinHelp1 (True/False) |
| 42 | `RCMPURC` | `BOOLEAN` | No |  | Boolean flag for RCMPURC (True/False) |
| 43 | `GSTSumItemWiseFields` | `BOOLEAN` | No |  | Boolean flag for GSTSumItemWiseFields (True/False) |
| 44 | `VchGSTSumItemWiseLocType` | `BOOLEAN` | No |  | Boolean flag for VchGSTSumItemWiseLocType (True/False) |
| 45 | `UpdateStateAndTypeOfDealerInVchGST` | `BOOLEAN` | No |  | Boolean flag for UpdateStateAndTypeOfDealerInVchGST (True/False) |
| 46 | `GSTAdvanceAmt` | `BOOLEAN` | No |  | Boolean flag for GSTAdvanceAmt (True/False) |
| 47 | `UpgradeForNoneUnit` | `BOOLEAN` | No |  | Boolean flag for UpgradeForNoneUnit (True/False) |
| 48 | `GSTPurcBillNo` | `BOOLEAN` | No |  | Boolean flag for GSTPurcBillNo (True/False) |
| 49 | `StateMastOtherUpgrade` | `BOOLEAN` | No |  | Boolean flag for StateMastOtherUpgrade (True/False) |
| 50 | `UpdateRCMAccTaxType` | `BOOLEAN` | No |  | Boolean flag for UpdateRCMAccTaxType (True/False) |
| 51 | `UNITINHSN` | `BOOLEAN` | No |  | Boolean flag for UNITINHSN (True/False) |
| 52 | `ItemMastTaxInclFld` | `BOOLEAN` | No |  | Boolean flag for ItemMastTaxInclFld (True/False) |
| 53 | `QLFld` | `BOOLEAN` | No |  | Boolean flag for QLFld (True/False) |
| 54 | `UPGUAE` | `BOOLEAN` | No |  | Boolean flag for UPGUAE (True/False) |
| 55 | `EWAYBILL` | `BOOLEAN` | No |  | Boolean flag for EWAYBILL (True/False) |
| 56 | `EWAYBILLCONFIG` | `BOOLEAN` | No |  | Boolean flag for EWAYBILLCONFIG (True/False) |
| 57 | `UpdateRegExpenseAccName` | `BOOLEAN` | No |  | Boolean flag for UpdateRegExpenseAccName (True/False) |
| 58 | `POSItemAliasFld` | `BOOLEAN` | No |  | Boolean flag for POSItemAliasFld (True/False) |
| 59 | `ConfigUAE` | `BOOLEAN` | No |  | Boolean flag for ConfigUAE (True/False) |
| 60 | `ConfigEWayBill` | `BOOLEAN` | No |  | Boolean flag for ConfigEWayBill (True/False) |
| 61 | `ITEMSPACC` | `BOOLEAN` | No |  | Boolean flag for ITEMSPACC (True/False) |
| 62 | `UMBSV` | `BOOLEAN` | No |  | Boolean flag for UMBSV (True/False) |
| 63 | `ItemCategory` | `BOOLEAN` | No |  | Boolean flag for ItemCategory (True/False) |
| 64 | `AccountCategory` | `BOOLEAN` | No |  | Boolean flag for AccountCategory (True/False) |
| 65 | `UFOESA` | `BOOLEAN` | No |  | Boolean flag for UFOESA (True/False) |
| 66 | `DUFBAF` | `BOOLEAN` | No |  | Boolean flag for DUFBAF (True/False) |
| 67 | `UVGS` | `BOOLEAN` | No |  | Boolean flag for UVGS (True/False) |
| 68 | `RESAVEGSTR1JSON` | `BOOLEAN` | No |  | Boolean flag for RESAVEGSTR1JSON (True/False) |
| 69 | `GroupParamOnSP` | `BOOLEAN` | No |  | Boolean flag for GroupParamOnSP (True/False) |
| 70 | `ITEMBCN` | `BOOLEAN` | No |  | Boolean flag for ITEMBCN (True/False) |
| 71 | `UFTDSCAT` | `BOOLEAN` | No |  | Boolean flag for UFTDSCAT (True/False) |
| 72 | `UFTCSTDS` | `BOOLEAN` | No |  | Boolean flag for UFTCSTDS (True/False) |
| 73 | `MRPNegativeStockWarning` | `SMALLINT` | Yes |  | Integer identifier or enum code for MRPNegativeStockWarning |
| 74 | `TEMCWiseRef` | `BOOLEAN` | No |  | Boolean flag for TEMCWiseRef (True/False) |
| 75 | `SupplierDutyDet` | `BOOLEAN` | No |  | Boolean flag for SupplierDutyDet (True/False) |
| 76 | `StateCodesUpdate` | `BOOLEAN` | No |  | Boolean flag for StateCodesUpdate (True/False) |
| 77 | `UpdateShowTaxSummary` | `BOOLEAN` | No |  | Boolean flag for UpdateShowTaxSummary (True/False) |
| 78 | `CountryCodesUpdate` | `BOOLEAN` | No |  | Boolean flag for CountryCodesUpdate (True/False) |
| 79 | `UpdateCurCodeInCurrency` | `BOOLEAN` | No |  | Boolean flag for UpdateCurCodeInCurrency (True/False) |

---

<a name="table-externaldata"></a>

### Table: `ExternalData`

> **Purpose:** Integration data bridge for external third-party software (CRM, WMS, eCommerce platforms).

- **Row Count in Active FY:** `0`
- **Total Columns:** `15`
- **Primary Key:** *None defined (surrogate or multi-column indexed)*

| # | Column Name | Data Type | Nullable | Primary Key | Description / Purpose |
|---|-------------|-----------|:--------:|:-----------:|-----------------------|
| 1 | `KeyType` | `SMALLINT` | Yes |  | Integer identifier or enum code for KeyType |
| 2 | `KeyCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for KeyCode |
| 3 | `AppName` | `WCHAR(20.0)` | Yes |  | Text attribute: AppName |
| 4 | `CanEditKeyData` | `BOOLEAN` | No |  | Boolean flag for CanEditKeyData (True/False) |
| 5 | `CanDeleteKeyData` | `BOOLEAN` | No |  | Boolean flag for CanDeleteKeyData (True/False) |
| 6 | `I1` | `SMALLINT` | Yes |  | Integer identifier or enum code for I1 |
| 7 | `L1` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for L1 |
| 8 | `D1` | `DOUBLE` | Yes |  | Numeric monetary / quantity value for D1 |
| 9 | `B1` | `BOOLEAN` | No |  | Boolean flag for B1 (True/False) |
| 10 | `DT1` | `DATETIME` | Yes |  | Timestamp / Date field for DT1 |
| 11 | `C1` | `WCHAR(20.0)` | Yes |  | Text attribute: C1 |
| 12 | `Connected` | `BOOLEAN` | No |  | Boolean flag for Connected (True/False) |
| 13 | `ConnectedCode` | `INTEGER (Long)` | Yes |  | Integer identifier or enum code for ConnectedCode |
| 14 | `WarningType` | `SMALLINT` | Yes |  | Integer identifier or enum code for WarningType |
| 15 | `C2` | `WCHAR(255.0)` | Yes |  | Text attribute: C2 |

---

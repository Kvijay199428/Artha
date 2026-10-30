# BusyWin Font Analysis & ARTHA Integration Guide

## Executive Summary

Through binary reverse-engineering and inspection of BusyWin (`C:\BusyWin\Busy21.exe`, `C:\BusyWin\SYSTEM\FORMATS.BDS`, `C:\BusyWin\DATA\setup.exe`, and the Windows system font subsystem), we identified the exact fonts bundled and utilized by BusyWin across its UI, billing formats, and print subsystem.

All identified font assets have been extracted, cataloged, and integrated directly into ARTHA's font suite under `public/fonts/` with `@font-face` definitions in `public/fonts/fonts.css` and linked in `src/index.html`.

---

## 1. BusyWin Font Inventory & Usage Breakdown

| Font Family | Font Files | Category / Purpose in BusyWin |
| :--- | :--- | :--- |
| **Oloron** | `Oloron__.TTF` | Core BusyWin high-density invoice and document font |
| **Oloron Condensed** | `OLORC___.TTF` (Regular)<br>`OLORCB__.TTF` (Bold)<br>`OLORCI__.TTF` (Italic)<br>`OLORCBI_.TTF` (Bold Italic) | Compact 80-column and 132-column printing; compact tables |
| **Oloron EXP** | `OLORE___.TTF` (Regular)<br>`OLOREB__.TTF` (Bold)<br>`OLOREI__.TTF` (Italic)<br>`OLOREBI_.TTF` (Bold Italic) | Expanded title banners and highlighted account names |
| **Oloron Ultra Condensed** | `OLORUC__.TTF` (Regular)<br>`OLORUCB_.TTF` (Bold)<br>`OLORUCI_.TTF` (Italic)<br>`OLORUCBI.TTF` (Bold Italic) | Narrow POS receipt slips (3-inch / 58mm / 80mm thermal rolls) |
| **Rupee Foradian** | `Rupee_Foradian.ttf` | Dedicated Indian Rupee (`₹`) currency symbol font |
| **Microsoft Sans Serif** | `micross.ttf` | Classical Win32 / VB6 application UI, dialogs, forms, menus |
| **Tahoma** | `tahoma.ttf`<br>`tahomabd.ttf` | Data grid headers, report titles, and dialog labels |
| **Calibri** | `calibri.ttf`<br>`calibrib.ttf`<br>`calibrii.ttf`<br>`calibriz.ttf` | Modern GST invoice template body font (`FORMATS.BDS`) |
| **Courier New** | `cour.ttf`<br>`courbd.ttf`<br>`couri.ttf`<br>`courbi.ttf` | Fixed-pitch dot-matrix / ESC-P printer emulation |

---

## 2. Technical Evidence & Discovery Details

### A. Oloron Font Family (BusyWin Proprietary Suite)
- **Installer Archive (`C:\BusyWin\DATA\setup.exe`)**:
  BusyWin installs the entire Oloron suite (`Oloron__.TTF`, `OLORC*.TTF`, `OLORE*.TTF`, `OLORUC*.TTF`) directly into Windows during setup.
- **Binary Code Reference (`C:\BusyWin\Busy21.exe` & `Busy2L21.dll`)**:
  Direct string references to `'Oloron'`, `'Oloron EXP'`, `'Oloron Condensed'`, and `'Oloron Ultra Condensed'` reside in the print engine and page formatting routines.

### B. Rupee Foradian Font
- Discovered in `setup.exe` (`F21639_Rupee_Foradian.ttf` -> `Rupee_Foradian.ttf`).
- Used by BusyWin accounting vouchers and invoices to render the rupee symbol using the backtick key (`` ` ``) prior to universal Unicode U+20B9 adoption.

### C. Document Formats (`C:\BusyWin\SYSTEM\FORMATS.BDS`)
Inspection of the formatting template strings inside `FORMATS.BDS` revealed explicit font directives:
```text
<DATA_FONT_ON,Calibri,8>
<DATA_FONT_ON,Calibri,10>
<DATA_FONT_ON,Calibri,12>
<DATA_FONT_ON,Courier New,8>
<DATA_FONT_ON,Tahoma,8>
<DATA_FONT_ON,Tahoma,10>
```

### D. Win32 VB6 UI Subsystem (`Busy21.exe`)
- `MS Sans Serif` (120 form references in binary)
- `Tahoma` (17 dialog references in binary)
- `Arial` (32 button/label references in binary)

---

## 3. ARTHA Integration Architecture

### Files Deployed to ARTHA
1. **Directory**: `d:\VEGA\ARTHA\public\fonts\`
   - 25 font binaries (`.ttf`) covering the complete Oloron family, Rupee Foradian, Microsoft Sans Serif, Tahoma, Calibri, and Courier New.
2. **CSS Definition**: `d:\VEGA\ARTHA\public\fonts\fonts.css`
   - Defines standard `@font-face` rules with `font-display: swap`.
3. **HTML Link**: `d:\VEGA\ARTHA\src\index.html`
   - Linked via `<link rel="stylesheet" href="/fonts/fonts.css" />`.
4. **Vite Production Build**: `d:\VEGA\ARTHA\dist\fonts\`
   - Automatically bundled into production distribution during `npm run build`.

---

## 4. How to Use in ARTHA Invoices & UI

### In CSS
```css
/* Compact BusyWin-style tabular print */
.busywin-table {
  font-family: 'Oloron Condensed', 'Calibri', sans-serif;
  font-size: 11px;
}

/* Thermal POS slip */
.pos-receipt {
  font-family: 'Oloron Ultra Condensed', monospace;
  font-size: 10px;
}

/* Legacy Rupee Symbol */
.currency-symbol {
  font-family: 'Rupee Foradian';
}
```


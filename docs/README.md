# Documentation

Detailed reference for **Free GST Billing Software**. The main project [README](../README.md) is the
overview and feature list — everything below is the deep-dive material.

| Document | What's in it |
|---|---|
| **[USER_GUIDE.md](./USER_GUIDE.md)** | Plain-language handbook for end users. Quick Start, daily-use walkthroughs, region preference, modules, PDF customisation, Terms presets, TDS / TCS, GST returns, E-Way Bill, backup & restore, moving to a new computer, FAQ, troubleshooting. |
| **[BUSYWIN_DATABASE_SCHEMA.md](./BUSYWIN_DATABASE_SCHEMA.md)** | Complete database table schemas and architectural reference for BusyWin (Microsoft Jet 4.0 / `.bds` databases). Covers all 108 tables (28 in `db.bds`, 80 in `db1YYYY.bds`), 3,628 columns, polymorphic `MasterType` enums, `VchType` voucher classifications, ER flow, and ARTHA migration mapping. |
| **[COMPETITOR_GAPS.md](./COMPETITOR_GAPS.md)** | Gap analysis vs the top 5 open-source GST projects on GitHub (ERPNext, Akaunting, Invoice Ninja, Crater, InvoiceShelf) and the top 5 commercial Indian tools (Tally, Vyapar, Zoho Books, ClearTax, Marg). Includes the prioritised roadmap and Indian Income Tax e-filing format notes. |
| **[TAX_HELPER_PLAN.md](./TAX_HELPER_PLAN.md)** | Three-tier proposal for the v1.5.x **Income Tax Helper** feature — bank-statement CSV import, ITR Filing Summary PDF, optional ITR-4 JSON generation. Explains what's possible and what isn't given the IT Department portal's constraints. |

> Looking for the version history? [CHANGELOG.md](../CHANGELOG.md) at the project root.
> Looking for licence terms? [LICENSE](../LICENSE) at the project root.
> Looking for installation? [Quick Start](../README.md#quick-start--installation) in the main README,
> or the [User Guide](./USER_GUIDE.md#quick-start) for the step-by-step version.

If you spot something stale in here, [open an issue](https://github.com/Kvijay199428/Artha/issues) — docs drift faster than code.

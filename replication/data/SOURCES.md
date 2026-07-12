# Data Sources & Manifest

This folder is the **bundled data snapshot**. It is authoritative for reproducing the
published figures. `run_all.py` reads these files by default (offline, no API key).

`--refresh` re-pulls only the **active** FRED series (needs a free `FRED_API_KEY`).
**Discontinued** series exist only as snapshots and cannot be re-pulled — which is
exactly why they are bundled. External / derived series are not FRED series and are
not auto-refreshed.

| File | FRED ID | Status | Description | Vintage |
|------|---------|--------|-------------|---------|
| CURRSL.csv | CURRSL | active | Currency component of M1 (transactional) | 2026-07 |
| DEMDEPSL.csv | DEMDEPSL | active | Demand deposits (transactional) | 2026-07 |
| M2SL.csv | M2SL | active | M2 money stock (broad) | 2026-07 |
| CPIAUCSL.csv | CPIAUCSL | active | US CPI, all urban consumers | 2026-07 |
| WSAVNS.csv | WSAVNS | **discontinued** | Savings deposits (weekly); ends 2020-04 at the M1 redefinition | snapshot |
| MDLM.csv | MDLM | active | Savings deposits; continues post-2020, splices to WSAVNS | 2026-07 |
| STDSL.csv | STDSL | active | Small-denomination time deposits (asset circuit) | 2026-07 |
| MANMM101USM189S.csv | MANMM101USM189S | active | OECD narrow money, US | 2026-07 |
| MANMM101JPM189S.csv | MANMM101JPM189S | active | OECD narrow money, Japan | 2026-07 |
| MABMM301JPM189S.csv | MABMM301JPM189S | active | OECD broad money, Japan | 2026-07 |
| JPNCPIALLMINMEI.csv | JPNCPIALLMINMEI | active | Japan CPI (OECD MEI) | 2026-07 |
| divisia_dm1.csv | — | external | CFS Divisia M1 (Center for Financial Stability) | 2026-07 |
| macro_1959_2026.csv | — | derived | Assembled macro panel from the Paper 10 package | 2026-07 |

## Why a snapshot at all?
Two honest reasons: (1) some series are **discontinued** (WSAVNS, and OCD before it),
so a live pull cannot reproduce the work — the snapshot is the only way. (2) FRED
revises data, so a snapshot pins the exact numbers behind the published figures.
`--refresh` is offered for anyone who wants current data and accepts it may differ
slightly from the published values.

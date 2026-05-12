# Citizens Standard — Paper 2 Replication Materials

Replication materials for *The Citizens Standard as Counterfactual Benchmark*
(Neo-Solon, 2026).

## What's in this package

| File | Purpose |
|------|---------|
| `citizens_standard_historical_data_1960_2025.csv` | Annual dataset 1960–2025 |
| `replication.py` | Self-contained replication script (no CSV dependency) |
| `paper2_authoritative_computation.py` | Alternative replication using the CSV |
| `audit_csv_returns.py` | Optional diagnostic: audits the CSV against Damodaran+BLS |
| `damodaran_authoritative.py` | Damodaran nominal and BLS CPI Dec-Dec data dicts |
| `citizens_standard_mc/` | Monte Carlo extension (Section 6) — engine, data, figures |

## Running the replication

### Option 1: Self-contained script (no CSV needed)
```bash
python3 replication.py
```
This script embeds all data inline and produces every table from Sections 4 and 5.

### Option 2: CSV-based script (reproducible from external sources)
```bash
python3 paper2_authoritative_computation.py
```
This reads `citizens_standard_historical_data_1960_2025.csv` and the BEA
real-GDP-growth series inlined in the script. Both options produce the same
headline figures to within $100 (small differences from rounding precision
between the embedded constants and CSV-stored values).

### Option 3: Verify data integrity
```bash
python3 audit_csv_returns.py
```
This audits the CSV's `sp500_real_total_return_pct` column against
authoritative Damodaran nominal returns Fisher-deflated by BLS CPI-U Dec-Dec.
Useful for confirming the CSV is internally consistent with its declared
sources.

### Monte Carlo (Section 6)
See `citizens_standard_mc/README.md`. Runtime ~20 seconds for the full
16-configuration grid (4 cohorts × 2 universes × 2 methods × 10,000 paths).

## Data sources

All sources are public and externally verifiable:

- **S&P 500 nominal total returns 1960–2025:** Damodaran (NYU Stern), January 5,
  2026 release, table at
  https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html
  2025 value: +17.78%. (Bloomberg and RBC report +17.9%; the 0.12pp difference
  is immaterial.)
- **CPI-U Dec-Dec percent changes 1960–2025:** BLS historical archive plus
  recent news releases. 2024: +2.9% (BLS news release Jan 15, 2025). 2025:
  +2.7% (BLS news release Jan 13, 2026).
- **Real GDP growth 1960–2025:** BEA chain-weighted (FRED A191RP1A027NBEA).
- **M2 money supply:** FRED M2SL annual averages.
- **Population:** Census Bureau mid-year estimates.
- **Nominal GDP:** BEA NIPA Tables / FRED GDPA.
- **Real S&P 500 returns:** Computed at the row level in the CSV as
  (1+nominal)/(1+CPI)−1 (Fisher equation) from the `sp500_nominal_total_return_pct`
  and `cpi_decdec_pct` columns.

## Citation

If you use this replication material, please cite:

> Neo-Solon. *The Citizens Standard as Counterfactual Benchmark: Empirical
> Analysis of an Alternative US Monetary Architecture, 1960–2055*. Working
> Paper, May 2026.

And for the companion architectural paper:

> Neo-Solon. *The Citizens Standard — One Model, Many Constitutional Systems*.
> Working Paper, May 2026. Available at
> https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6702518.

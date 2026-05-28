# Replication Materials — Citizens Standard as Counterfactual Benchmark

Replication code, data, and figures for the working paper:

> Neo-Solon (2026). *The Citizens Standard as Counterfactual Benchmark: Empirical Analysis of an Alternative US Monetary Architecture, 1960–2055.* Working Paper.
> SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6735078

These materials reproduce every number, table, and figure in the empirical paper from authoritative primary-source data (FRED, BLS, BEA, Census, Damodaran/NYU Stern). They also reproduce the headline cross-references in the architectural companion paper:

> Neo-Solon (2026). *The Citizens Standard — One Model, Many Constitutional Systems.* Working Paper.
> SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6702518

## Quick start

Requirements: **Python 3.8 or newer** with `numpy` and `matplotlib`.

```bash
pip install numpy matplotlib
python3 code/run_all_tables.py
```

Runtime is approximately 1 second on a modern single core. Output is written to stdout and to `all_results.txt`.

To regenerate the four Monte Carlo figures:

```bash
python3 code/mc_plots.py
```

Figures are written to `figures/`.

## Folder structure

```
replication/
├── README.md                        ← this file
├── AUDIT.md                         ← data verification report with primary-source citations
├── all_results.txt                  ← full text output of every table in the paper
├── data/
│   ├── citizens_standard_historical_data_1960_2025_v2.csv   (66 rows — main paper)
│   └── citizens_standard_historical_data_1928_2025_full.csv (97 rows — Monte Carlo)
├── code/
│   ├── authoritative_data.py        ← source-of-truth historical data dicts (1928–2025)
│   ├── deterministic_engine.py      ← K1/K2 formulas; cohort computation (Sections 3–5)
│   ├── mc_engine.py                 ← Monte Carlo bootstrap engine (Section 6)
│   ├── mc_plots.py                  ← generates Figures M1–M4
│   ├── run_all_tables.py            ← runs every table in the paper; writes all_results.txt
│   ├── build_csv.py                 ← exports authoritative_data.py as CSV
│   └── compare_to_paper.py          ← audits paper claims against reconstruction
└── figures/
    ├── figure_M1_distributions.png        ← MC distribution density plots
    ├── figure_M2_percentile_bands.png     ← MC percentile bands by cohort
    ├── figure_M3_p_below_median.png       ← P(<median) bar chart across configurations
    └── figure_M4_p50_p5_sensitivity.png   ← P50/P5 sensitivity to bootstrap configuration
```

## What each script does

**`authoritative_data.py`** is the source of truth. Every historical series (CPI, GDP, real GDP growth, S&P 500 nominal total return, M2, population) lives here as a Python dictionary keyed by year. Every value is documented in `AUDIT.md` with its primary-source citation. **If a number is wrong, this is the file to fix.**

**`deterministic_engine.py`** implements the K1 and K2 issuance formulas from the architectural paper and computes cohort outcomes for the four cohorts tracked in Sections 4–5 (born 1960, 1970, 1980, 1990). All deposits are deflated to December 2025 purchasing power using the BLS CPI-U Dec-Dec chain before compounding at real returns. Also contains the Depression-era (1929–1945) and Stagflation-era (1966–1982) stress sequences used in Section 5.

**`mc_engine.py`** implements the Section 6 Monte Carlo. Two universes (1929–2025 and 1960–2025), two resampling methods (IID and 5-year moving block bootstrap), four cohorts — 16 configurations, 10,000 paths each, 160,000 simulated lives total. Random seeds are fixed; results are reproducible exactly.

**`mc_plots.py`** generates the four figures that appear in Section 6 of the paper.

**`run_all_tables.py`** runs everything end to end and produces `all_results.txt` — a single text file containing every numerical claim in the paper, formatted for one-glance verification against the published text.

**`build_csv.py`** is a convenience script that exports the historical data dicts to CSV for readers who want to inspect the data without running Python.

**`compare_to_paper.py`** is an audit script: it loads the paper's headline claims (the 2.21×–3.21× deterministic range, the 1.96×–4.52× bootstrap P50 range, the 5.7%–28.9% P(<median) range, etc.) and verifies them against the reconstructed results.

## Data sources

All data is from authoritative public sources. Source-by-source documentation with vintage dates is in `AUDIT.md`. Summary:

| Series | Source | Vintage |
|---|---|---|
| CPI-U Dec-Dec | BLS | Jan 2026 release |
| Nominal GDP | FRED GDPA | April 9, 2026 vintage |
| Real GDP growth | FRED A191RL1A225NBEA (BEA chain-weighted) | April 2026 |
| S&P 500 nominal total return | Damodaran/NYU Stern | Jan 2026 release |
| M2 money supply | FRED M2SL (end-of-period December) | Jan 2026 |
| Population | Census Bureau Vintage 2025 | Jan 27, 2026 release |

## Methodology notes

- **Real returns are computed via the Fisher equation:** `(1 + nominal) / (1 + CPI) − 1`. All deposits are deflated to December 2025 purchasing power before compounding at real returns. This ensures all Stable Floor balances are directly comparable to 2025 retirement-account balances.
- **K1 calibration:** 2.5% of GDP per capita at each new-citizen event (birth).
- **K2 calibration:** 0.5 × max(0, real GDP growth) × prior-year M2, distributed equally per living citizen.
- **Post-2025 projections (central scenario):** 4.5% real equity return, 4.0% nominal GDP growth, 4.5% M2 growth, 0.4% population growth, 1.8% real GDP growth, 2.5% CPI. Source: CBO Long-Term Budget Outlook 2025 baseline.
- **Monte Carlo:** 10,000 paths per configuration. Bootstrap resamples joint `(return, CPI, real-GDP-growth)` triples from the historical universe; the M2 trajectory is held deterministic. Block bootstrap uses 5-year moving blocks with circular wraparound.

## Reproducibility

Random seeds are fixed in `mc_engine.py`. Running `run_all_tables.py` reproduces every number in the paper exactly. If a number in the script output differs from the paper, the discrepancy is a bug — please open an issue at the GitHub repository.

## Headline results to verify

After running `python3 code/run_all_tables.py`, the following should appear in `all_results.txt`:

- **Section 4.1 deterministic central scenario:** Cohort A through D Stable Floors of $684,590 / $717,082 / $706,164 / $463,729 (2025 real dollars).
- **Median advantage (deterministic):** 2.63× / 2.99× / 3.21× / 2.21× — range 2.21×–3.21×.
- **Section 6 Monte Carlo P50 (1960–2025 block bootstrap):** 1.96× / 2.76× / 3.82× / 4.52× median-actual advantage by cohort.
- **Section 6 P(<median actual):** 22.6% / 13.5% / 7.5% / 5.7% (1960–2025 block bootstrap) — range 5.7%–28.4%.

These numbers should reproduce exactly. If they don't, something has changed in the environment (numpy version differences in random number generation are the most common cause).

## Banking Architecture Stress Tests

Three companion scripts address credit loss and cascade dynamics:

| Script | Description |
|--------|-------------|
| `credit_stress_test.py` | Static stress test: 7 loss rates × 5 durations. Verifies layered buffer structure (equity → TLF → payment system). |
| `credit_cascade_test_v2.py` | Fisher debt-deflation cascade model. Dynamic feedback: equity depletion → lending contraction → M2 contraction → asset deflation → additional defaults. 14-tool vs 15-tool toolkit comparison. |

Key finding: full-reserve separation protects the payment system ($8,946B transaction 
pool) under all scenarios including Depression-magnitude. M2 contraction is bounded 
by the term deposit share (60% of M2 maximum). Tool 15 reduces acute cascade 
magnitude by approximately 2-3pp; 18-month sunset limits effectiveness in prolonged 
scenarios by design.

## License

Code and data are released under CC BY 4.0. Attribution: cite the SSRN working paper.

## Companion materials

- **GitHub:** https://github.com/Neo-Solon/Citizens-Standard
- **Interactive engine** (web app for parameter exploration): see top-level repo README.
- **Architectural paper:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6702518
- **Empirical paper (this folder's companion):** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6735078

## Contact and issues

Issues, errors, or replication failures: open an issue on the GitHub repository.

Email: Neo-Solon@hotmail.com

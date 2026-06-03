# Replication Data and Code for: The Citizens Standard as Counterfactual Benchmark and Forward Projection

**Author:** Neo-Solon
**Contact:** Neo-Solon@hotmail.com
**Version:** v3 (full-rate Mode T-stable calibration; adds forward transition projection)
**License:** CC BY 4.0

This archive is the replication package for the working paper:

> Neo-Solon (2026). *The Citizens Standard as Counterfactual Benchmark and Forward Projection: An Empirical Analysis of an Alternative US Monetary Architecture, 1960–2121.* Working Paper. SSRN: 6735078

Companion papers in the series:

> Neo-Solon (2026a). *The Citizens Standard — One Model, Many Constitutional Systems.* SSRN: 6702518
> Neo-Solon (2026c). *The Citizens Standard: Transition Architecture and Migration Mechanics.* SSRN: 6810741
> Neo-Solon (2026d). *The Citizens Standard: A Statutory Implementation Pathway.* Working Paper.

---

## What changed in v3

The v1 paper modeled the framework at a **half-rate K2 calibration** (K2 = 0.5 × real GDP growth × M2), which produces mild deflationary drift. The v3 paper recalibrates to the **full real-growth-matched rate** (K2 = 1.0 × real GDP growth × M2), which is the calibration of **Mode T** and its permanent steady-state successor **Mode T-stable** (architectural paper, Section 8A). Under full-rate K2 the money supply grows at the rate of real output, producing true price stability by construction.

v3 also adds **Part II** — a forward projection of the debt-retirement transition period, modeling cohorts born 2026–2056 who live through the transition described in the transition paper (2026c). These are forward projections, clearly distinguished from the historically grounded reconstruction of Part I.

### The single calibration change

The only methodological change from v1 to v3 is one constant:

```
# deterministic_engine.py     (v1, half-rate)
K2_FRACTION = 0.5

# deterministic_engine_v3.py  (v3, full-rate Mode T-stable)
K2_FRACTION = 1.0
```

Everything else — K1, the historical data, the equity-return series, the deflation handling, the Monte Carlo bootstrap, the seeds — is identical. The v1 (half-rate) engine is retained in this archive so reviewers can confirm that the engine reproduces the published v1 figures exactly before the calibration change.

---

## Headline v3 results

### Part I — Historical counterfactual (full-rate Mode T-stable, central 4.5% real post-2025)

| Cohort | Born | Retire | Stable Floor | vs median | vs mean |
|---|---|---|---|---|---|
| A | 1960 | 2025 | $1,315,898 | 5.06× | 1.97× |
| B | 1970 | 2035 | $1,367,196 | 5.70× | 2.11× |
| C | 1980 | 2045 | $1,277,574 | 5.81× | 2.03× |
| D | 1990 | 2055 | $844,376 | 4.02× | 1.36× |

Decomposition (Cohort A): K1 $816 (0.06%), K2 $67,892 (5.16%), equity compounding $1,247,190 (94.78%).

### Part II — Forward transition cohorts (projection; full-rate K2, 0.5pp paydown compression 2026–2071)

| Cohort | Born | Retire | Pessimistic (3.0%) | Central (4.5%) | Optimistic (6.5%) | Transition cost |
|---|---|---|---|---|---|---|
| T1 | 2026 | 2091 | $327,873 | $593,225 | $1,430,549 | −11.4% |
| T2 | 2036 | 2101 | $395,120 | $717,060 | $1,732,750 | −7.9% |
| T3 | 2046 | 2111 | $473,128 | $862,111 | $2,090,735 | −4.7% |
| T4 | 2056 | 2121 | $562,468 | $1,029,284 | $2,507,336 | −2.1% |

"Transition cost" is the reduction in the central-scenario Stable Floor caused by the paydown-window return compression. It declines across cohorts because later cohorts experience proportionally less of their accumulation under compression. It is the empirical counterpart to the transition paper's claim that the debt is retired without drawing on citizen accounts.

---

## Archive structure

```
replication_v3/
├── README.md                        ← this file
├── AUDIT.md                         ← data verification + validation report
├── all_results_v3.txt               ← full text output, all v3 tables (Parts I & II)
├── all_results_halfrate_v1.txt      ← original v1 half-rate output (for reference)
├── data/
│   ├── citizens_standard_historical_data_1960_2025_v2.csv   (66 rows — main paper)
│   └── citizens_standard_historical_data_1928_2025_full.csv (97 rows — Monte Carlo)
├── code/
│   ├── authoritative_data.py        ← source-of-truth historical data dicts (1928–2025)
│   ├── deterministic_engine.py      ← v1 half-rate engine (K2_FRACTION=0.5) — reference
│   ├── deterministic_engine_v3.py   ← v3 full-rate engine (K2_FRACTION=1.0) — PRIMARY
│   ├── mc_engine.py                 ← v1 half-rate Monte Carlo — reference
│   ├── mc_engine_v3.py              ← v3 full-rate Monte Carlo — PRIMARY
│   ├── transition_cohorts_v3.py     ← Part II forward transition projection (NEW)
│   ├── run_all_tables.py            ← v1 table runner — reference
│   ├── run_all_tables_v3.py         ← v3 table runner (Part I) — PRIMARY
│   ├── mc_plots.py / mc_plots_v3.py ← figure generation (v1 / v3)
│   ├── make_fig_M5.py               ← Figure M5, forward transition cohorts (NEW)
│   ├── build_csv.py                 ← exports authoritative_data.py as CSV
│   └── compare_to_paper.py          ← audits paper claims against reconstruction
└── figures/
    ├── figure_M1_distributions_v3.png        ← MC distributions (full-rate)
    ├── figure_M2_percentile_bands_v3.png     ← MC percentile bands (full-rate)
    ├── figure_M3_p_below_median_v3.png       ← P(<median) across configs (full-rate)
    ├── figure_M4_p50_p5_sensitivity_v3.png   ← P50/P5 config sensitivity (full-rate)
    ├── figure_M5_transition_cohorts_v3.png   ← Part II forward cohorts (NEW)
    └── figure_M1..M4 (no _v3 suffix)         ← original v1 half-rate figures (reference)
```

---

## How to reproduce

Requirements: Python 3.10+, `numpy`, `matplotlib`.

```bash
cd code

# Part I — full-rate Mode T-stable tables (cohorts, decomposition, stress, Monte Carlo)
python run_all_tables_v3.py

# Part II — forward transition cohort projection
python transition_cohorts_v3.py

# Regenerate all figures
python mc_plots_v3.py        # Figures M1–M4
python make_fig_M5.py        # Figure M5

# OPTIONAL — confirm the engine reproduces the published v1 half-rate figures
# (faithfulness check before the calibration change):
python run_all_tables.py     # should print Cohort A = $684,590, etc.
```

The Monte Carlo uses a fixed base seed (`numpy.random.default_rng`, `base_seed=20260512`); results are reproducible across runs and stable across alternative seeds (variation < 0.3% on P50).

---

## The honesty boundary (important)

**Part I is a historical counterfactual.** It replays the actual 1960–2025 record (real returns, inflation, growth from primary sources) as if the mature full-rate system had existed. Its figures are grounded in observed data.

**Part II is a forward projection.** It models citizens born after enactment, using *assumed* returns (3.0% / 4.5% / 6.5% real) because the relevant period has not yet occurred. Its figures are conditional on those assumptions and are not historical observations.

The paper and this archive keep the two strictly separate and never present a Part II projection as an empirical finding. The `transition_cohorts_v3.py` module is segregated from the historical engine for exactly this reason.

---

## Data sources

All historical series in `authoritative_data.py` are from authoritative public primary sources, verified to the latest available vintage. See `AUDIT.md` for the per-series verification table. Sources: FRED (M2SL, GDP), BEA (real GDP growth), BLS (CPI-U), US Census Bureau (population), Damodaran/NYU Stern (S&P 500 total returns), SCF 2022 (retirement-wealth benchmarks), Dimson-Marsh-Staunton (global returns for non-survivor analysis).

---

## Banking architecture stress tests

Two companion scripts in `code/` address credit-loss and cascade dynamics
(added in response to academic review):

| Script | Description |
|--------|-------------|
| `credit_stress_test_v2.py` | Static no-feedback bound. Layered waterfall: bank equity ($4,473B) → TLF ($492B) → term depositors; payment pool ($8,946B) always protected. Explicitly a lower bound. |
| `credit_cascade_test_v3.py` | Dynamic Fisher debt-deflation cascade (the binding analysis). Corrected methodology: NET-M2 deflation ordering, double-entry injections, evidence-grounded transmission, modeled Tool 15 sunset, corrected current-system baseline. 14-tool vs 15-tool. |

Read the two together: the static test shows the buffer stack holds absent
amplification; the cascade shows what happens once losses compound through
debt-deflation. Where they differ, the cascade governs. Full-reserve separation
protects the payment system in both; M2 contraction is bounded by the term-
deposit share (60% maximum). Tool 15 reduces acute cascade magnitude by ~3–4pp,
sunset-bounded in prolonged scenarios.

Run:
```bash
python3 code/credit_stress_test_v2.py
python3 code/credit_cascade_test_v3.py
```

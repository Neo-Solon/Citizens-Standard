# Replication Data and Code for: The Citizens Standard as Counterfactual Benchmark and Forward Projection

**Author:** Neo-Solon
**Contact:** Neo-Solon@hotmail.com
**Version:** v3.1 (residual K1-funded full-rate calibration; adds forward transition projection)
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

## What changed in v3.1 — residual K1 funding

The v3 full-rate engine set K2 = real-growth × M2 for the whole population **and** paid the K1 citizenship deposit on top. At the aggregate that issued K1_agg + g_r·M2 — slightly **above** the real-growth line (~0.04% of M2 with current new-citizen flows), contradicting the "zero drift by construction" claim. v3.1 corrects this: **K1 is funded first from the real-growth line, and K2 receives the residual**, so that

```
K1_agg + K2_agg = g_r * M2          (the real-growth line; zero drift in growth years)
K2_agg          = g_r * M2 - K1_agg (residual)
```

Computing the residual requires the annual count of new citizens (births + naturalizations), now supplied as a sourced data module (`authoritative_newcitizens.py`). K1_agg uses the deposit-weighted count: births at the full deposit, naturalizations pro-rated by (65 − mean age)/65 per the framework rule. With FY2024-scale flows (~4.45M new citizens) K1_agg ≈ $9B, leaving K2 ≈ $438B (~$1,280/citizen) of the $447B line.

The correction lowers the headline ~2% (Cohort A $1,315,898 → **$1,290,675**, 5.06× → **4.96×**) and leaves the qualitative story unchanged. It is toggled by `K2_RESIDUAL` in `deterministic_engine_v3.py` (default `True`; set `False` to recover the v3 full-rate figures).

**One honest nuance:** in contraction years (real growth ≤ 0) K2 is already zero, so K1 cannot be netted against it and flows on top — a small **counter-cyclical** injection. The system is therefore zero-drift in growth years with a mild automatic stabilizer in downturns, not literally zero-drift in every year. (1960–2025 contains 7 such years.)

---

## Headline v3 results

### Part I — Historical counterfactual (residual K1-funded full-rate, central 4.5% real post-2025)

| Cohort | Born | Retire | Stable Floor | vs median | vs mean |
|---|---|---|---|---|---|
| A | 1960 | 2025 | $1,290,675 | 4.96× | 1.93× |
| B | 1970 | 2035 | $1,342,247 | 5.59× | 2.07× |
| C | 1980 | 2045 | $1,253,891 | 5.70× | 1.99× |
| D | 1990 | 2055 | $825,881 | 3.93× | 1.33× |

Decomposition (Cohort A): K1 $816 (0.06%), K2 $66,518 (5.15%), equity compounding $1,223,341 (94.78%).

### Part II — Forward transition cohorts (projection; full-rate K2, 0.5pp paydown compression 2026–2071)

| Cohort | Born | Retire | Pessimistic (3.0%) | Central (4.5%) | Optimistic (6.5%) | Transition cost |
|---|---|---|---|---|---|---|
| T1 | 2026 | 2091 | $322,105 | $582,542 | $1,404,338 | −11.4% |
| T2 | 2036 | 2101 | $388,727 | $705,184 | $1,703,534 | −7.9% |
| T3 | 2046 | 2111 | $466,087 | $848,974 | $2,058,290 | −4.7% |
| T4 | 2056 | 2121 | $554,772 | $1,014,858 | $2,471,530 | −2.1% |

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
│   ├── authoritative_newcitizens.py ← births (NCHS) + naturalizations (OHSS/USCIS) for K1 residual (NEW)
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
│   ├── compare_to_paper.py          ← audits paper claims against reconstruction
│   ├── paper1_figures.py            ← architecture-paper Stable Floor figures (real-return floors A $160K / B $745K / C $158K)
│   └── transition_lifetime.py       ← lifetime real value by mode-transition scenario (reproduces the 8-bar panel in paper1_figures.py)
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

# Part I — residual K1-funded tables (set K2_RESIDUAL=False in deterministic_engine_v3.py for v3 full-rate) (cohorts, decomposition, stress, Monte Carlo)
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

All historical series in `authoritative_data.py` are from authoritative public primary sources, verified to the latest available vintage. See `AUDIT.md` for the per-series verification table. Sources: FRED (M2SL, GDP), BEA (real GDP growth), BLS (CPI-U), US Census Bureau (population), Damodaran/NYU Stern (S&P 500 total returns), SCF 2022 (retirement-wealth benchmarks), Dimson-Marsh-Staunton (global returns for non-survivor analysis). New-citizen series in `authoritative_newcitizens.py`: NCHS National Vital Statistics System (annual births, 1960–2024) and DHS Office of Homeland Security Statistics / USCIS (annual naturalizations, 1960–2024; gap years interpolated).

## Demographic equity-flow model (corrected)
`code/demographic_flow_model.py` — overlapping-generations model of the Stable
Floor system's net EXTERNAL equity flow = issuance into floors minus retiree
consumption (reinvested dividends are a wash against the ex-dividend price drop,
not independent demand). Result, consistent with Macro paper Proposition 2 (§6.2)
and now dated in §6.6/A.6: the floors are net BUYERS during the accumulation
decades and cross to net SELLERS around year ~55 (robustly 43–67). The mature
outflow is the r>g rebalancing, equal at a bounded market share to (r−g)×floor
stock — a few % of GDP/yr, smooth and bounded, vanishing when r≤g. The flood-as-
crash is ruled out (gradual ramp; inheritance prevents a death-liquidation spike,
which would roughly double the outflow). Inheritance keeps the flow smooth and
bounded but does NOT make the floors permanent net buyers.
Reproduces demographic_flow.png. Run: `python code/demographic_flow_model.py`

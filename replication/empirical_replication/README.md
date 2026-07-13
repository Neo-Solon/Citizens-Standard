# Replication Data and Code for: The Citizens Standard — A Historical Counterfactual

**Author:** Neo-Solon
**Contact:** Neo-Solon@hotmail.com
**Version:** v4 (general-equilibrium realizable-return basis; Mode B 60/40 floor/dividend split)
**License:** CC BY 4.0

This archive is the replication package for the working paper:

> Neo-Solon (2026b). *The Citizens Standard: A Historical Counterfactual — Empirical Analysis of an Alternative US Monetary Architecture, 1960–2055.* Working Paper. SSRN: 6735078

Companion papers in the series:

> Neo-Solon (2026a). *The Citizens Standard: One Model, Many Systems — A Constitutional Monetary Architecture.* SSRN: 6702518
> Neo-Solon (2026c). *The Citizens Standard: Transition Architecture and Migration Mechanics.* SSRN: 6810741
> Neo-Solon (2026d). *The Citizens Standard: A Statutory Implementation Pathway.* SSRN: 6873798
> Neo-Solon (2026e). *The Citizens Standard: A Macroeconomic Model of a Two-Circuit Monetary System.* SSRN: 6939418

---

## Version history

Earlier versions of this package evolved the calibration in two steps before arriving at the current realizable-return basis: v1 modeled a half-rate K2 (K2 = 0.5 × real growth × M2, mild deflationary drift); v3 moved to the full real-growth-matched rate (K2 = 1.0 × real growth × M2, true price stability), added Part II's forward transition projection, and funded K1 first from the growth line with K2 as the residual. **v4 (current)** keeps the full-rate residual calibration and the 60/40 Mode B split, and replaces the price-taker realized return with the general-equilibrium realizable return described above.

---

## What changed in v4 — the general-equilibrium realizable return

The decisive change in this version is the return at which citizen deposits compound. Earlier versions compounded universal deposits at the realized historical S&P 500 return (~6.5% geometric real). At universal scale that is a fallacy of composition: a program that channels a share of national saving into citizen-owned equity for everyone deepens the aggregate capital stock, and a deeper stock earns a lower marginal product. The companion macroeconomic model (Neo-Solon, 2026e, Section 6.7) solves the general-equilibrium fixed point and reports, for Mode B at its 60/40 capture, a **realizable return of 4.26% real** (band 3.30%–5.03%). Every deterministic balance now compounds at that realizable return; the Monte Carlo recenters the bootstrapped historical return distribution onto it (geometric mean), preserving volatility and sequence structure.

The engine also now implements **Mode B's 60/40 split**: 60% of the post-K1 residual builds the locked floor (K2), 40% is paid as the liquid citizen dividend (K3). Two parameters control the basis, both in `deterministic_engine.py`:

```
GE_REALIZABLE_RETURN = 0.0426   # set None (and disable MC recentering) to recover the price-taker reconstruction
FLOOR_SHARE          = 0.60     # Mode B 60/40 floor share
```


---

## Headline v4 results (general-equilibrium realizable basis)

### Part I — Historical counterfactual (locked floor, Mode B 60/40, realizable return 4.26% real)

| Cohort | Born | Retire | Locked floor | vs median | vs mean | + dividend (cash) |
|---|---|---|---|---|---|---|
| A | 1960 | 2025 | $209,942 | 0.81× | 0.31× | $236,549 (0.91×) |
| B | 1970 | 2035 | $215,961 | 0.83× | 0.32× | $243,626 (0.94×) |
| C | 1980 | 2045 | $229,696 | 0.88× | 0.34× | $259,441 (1.00×) |
| D | 1990 | 2055 | $245,435 | 0.94× | 0.37× | $277,892 (1.07×) |

The floor universalizes approximately the **median** (0.81×–1.17×) at roughly **0.4× the mean** — the egalitarian signature of a universal floor. Decomposition (Cohort A): K1 $816 (0.39%), K2 floor $39,911 (19.01%), compounding gain $169,216 (80.60%) — an **81/19** split (versus 95/5 under the price-taker return). Monte Carlo (block, 1929–2025, recentered): P(floor &lt; median) = 54% (A), 40% (B), 28% (C), 22% (D); reinvesting the liquid dividend at after-tax rates reduces this to 34/22/15/11% and lifts every cohort's P50 above the median.

### Part II — Forward transition cohorts (projection; locked floor, realizable band, 0.5pp paydown compression 2026–2071)

| Cohort | Born | Retire | Low band (3.30%) | Central (4.26%) | High band (5.03%) | Transition cost |
|---|---|---|---|---|---|---|
| T1 | 2026 | 2091 | $222,624 | $327,986 | $455,997 | −11.5% |
| T2 | 2036 | 2101 | $268,606 | $396,372 | $551,561 | −7.9% |
| T3 | 2046 | 2111 | $322,106 | $476,420 | $663,935 | −4.8% |
| T4 | 2056 | 2121 | $383,531 | $568,696 | $793,933 | −2.2% |

"Transition cost" is the reduction in the central-case locked floor caused by the paydown-window return compression. It declines across cohorts because later cohorts experience proportionally less of their accumulation under compression — the empirical counterpart to the transition paper's claim that the debt is retired without drawing on citizen accounts.

---

## Archive structure

```
replication_v3/
├── README.md                        ← this file
├── AUDIT.md                         ← data verification + validation report
├── data/
│   ├── citizens_standard_historical_data_1960_2025_v2.csv   (66 rows — main paper)
│   └── citizens_standard_historical_data_1928_2025_full.csv (97 rows — Monte Carlo)
├── code/
│   ├── authoritative_data.py        ← source-of-truth historical data dicts (1928–2025)
│   ├── authoritative_newcitizens.py ← births (NCHS) + naturalizations (OHSS/USCIS) for K1 residual
│   ├── deterministic_engine.py      ← PRIMARY: GE realizable-return engine, Mode B 60/40 (GE_REALIZABLE_RETURN, FLOOR_SHARE)
│   ├── mc_engine.py                 ← PRIMARY: Monte Carlo, returns recentered on the realizable geometric mean
│   ├── transition_cohorts.py        ← PRIMARY: Part II forward transition projection (GE band)
│   ├── run_ge_results.py            ← PRIMARY: runs every table on the realizable basis
│   ├── run_all_tables.py            ← full table runner → all_results.txt
│   ├── mc_plots.py                  ← Figures M1–M4 generation (realizable basis)
│   ├── make_fig_M5.py               ← Figure M5, forward transition cohorts
│   ├── build_csv.py                 ← exports authoritative_data.py as CSV
│   ├── compare_to_paper.py          ← audits paper claims against reconstruction
│   └── transition_lifetime.py       ← lifetime real value by mode-transition scenario
└── figures/
    ├── figure_M1_distributions_v3.png        ← MC distributions (realizable basis)
    ├── figure_M2_percentile_bands_v3.png     ← MC percentile bands (realizable basis)
    ├── figure_M3_p_below_median_v3.png       ← P(<median) across configs (realizable basis)
    ├── figure_M4_p50_p5_sensitivity_v3.png   ← P50/P5 config sensitivity (realizable basis)
    └── figure_M5_transition_cohorts_v3.png   ← Part II forward cohorts (realizable band)

tool14_inflation/                    ← inflation-counterfactual appendix (self-contained)
├── code/  data/  figures/           ← Tool 14 vs the 2022 and 1972–1983 inflations
├── README.md  AUDIT.md  results.txt
   reduced form + the macro paper's Proposition 6 transmission, cross-validated;
   demand split from BLS CPI + SF Fed (Shapiro) monthly data.
```

The `tool14_inflation/` subfolder is the inflation-counterfactual appendix to this
paper. It is independent (its own README, data, and `run_counterfactual.py` /
`structural_run.py`), and it cites the macro paper's Proposition 6 (SSRN 6939418)
for the transmission it uses.

---

## How to reproduce

Requirements: Python 3.10+, `numpy`, `matplotlib`.

```bash
cd code

# Part I — cohort tables, decomposition, stress, Monte Carlo (realizable basis)
python run_ge_results.py
python run_all_tables.py     # writes all_results.txt

# Part II — forward transition cohort projection (realizable band)
python transition_cohorts.py

# Regenerate all figures
python mc_plots.py           # Figures M1–M4
python make_fig_M5.py        # Figure M5

# OPTIONAL — recover the price-taker reconstruction (realized ~6.5% return) for comparison:
# in deterministic_engine.py set GE_REALIZABLE_RETURN = None, then rerun the price-taker
```

The Monte Carlo uses a fixed base seed (`numpy.random.default_rng`, `base_seed=20260512`); results are reproducible across runs and stable across alternative seeds (variation < 0.3% on P50).

---

## The honesty boundary (important)

**Part I is a historical counterfactual.** It replays the actual 1960–2025 record (real returns, inflation, growth from primary sources) as if the mature full-rate system had existed. Its figures are grounded in observed data.

**Part II is a forward projection.** It models citizens born after enactment, using *assumed* returns (3.0% / 4.5% / 6.5% real) because the relevant period has not yet occurred. Its figures are conditional on those assumptions and are not historical observations.

The paper and this archive keep the two strictly separate and never present a Part II projection as an empirical finding. The `transition_cohorts.py` module is segregated from the historical engine for exactly this reason.

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


## One-command run (added 2026-07-07)
`pip install -r requirements.txt && python3 run_all.py` — runs the deterministic tables + Monte Carlo (refreshing `all_results.txt` at the package root), the GE results, and the to-the-dollar paper comparison. Per-script commands below remain valid.

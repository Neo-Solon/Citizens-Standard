# AUDIT — Tool 14 inflation counterfactual

Provenance of every quantitative input. The module contains no hand-fitted
parameters; the only per-episode inputs are raw BLS data and a published Fed
demand/supply share.

## Actual CPI series (raw data, not modeled)

* **2022 (Jan 2021 – Dec 2023, 36 months).** BLS CPI-U, all items, 12-month
  change, not seasonally adjusted. Exact monthly values, incl. peak 9.1% (Jun
  2022), 8.5/8.3/8.2 (Jul–Sep 2022), trough 3.0% (Jun 2023). Source: BLS;
  cross-checked against usinflationcalculator monthly table (BLS CUUR0000SA0).
* **1980 / Great Inflation (Jan 1972 – Jun 1983, 138 months).** 12-month %
  change computed directly from the BLS CPI-U monthly index (1982-84=100,
  Historical Table 24), so every value is exact and reproducible from the index
  rather than transcribed from a YoY table. The full window opens at 3.3% (Jan
  1972) and runs through both oil shocks (12.3% Dec 1974) to the 14.8% peak (Mar
  1980) and the Volcker disinflation (2.6% Jun 1983) — this is what lets the
  structural model test PREVENTION (framework present through the build-up)
  rather than only a drop-in. The earlier 48-month (Jul 1979–) window measured a
  drop-in and is superseded. Index source: U.S. BLS, bls.gov/cpi historical
  CPI-U tables. Narrative anchors: Federal Reserve History "The Great Inflation."

## Demand / supply split (the key sourced input)

* **2022.** SF Fed (Shapiro) **monthly** decomposition of year-over-year headline
  PCE inflation, taken directly from the FRBSF chart CSV
  (`supply-demand-pce-headline-yoy-chart-3.csv`), stored in `data.py` as
  `SFFED_2022` and re-exported to `data/sffed_demand_share_2022.csv`. The
  removable (demand-driven) fraction each month = demand / (demand + ambiguous +
  supply); it runs ~0.30–0.48 across the surge and is ~0.38 at the June 2022 CPI
  peak. The `ambiguous_weight` parameter allocates the ambiguous bucket (0 =
  demand-only, the conservative headline). This replaces the earlier judgment-call
  constant; grounding it in the data RAISED the framework's 2022 peak.
* **1980.** No SF Fed series (begins 1998). Federal Reserve History "The Great
  Inflation": "little debate about its source ... policies that allowed excessive
  growth in the supply of money." Carried as a literature band (low 0.55, central
  0.70, high 0.80), disclosed as an attribution rather than a decomposition.

## Framework constants

* `ANCHOR_CPI = 1.0` — near-zero price-stability anchor (Mode B), architecture paper.
* `TRIGGER_OVER = 3.0` — Tool 14 fires at anchor+3pp; Paper 1 §13.2 (Tool 14a).
* `M2_LEVEL = 22.4e12`, `GDP_LEVEL = 30.762e12` — launch-scale aggregates;
  identical to `transition_replication/appendix_A2_kt_inflation.py`.
* `TOOL14_CAP_PCT = 0.03` — Tool 14 ceiling, 3% of M2/yr (~$671B); Paper 1 §13.2.
* `PASS_THROUGH = 1.0` — unit quantity-theoretic pass-through on the demand share,
  identical convention to the KT consumer-price appendix.
* Derived: `TOOL14_MAX_PULL_PP = 0.03 * 22.4e12 / 30.762e12 * 100 ≈ 2.18pp/yr`.

## Policy-cost facts (the conventional cure, for contrast)

* **2022 Fed funds** 0.1%→5.3%, 7 hikes, first Mar 2022 (after CPI >8%). Federal
  Reserve History; Bankrate federal-funds history.
* **2022 mortgages** 30-yr fixed 3.22% (Jan) → 7.08% (Oct). Freddie Mac PMMS.
* **1980 Fed funds** peak ~19% (effective ~20%), Jun 1981. Federal Reserve
  History; Statista; St. Louis Fed.
* **1980 unemployment** 10.8%, Nov–Dec 1982 (post-WWII record at the time). BLS.
* **Sacrifice ratio ~2.5** unemployment-point-years per point of disinflation —
  standard Volcker-disinflation estimate (Goodfriend-King 2005 and successors).

## Reproducibility

`run_counterfactual.py` and `sensitivity.py` are deterministic (no RNG). Outputs
are captured in `results.txt`. Figures regenerate identically via `make_figures.py`.

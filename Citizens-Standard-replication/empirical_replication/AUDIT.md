# Citizens Standard — Data Audit and Validation Report (v3)

**Status:** All data verified against authoritative primary sources; all v3 figures validated against the engine.

This report documents two things: (1) that the historical data is sourced and correct, and (2) that the v3 full-rate engine is faithful — it reproduces the published v1 half-rate figures exactly before the calibration change, and every figure in the v3 paper traces to its output.

---

## 1. Data verification

Every variable in `authoritative_data.py` was checked against the latest available primary source.

| Series | Source | Years | Status |
|---|---|---|---|
| CPI_DECDEC | BLS historical CPI-U (Dec 2024) + Jan 2026 release | 1928–2025 (98) | All match within 0.05pp |
| CPI_ANNUAL | BLS historical CPI-U table | 1928–2025 (98) | All match within 0.05 |
| GDP_NOMINAL_B | FRED GDPA (April 2026 vintage) | 1929–2025 (97) | All match within 0.5B |
| REAL_GDP_GROWTH | FRED A191RL1A225NBEA (BEA chain-weighted) | 1929–2025 (97) | 2021–2025 confirmed directly; pre-2020 within 0.15pp |
| SP500_NOMINAL | Damodaran NYU Stern (Jan 2026 release) | 1928–2025 (98) | All match exactly |
| POPULATION_M | Census Bureau Vintage 2025 (Jan 2026) | 1928–2025 (98) | All match |
| M2_BILLIONS | FRED M2SL end-of-period (December) | 1928–2025 (98) | All match |

---

## 2. Engine faithfulness — v1 half-rate reproduction

Before changing the calibration, the engine must reproduce the published v1 figures exactly. It does:

| Cohort | Published v1 | Engine (K2=0.5) | Match |
|---|---|---|---|
| A | $684,590 | $684,590 | EXACT |
| B | $717,082 | $717,082 | EXACT |
| C | $706,164 | $706,164 | EXACT |
| D | $463,729 | $463,729 | EXACT |

Monte Carlo (Cohort A, 1929–2025 block): P5 $79K, P50 $484K, P95 $2.86M, P(<median) 28.4% — all match the published v1 figures exactly.

Run `python run_all_tables.py` to confirm.

---

## 3. v3 full-rate validation

The calibration change (K2_FRACTION 0.5 → 1.0) was validated through multiple independent checks:

**Mechanical check.** Full-rate K2 deposits are exactly 2.000× the half-rate deposits for every cohort; K1 and all returns are identical. The change does only what it should.

**Hand-computation.** An independent year-by-year reconstruction of Cohort A (deposit, deflate, compound) reproduces $1,315,898 exactly.

**Decomposition.** All four cohorts' components (K1 + K2 + compounding) sum to the final balance, and shares sum to exactly 100% (Cohort A: 0.06% + 5.16% + 94.78% = 100.00%).

**Distribution integrity.** Monte Carlo percentiles are correctly ordered (P5 < P25 < P50 < P75 < P95) and right-skewed (P50 < mean), as equity distributions must be.

### v3 headline figures (full-rate, central 4.5% real)

| Cohort | Stable Floor | vs median | vs mean |
|---|---|---|---|
| A | $1,315,898 | 5.06× | 1.97× |
| B | $1,367,196 | 5.70× | 2.11× |
| C | $1,277,574 | 5.81× | 2.03× |
| D | $844,376 | 4.02× | 1.36× |

### v3 Monte Carlo (1929–2025 block, 10K paths)

| Cohort | P5 | P50 | P95 | Mean | P(<median) |
|---|---|---|---|---|---|
| A | $155K | $930K | $5.41M | $1.62M | 12.2% |
| B | $211K | $1.28M | $7.62M | $2.29M | 6.4% |
| C | $275K | $1.66M | $10.54M | $3.09M | 3.0% |
| D | $329K | $1.92M | $12.05M | $3.53M | 1.7% |

---

## 4. Correction logged

An earlier simplified side-model (not part of this engine) estimated the full-rate Cohort A floor at approximately $1.95M. That figure was **incorrect** — it assumed the 2025-dollar K2 value applied across a citizen's entire life, whereas K2 scales with M2, which was roughly 70× smaller in 1960. The authoritative engine gives **$1,315,898** for Cohort A, and that is the figure used in the v3 paper. This is noted here so that no stale $1.95M figure is mistaken for a v3 result.

---

## 5. Part II forward-projection validation

The forward transition cohorts (`transition_cohorts_v3.py`) use the same per-year accounting as the historical engine, with two differences: post-2025 returns are assumed (not historical), and a 0.5pp compression applies during the 2026–2071 paydown window. Every figure in the paper's Tables 9 and 10 reproduces from this module:

| Cohort | Pessimistic | Central | Optimistic | Transition cost |
|---|---|---|---|---|
| T1 | $327,873 | $593,225 | $1,430,549 | −11.4% |
| T2 | $395,120 | $717,060 | $1,732,750 | −7.9% |
| T3 | $473,128 | $862,111 | $2,090,735 | −4.7% |
| T4 | $562,468 | $1,029,284 | $2,507,336 | −2.1% |

These are **forward projections**, conditional on the stated return assumptions, and are kept strictly separate from the historical reconstruction of Part I.

---

## 6. External factual anchors (verified March 2026)

The companion transition and statutory papers rely on these figures, verified against primary sources:

- Gross federal debt $39.0T; debt held by public $31.4T (~100% of GDP); intragovernmental $7.6T (CRFB, March 2026; corroborated by CBO 2026 Outlook).
- "Intragovernmental debt has no net effect on the government's overall finances" (CRFB, direct quotation; corroborated by CBO).
- CBO projection of debt held by the public rising under current law (CBO Long-Term Budget Outlook).

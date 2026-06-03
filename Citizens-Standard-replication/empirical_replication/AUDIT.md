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

---

## 7. Banking architecture stress tests

Added in response to academic review on credit-loss handling and Depression-era
cascade dynamics (r/AcademicEconomics). Two companion scripts in `code/`.

### credit_stress_test_v2.py
Run: `python3 code/credit_stress_test_v2.py`
The STATIC, no-feedback bound. Applies fixed annual loss rates (0.5–10%/yr) over
1–10 years to the lending book and runs a single coherent waterfall:
bank equity ($4,473B) → TLF ($492B) → term depositors; transaction pool
($8,946B) never enters the waterfall.
Key finding: at 6%/yr for 4 years (Depression-magnitude), cumulative loss
(~$4,294B) is just within the equity buffer (~$4,473B), so the static bound
shows near-zero depositor loss. This is explicitly a lower bound — it omits
deleveraging and Fisher amplification. The binding analysis is the cascade
model below. (v2 fixes a v1 accounting inconsistency in which the loop and
summary depositor-loss calculations disagreed at the equity crossover.)

### credit_cascade_test_v3.py
Run: `python3 code/credit_cascade_test_v3.py`
The DYNAMIC, binding analysis. Fisher debt-deflation cascade across 5 scenarios
and three toolkit configurations (none / 14-tool / 15-tool), with a corrected
current-system comparison baseline.
v3 corrects three methodology errors present in v1 and v2:
  1. Deflation was computed from pre-toolkit M2 then the toolkit added after,
     making intervention appear to worsen deflation. v3 drives deflation from
     NET post-toolkit M2.
  2. Injections were single-entry; v3 tracks injected outside money with a
     matching asset entry (net M2 = transaction pool + surviving term deposits
     + outside money in circulation).
  3. Undocumented per-tool multipliers replaced with evidence-grounded first-year
     transmission: 0.35 for direct per-citizen transfers (recession stimulus MPC),
     0.25 for asset-market tools (Depression velocity collapse). Tool 15's
     18-month sunset is modeled (1.5× annual ceiling per activation).
Key findings (corrected):
  - 2008-equivalent (3%/yr, 3yr): M2 contraction 12.4% (14-tool) → 8.1% (15-tool).
  - Depression-magnitude (6%/yr, 3yr): 21.9% → 18.2%; vs historical ~30%.
  - Tool 15 contributes ~3–4pp in acute scenarios, sunset-bounded in prolonged.
  - Deflation falls with intervention in every scenario.
  - Transaction pool ($8,946B) protected throughout; corrected current-system
    baseline contracts 29–94% (no lender-of-last-resort backstop), confirming
    the "better failure mode" claim.
References: Fisher (1933) Econometrica Vol.1 No.4; Benes & Kumhof (2012) IMF
WP/12/202; recession-MPC literature (Parker et al. 2013; Baker et al. 2020;
NBER w27693) and Depression-velocity literature (NBER w22100). Results informed
Tool 15 (M2 Contraction Floor) in Paper 1 Section 10.1 and Paper 3 Sections
4.2.1 / 5.

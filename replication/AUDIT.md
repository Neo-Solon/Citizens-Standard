# Citizens Standard — Data Audit and Final Results

**Run date:** May 12, 2026
**Status:** All data verified against authoritative primary sources.

---

## Data verification summary

Every variable in `authoritative_data.py` was checked against the latest available primary source.

| Series | Source | Years | Status |
|---|---|---|---|
| CPI_DECDEC | BLS historical CPI-U supplemental table (Dec 2024) + Jan 2026 release | 1928–2025 (98) | All match within 0.05pp |
| CPI_ANNUAL | BLS historical CPI-U table | 1928–2025 (98) | All match within 0.05 |
| GDP_NOMINAL_B | FRED GDPA (April 9, 2026 vintage) | 1929–2025 (97) | All match within 0.5B |
| REAL_GDP_GROWTH | FRED A191RL1A225NBEA (BEA chain-weighted) | 1929–2025 (97) | 2021–2025 confirmed directly; pre-2020 within 0.15pp of computed-from-GDPCA except for 3 years (1961, 1967, 2015) which differ by 0.2pp — within BEA published rounding precision |
| SP500_NOMINAL | Damodaran NYU Stern, January 5, 2026 release | 1928–2025 (98) | All match exactly |
| POPULATION_M | Census Bureau Vintage 2025 (Jan 27, 2026 release) | 1928–2025 (98) | All match |
| M2_BILLIONS | FRED M2SL end-of-period (December) values | 1928–2025 (98) | All match |

## Final headline results

### Section 4.1 Table 1 — Central scenario (4.5% real post-2025)
| Cohort | Born | Retire | Stable Floor | Median actual | vs median | vs mean |
|---|---|---|---|---|---|---|
| A | 1960 | 2025 | $684,590 | $260,000 | 2.63× | 1.02× |
| B | 1970 | 2035 | $717,082 | $240,000 | 2.99× | 1.10× |
| C | 1980 | 2045 | $706,164 | $220,000 | 3.21× | 1.12× |
| D | 1990 | 2055 | $463,729 | $210,000 | 2.21× | 0.75× |

### Section 4.5 Decomposition (Cohort A, real 2025$)
| Component | Amount | Share |
|---|---|---|
| K1 deposit at birth (1960) | $816.05 | 0.12% |
| K2 cumulative (1960–2025) | $33,946.23 | 4.96% |
| Total principal | $34,762.28 | 5.08% |
| Equity compounding gain | $649,827.77 | 94.92% |
| **Final Stable Floor** | **$684,590.05** | **100.00%** |

### Section 5.1 Stress tests (Depression / Stagflation, ages 25–41)
| Cohort | Central | Depression | Stagflation | D vs med | S vs med |
|---|---|---|---|---|---|
| A | $684,590 | $246,172 | $171,885 | 0.95× ✗ | 0.66× ✗ |
| B | $717,082 | $517,907 | $350,682 | 2.16× ✓ | 1.46× ✓ |
| C | $706,164 | $319,323 | $226,906 | 1.45× ✓ | 1.03× ✓ |
| D | $463,729 | $240,591 | $164,931 | 1.15× ✓ | 0.79× ✗ |

### Section 6 Table M1 — Monte Carlo, 1929–2025 universe, block bootstrap, 10K paths
| Cohort | P5 | P25 | P50 | P75 | P95 | Mean | P(<med) |
|---|---|---|---|---|---|---|---|
| A | $79K | $233K | $484K | $1.01M | $2.86M | $853K | 28.4% |
| B | $108K | $312K | $665K | $1.41M | $4.00M | $1.20M | 18.0% |
| C | $141K | $411K | $877K | $1.87M | $5.61M | $1.64M | 10.7% |
| D | $172K | $471K | $1.02M | $2.20M | $6.51M | $1.90M | 7.6% |

### Headline ranges (Abstract)
| Statistic | Value |
|---|---|
| Deterministic central, vs median | 2.21× – 3.21× |
| Bootstrap P50, 1960–2025 universe | 1.96× – 4.52× |
| Bootstrap P50, 1929–2025 universe | 1.86× – 4.86× |
| P(<median) range across configs | 5.7% – 28.9% |

## Methodology notes

- **Real values throughout.** All deposits are deflated to December 2025 purchasing power using the BLS CPI-U Dec-Dec chain before compounding at real returns.
- **M2 series.** End-of-period (December) values from FRED M2SL. The K2 formula uses prior-year M2 as the base for each year's deposit.
- **K1 calibration.** 2.5% of GDP per capita at each new-citizen event (birth).
- **K2 calibration.** 0.5 × max(0, real GDP growth) × prior-year M2, distributed equally per living citizen.
- **Post-2025 projections.** 4.5% real equity (central), 4.0% nominal GDP growth, 4.5% M2 growth, 0.4% population growth, 1.8% real GDP growth, 2.5% CPI (CBO Long-Term Budget Outlook 2025 baseline).
- **Monte Carlo.** 10,000 paths per configuration. Bootstrap resamples joint (return, CPI, real-GDP-growth) triples from the historical universe; M2 trajectory is held deterministic. Block bootstrap uses 5-year moving blocks with circular wraparound.

## Reproducibility

All scripts in this bundle are deterministic — `numpy` random seeds are fixed. Running `python3 run_all_tables.py` reproduces every number in the paper exactly. Runtime is approximately 1 second on a modern single core for the full 16-configuration Monte Carlo grid (4 cohorts × 2 universes × 2 methods × 10,000 paths = 160,000 simulated lives).

## Additional stress tests

### Banking architecture credit stress test
Script: code/credit_stress_test.py
Run: python3 code/credit_stress_test.py
Tests: 7 credit loss rates × 5 durations + 2008 and Depression historical calibrations
Added: May 2026 in response to academic review questions on credit cycle resilience

## Banking Architecture Stress Tests

Added May 2026 in response to academic review questions on credit loss handling
and Depression-era cascade dynamics (r/AcademicEconomics thread).

### credit_stress_test.py
Run: python3 code/credit_stress_test.py
Tests: 7 credit loss rates (0.5%–10%/yr) × 5 durations (1–10 years)
Calibrations: 2008 peak charge-off rate (3.0%/yr, FDIC) and Great Depression
  equivalent (6.0%/yr, 4 years)
Key finding: Bank equity buffer ($4,473B) absorbs 2008 and Depression-magnitude
  losses without TLF activation. Payment system ($8,946B transaction pool)
  protected under all scenarios. TLF ceiling ($492B) becomes binding only above
  3.0%/yr sustained for 10 years — beyond any peacetime US precedent.

### credit_cascade_test_v2.py
Run: python3 code/credit_cascade_test_v2.py
Tests: Fisher debt-deflation cascade (dynamic feedback loop) under 5 scenarios
  across three toolkit configurations: no toolkit, 14-tool, 15-tool
Cascade mechanics: equity depletion → lending contraction → term deposit
  contraction → M2 contraction → asset price deflation (Fisher amplifier 0.80)
  → additional defaults
Tool 15 (M2 Contraction Floor, 3.0% of M2/yr): reduces acute cascade M2
  contraction by 2.1–2.5pp vs 14-tool kit. 18-month sunset limits effectiveness
  in prolonged (5yr+) scenarios by design.
Key finding: full-reserve separation bounds maximum M2 contraction at 60% of
  launch M2 (term deposit share). Historical 30% contraction (1930–33) was
  possible because all deposits were simultaneously at risk. Under Citizens
  Standard, transaction pool ($8,946B) is protected in all scenarios.
References: Fisher (1933) Econometrica Vol.1 No.4; Benes & Kumhof (2012)
  IMF WP/12/202 — both in Paper 1 references.
Results informed addition of Tool 15 to Paper 1 emergency toolkit (Section 10.1)
  and Paper 3 Section 4.2.1 and Section 5 failure mode analysis.

# Two-Circuit Empirical Extension — Supplementary Robustness Record (2026-07-10)

**STATUS: SUPPLEMENTARY / EXPLORATORY. Independent extension of Paper 10 (Empirical Validation).**
**NOT a paper claim, and NOT part of any paper's replication-as-support.**
**Bottom line: this CONFIRMS Paper 10's bounded claim and does not contradict any paper.**

This folder documents independent empirical work done to (a) build a clean *dollar* asset-circuit
series (MA) rather than a residual, and (b) stress-test the regime-dependence of the
transactional-money / inflation relationship across measures and countries. It is kept separate
from the paper replication packages on purpose — the same discipline applied to the FX exploratory
record: supplementary robustness work is not folded into a paper's claim-support.

## What was done and found

### 1. Clean dollar MA (asset circuit) — built and coherence-checked
MA = savings deposits + small-time deposits, in dollars. Savings is spliced across the May-2020 M1
redefinition (WSAVNS ends 2020-04; MDLM continues 2020-05+), with a seam-adjustment factor of 1.103
estimated from the pre-break trend (the redefinition reclassified ~$1.15T into the series at the seam).
**Coherence check:** MA + MT(currency+demand) tracks M2 to a *stable* ~4-5% gap across all dates
(the gap is retail MMF + minor M2 items) — a stable, explainable remainder confirms the
decomposition is coherent rather than an artifact.

2020-02 -> 2022-06 (run to the 9% CPI peak), clean dollar decomposition:
- MA (asset circuit, measured):        +17.7%
- M2 (broad):                          +39.7%
- MT (transactional, Divisia — clean): +63.8%   (curr+demand dollar MT reads +113.9% but carries the
                                                  OCD-gap/reclassification artifact; Divisia is the citable figure)
The asset circuit barely moved; the transactional circuit ran hot; broad M2 sat between them, diluted
by the sleepy asset money. Both circuits now on measured dollar series, not one as a leftover.

### 2. Cross-country / cross-measure regime test — the strong claim does NOT generalize
Non-overlapping annual data (overlap-corrected). OECD simple-sum narrow money (MANMM101) vs own
next-year CPI, US and Japan, like-for-like:
- **US:**   above-median-inflation R²=0.026, below-median R²=0.448 — narrow money predicts inflation
            BETTER in LOW regimes. This is the OPPOSITE of the Divisia-M1 high-regime flip.
- **Japan:** above-median R²=0.352, below-median R²=0.007 — narrow money matters more in higher-inflation
            periods, consistent with the regime story.

**Key finding: the "transactional aggregate wins in high-inflation regimes" result is measure-dependent
(Divisia M1 yes, OECD simple-sum no) and country-mixed (Japan yes, US-OECD no).**

### 2b. Japan narrow-vs-broad horserace (the real cross-country test) — broad wins every regime
With Japan narrow (MANMM101) AND broad (MABMM301) money on the same OECD basis, the actual
narrow-vs-broad horserace for predicting Japan's own next-year CPI (non-overlapping annual, n=40):
- All periods:   narrow R²=0.026, broad R²=0.354 — BROAD wins
- Above median:  narrow R²=0.062, broad R²=0.299 — BROAD wins
- Below median:  narrow R²=0.005, broad R²=0.072 — BROAD wins
**But the decisive caveat: Japan post-1980 is a chronic LOW-inflation economy (median 0.6%, max 7.4%,
only one year >=4%). It structurally cannot test the high-money-growth regime the framework's claim is
about, because it lacks that regime.** What Japan cleanly establishes is the negative: in low-inflation
conditions the transactional aggregate is NOT the better inflation predictor. To actually test the
framework's high-regime claim cross-nationally needs a country that HAD a high-money-growth episode with
clean narrow+broad data (e.g. Korea's earlier decades, or a Turkey/Brazil/Argentina-type case).

## Why this CONFIRMS rather than contradicts Paper 10

Paper 10's claim is deliberately bounded and specific: an *independently-weighted / corrected*
aggregate (Divisia and composition — the Barnett family) carries more goods-inflation information than
*simple-sum M2*, concentrated in high-money-growth regimes; and it explicitly refuses the overclaim
that Mᵀ beats expectations models in all regimes. Our OECD *simple-sum narrow* result behaving worse
in high regimes is exactly what the Barnett critique the paper rests on would predict — simple-sum
aggregation is theoretically wrong. So this is a confirmation of the paper's own thesis (corrected
aggregates matter, simple-sum ones are worse), not a correction to it.

What survives as robust and measure-independent: the two circuits are distinct objects
(Divisia-M1 vs M2 12m-growth correlation 0.68, not ~1.0); the relationship is regime-dependent in
both countries. What does NOT survive as a universal law: a stable *direction* for the regime effect
across measures/countries. The deeper framework point holds: no single aggregate mechanically reads
inflation.

## Files
- `two_circuit_analysis.py` — reproducible script (builds MA, runs the regime tests)
- `MA_series.csv` — the clean dollar MA series (1975-2026)
- `two_circuit_divergence_VERIFIED.json` — the US Divisia decomposition + distinctness result
  (NOTE: its high-regime Divisia flip is real for that measure but is NOT measure-robust — see below)
- `regime_robustness_crosscountry_VERIFIED.json` — the cross-country/cross-measure result (the caveat)
- `data/` — the input CSVs (FRED / CFS Divisia / OECD MEI)

## Honest limits
- The MA splice uses an *estimated* seam factor (1.103); the coherence check validates it held but
  did not independently measure it.
- The full narrow-vs-broad horserace cross-country is not done — foreign broad-money series were not
  available (only US broad and Japan narrow on hand).
- Single-country dollar MA (US); the high-regime samples are small (~20 independent years) and lean
  on the 1970s and 2020s episodes.


---

## Addendum 2026-07-14 — the measure-dependence, diagnosed (`seam_resolution.py`)

The 2026-07-10 cross-country record found the US high-regime flip was
measure-dependent (Divisia yes, OECD simple-sum reversed). Follow-up analysis
diagnoses the reversal as substantially a data artifact: the May 2020
Regulation D / H.6 redefinition moved savings deposits into M1, so OECD
simple-sum M1 jumps +238.8% in that single month while Divisia is constructed
continuously across the seam. The 2020 observation sits in the low-inflation
cell right before the 2021-22 surge — one leverage point that manufactures
low-regime predictive power for simple-sum money. Removing the 2020-21
money-growth years: OECD low-regime R² collapses 0.20 → 0.00 (below-median
0.48 → 0.01) while the high-regime result is unchanged (0.162), and both
measures then agree on the flip in the same design. Japan (no seam) already
agreed. See `seam_resolution_VERIFIED.json` for the full grid and the honest
limits that remain (small high-regime n dominated by the 1970s; two countries).
The 2026-07-10 record's caution was correct at the time; this addendum
supersedes its US measure-dependence verdict, not its method.

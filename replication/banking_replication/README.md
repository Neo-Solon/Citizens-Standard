# Replication package — The Citizens Standard: Full-Reserve Banking and the Two-Circuit System (Neo-Solon, 2026f)

This package reproduces every quantitative claim and figure in the banking paper.
All code is pure Python with `numpy` and `matplotlib` only (no SciPy). From `code/`:

```
python3 paper6_model.py          # derives the five results + regenerates figures
python3 test_propositions.py     # automated proposition tests (N1-N5)
```


## Quick start

One command runs the full analytical battery and prints a consolidated evidence
report (propositions, balance sheet, sensitivity + thresholds + 10,000-draw Monte
Carlo, discovered boundaries, and parameter importance):

```
python3 code/run_analysis.py            # full consolidated report
python3 code/run_analysis.py dashboard  # one-page verification dashboard
python3 code/run_analysis.py summary    # one-screen headline numbers
python3 code/run_analysis.py robustness # just the 10k Monte Carlo pass rates
python3 code/run_analysis.py thresholds # just the discovered boundaries
python3 code/run_analysis.py importance # just parameter importance
python3 code/run_analysis.py what-if collateral=2.0
python3 code/run_analysis.py boundary chi_c
```

The driver dispatches to the modules below; it adds no new analysis, only a single
entry point over them.

## Modules

| Module | Reproduces |
|---|---|
| `paper6_model.py` | The five quantitative results of the paper on verified anchors, including the named Loanable-Funds Frontier (Result 3) and its elasticity robustness sweep (low/baseline/high) (Paper 5 launch aggregates; Fed Z.1 Q4-2025 / H.6 / H.8 current values): complete monetary control (M_T = M_o), the entirely-sovereign transaction aggregate, credit supply under the 4:1 leverage cap, run-proofness, and the near-money boundary. Regenerates the figures into `figures/`. |
| `balance_sheet.py` | Explicit two-account balance sheet (reserved transaction accounts + at-risk term deposits + equity floor) for both the incumbent fractional-reserve system and the Citizens Standard full-reserve system. The propositions are *derived* from this mechanism: inside money, runnable money, credit capacity, and the contraction bound are computed from accounting identities, not asserted. |
| `test_propositions.py` | Automated tests of the paper's banking propositions **N1-N5**, in the style of the Paper 1 and Paper 8 `verify_prop` suites. Each proposition is checked against quantities *derived* from `balance_sheet.py`, so a test fails if the underlying mechanism is wrong (verified: violating the reserve identity trips N1, a runnable reserved layer trips N4, leverage above the cap trips N3), not merely if a constant is mistyped. Prints one PASS line per proposition; exits non-zero on any failure. |
| `sensitivity.py` | Three evidence-generating exercises beyond the baseline: (1) a **sensitivity table** sweeping phi_liq and leverage; (2) **algorithmic threshold discovery** (max credit intensity preserving N2's separation; max observable near-money preserving N5's throttle bound, found by bisection, not hardcoded); (3) **randomized invariant testing** over 10,000 economically admissible calibrations, confirming the structural propositions N1 and N4 hold for every draw (100%) while reporting honest pass rates for the calibration-dependent N2/N3/N5. |
| `parameter_importance.py` | **Parameter importance analysis.** For each proposition, decomposes the variance of its margin (signed distance from threshold) across the assumptions, identifying which ones most strongly drive the result. Uses a model-free first-order variance share plus Spearman rank correlation; validated on a known-answer linear case. Finds separation (N2) is driven chiefly by the pledgeable fraction phi_liq, and credit capacity (N3) by the money-stock scale and term share rather than the leverage cap. |
| `explore.py` | **Exploration interface** (turns the package from verification into a research tool). Discovers the model's boundary quantities algorithmically (maximum term-deposit share preserving an adequate transaction aggregate; maximum credit intensity preserving separation; maximum observable near-money preserving controllability) and answers parametric "what-if" queries from the command line (`--what-if collateral=2.0`, `--boundary chi_c`). |
| `make_figures.py` | Regenerates the figures into `figures/`. |

## Propositions tested (N1-N5)

| Prop | Claim checked |
|---|---|
| **N1** (complete monetary control) | Under full reserve banks create no transactional money, so the price-relevant aggregate is M_T = M_o; the throttle sets it directly (no inside-money offset, no saturation), and the Paper 5 determinacy root theta = 1+(1+phi)/alpha > 1 applies to M_o. |
| **N2** (separation survives bank credit) | The asset-to-consumer coupling lambda_leak + chi_c·kappa_bank stays below the separation/determinacy threshold zeta* ≈ 0.13; equivalently kappa_bank < (zeta*-lambda)/chi_c ≈ 0.33. |
| **N3** (credit supply under full reserve) | Bank credit L ≤ D + E with D ≤ 3E (leverage ≤ 4:1), so a term-deposit base D ≈ 60% of launch M2 ≈ $13.4T supports credit up to D·4/3 ≈ $17.9T; full reserve binds only bank-intermediated credit. |
| **N4** (run-proof payments) | Reserved transaction accounts cannot be run and the locked floor is non-demandable equity, so the maximum systemic money contraction is bounded by the term-deposit share (~60%) rather than ~the entire deposit stock (1930-33). |
| **N5** (near-money boundary) | A full-reserve rule raises the cost/visibility of near-money without abolishing it; because the throttle targets the total transactional aggregate, observable near-money enters the price-relevant quantity and is offset when observable — a bounded, conditional claim, not a guarantee. |

## Structural vs calibration-dependent

The suite labels each proposition by what it depends on, so a reader can see what
survives a change in parameters:

- **Structural (N1, N4):** identities that hold for any admissible parameters.
  Inside-money creation is zero and the reserved layer is unrunnable by the
  full-reserve rule itself, independent of the term share or M2.
- **Calibration-dependent (N2, N3, N5):** the PASS or the reported magnitude
  depends on the calibrated values (credit intensity, term share, near-money
  fraction). N2 in particular flips to FAIL past the derived ceiling, so a
  sensitivity sweep over the credit intensity kappa is reported alongside it.

## Expected output

```
STRUCTURAL (unchanged if parameters change):
  PASS  N1  (complete monetary control)
  PASS  N4  (run-proof payments)
CALIBRATION-DEPENDENT (contingent on the calibrated values):
  PASS  N2  (separation survives bank credit)
  PASS  N3  (credit supply under full reserve)
  PASS  N5  (near-money boundary is bounded and conditional)

N2 sensitivity -- separation coupling vs credit intensity kappa:
    kappa = 0.05  ->  coupling = 0.045  PASS
    kappa = 0.10  ->  coupling = 0.060  PASS
    kappa = 0.15  ->  coupling = 0.075  PASS
    kappa = 0.30  ->  coupling = 0.120  PASS
    kappa = 0.34  ->  coupling = 0.132  FAIL
ALL PROPOSITIONS PASS  (5/5)
```

## Grounding

The proposition tests are derived, not asserted. `balance_sheet.py` builds the money
stock and lending base from primitives; the tests read the claims off that mechanism.
This was checked by fault injection: breaking the full-reserve identity (banks holding
less than 100% reserves against transaction accounts) makes inside money positive and
fails N1; making the reserved layer runnable fails N4; leverage above 4:1 fails N3.

## Parameter importance

`parameter_importance.py` identifies which assumptions each proposition depends
on most, over 20,000 admissible draws (variance decomposition + rank correlation):

- **N2 (separation):** driven chiefly by the pledgeable fraction phi_liq (about 46%
  of the margin variance), then chi_c and zeta*. phi_liq is the assumption to
  scrutinize for the separation result.
- **N3 (credit capacity):** driven by the money-stock scale M2 (about 60%) and the
  term-deposit share (about 34%); the 4:1 leverage cap contributes only about 2%.
- **N4 (run-proof share):** fully determined by the term-deposit share (100%), a
  known-answer identity that also validates the method.

## Exploration (beyond verification)

`explore.py` lets a researcher explore the model rather than only re-run the
baseline. Discovered boundaries (publishable quantities, computed by bisection):

- Maximum transactional (term-deposit) share keeping M_o >= 25% of M2: **0.750**
- Maximum credit intensity preserving circuit separation (N2): **0.333** (baseline 0.150)
- Maximum observable near-money before it exceeds 25% of M_T (N5): **16.7%** of term deposits
- Circuit separation survives a collateral shock up to **2.22x** the baseline pledgeable fraction

What-if queries answer parametric questions directly, e.g.:

```
python3 code/explore.py --what-if collateral=2.0   # coupling 0.075 -> 0.120, separation holds
python3 code/explore.py --what-if collateral=3.0   # coupling 0.075 -> 0.165, separation FAILS
python3 code/explore.py --boundary chi_c           # separation flips at chi_c = 0.667
```

## Evidence beyond one calibration

`sensitivity.py` demonstrates that the structural propositions are properties of
the design rather than of a chosen parameter set:

- **Sensitivity table:** derived quantities (binding constraint, coupling, credit
  capacity) across a sweep of phi_liq and the leverage cap.
- **Threshold discovery:** boundaries are computed, not stated. The maximum credit
  intensity preserving separation (N2) and the maximum observable near-money the
  throttle can still bound (N5) are found by bisection.
- **Randomized invariant testing:** 10,000 random admissible calibrations. N1 and
  N4 (structural) pass 100%; a deliberately false invariant is caught at well under
  100%, so the 100% figures are meaningful. N2 passes ~81% -- it holds across most
  of the space and fails only in the high-credit-intensity corner it is defined to
  bound, which is the honest, correct behavior for a calibration-dependent claim.

## Calibration

Launch anchors (Paper 5): GDP $30,762B, M2 $22,366B, g_r = 2.0%/yr, T = 65.
Current US (Fed Z.1 Q4-2025 / H.6 / H.8): household net worth ~$184.1T, private
non-financial credit ~$42.4T, commercial-bank deposits $18.55T (Dec 2025, FRED DPSACBM027SBOG). Banking parameters
(Papers 1, 3, 5): pledgeable/liquid fraction phi_liq ~0.15, credit intensity
kappa_bank = m·phi_liq ~0.075, term-deposit share ~60% of launch M2, leverage cap
4:1 (countercyclical 3:1/5:1), separation threshold zeta* ≈ 0.13 (coupling route
0.32). All figures are illustrative calibrations on verified anchors, not forecasts.

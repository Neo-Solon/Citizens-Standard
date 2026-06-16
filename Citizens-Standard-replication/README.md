# The Citizens Standard — Replication Archives

This directory holds the reproducibility archives for the Citizens Standard research
program. Every paper with a computational component has its own self-contained subfolder
that regenerates the figures and quantitative claims printed in that paper. Each subfolder
runs independently.

```
Citizens-Standard-replication/
├── empirical_replication/         ← Paper 2  Historical Counterfactual                        (SSRN 6735078)
├── transition_replication/        ← Paper 3  Transition Architecture                          (SSRN 6810741)
├── macro_replication/             ← Paper 5  Macroeconomic Model                              (SSRN 6939418)
├── banking_replication/           ← Paper 6  Full-Reserve Banking and the Two-Circuit System  (SSRN 6939498)
├── interoperability_replication/  ← Paper 7  External Interoperability                        (SSRN 6939600)
└── structural_buyer_replication/  ← Paper 8  Structural Buyer                                 (SSRN 6945320)
```

## Which subfolder reproduces what

- **empirical_replication/ — Paper 2.** The Monte Carlo and historical-counterfactual engine
  (1960–2055): cohort outcomes, percentile bands, stress cohorts, and the forward transition
  projection, plus the banking stress tests — a static no-feedback bound and a dynamic Fisher
  cascade — that informed Tool 15. Ships `data/` (historical input CSVs), the generated M1–M5
  figures, and an `AUDIT.md` figure-by-figure reproduction record.

- **transition_replication/ — Paper 3.** The deterministic Technical Appendix models:
  debt-retirement trajectory and KT consumer-price neutrality (A.2), banking/KT synergy (A.3),
  equity rotation and its sensitivity (A.4 / A.4.4), and constitutional-lock credibility (A.5).
  Includes an `AUDIT.md`.

- **macro_replication/ — Paper 5.** A computational supplement to the theory paper. The
  propositions are proved in closed form and stand on their own; the scripts let a reader watch
  them behave — Proposition 3 (convergence classification), 4 (labor-supply bounds), 5 (two-speed
  delayed-feedback damping), 6 (impulse responses of the linearized two-circuit system), 7
  (forward-looking determinacy without a Taylor principle), and 8 (welfare-optimal dividend share)
  — and recompute every illustrative magnitude from the printed inputs. There is no dataset; the
  worked numbers are illustrations, not calibrations.

- **banking_replication/ — Paper 6.** Reproduces the five banking propositions and four figures:
  the transactional-money price level with the KI throttle offsetting inside money one-for-one
  (B1), the lending cap and the ≈0.13 inside-money share under the binding collateral bound (B2),
  the throttle's price-path preservation (B3), the implied minimum capital requirement (B4), and
  the run-proof locked-floor result (B5). Pure Python (`numpy`/`matplotlib`, no SciPy).

- **interoperability_replication/ — Paper 7.** Reproduces every quantitative result in Paper 7,
  split into two classes held to different standards. The **domestic** results are computed on the
  CS issuance engine at real launch calibration (M2 = $22,366B, 2% real growth, K1 = 2.5% of GDP
  per capita) and reproduce the published figures to the dollar. The **external EQUA layer** is a
  proposed mechanism with no real-world instance, so its results are reported as a
  calibrated-mechanism finding — robust across the observed ranges of cross-country productivity
  growth and wage stickiness — not a forecast. Ships `RESULTS_manifest.md` (claim → script → output
  map), `outputs/` (captured stdout from every script), a pinned `requirements.txt`, and
  `LICENSE.txt`.

- **structural_buyer_replication/ — Paper 8.** A code-only computational supplement (no dataset, no
  figures) that verifies the numerical claims behind the analytically-tractable propositions: the
  bounded valuation premium A\*/φ and its stability band (Prop 1), the steady-state identity I\* = A\*
  with geometric repricing decay and total repricing A\*/φ (Prop 2), the κ_W-bounded consumption leak
  (Prop 3), and the mirror-voting neutrality identity (Prop 7), plus the ownership-plateau result
  ψ\* = c·dur (Appendix A.6). Propositions 4–6 are mechanism/threshold results argued in the main
  text. Pure Python (`numpy`).

## Papers without a standalone package

Papers 1 (Architecture, SSRN 6702518) and 4 (Statutory Implementation, SSRN 6873798) have no
standalone computational model; they cite the figures reproduced in the archives above. Paper 1's
interactive companion is the `Citizens_Standard_Engine.html` at the repository root.

## How to run

Each subfolder is independent. Python 3.10+ with `numpy` and `matplotlib` covers all five packages;
`interoperability_replication/` additionally pins its environment in `requirements.txt`.

```bash
# Paper 2 — empirical
cd empirical_replication
python3 code/run_all_tables_v3.py        # Part I tables
python3 code/transition_cohorts_v3.py    # Part II forward cohorts
python3 code/credit_stress_test_v2.py    # static banking stress bound
python3 code/credit_cascade_test_v3.py   # dynamic Fisher cascade

# Paper 3 — transition
cd transition_replication/code
python3 run_all_appendix.py              # all Technical Appendix models

# Paper 5 — macro
cd macro_replication/code
python3 run_all.py                       # all proposition checks + figures

# Paper 6 — banking
cd banking_replication/code
python3 run_all.py > ../all_results.txt  # five verifiers + four figures

# Paper 7 — interoperability
cd interoperability_replication
pip install -r requirements.txt
python run_all.py                        # deterministic; full claim → output map in RESULTS_manifest.md

# Paper 8 — structural buyer
cd structural_buyer_replication/code
python3 run_all.py                       # five proposition verifiers (no dataset, no figures)
```

Each model is parameterized from the figures stated in its header. Where a subfolder ships an
`AUDIT.md` (empirical, transition), that file carries the figure-by-figure reproduction record.
Where results are calibrated mechanisms rather than empirical forecasts — the EQUA layer in
Paper 7, the illustrative magnitudes in Paper 5 — the package labels them as such, so a reader
never mistakes a mechanism demonstration for a calibrated prediction.

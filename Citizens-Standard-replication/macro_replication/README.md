# Computational Supplement for: The Citizens Standard — A Macroeconomic Model of a Two-Circuit Monetary System

**Author:** Neo-Solon
**Contact:** Neo-Solon@hotmail.com
**License:** CC BY 4.0

This supplement accompanies:

> Neo-Solon (2026e). *The Citizens Standard: A Macroeconomic Model of a Two-Circuit Monetary System.* Working Paper.

Companion papers:

> Neo-Solon (2026a). *The Citizens Standard — One Model, Many Constitutional Systems.* SSRN: 6702518
> Neo-Solon (2026b). *The Citizens Standard as Counterfactual Benchmark.* SSRN: 6735078
> Neo-Solon (2026c). *The Citizens Standard: Transition Architecture and Migration Mechanics.* SSRN: 6810741
> Neo-Solon (2026d). *The Citizens Standard: A Statutory Implementation Pathway.* SSRN: 6873798

---

## What this supplement is — and is not

This is a **theory paper**. Its three propositions are established by closed-form
proof in the Technical Appendix and **stand on their own**; they do not require
code to be correct. This supplement is provided as a convenience so a reader can
(a) watch Proposition 3's convergence classification behave as the proof states,
and (b) recompute every illustrative magnitude in Sections 3.2a and 6.5 from the
inputs printed in those sections, without trusting the arithmetic on faith.

There is **no dataset** here, and none is needed: the model is analytical, and the
worked magnitudes are explicitly *illustrations, not calibrations* (the paper says
so). The quantities a full empirical calibration would pin down — the money share
μ*, the locked-float path s_t, net absorption A*, total capitalization, and the
supply elasticity φ — are the open problems flagged in Section 8, not results
claimed here.

| Module | Reproduces |
|---|---|
| `verify_proposition_3.py` | Proposition 3 convergence classification: monotone (ψλ ≤ 1), damped oscillation (1 < ψλ < 2), marginal (ψλ = 2), divergence (ψλ > 2); the self-correction property (any ψ stabilized by λ < 1/ψ); and K3_T inheriting stability with margin (Section 4.6). |
| `recompute_illustrations.py` | The §3.2a consumer-price leak bounds and the §6.5 structural-buyer premium bounds, reproduced exactly from the stated inputs. |
| `make_figure.py` | `figure_P3_convergence_regimes.png` — gap-closure trajectories across the three regimes. |
| `run_all.py` | Runs all three and prints the captured output. |

---

## How to run

```bash
cd code
python run_all.py
```

Requirements: Python 3.9+, `numpy`, `matplotlib` (only `make_figure.py` needs matplotlib).

```bash
pip install numpy matplotlib
```

---

## Expected output (abridged)

`verify_proposition_3.py` prints a table in which every **observed** regime matches
the **analytic** regime boundary, ending with:

```
All observed regimes match the analytic boundaries: True
```

`recompute_illustrations.py` reproduces, among others:

```
Mode B central (kappa_W=0.03, mu*=0.15, s_t=0):
   leak = $91B  =  0.41% of M2   [paper: ~$91B, 0.41%]
...
Valuation premium at mid drawdown:
   phi=0.5 -> 0.66% ; phi=1.0 -> 0.33% ; phi=2.0 -> 0.17%   [paper: 0.66 / 0.33 / 0.17 %]
```

Every printed value carries its paper reference in brackets for direct comparison.

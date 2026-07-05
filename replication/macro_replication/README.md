# Computational Supplement for: The Citizens Standard — A Macroeconomic Model of a Two-Circuit Monetary System

**Author:** Neo-Solon
**Contact:** Neo-Solon@hotmail.com
**License:** CC BY 4.0

This supplement accompanies:

> Neo-Solon (2026e). *The Citizens Standard: A Macroeconomic Model of a Two-Circuit Monetary System.* Working Paper.

Companion papers:

> Neo-Solon (2026a). *The Citizens Standard — One Model, Many Systems — A Constitutional Monetary Architecture.* SSRN: 6702518
> Neo-Solon (2026b). *The Citizens Standard: A Historical Counterfactual — Empirical Analysis of an Alternative US Monetary Architecture, 1960–2055.* SSRN: 6735078
> Neo-Solon (2026c). *The Citizens Standard: Transition Architecture and Migration Mechanics.* SSRN: 6810741
> Neo-Solon (2026d). *The Citizens Standard: A Statutory Implementation Pathway.* SSRN: 6873798

---

## What this supplement is — and is not

This is a **theory paper**. Its propositions are established by closed-form
proof in the Technical Appendix and **stand on their own**; they do not require
code to be correct. This supplement is provided as a convenience so a reader can
(a) watch Proposition 3's convergence classification behave as the proof states,
(b) confirm the Proposition 4 labor-supply bounds (Section 5.5) numerically, and
(c) check the Proposition 5 two-speed result (delayed feedback loses damping like
|ln lambda_L|/d), (d) trace the Proposition 6 impulse responses of the linearized
two-circuit system (floor cushion, KI self-correction, asset containment),
(e) confirm the Proposition 7 forward-looking determinacy result (the money-quantity
anchor pins a unique RE price path without a Taylor principle),
(f) trace the Proposition 8 welfare-optimal dividend share (kappa_d=0 maximizes
wealth, but the welfare optimum is positive under positive net discounting), and
(g) recompute every illustrative magnitude in Sections 3.2a and 6.5 from the inputs
printed in those sections, without trusting the arithmetic on faith.

There is **no dataset** here, and none is needed: the model is analytical, and the
worked magnitudes are explicitly *illustrations, not calibrations* (the paper says
so). The quantities a full empirical calibration would pin down — the money share
μ*, the locked-float path s_t, net absorption A*, total capitalization, and the
supply elasticity φ — are the open problems flagged in Section 8, not results
claimed here.

| Module | Reproduces |
|---|---|
| `verify_proposition_3.py` | Proposition 3 convergence classification: monotone (ψλ ≤ 1), damped oscillation (1 < ψλ < 2), marginal (ψλ = 2), divergence (ψλ > 2); the self-correction property (any ψ stabilized by λ < 1/ψ); and KI_T inheriting stability with margin (Section 4.7). |
| `verify_proposition_3prime.py` | **Proposition 3' (Section 3.6):** the structural pass-through ψ = M2/M^T reproduced directly from the price mechanism; the stability regime by transactional money share; the maturing-circuit drift (ψλ rising as the asset circuit grows under M2-indexing); the M^T-indexing / adaptive-gain remedies that hold ψλ fixed at all maturities; and the minimum-variance gain (stationary-variance floor at ψλ = 1) with the robustness rationale for the baseline ψλ = 0.90. The result is scoped as local stability of the (backward-looking) path-targeting feedback; full forward-looking determinacy is noted as future work. |
| `verify_proposition_4.py` | **Proposition 4 (Section 5.5 / A.7):** the bounded labor-supply response to a locked floor — the reduced first-order condition ℓ^(1+1/ν)+b·ℓ^(1/ν)=1 and its elasticity −ν/(1+ν); the lock factor ρ_eff/r (a liquid floor of ~16× income cuts labor ~19%, the lock brings it to ~1–5% and to zero as κ_d→0); the scale-invariance of b (a one-time level effect, not a trend change); and the growth-indexed labor–growth loop as a contraction (fixed point ~0.984, loop gain ~0.016). |
| `make_labor_figure.py` | `figure_P4_labor_growth.png` — the three-panel labor-supply figure (response, locked-vs-liquid, self-correction) for Section 5.5. |
| `verify_proposition_5.py` | **Proposition 5 (Section 3.6 / A.8):** the two-speed result. With delayed feedback x_t=(1−ψλ)x_(t−1)−λ_L x_(t−d), the small-gain box |1−ψλ|+|λ_L|<1 is stable at every delay; the critical gain collapses toward 1−|1−ψλ| as d grows (1.00 at d≤2, 0.93 at d=4, 0.91 at d=8 → 0.90); and at fixed λ_L the slowest-mode damping vanishes like |ln λ_L|/d — so a decade-scale lever is stable but arbitrarily sluggish, which is why the liquidation schedule is committed as feedforward. |
| `make_delay_figure.py` | `figure_P5_delay_feedback.png` — the three-panel delay-feedback figure (region collapse, vanishing damping, feedforward-vs-feedback impulse responses) for Section 3.6 / A.8. |
| `verify_proposition_6.py` | **Proposition 6 (Section 7.6 / A.9):** the linearized two-circuit system s_t = A s_(t−1) + e_t. Stability (eigenvalues 0.12, 0.68, 0.90) and reduction to the Prop 3′ recursion when decoupled; the demand-shock output trough scaling with (1−ω_F) (the acyclical floor cushion, −15% at ω_F=0.15); cost-push return at rate ≈1−ψλ under KI versus a unit root with KI off; and asset-shock consumer-price containment bounded by λ_leak/(ψλ) ≈ 3%. |
| `make_irf_figure.py` | `figure_P6_irf.png` — the three-panel impulse-response figure (demand cushion, cost-push self-correction, asset containment) for Section 7.6 / A.9. |
| `verify_proposition_7.py (confirms P7); stress_proposition_7.py (stress-tests P7)` | **Proposition 7 (Section 3.7 / A.10):** forward-looking determinacy. The explosive root θ = 1 + (1+φ)/α > 1 for all α>0, φ≥0, so the money-quantity anchor is determinate even with a passive gap response (no Taylor principle); the interest-rate analog has root φ and needs φ>1; and the two-circuit (two-jump) system stays determinate until the asset↔consumer coupling reaches ≈0.13, inside which the calibrated leak (≈0.03) lies. |
| `make_forward_figure.py` | `figure_P7_forward_determinacy.png` — determinacy frontier (money vs interest-rate rule), unique-path-vs-sunspot-fan, and the two-circuit Blanchard–Kahn count vs coupling, for Section 3.7 / A.10. |
| `verify_proposition_8.py` | **Proposition 8 (Section 5.6 / A.11):** the welfare-optimal dividend share. Wealth is maximized at κ_d=0; welfare at an interior κ_d* governed by the retention premium R = βΩ(1+r); κ_d* falls with patience, return, and the terminal-value weight Ω; the wealth-maximizing corner κ_d*=0 is reached only near R≈1.2 (effectively negative net discount); and the Prop 4 labor distortion is second-order at the private optimum (the envelope identities verify to machine precision). |
| `make_welfare_figure.py` | `figure_P8_welfare_dividend.png` — κ_d* vs the retention premium, κ_d* vs the return for several patience levels, and welfare W(κ_d) showing wealth-max ≠ welfare-max, for Section 5.6 / A.11. |
| `verify_proposition_8.py` | **Proposition 8 (Section 5.6 / A.11):** welfare-optimal dividend share. Confirms terminal wealth is maximised at κ_d=0; the welfare optimum solves c2/c1 = R with R = βΩ(1+r), interior at κ_d*≈0.795 for the baseline (β=0.90, Ω=1, r=4.5%); κ_d* is decreasing in R and reaches the wealth-max corner κ_d*=0 only for R≳1.21 (βΩ≳1.16, non-positive net time preference); and the labour-supply response is second-order by the envelope theorem (residuals at machine precision), first-order only under an explicit labour wedge. |
| `make_welfare_figure.py` | `figure_P8_welfare_dividend.png` — welfare vs κ_d by patience, the optimal-share schedule κ_d*(R) with both corners, and the envelope decomposition, for Section 5.6 / A.11. |
| `verify_proposition_9.py` | **Proposition 9 (Section 3.8 / A.12):** robustness of circuit separation to bank credit. Confirms bank lending adds an asset→consumer coupling χ_c·m·φ_liq; under the conservative (financial-accelerator) reading separation holds iff the credit intensity m·φ_liq < (ζ*−λ)/χ_c ≈ 0.32; because locked floors are non-pledgeable (φ_liq≈0.15) the critical LTV exceeds 2 (no feasible leverage breaks separation), whereas fully pledgeable wealth breaks it at LTV≈0.32; and the rule-bound structural buyer damps the accelerator, raising the critical intensity to ≈1.7 (a second, independent safeguard). |
| `make_banking_figure.py` | `figure_P9_banking_separation.png` — the separation region in (credit intensity, spend-through), the critical-LTV/liquid-fraction relation, and the two-safeguard eigenvalue plot, for Section 3.8 / A.12. |
| `make_determinacy_figure.py` | `figure_P3prime_determinacy.png` — the three-panel determinacy figure (region, regimes, maturing-circuit drift) for Section 3.6. |
| `recompute_illustrations.py` | The §3.2a consumer-price leak bounds and the §6.5 structural-buyer premium bounds, reproduced exactly from the stated inputs. |
| `make_figure.py` | `figure_P3_convergence_regimes.png` — gap-closure trajectories across the three regimes. |
| `run_all.py` | Runs every module above and prints the captured output. |

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
   leak = $89B  =  0.40% of M2   [paper: ~$89B, 0.40%]
...
Valuation premium at mid drawdown:
   phi=0.5 -> 0.66% ; phi=1.0 -> 0.33% ; phi=2.0 -> 0.17%   [paper: 0.66 / 0.33 / 0.17 %]
```

`verify_proposition_4.py` reproduces, among others:

```
nu=0.50  dl/db|0  numeric=-0.3333  analytic=-0.3333  match=True
liquid (full return spendable)         b=0.720 -> l=0.8088 (-19.1% labor)
locked, kappa_d distributes ~1%        b=0.160 -> l=0.9494 (-5.1% labor)
fixed point g/g* = 0.9841 ; loop gain |dg'/dg| = 0.0156 (<1 => contraction)
All Proposition 4 claims reproduced: True
```

`verify_proposition_5.py` reproduces, among others:

```
d=  8 : lamL_crit = 0.9082
d=  8 : max|z|=0.9290  damping=0.0710   |ln lamL|/d=0.0866
All Proposition 5 claims reproduced: True
```

`verify_proposition_6.py` reproduces, among others:

```
eigenvalues = [0.1207, 0.6793, 0.9] ; max|eig| = 0.9000 ; stable = True
omega_F=0.15 : trough=-0.8500  (=0.85 x no-floor ; expect 0.85)
bound leak/(psi*lam) = 0.0333 ; observed peak x/peak v = 0.0300
All Proposition 6 claims reproduced: True
```

`verify_proposition_7.py` reproduces, among others:

```
alpha=4.0 | phi=0.0:theta=1.250(det)  phi=0.5:theta=1.375(det)
interest-rate: phi=0.5 root=0.50 INDETERMINATE ; phi=1.5 root=1.50 det
determinacy threshold coupling = 0.127 ; calibrated leak ~0.03 lies inside
All Proposition 7 claims reproduced: True
```

`verify_proposition_8.py` reproduces:

```
baseline beta=0.90, Omega=1, r=4.5%: R=0.9405
kappa*_FOC=0.7953  kappa*_grid=0.7953  c2/c1=0.9405
wealth-max corner threshold R = c2/c1|_{kappa=0} = 1.209
All Proposition 8 claims reproduced: True
```

`verify_proposition_9.py` reproduces:

```
locked baseline phi_liq=0.15 m=0.50 kappa_bank=0.075 zeta_tot=0.052 sep=True
NO-LOCK phi_liq=1.00 m=0.50 kappa_bank=0.500 zeta_tot=0.180 sep(conservative)=False
kappa_bank* = 0.323 ; locked m*=2.16 (>1) ; no-lock m*=0.32
damped-accelerator critical intensity = 1.694
All Proposition 9 claims reproduced: True
```

`verify_proposition_8.py` reproduces, among others:

```
baseline R=0.941 kappa*=0.795 ; W(k*) >= W(0): True
r up -> kappa* down ; beta down -> kappa* up ; Omega down -> kappa* up
corner kappa*=0 reached at R ~ 1.21 (needs negative net discount)
labor FOC |1/c1 - h^(1/nu)|=2e-16 ; kappa FOC |c2/c1 - R|=7e-15  (envelope)
All Proposition 8 claims reproduced: True
```

`verify_proposition_9.py` reproduces:

```
locked baseline phi_liq=0.15 m=0.50 kappa_bank=0.075 zeta_tot=0.052 sep=True
NO-LOCK phi_liq=1.00 m=0.50 kappa_bank=0.500 zeta_tot=0.180 sep(conservative)=False
kappa_bank* = 0.323 ; locked m*=2.16 (>1) ; no-lock m*=0.32
damped-accelerator critical intensity = 1.694
All Proposition 9 claims reproduced: True
```

Every printed value carries its paper reference in brackets for direct comparison.


## Calibrated dynamic model (`dynamic_model.py`)

Simulates the linearized system of Appendix A.9 (`s_t = A s_{t-1} + e_t`) as a
*calibrated, not estimated* exercise. Estimation is deliberately avoided: the
Citizens Standard has never operated, so fitting the system to fractional-reserve
data and assuming the parameters carry over would be the Lucas critique. The module
(1) reproduces the paper's stated baseline eigenvalues (0.12, 0.68, 0.90) as a
validation check; (2) reports numeric impulse responses to price, demand, and asset
shocks -- the asset shock reaches consumer prices only through the bounded leak
(peak price-gap 0.030, at the theoretical bound leak/psi*lam = 0.033), showing
circuit separation holds under dynamics; and (3) runs a randomized dynamic-robustness
test over 10,000 admissible calibrations, with stability and separation holding in
100% of draws (a deliberately unstable region is caught at under 100%, so the figure
is meaningful). Run: `python3 code/dynamic_model.py`.

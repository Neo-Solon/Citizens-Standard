# Replication package — The Citizens Standard: Full-Reserve Banking and the Two-Circuit System (Neo-Solon, 2026f)

This package reproduces every quantitative claim and figure in the banking paper. All
code is pure Python with `numpy` and `matplotlib` only (no SciPy). From `code/`:

```
python3 run_all.py > ../all_results.txt
```

This runs the five proposition verifiers and regenerates the four figures into `figures/`.

## Modules

| Module | Reproduces |
|---|---|
| `verify_B1.py` | **Proposition B1 (Section 3):** the price level is set by total transactional money M_T = M_o + d_T·D; the KI throttle offsets inside money one-for-one (M_o = M* − d_T·D); the forward-looking determinacy of Proposition 7 (2026e) carries over to M_T; and KI saturates iff d_T·D > M*. |
| `verify_B2.py` | **Proposition B2 (Section 4):** bank lending is capped by min(capital E/k, reserves R_b/ρ, collateral m·φ_liq·W). Because locked floors are non-pledgeable the collateral cap binds at the baseline, holding the inside-money transactional share σ ≈ 0.13; removing the lock (φ_liq = 1) enlarges the collateral base ≈ 1/φ_liq ≈ 7× and makes capital bind instead. |
| `verify_B3.py` | **Proposition B3 (Section 5):** the throttle keeps the price path iff inside deposits satisfy d_T·D ≤ (1 − β)·M*; the B2-bounded baseline lies strictly inside. |
| `verify_B4.py` | **Proposition B4 (Section 5):** the controllability ceiling maps to a minimum capital requirement k ≥ E/D_ctrl (≈ 0.067 at baseline), increasing in bank equity and in any relaxation of the lock. |
| `verify_B5.py` | **Proposition B5 (Section 6):** locked floors are non-withdrawable hence run-proof; the run-proof share is 1 − φ_liq ≈ 0.85, the maximum systemic run is the liquid share φ_liq, and the lender-of-last-resort need scales with runnable deposits d_T·m·φ_liq·W. |
| `make_figures.py` | Regenerates `figure_B1_inside_money.png`, `figure_B2_multiplier_bound.png`, `figure_B3B4_controllability.png`, `figure_B5_runproof_floor.png`. |

## Expected output (excerpt)

```
All B1 claims reproduced: True
L_max=0.300 binding=collateral ; sigma = 0.130
k_min = E/D_ctrl = 0.067
run-proof=0.85  runnable=0.15 ; LOLR locked=0.15 no-lock=1.00 (6.7x)
All B5 claims reproduced: True
```

## Calibration

d_T = 0.5 (transactional deposit share); k = 0.08, ρ = 0.10, m = 0.50 (loan-to-value);
φ_liq = 0.15 (liquid/pledgeable fraction; floors locked); E = 0.10, R_b = 0.12 (units of M_o);
W = 4.0 (citizen asset wealth in units of M_o); β = 0.25 (shock-response buffer); M* = 1.0.
Every printed value carries its proposition reference in brackets for direct comparison.

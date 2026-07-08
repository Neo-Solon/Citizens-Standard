# Replication package — The Citizens Standard: The Structural Buyer (Neo-Solon, 2026h)

This package reproduces the numerical claims behind the analytically-tractable propositions of
Paper 8 (SSRN 6945320). Like the macroeconomic supplement (Paper 5), it is a **computational
supplement to a theory paper**: the propositions are established by closed-form proof in Appendix A
and stand on their own; the scripts let a reader watch each result behave and confirm the stated
magnitudes rather than trust the algebra on faith. There is **no dataset and no figure** — Paper 8
contains neither; every result is a self-contained numerical check. All code is pure Python with
`numpy` only.

From `code/`:

```
python3 run_all.py > ../all_results.txt
```

This runs the five verifiers (Propositions 1, 2, 3, 7, and the Appendix A.6 ownership-plateau identity).

## Modules

| Module | Reproduces |
|---|---|
| `verify_prop1_premium.py` | **Proposition 1 (Appendix A.2):** the valuation premium converges to the finite fixed point Q\* − Q_baseline = A\*/φ; the affine repricing recursion is stable iff 0 < θφ < 2 (divergent at 2.5); the premium is strictly decreasing in the net equity-supply response φ. |
| `verify_prop2_investment.py` | **Proposition 2 (Appendix A.3):** at the fixed point net issuance equals absorption (I\* = A\*), so the float is constant; along the transition the per-period repricing decays geometrically at \|1 − θφ\|, the share of the flow met by primary issuance rises monotonically from 0 to 1, and total repricing equals A\*/φ — a once-for-all level effect, not perpetual asset inflation. |
| `verify_prop3_leak.py` | **Proposition 3 (Appendix A.4):** the consumption leak from the asset circuit into the transactional circuit is bounded by κ_W·Δ; at the central κ_W ≈ 0.03 the leak is ~3% and ≥ 97% of secondary proceeds re-enter M^A; the bound holds across the literature range κ_W ∈ [0.025, 0.05]. |
| `verify_prop7_mirror_voting.py` | **Proposition 7 (Appendix A.5):** under the mirror rule the FDCA casts its vote share ψ in residual-shareholder proportions, so the total YES share equals the residual YES share p for every ψ (verified to machine precision over random ψ, p); the outcome matches the residual shareholders' at every threshold τ, and the FDCA is never pivotal. |
| `verify_psi_plateau.py` | **Appendix A.6:** the zero-growth stock-flow value is ψ\* = c·dur ≈ 0.20 at Mode B (c ≈ 0.005, dur ≈ 40), verified under both the constant-hazard and fixed-duration decumulation models; under positive growth the realized share is lower, ψ\* = c·annuity(g, dur) ≈ 0.12 at 2% growth, bounded above by c/g ≈ 0.25 — so a 30% share is unreachable at Mode B under positive growth. |

## Expected output

```
A.2 PASSED: premium = A*/phi = 0.9000 (sim 0.9000); stable for theta*phi in (0,2), divergent at 2.5; premium decreasing in phi.
A.3 PASSED: I*=A*=0.45; float constant; repricing decays at |1-theta*phi|=0.75; sum(repricing)=0.9000=A*/phi; issuance share 0 -> 1.
A.4 PASSED: leak <= kappa_W*Delta; central kappa_W=0.03 -> 3% leak, 97% re-enters M^A; working range [0.025, 0.05].
A.5 PASSED: YES_total = p for all psi (machine precision); outcome = residual outcome at every threshold; FDCA never pivotal.
Appendix A.6 verification PASSED:
  zero-growth  c*dur = 0.198  (Mode B, dur=40)
  realized     psi* = c*annuity = 0.123  (g=2%; hazard 0.110, annuity 0.135)
  ceiling      c/g = 0.248  (dur -> inf)
  30% share needs zero growth and dur ~ 61 yr; unreachable at Mode B under 2% growth.
All Paper 8 verifications passed.
```

## Scope and calibration

Propositions 4–6 (price discovery above the active-float threshold; the cost-of-capital and
index-capture results) are **mechanism-design / threshold results argued in the main text**, not
closed-form proofs, and are not script-verifiable here. The price-discovery threshold (active float
1 − ψ_t > f_min) is the live design constraint that motivates a holdings ceiling or float-recycling
lever.

The parameter values in the recursion scripts (A\*, θ) are **illustrations, not calibrations** —
Paper 8 states its magnitudes the same way. The one load-bearing empirical quantity is **φ, the net
equity-supply response**: Propositions 1–2 require φ > 0, which in the present US regime is *not*
satisfied (net issuance has been persistently negative; buybacks are procyclical). The paper
therefore carries the **buyback-constrained regime as its baseline** — a graduated repurchase tax or
cap that secures φ > 0 — and treats the unconstrained regime as the counterfactual in which the
premium A\*/φ is large rather than translating into real investment. See the paper's §9 (Calibration
and Falsification) for the empirical anchor and falsification point of each quantity.

Requirements: Python 3.10+ with `numpy`. All scripts are deterministic.

## Figures
`code/make_figures.py` reproduces the two paper figures from the verified proposition math: `figure_prop1_premium_stability.png` (Proposition 1 — bounded premium A*/phi and the 0<theta*phi<2 convergence band) and `figure_psi_plateau.png` (psi* = c*annuity(g,dur) saturating at c/g under growth). Output to `figures/`.


## Consolidated verification (`code/verify_all.py`)

One command runs all five propositions as a single PASS/FAIL report with a
structural-vs-calibration classification and a one-page diagnostic dashboard:

```
python3 code/verify_all.py            # full report + dashboard
python3 code/verify_all.py dashboard  # one-page dashboard only
```

Structural propositions (P1 premium = A*/phi, P2 flow funds investment, P7
mirror-voting neutrality) hold as identities for any admissible parameters;
calibration-dependent ones (P1b convergence band, P3 leak range, psi* bound)
depend on the calibrated magnitudes. The harness reproduces the same computed
values as the individual `verify_prop*.py` scripts.


*`requirements.txt` added 2026-07-07 (numpy, matplotlib); run remains `cd code && python3 run_all.py`.*

# Growth-Measurement Error and Price Drift

Grounds the recurring objection that "issuance matched to real growth" is only as
good as real-time growth *measurement*: if issuance is set to measured growth but
the truth is revised, the mismatch leaks as price drift.

## Result (headline)

| Source of error | 40-year cumulative price drift |
|---|---|
| Revision noise, Mode B (uncorrelated) | ~0% median (-1.8% to +1.9%) |
| Revision noise, Mode D | ~0% median (-4.7% to +4.5%) |
| Systematic +0.2pp bias, Mode B | +2.1% (+0.3% to +3.9%) |
| Systematic +0.2pp bias, Mode D | +5.4% (+0.6% to +9.9%) |

**Revision noise washes out; systematic bias does not.** Because BEA estimates
mean-revert (the third estimate corrects most of the advance error) and the engine
re-matches as data is revised, ordinary measurement noise produces near-zero
cumulative drift over decades. A *persistent measurement bias* (systematic over- or
under-measurement) is the real exposure, accumulating to a few percent of the price
level over 40 years — larger in Mode D, because more of the mis-issued money
reaches the goods circuit.

**Bottom line:** the matching rule is robust to the measurement noise BEA data
actually exhibits; its vulnerability is a persistent bias, which is a data-quality
and institutional dependency (keep the growth estimate unbiased) rather than a flaw
in the rule. Running floor-weighted (low kappa_d) shrinks the exposure further,
since less mis-issued money reaches the goods market.

## Method
- One-year drift = measurement error (pp) routed by kappa_d into the transactional
  circuit M^T (~0.30*M2); the floor-bound share lands in the asset circuit and does
  not move CPI (the same two-lane logic as the rent and demand-impulse modules).
- Multi-year: 40-year Monte Carlo (4,000 trials) over revision noise (mean-zero,
  sigma ~0.65pp), error persistence, and an optional systematic bias; only the
  post-revision residual (~20% of each year's error) persists.

## Verification / anchor
- **BEA reliability study (Survey of Current Business, 2024/2026): advance-to-third
  real GDP growth revisions averaged 0.52pp over 2000-2024**, trending lower; this
  sets sigma ~0.65pp.
- Routing (kappa_d to M^T, floor share to asset circuit) matches the issuance
  engine's two-circuit structure.
- Mis-issuance is routed by kappa_d (dividend share to the goods circuit, floor share
  to the asset circuit), matching the issuance engine's two-circuit structure, so the
  drift reflects only the goods-circuit portion.

## Caveats
- One-year passthrough to prices assumed 100% (conservative; overstates).
- The persistent-residual fraction (20%) and the bias magnitude (0.2pp) are
  illustrative; the qualitative split (noise washes out, bias accumulates) is the
  robust finding.
- Partial equilibrium; no monetary-policy offset, which would further damp drift.

## Reproduce
```
cd code
python3 stage1_measurement_drift.py
python3 stage2_drift_accumulation.py
```

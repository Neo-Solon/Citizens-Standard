# Structural-Buyer Endgame: the Ownership Plateau

Tests Paper 8's long-run accumulation claim (Proposition 4 / §6.2): that the floor
does NOT accumulate toward owning the market, because each retiring cohort liquidates
its floor and returns equity to the active float, bounding the steady-state ownership
share at psi* ~ c·dur (deposit-rate-in-equity-terms times mean holding duration),
computed at ~0.10 (0.09-0.11), leaving ~88-90% in active float.

## Result (this one largely vindicates the paper)

1. **The plateau is real (Proposition 4 holds).** A cohort accumulation/decumulation
   simulation converges and never runs toward 1 in any swept case — decumulation
   structurally bounds the share. The "permanent buyer eventually owns everything"
   objection is genuinely defeated.

2. **The number is sound.** The simulation reproduces the paper's closed-form
   psi* = c·annuity(g,dur) identity exactly, and the central plateau (verified 0.39%
   flow, ~40-year duration, 2% growth) is **10.9%** — squarely in the paper's stated
   0.09–0.11 bracket.

3. **Nuance (the honest addition).** The plateau *level* is duration- and
   flow-sensitive, ranging ~6% (short duration / low flow) to ~21% (long duration /
   high floor-weighting). The paper's ~10% is the central case of that range, not a
   fixed point; at long holding durations it could reach the high-teens to ~20%.

| holding dur | c=0.30% | c=0.39% | c=0.50% | c=0.65% |
|---|---|---|---|---|
| 25y | 6.0% | 7.8% | 10.0% | 12.9% |
| 30y | 6.9% | 8.9% | 11.4% | 14.8% |
| 40y | 8.4% | 10.9% | 14.0% | 18.1% |
| 50y | 9.6% | 12.5% | 16.0% | 20.8% |

**Float threshold (price discovery):** active float stays ~79–94% across the whole
range, well above the ~40–50% passive-ownership level where price-discovery concerns
bite in the index-fund literature. The paper's "discovery survives above a float
threshold" claim holds throughout.

## Verdict
The endgame is bounded as Paper 8 argues. The decumulation mechanism works, ~10% is a
fair central plateau, and price discovery is preserved. The one amendment: present
the plateau as a ~6–21% range centered near 10%, duration-driven, rather than a
single number — which makes the bound more credible by showing its sensitivity.

## Verification / grounding
- Verified flow anchor A*/M_index ~ 0.39%/yr at Mode B (Paper 8 §10.1, reproduced in
  the asset_price_impact module).
- Cohort accumulation/decumulation logic mirrors the repo's demographic_flow_model.py
  (which independently finds the buyer turns net seller ~year 55 as retirees mature).
- The dynamic simulation and the paper's closed-form identity agree to <0.2pp.
- Parameters (flow, holding duration, growth) swept across plausible ranges, not
  point-guessed.

## Caveats
- A reduced-form stock-flow model: uniform holding duration, level flow-as-share,
  constant growth. No return volatility, no cohort-size demographics beyond duration,
  no behavioral decumulation timing. It tests the plateau identity and its
  sensitivity, not a full demographic micro-path (that is demographic_flow_model.py).
- Long-horizon extrapolation; the plateau is a steady-state property, not a forecast.

## Reproduce
```
cd code
python3 stage1_ownership_plateau.py
python3 stage2_float_and_verdict.py
```

# Floor-Lane Asset-Price Impact

Grounds the floor-lane asset-price-pressure concession -- the structural buyer
bids up the very equities it accumulates, which is *why* Paper 2 uses an attenuated
4.26% real return rather than the historical price-taker return -- against the
empirical inelastic-markets literature, and checks whether the attenuation Paper 2
already takes is consistent with that price impact.

## Result (headline)

**The 4.26% attenuated return is broadly consistent with the floor's own empirical
price impact.** The floor's annual valuation impulse (flow x price multiplier) is:

| Price multiplier M | Impulse/yr (Mode B) | vs ~2.2pp attenuation already taken |
|---|---|---|
| 1.0 (order-unity, Bouchaud microstructure) | 0.4% | within |
| 5.0 (Gabaix-Koijen central, inelastic markets) | 1.9% | within |
| 8.0 (GK high) | 3.1% | exceeds (upper-corner caution) |

Across most of the multiplier range the floor's price impact is at or below the
~2.2pp the return was already attenuated by (historical ~6.5% real to Paper 2's
4.26%). The strongest contrary evidence (GK inelastic markets) pushes toward the
**conservative end of Paper 2's stated band (3.30-5.03%)**, rather than refuting
the attenuation. Only the M=8 corner exceeds it, and that is a single-year flow
impulse, not a permanent annual drag (the premium stabilises via Paper 8's bounded
fixed point), so it is a caution worth stating, not a contradiction.

**Practical anchor:** the floor's flow (0.39%/yr Mode B) is ~1/4 of the ~1.5%/yr
corporate-buyback flow the market already absorbs, so it is not unprecedented in
magnitude -- though it is permanent and rule-bound.

## Method
- `stage1_valuation_premium.py`: combines Paper 8's verified absorption flow
  (0.39%/yr Mode B, 0.65%/yr floor-max) with two **separately-cited** facts:
  (1) the Gabaix-Koijen (NBER 28967) demand-side price multiplier M (central 5,
  range 3-8; Bouchaud microstructure dissent ~1), giving a short-run impulse f x M;
  (2) Paper 8's supply-side bounded premium A*/phi. These are kept separate by
  design -- M (demand-side) and phi (supply-side) are different parameters and are
  NOT fused into a single derived number.
- `stage2_return_consistency.py`: compares the f x M impulse to the ~2.2pp
  attenuation Paper 2 already took (historical ~6.5% to 4.26%), swept over M.

## Verification
- Absorption flow verified against Paper 8 (0.39% at kappa_d=0.4, 0.65% at kappa_d=0).
- GK multiplier and range taken from the NBER paper directly; microstructure
  dissent (Bouchaud 2021) included as the low end.
- The model keeps GK's demand multiplier and Paper 8's supply elasticity as distinct
  objects rather than fusing them; it does NOT claim GK implies a specific phi. The
  price impact is reported as the two-fact framing above (verified flow x literature
  multiplier range).

## Caveats
- The short-run impulse (f x M) is the **level** impact of a year's flow; the
  long-run **return** drag is not the same object and depends on the supply
  response phi, which neither Paper 8's illustration nor GK pins down empirically.
  The consistency check treats the impulse as a return headwind, which is a
  conservative bound, not a structural estimate.
- Steady-state, partial-equilibrium; no crisis/drawdown dynamics (Paper 8 defers
  those explicitly).
- GK's M is estimated on US flows 1993-2019; applicability to a permanent
  sovereign buyer of this specific size is an extrapolation.

## Reproduce
```
cd code
python3 stage1_valuation_premium.py
python3 stage2_return_consistency.py
```

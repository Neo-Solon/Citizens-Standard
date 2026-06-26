# Credit Displacement / Double-Claim Test

The framework's single most load-bearing unverified claim: growth-matched issuance
is net-neutral to inflation *because* the new sovereign money displaces credit
banks would otherwise have created. If displacement is complete, money growth is
unchanged and there is no inflation; if partial, the un-displaced share is additive
and inflationary. This module tests that claim on verified data, sweeping the one
irreducibly-uncertain parameter (the displacement ratio delta) across the empirical
literature range rather than guessing a point value.

## Result (honest, and it qualifies the claim)

**Relying on credit displacement to neutralize a cash dividend does not hold up.**

| Mode | Break-even displacement needed (impulse < 1%) |
|---|---|
| Mode D (pure dividend, kappa_d=1) | **89%** |
| Mode B (floor-weighted, kappa_d=0.4) | **73%** |
| Floor-max (kappa_d=0) | none (no goods-circuit exposure) |

The empirical crowding-out literature finds displacement is **partial, never
complete, and state-dependent** (near-zero in slack, e.g. 2008-09; larger near full
employment). It does not reach the 73-89% a dividend would need. So a large cash
dividend's price neutrality **cannot** rest on displacement.

Price impulse from the un-displaced share (2024 issuance, by mode):

| delta | Mode B impulse | Mode D impulse |
|---|---|---|
| 1.0 | 0.00% | 0.00% |
| 0.6 | 1.49% | 3.73% |
| 0.2 | 2.99% | 7.47% |
| 0.0 (Chartalist additive) | 3.73% | 9.33% |

## The reframe this forces (constructive)

The framework's real inflation defense was never displacement. It is:
1. **Growth-matched issuance caps the quantity** -- the dividend is bounded by
   realized growth and cannot run away regardless of delta. First-order control.
2. **Floor-weighting keeps most issuance out of the goods circuit** -- at Mode B
   only 40% reaches the lane where displacement matters; the floor share is an
   asset-price question (see the asset_price_impact module), not a goods-inflation
   one. The two-circuit structure is the structural mitigant.

So the honest position: the double-claim concern is **real**, a pure-dividend Mode D
carries a **genuine bounded inflation risk** from the un-displaced share, and the
defensible neutrality argument is growth-matching plus floor-weighting -- not
credit displacement. This argues for floor-weighting and a modest dividend, which
is the framework's recommended operating point anyway.

## Method
- delta applies to the **dividend lane only** (kappa_d x issuance): the floor lane
  buys existing equities in the asset circuit and does not create goods-circuit
  money, so its neutrality is the asset-price question, not the displacement one.
- Price impulse = additive goods-circuit money / M^T stock (~0.30 x M2), consistent
  with the demand-impulse and growth-measurement modules.
- Break-even delta = the displacement that holds the impulse under a 1% tolerance.

## Verification / empirical grounding
- Bank-created share of US M2 ~90% (verified, US Dec-2010); long-run bank-created
  flow ~3.3% of GDP/yr (verified, 1960-2025 series).
- CS issuance from the engine's growth-matching rule on the historical series
  (2024: $584B, 2.0% of GDP).
- Displacement bounds from the crowding-out literature (Mercatus, IWU, Albert:
  "partial crowding out is the most empirically relevant case"; 2008-09 slack
  episode; Chartalist/Post-Keynesian additive view as the bear case).
- **A category error was avoided**: the standard crowding-out coefficient measures
  government *borrowing* displacing private credit; CS issuance is *money creation*,
  not borrowing, so that coefficient is NOT imported as delta. The literature is
  used only for the robust qualitative bounds (partial, state-dependent), and delta
  is swept, not assigned.

## Caveats
- delta for money creation (vs borrowing) is genuinely unmeasured; the module
  reports the requirement and its plausibility, not a point estimate of inflation.
- Partial equilibrium, single representative year; no monetary-policy offset.
- The 1% tolerance and the 0.30 M^T/M2 ratio are modeling choices, stated; the
  qualitative conclusion (displacement can't carry a large dividend) is robust to
  both.

## Reproduce
```
cd code
python3 stage1_displacement_requirement.py
python3 stage2_breakeven_and_plausibility.py
```

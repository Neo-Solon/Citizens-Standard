# PPP Half-Life Test — Pre-Registered Protocol (FROZEN before estimation)

**Written and frozen BEFORE running the test**, in response to the monthly Line A failing
its falsification condition. The monthly test is not repeated or reinterpreted; this is a
distinct, properly-specified test at the horizon where the mechanism is claimed to operate.
Any deviation discovered during execution will be reported AS a deviation, not silently fixed.

## The claim being tested

The CS FX-stability claim, stated in the form the international-finance literature can test:
**a currency with a rule-fixed nominal/inflation anchor exhibits lower real-exchange-rate
variance and/or faster mean-reversion of PPP deviations than a freely-floating currency.**

This is the Rogoff (1996) "PPP puzzle" framework. It is the academically standard way to ask
whether an anchor stabilizes the *real* exchange rate over the horizons that matter for trade.

## Data (fixed)

- FX: FRED DEX* daily, 1971-2026 (CAD, JPY, SEK, DKK, CHF vs USD, 55yr; KRW, HKD ~45yr),
  aggregated to monthly (month-end).
- CPI: FRED/OECD monthly — US (CPIAUCSL), and partner CPI (CAN, SWE, DNK, CHE full; JPN to
  2021-06 only → Japan tested on its available sample and flagged).
- Real exchange rate: q = log(S) + log(P_foreign) − log(P_US), where S = foreign currency per USD.
  (q is the log real exchange rate; PPP deviations are deviations of q from its mean.)

## Regime classification (fixed in advance)

- **Anchored:** HKD (hard USD currency board, 1983–). This is the one clean USD anchor.
- **EUR-anchored (reported separately, NOT pooled with USD-anchored):** DKK (ERM/ERM-II).
  Measured vs USD it inherits EUR/USD variance — so it is NOT a USD anchor and is reported
  as its own category, per the DKK lesson from the panel.
- **Floating:** CAD, SEK, JPY, KRW (free floats over most of the sample).
- **Soft/managed float:** CHF (low-inflation float; reported separately, not as a hard anchor).

## Method (fixed)

**Primary test — half-life of PPP deviations.**
For each currency, estimate the AR(1) mean-reversion of the log real exchange rate q:
  Δq_t = α + β·q_{t−1} + ε_t     (equivalently q_t = μ + ρ·q_{t−1} + ε_t, ρ = 1+β)
Half-life = ln(0.5) / ln(ρ), in months. Report with a bias-aware method:
  - OLS ρ (known to be downward-biased in small samples),
  - and note the sign of the bias; do not over-interpret point half-lives.
Also run an **ADF unit-root test** on q per currency: rejection of a unit root ⇒ PPP
reversion exists (q is stationary). Report the ADF stat and p-value.

**Secondary test — real-exchange-rate variance.**
Annualized variance (and long-horizon variance ratio) of q, anchored vs floating.

**Comparison (the actual hypothesis).**
- H: anchored (HKD) shows SHORTER half-life and/or LOWER real-rate variance than floaters.
- Report anchored vs floating vs EUR-anchored vs soft-float as separate groups.

## Falsification (fixed in advance)

The anchor-stabilizes-the-real-rate claim FAILS if **either**:
  (G1) the anchored currency's real-rate half-life is NOT shorter than the floating group's
       (i.e. anchoring does not speed PPP reversion), AND its real-rate variance is not lower; OR
  (G2) real exchange rates are stationary (fast reversion) for floaters too, at similar speed —
       i.e. the anchor adds nothing the float already has.

If falsification fires, the honest report is that real-rate stability is not a demonstrable
CS advantage on this test, exactly as with the monthly Line A.

## Honest limits (stated up front)

- **PPP half-lives are notoriously imprecise** — the literature's confidence intervals are
  very wide (the "3–5 year consensus" masks huge uncertainty). Point estimates are indicative.
- **HKD is a hard peg, not a CS-style inflation-anchored float** — it is the low bracket, not
  the CS point. CS floats nominally, so its real-rate behavior would sit between HKD and floaters.
- **The peg mechanism ≠ the inflation anchor** — HKD's real-rate behavior reflects the board,
  which is more rigid than a CS inflation rule. Bracketing logic only.
- **Japan sample ends 2021-06** (CPI discontinued on this vintage) — Japan tested on its
  available span and flagged; not dropped silently.
- **Structural breaks** (Bretton Woods collapse 1971-73, ERM crises, 2008, 2020) are in the
  sample; a robustness cut post-1973 (pure float era) is pre-specified.

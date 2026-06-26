# Procyclical Dividend: Magnitude and Floor-Stock Survival

Grounds the Crisis-Behaviour claim (Paper 12) that the dividend is procyclical
"by construction" -- the **signature failure mode** -- on actual US history
1960-2025, and tests whether the two claimed mitigants hold.

## Result (headline)

**The procyclical collapse is total and confirmed, and slightly worse than the
paper's language implies:**

- In all **7 historical contraction years** (1974, 1975, 1980, 1982, 1991, 2009,
  2020) the growth-matched dividend (K2 = max(0, real growth) x M2) falls to
  **exactly zero** -- a 100% drop, precisely when households most need it.
- The K1 per-citizen endowment keeps paying in contractions, but it provides
  **~1% of the lost dividend** -- *not* a meaningful cushion. K1 endows only new
  citizens (~3M births/yr at 2.5% of GDP/capita), so it is structurally tiny vs
  the ~$170B dividend. The paper's "partially offsets" overstates it: K1 is a
  birthright grant, not a stabiliser.

**The genuine protection is the floor STOCK, which survives -- with a real but
bounded tail risk:**

| Scenario | Floor-stock max drawdown |
|---|---|
| Actual historical sequence | 40% |
| Bootstrap median (2000 resamples) | 38% (5th-95th: 23%-59%) |
| Adversarial worst-late sequencing | 91% |

So in typical histories the accumulated floor draws down 23-59% in the worst
downturn and recovers; under adverse sequence-of-returns (worst crashes stacked at
peak accumulation) it can fall ~91%. The qualitative claim holds -- the **flow**
vanishes in a contraction but the **stock** (wealth already owned) persists, the
structural difference from a pure cash UBI -- but "the stock survives" is
conditional on sequencing, consistent with Paper 2's own stress-test caveat.

## Method
- `stage1_procyclicality.py`: computes K2 dividend and K1 endowment for every year
  1960-2025 using the verified `deterministic_engine.py` formula (k1=2.5%,
  K2 = max(0, real growth) x M2[y-1], residual calibration), identifies
  contractions, measures dividend drop and K1 offset, accumulates the floor stock.
- `stage2_stock_survival.py`: stress-tests the floor-stock max drawdown under the
  actual sequence, adversarial re-sequencing, and 2000 bootstrap resamples of the
  real-return series.

## Verification
- Contraction years match known US recessions with negative annual real GDP.
- K1 magnitude sanity-checked (GDP/capita = $64.5k for 2020, correct).
- Formula and parameters reused from the verified deterministic_engine.py.
- The ~1% K1 offset confirmed structural (per-new-citizen grant), not a bug.

## Caveats
- The $69T accumulated 2025 floor is illustrative of stock survival, not a precise
  wealth claim (mixes nominal flows with real returns); the load-bearing output is
  the **drawdown**, not the level.
- Annual data: sub-year contractions (e.g. 2008 Q4) show as small-positive annual
  growth, so the 7 contraction-years undercount intra-year stress slightly.
- The adversarial sequencing is a deliberately pessimistic construct (not a
  forecast); it bounds the tail, it is not the expected case.

## Reproduce
```
cd code
python3 stage1_procyclicality.py
python3 stage2_stock_survival.py
```

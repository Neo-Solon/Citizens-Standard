# Capture / Fig-Leaf Risk: Empirical Override Base Rate

Grounds the capture objection ("once you centralize the issuance dial, every crisis
becomes an excuse to override it, and the citizen floor is a fig leaf on an
arbitrary printing machine"). Rather than defend against it, this module **measures
how often comparable formal monetary and fiscal commitment rules have actually been
overridden**, and lets the data say whether the risk is real.

**It is. The data supports the objection, not the design.** That is the honest
finding, and it is the point of building this.

## Result (the override base rate is high)

**Fiscal rules** (IMF Fiscal Rules Database, 1985-2024, 100+ countries):
- ~90% of countries breached deficit-rule limits in 2020 (COVID) — override is
  near-universal in crisis.
- Even in normal times (2014-2019): ~60% of advanced economies and ~40% of EMDEs
  failed debt rules; ~20% (AE) / ~40% (EMDE) breached deficit limits.
- By 2024, two-thirds of fiscal rules had built-in escape clauses (double 2000);
  escape-clause use rose from ~5% (GFC) to widespread (COVID).
- Deviations are "highly persistent" and "very difficult to reverse."

**Central-bank independence** (closer monetary analogue):
- IMF WP 2026/040: of 132 governor transitions (28 countries, 2000-2024), 38% were
  politically motivated; ~50% in emerging markets.
- Romelli CBI dataset (1950-2023): of 370 legislative reforms, ~25% (91) *reversed*
  independence.
- De jure protection is "no guarantee" of de facto independence.

## What (partially) helps — and where CS sits

The same literature identifies factors correlating with rules holding *somewhat*
better: a compliance **track record**, independent **monitoring** (fiscal
councils), **well-designed escape clauses** (bounded, on-the-record deviation), and
de facto institutional strength.

Against that, CS honestly scores **mixed-to-poor**:
- Its formula-bound, auditable issuance rule is the transparency/monitoring factor
  built into the mechanism — which by the evidence should *raise the cost* of
  override, not prevent it.
- CS has **no operating track record** — the single factor most associated with
  rules holding — so on the strongest empirical mitigant it scores worst.
- Centralizing the lever is exactly the failure surface the objection names;
  auditability makes a breach *legible*, not less *tempting* under crisis, which is
  when the base rate shows rules fall.

## Honest bottom line
The fig-leaf risk is real and substantial. CS's auditability is a genuine but
partial mitigant (visibility raises the cost of override; it is not protection),
and CS is weak on track record because it has never run. The defensible claim is
not "the rule is safe" but "the rule makes override visible, and visibility is
worth something but is not protection." Capture remains on the unsolved list — this
module strengthens that conclusion rather than softening it.

## Verification / sources
- IMF Fiscal Rules Database and "Fiscal Rules and Fiscal Councils" (WP 2022/011;
  2025 update WP 2025/198): breach/compliance/escape-clause figures.
- IMF WP 2026/040, "Macroeconomic Consequences of Undermining Central Bank
  Independence": 132 transitions, 38% politically motivated.
- Romelli (2024), CBI dataset 1950-2023: 370 reforms, 91 reversals.
All figures are reported as cited; this module aggregates published rates, it does
not estimate a new probability of failure (no such parameter exists, and inventing
one would be false precision).

## Caveats
- These are *analogues*, not CS itself; no full-reserve sovereign-issuance rule has
  ever run, so the base rate is indicative, not a direct forecast.
- Rates vary widely by institutional context (advanced vs emerging); the high end
  is emerging-market, the low end advanced-economy normal-times.
- The module deliberately does NOT produce a single "CS failure probability" — it
  reports the override frequency of comparable rules and lets the reader judge.

## Reproduce
```
cd code
python3 stage1_override_baserate.py
python3 stage2_mitigants_and_cs.py
```

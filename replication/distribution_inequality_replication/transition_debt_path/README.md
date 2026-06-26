# Transition Debt-Retirement Path

Tests Paper 3's central quantitative transition claim — that under Mode T, a
transition-only channel (KT) retires legacy public debt while staying consumer-price
neutral, taking debt-to-GDP from ~102% at enactment to ~39% by Year 30 and ~15% by
Year 45 — against real fiscal data, sweeping the uncertain macro parameters rather
than guessing them.

## Result (honest, and it qualifies the paper)

**The path is reachable but optimistic-leaning, and the mechanism attribution is
off.**

1. **Timeline.** The 39%/15% milestones hold only at a near-maximal KT share (~1.0)
   or high-end growth (~2.7%+). Under central assumptions (real growth 2.0%, avg
   rate 3.3%, KT share 0.6), debt/GDP reaches 39% around **Year 40**, not Year 30,
   and does not reach the 15% floor within the horizon.

2. **Budget tension.** The paper promises citizen K1/K2 run at full price stability
   throughout, but the fast path needs KT near the whole growth-matched budget — and
   KT and K1/K2 draw on the *same* budget. Maxing both at once is not possible
   (slack early, when citizen draw is ~0.15% of GDP; binding later as K2 scales).

3. **Mechanism (the load-bearing point).** The growth-matched budget is ~1.5% of
   GDP/yr; interest on the debt stock is ~3.3% of GDP/yr early. So KT cannot outpay
   interest in the early decades — debt/GDP falls mainly because **nominal GDP
   growth expands the denominator**, not because KT retires principal. This is how
   postwar economies actually reduced debt/GDP (grow out of it), so it is
   defensible, but it reframes KT as an **assist**, not the retiring agent. The
   honest claim is the stronger one: the system grows out of the debt under price
   stability, KT accelerating at the margin and guaranteeing no new borrowing.

## Why this is not an understatement of KT
The KT cap used is the paper's *own* constraint: KT is "calibrated to a price-level
path" and "self-throttling on inflation" (Paper 3), i.e. bounded by the
non-inflationary headroom. The slower path follows from the paper's own rule, not
from a conservative assumption imposed here.

## Verified anchors
- Gross federal debt > $39T (exceeded March 2026); debt held by public ~$28–30T,
  ~98–100% of GDP (FY2024 actual: $28.2T, 98%). The paper's $31.4T/102% is a
  near-term forward figure; the model anchors transparently at ~100% and notes this.
- GDP ~$29T; real growth 1.8–2.7% (CBO 2025–2035); net interest ~3.2% of GDP, avg
  rate ~3.3%; M2 ~$21.5T.

## Caveats
- A reduced-form debt-dynamics model (one economy-wide debt stock, constant average
  rate, growth-matched KT). No term structure, no rate response to the program, no
  phase-by-phase KT scaling. It tests the aggregate retirement arithmetic, not the
  micro path.
- The 15% operational floor is imposed as the paper specifies.
- Single deterministic paths swept over the central parameters; not a stochastic
  projection.

## Reproduce
```
cd code
python3 stage1_debt_path.py
python3 stage2_sweep_plausibility.py
```

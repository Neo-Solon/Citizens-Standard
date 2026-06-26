# Full-Reserve Credit-Supply Gap

Addresses the hardest open objection (Wilson's / blackout's frontier): under full
reserve, banks no longer create money by lending; credit is intermediated from real
savings. Can intermediation supply enough credit, or does removing money-creation-
via-lending starve credit?

## What this module does -- and deliberately does not -- do

It **sizes the gap** (quantifiable, data-grounded). It does **not** claim to resolve
whether intermediation fills it, because that is a genuine unsettled macro debate
with no empirical parameter to ground a number. We refuse to fabricate a "credit
availability = X%" result; that would be false precision. Both sides of the debate
are stated with citations instead.

## Result (the quantifiable part)

| Quantity | Value |
|---|---|
| Bank-created share of US broad money (M2) | ~90% (verified) |
| Annual bank-created money flow (long-run median) | ~3.3% of GDP |
| Residual after CS growth-matched issuance | ~1.1% of GDP/yr (typical) |

The flow full reserve removes is the bank-lending money-creation channel, ~3.3% of
GDP per year. But CS sovereign issuance (growth-matched, G = k2 x M2 x g) directly
supplies the growth-matched core, so the **residual that term-deposit
intermediation must cover shrinks to ~1.1% of GDP per year** -- roughly a third of
the raw gap. That is the real, bounded statement of the challenge.

## The unresolved question (stated, not numbered)

**For (intermediation suffices):** Benes & Kumhof (IMF WP 2012, "The Chicago Plan
Revisited") simulate the transition and find credit provision maintained or
improved with lower volatility; McLeay et al. (BoE 2014) note the binding
constraint on lending is loan demand and capital, not deposits; and CS adds a
sovereign-issuance channel the classic Chicago Plan lacked, shrinking the residual.

**Against (intermediation falls short):** critics (sovereignmoney.site; Austrian
intermediation theorists) argue maturity transformation and the sheer volume of
bank-created credit cannot be replicated by term deposits without raising the cost
of capital and rationing credit to riskier productive borrowers; and full reserve
does not by itself solve the credit-allocation/screening function banks provide.

**Where CS sits:** CS does not claim intermediation seamlessly replaces bank credit
at current volume. It claims sovereign issuance supplies the growth-matched core,
the residual is intermediated, and the likely result is **less total credit at a
higher cost of capital** than today -- a deliberate trade (less credit-fuelled
boom-bust for less credit) whose net desirability is contested and unproven. This
module sizes the gap; it does not close it.

## Verification / anchors
- **~90% US bank-created share of M2**: from US Dec-2010 M2 $8,853B, currency
  $915.7B (FRS via Wikipedia); UK/M4 figure is 97% (McLeay et al., BoE 2014;
  Werner 2005, "similar proportions in most industrialised economies"). 90% used
  as the conservative US figure.
- M2 flows from the bundled 1960-2025 series; CS issuance from the engine's
  growth-matching rule.

## Caveats
- The residual (~1.1%/GDP) is a flow-accounting figure, not a claim that
  intermediation supplies exactly that much; it sizes what must be covered.
- Whether the residual is met, and at what cost of capital, is the unresolved
  question this module explicitly does not answer with a number.
- COVID-era spikes (2020 M2 +16%/GDP) and contraction years (negative) are shown
  but excluded from the typical figure via the median.

## Reproduce
```
cd code
python3 stage1_gap_sizing.py
python3 stage2_residual_and_debate.py
```

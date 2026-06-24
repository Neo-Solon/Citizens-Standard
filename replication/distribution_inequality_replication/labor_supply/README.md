# Labor-Supply Response to the Dividend

How much does the cash dividend deter work? Grounds the implicit "it's not enough
to stop working, and that's part of the point" claim against the cleanest US
income-effect estimate.

## Result (headline)

| Measure | Central | Swept range |
|---|---|---|
| Participation, low-wage segment | -0.23 pp | -0.10 to -0.55 pp |
| Participation, all-worker average | -0.05 pp | -0.02 to -0.11 pp |
| Hours | ~-5 min/week | -- |

**The dividend is too small to meaningfully deter work.** Even in the low-wage
segment where the disincentive concentrates, the participation effect is well
under half a percentage point; economy-wide it rounds to ~0.05pp.

This sits **below** Wilson's stated -0.5 to -1pp low-wage band -- correctly,
because the CS dividend ($672/yr) is far smaller than the transfers underlying
that band.

## Method
Calibrated to **Vivalt et al., NBER WP 32719 (2024)** -- the OpenResearch
$1,000/month unconditional-cash RCT, the cleanest US income-effect estimate (and
the one Wilson cited):
- transfer $12,000/yr (40% income boost on ~$30k households)
- **-4.1pp** labor-force participation, **-1.3 to -1.4 hrs/week**, -$1,500/yr earnings

The CS Mode D dividend ($672/yr, verified v3_10) is ~1/18 the RCT transfer. The
income effect is scaled by transfer size and swept:
- **sub-linear** (scale^1.3) -- most likely, since tiny transfers rarely move the
  participation margin at all (nobody quits over $56/mo)
- **linear** (central)
- **super-linear** (scale^0.7) -- conservative upper bound

Concentration is reconciled: the RCT sample was itself low-income, so -4.1pp x
scale is the low-wage *segment* effect; diluting by the low-wage share of workers
(20%, 18.7M of 92M) gives the all-worker average.

## Verification
- Weight baseline asserted; RCT figures taken from the NBER source directly, not
  paraphrase.
- Worker/low-wage segmentation from SCF WAGEINC and income deciles (verified:
  70% of households have wage income, 18.7M low-wage worker households).
- Dividend = verified $672/yr Mode D figure.

## Caveats
- **Linear-ish scaling is an assumption**, swept across sub/super-linear. The true
  effect for a transfer this small is most plausibly at or below the sub-linear
  end, because small transfers rarely trigger discrete participation changes.
- Partial equilibrium, income-effect only; no GE wage adjustment. The withdrawal
  of the "desperation subsidy" at the bottom is, per the framework, a *feature*
  (un-rigging reservation wages), not just a cost.
- The RCT ran $1,000/mo for 3 years; a permanent universal payment may have
  somewhat different dynamics (the framework argues universality/permanence push
  the effect toward the small end via zero EMTR change).

## Reproduce
```
cd code
python3 stage1_labor_supply.py
python3 stage2_labor_sweep.py
```

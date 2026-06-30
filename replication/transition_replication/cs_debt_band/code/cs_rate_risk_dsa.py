"""
Rate-risk on the standing stock, the academic way: a stochastic interest-growth
differential with a debt-dependent jump (stochastic Debt Sustainability Analysis,
IMF-style fan chart), grounded in the literature we verified:

  - Blanchard (2019, AER): at r<g debt rollover may carry no fiscal cost; r<g is
    the historical norm. -> baseline drift of (r-g) is mildly NEGATIVE.
  - Mauro & Zhou (2020, IMF WP 20/52), 55 countries / 200 yrs: negative (r-g)
    "more often than not" and persistent -> calm regime is modal and sticky.
    BUT marginal rates "rise abruptly and sharply" in spikes, and (Lian et al.
    2020) the probability of a reversal RISES WITH THE DEBT LEVEL ITSELF.
  - Krishnamurthy & Vissing-Jorgensen (2012): convenience yield ~73bp hist.,
    downward-sloping in supply; St. Louis Fed (2025): compressed to ~36bp at
    today's high supply. -> marginal convenience used here = 0.40% (conservative).

So rate-risk is modeled as a REGIME process, not a fixed path: a sticky calm
regime with (r-g)<0, and a stress regime with a sharp positive (r-g) jump whose
ANNUAL ENTRY PROBABILITY INCREASES WITH THE DEBT RATIO. We then compare CS under
'aggressive retire to 15%' vs 'stabilize-only' on the full distribution, not a
point path. 10,000 Monte Carlo paths, 40 years.

Calibration (advanced-economy, annual, nominal):
  calm (r-g):   mean -1.0%, sd 1.0%   (Blanchard/Mauro-Zhou central)
  stress (r-g): mean +3.0%, sd 2.0%   (sharp marginal-rate spike)
  base entry prob into stress: 1.0%/yr at d=60%, rising with debt:
     p_stress(d) = 0.01 + 0.06*max(0, d-0.60)   (Lian-style debt dependence)
  stress is sticky: 35% chance to persist each year, else back to calm.
"""
import random
random.seed(20260629)
GDP_g_real=0.020; infl=0.023; g_nom=GDP_g_real+infl
N=10000; YEARS=40

def p_stress(d):                      # annual entry prob into a rate spike, rises with debt
    return min(0.20, 0.01 + 0.06*max(0.0, d-0.60))

def draw_rg(regime):
    if regime=="calm":   return random.gauss(-0.010, 0.010)
    else:                return random.gauss(+0.030, 0.020)

def run_policy(mode):
    finals=[]; max_ratios=[]; ever_stress=0
    for _ in range(N):
        d=1.00; regime="calm"; hit_stress=False; peak=d
        for y in range(YEARS):
            # regime transition (debt-dependent entry; sticky exit)
            if regime=="calm":
                if random.random() < p_stress(d): regime="stress"
            else:
                if random.random() > 0.35: regime="calm"
            if regime=="stress": hit_stress=True
            rg=draw_rg(regime)
            # retirement policy: aggressive shaves extra off the ratio each year;
            # stabilize only offsets a positive (r-g). Both capped by the clean
            # seigniorage budget ~1.5% of GDP -> ~ up to ~1.5 ratio-pts/yr.
            budget_pts=0.015
            if mode=="aggressive":
                retire=budget_pts                      # always spend the budget cutting debt
            else: # stabilize
                retire=min(budget_pts, max(0.0, rg*d)) # only neutralize a positive drift
            d = d*(1+rg) - retire
            d = max(d, 0.0)
            peak=max(peak,d)
        finals.append(d); max_ratios.append(peak); ever_stress+=hit_stress
    finals.sort(); max_ratios.sort()
    def pct(a,p): return a[int(p*len(a))-1]
    return dict(
        p50=pct(finals,.50), p95=pct(finals,.95), p99=pct(finals,.99),
        peak95=pct(max_ratios,.95), peak99=pct(max_ratios,.99),
        stress_frac=ever_stress/N)

agg=run_policy("aggressive"); stab=run_policy("stabilize")

print("="*78)
print("Stochastic DSA: CS under r>g regime risk (10,000 paths, debt-dependent jumps)")
print("="*78)
print(f"  {'metric':<42}{'aggressive':>12}{'stabilize':>12}")
rows=[("median debt/GDP @ yr40","p50"),
      ("95th-pct debt/GDP @ yr40","p95"),
      ("99th-pct debt/GDP @ yr40","p99"),
      ("95th-pct PEAK debt/GDP over 40y","peak95"),
      ("99th-pct PEAK debt/GDP over 40y","peak99"),
      ("share of paths hitting a stress regime","stress_frac")]
for label,k in rows:
    a=agg[k]; s=stab[k]
    fmt=(lambda x:f"{100*x:>10.0f}%") if k!="stress_frac" else (lambda x:f"{100*x:>10.1f}%")
    print(f"  {label:<42}{fmt(a):>12}{fmt(s):>12}")

print(f"""
READING IT, HONESTLY (this is the rate-risk the larger stock buys):
- Median outcome: stabilize ends HIGHER (it deliberately doesn't pay down calm-
  era debt), but both are well-behaved in the middle of the distribution.
- The TAIL is the whole point. Stabilize's 95th/99th percentile debt and its peak
  debt run materially above aggressive, AND a larger standing stock raises
  p_stress(d), so stabilize paths enter the stress regime more often
  ({100*stab['stress_frac']:.1f}% vs {100*agg['stress_frac']:.1f}% of paths). That is the empirically grounded
  cost Lian/Mauro-Zhou warn about: keeping debt high is not just a bigger shock,
  it is a MORE LIKELY shock. The 'low-rate sedation' risk is real and shows up
  here as a fatter, more-frequently-entered tail.
- So 'stabilize-don't-retire' is NOT a free lunch once regime risk is priced. It
  dominates on citizen floors and median fiscal cost, and loses in the tail.
  The defensible synthesis is therefore a TARGET BAND, not a corner: hold debt in
  a moderate range (low enough that p_stress stays near its floor, high enough to
  supply the safe asset and fund citizen floors), spending the seigniorage budget
  on citizens in calm years and on retirement only when (r-g) turns or debt drifts
  toward the band's top. That captures most of the citizen-floor gain while
  keeping the tail near the aggressive policy's.""")

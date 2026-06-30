# CS Debt Policy: From a 15% Floor to a Moderate Band

## A design revision grounded in stochastic debt-sustainability analysis

### Summary of the result

The current CS design retires legacy sovereign debt aggressively toward a ~15% floor.
This note argues, on empirically grounded and verified modeling, that the welfare-optimal
policy is instead to hold debt in a **moderate band of roughly 30-60% of GDP**, routing the
growth-matched seigniorage to citizen floors by default and retiring debt only to defend the
band. The recommendation is a robust range, not a single point, and the one genuine swing
variable (CS's safe-haven strength) is named and sourced rather than assumed.

The conclusion rests on four links, each independently grounded:

1. **Standing debt at r < g is benign-to-useful**, so aggressive retirement is not required
   for sustainability (Blanchard 2019; Mauro & Zhou 2020).
2. **Aggressive retirement wastes citizen seigniorage.** At r < g the growth snowball lowers
   the debt ratio for free, so seigniorage spent retiring debt is seigniorage not given to
   citizens. The cost is large (tens of trillions over 40 years in the central case).
3. **But keeping debt high raises crisis risk**, because the probability and severity of an
   adverse interest-growth reversal rise with the debt level (Lian, Presbitero & Wiriadinata
   2020). This is the cost that caps the band from above.
4. **CS's exposure to that crisis risk is damped by its monetary sovereignty.** Own-currency
   issuance with its own monetary authority removes the self-fulfilling-liquidity-crisis
   channel (De Grauwe 2011; UK-vs-Spain). CS has this structural property by construction,
   which is why a moderate band, not a low floor, is defensible.

The optimum balances (2) against (3), with (4) setting how hard (3) bites. The result is
stable across random seeds and robust across the plausible range of the safe-haven parameter.

---

### 1. The foundation: standing debt at r < g

The case for retiring debt aggressively assumes standing sovereign debt is costly to hold.
The empirical record says otherwise for the relevant regime. Blanchard's 2019 AEA
Presidential Address establishes that when the safe interest rate is below the growth rate,
debt rollover may carry no fiscal cost, and that r < g is the historical norm rather than the
exception. Mauro & Zhou (2020), across 55 countries and 200 years, find negative
interest-growth differentials "more often than not," persisting for long stretches.

So at r < g the debt ratio drifts down on its own through growth, and a fixed stock is close
to self-financing. Retiring it faster than the snowball does is optional, and it has an
opportunity cost.

### 2. The opportunity cost of aggressive retirement

CS retires debt by routing a share of its growth-matched seigniorage (the KT channel) to
redemption instead of to citizen floors. Module `cs_refine1.py` compares aggressive
retirement (a fixed 60% KT share) against a "stabilize-only" policy that retires just enough
to hold the ratio flat (zero when r < g). In the central r < g path, stabilize-only hands
citizens roughly $27 trillion more over 40 years while debt still drifts down through growth.
Aggressive retirement buys a lower debt ratio that, at r < g, was not needed, and pays for it
in citizen floors.

This is the pressure pushing the band *up*: the more debt you insist on retiring, the less
goes to citizens, for a sustainability benefit you largely already get for free.

### 3. The cost that caps the band: debt-dependent crisis risk

The pressure pushing the band *down* is rate risk. The risk is not a gentle drift of r above
g; it is an abrupt regime reversal whose probability rises with the debt level itself. Lian,
Presbitero & Wiriadinata (2020) document that as debt rises from 40% to 120% of GDP, the
90th percentile of the 5-year-average interest-growth differential rises from about 0 to +2%,
and the likelihood of a reversal from a negative-r-g regime to a positive one rises from about
25% (below-median debt) to more than 75% (top quartile). Keeping debt high is therefore not
just a bigger potential shock but a more likely one.

#### 3a. A validated stochastic process for r - g

To price this, we built a stochastic process for the annual interest-growth differential and
calibrated it to the published moments. After testing and rejecting a Gaussian regime-switching
family (which cannot simultaneously match the severity quantiles and the low-debt reversal
frequency, for a structural reason explained below), we adopted a **compound-jump process**:

- a tight, reliably negative baseline (calm r < g, financial-repression / safe-haven regime);
- rare, large, positive **jumps** (crises, sudden stops, rate shocks) whose *magnitude*
  generates the severity tail and whose *persistence* generates sustained reversal episodes;
- both jump intensity and jump persistence **rise with the debt ratio**, per Lian et al.

The jump structure is not a curve-fitting convenience. Real interest-growth differentials are
not Gaussian: calm periods are tightly negative, and upside risk arrives as rare large spikes,
not gentle elevation. The Gaussian family fails precisely because it locks the magnitude of
the upper tail to the frequency of positive years through a single variance; a jump process
breaks that lock, which is why it reproduces both the severity curve and the reversal gradient
from one coherent mechanism.

#### 3b. Verification

The locked process (`dsa_locked.json`) reproduces **all six** calibration moments plus a
**held-out** moment it was never fit to, stable across two independent seeds at N = 12,000
(`dsa_jump_verify.py`):

| moment | model | target | source |
|---|---|---|---|
| 90th-pct 5y r-g @ debt 40% | 0.01% | ~0.0% | Lian et al. 2020 |
| 90th-pct 5y r-g @ debt 120% | +2.0% | +2.0% | Lian et al. 2020 |
| median r-g @ debt 40% | -1.05% | -1.2% | Blanchard 2019 / Mauro-Zhou 2020 |
| median rise (40%->120%) | +0.93% | +0.8% | Lian et al. 2020 |
| reversal prob @ debt 45% | 24% | ~25% | Lian et al. 2020 |
| reversal prob @ debt 100% | 82% | >75% | Lian et al. 2020 |
| share of negative-r-g years (held-out) | 89% | >50% | Mauro & Zhou 2020 |

A second out-of-sample check (the 2-year severity shape, also not fit to) is reproduced:
the 2-year tail sits above the 5-year tail and rises with debt, as in the data.

### 4. CS's safe-haven status, grounded empirically

The crisis-risk term (3) damps if the issuer is insulated from self-fulfilling debt-driven
panic. The literature splits "safe-haven status" into two distinct properties:

- **Property 1 - fragility immunity.** De Grauwe's hypothesis, empirically well-supported,
  is that self-fulfilling liquidity crises strike sovereigns issuing in a currency they do not
  control; this does not arise in standalone countries whose central bank can act as lender of
  last resort. His UK-vs-Spain natural experiment shows the difference in default-risk pricing
  tracks monetary control, not fiscal fundamentals alone. This is exactly the debt-dependent
  crisis channel the band model prices. **CS has Property 1 by construction** (own-currency
  issuance, own monetary authority).
- **Property 2 - reserve-currency flight-to-quality** (yields actively fall in global stress).
  This is *earned* over decades of track record and reserve demand. **CS lacks Property 2 at
  launch**, so the model credits no flight-to-quality bonus.

The band model's safe-haven damping acts on Property 1 (the debt-dependence of crisis
intensity), which CS has, not on Property 2, which it does not. This justifies placing CS in
the **moderate-to-strong damping** range, not the zero-damping "treated like a Eurozone member
or EM borrower" case, which corresponds to a sovereign *lacking* monetary control.

**Honest caveat (multiplist):** monetary sovereignty removes the illiquidity/panic channel,
not the fundamental-solvency channel. Self-fulfilling dynamics unfold only in an intermediate
fundamentals range; very bad fundamentals trigger crisis regardless. CS is therefore immune to
a confidence-driven rollover run but not to a genuine over-issuance / inflation crisis. This is
why the band has a ceiling at all, and why it should not run high.

### 5. The optimal band

Module `cs_band_welfare.py` puts benefit and cost on one welfare scale: citizen seigniorage in
dollars (rises with the band, as the snowball frees seigniorage) against expected crisis cost
(rises with the band via the validated jump tail; crisis modeled as a one-time loss of ~10% of
GDP if peak debt breaches 90%). Verified at N = 6,000 across two seeds
(`cs_band_verify_final.py`):

- **Strong Property-1 damping:** welfare-optimal band 40-80%, central tendency ~30-60%.
- **Moderate Property-1 damping:** welfare-optimal band 30-60%.

The optimum is a **shallow maximum**: across roughly 20-60%, net welfare differs by under ~1.5%,
so the honest claim is a range, not a point. The indistinguishable set (within 1% of best) is
the same under both damping settings and clusters in the moderate region, **excluding both the
15% corner and the high (>80%) region**. Crisis probability stays near zero up through the
moderate bands precisely because CS's monetary sovereignty damps the debt-dependent jump
intensity.

### 6. Recommendation

Replace aggressive retirement-to-15% with a **moderate debt band of ~30-60% of GDP**:

- route the growth-matched seigniorage to citizen floors by default;
- retire debt only to defend the band's ceiling or offset a positive drift;
- hold the standing stock mostly **non-interest-bearing** (zero-coupon), which captures the
  safe-asset collateral and convenience value while removing the steady-state public-to-holder
  transfer (see the companion floor-value analysis), reserving a thin coupon tranche only if a
  benchmark yield curve is wanted.

The exact center of the band (toward 30-40% if CS's safe-haven strength is treated
conservatively, up toward 60% if treated strongly) depends on CS's monetary-sovereignty
damping, which is itself the one empirical question the recommendation is conditional on. The
moderate-band conclusion is invariant to that choice.

---

### Documented residuals and limitations (honest ledger)

- **median r-g @ 40% is -1.05% vs a -1.2% anchor** (~0.15pp shy). The anchor is from
  Blanchard / Mauro-Zhou, not a hard Lian figure; being less negative is conservative for
  band-sizing (it makes low debt look marginally less free than it is).
- **Low-debt reversal frequency is matchable only by the jump model, not the Gaussian family.**
  This was a finding, not a defeat: five structurally-motivated fixes to the Gaussian model
  (horizon, stress persistence, autocorrelation, magnitude/frequency separation, calm
  persistence) all failed at high N, and only switching model class resolved it. The horizon
  also had to be corrected to Lian's measurement window (~28 years), which alone moved the
  high-debt reversal from 89% to 77%.
- **Crisis-cost parameters** (10% of GDP loss, 90% danger threshold) are illustrative within a
  citable range (5-15% output loss). The sensitivity sweep (`cs_band_sensitivity.py`) shows the
  optimum moves with the safe-haven damping but barely with these, so the recommendation is not
  hostage to them.
- **The convenience yield** (the safe-asset value of the standing stock) is ~73bp historically
  (Krishnamurthy & Vissing-Jorgensen 2012), compressed to ~36bp at today's high supply
  (St. Louis Fed 2025). It is the swing variable for the floor-value / coupon question, treated
  as declining in supply, never as a constant.

### Sources

- Blanchard, O. (2019). "Public Debt and Low Interest Rates." *American Economic Review* 109(4).
- Mauro, P. & Zhou, J. (2020). "r minus g negative: Can We Sleep More Soundly?" IMF WP / IMF
  Economic Review.
- Lian, W., Presbitero, A. & Wiriadinata, U. (2020). "Public Debt and r - g at Risk." IMF WP
  20/137.
- Krishnamurthy, A. & Vissing-Jorgensen, A. (2012). "The Aggregate Demand for Treasury Debt."
  *Journal of Political Economy* 120(2). (Plus St. Louis Fed 2025 update on convenience-yield
  compression.)
- De Grauwe, P. (2011). "The Governance of a Fragile Eurozone." CEPS. (Plus the empirical
  fragility-hypothesis tests, e.g. Saka, Fuertes & Kalotychou 2015.)

### Reproducing

All figures regenerate from the inputs:

- `code/dsa_jump_calibrate.py` - calibrate the compound-jump process to the six moments.
- `code/dsa_jump_verify.py` - high-N two-seed verification + out-of-sample checks.
- `code/cs_refine1.py` - stabilize-vs-aggressive citizen-seigniorage comparison.
- `code/cs_band_welfare.py` - the welfare-scale band objective.
- `code/cs_band_sensitivity.py` - optimum across safe-haven / threshold / severity assumptions.
- `code/cs_band_verify_final.py` - final band verification at the grounded damping, two seeds.
- `dsa_locked.json` - the locked, validated process parameters.

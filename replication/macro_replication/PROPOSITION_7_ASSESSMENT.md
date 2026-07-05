# Proposition 7: verification + literature positioning

## VERIFICATION (done — result is mathematically sound)
All three parts independently verified (see code/verify_prop7_analytics.py):
- (i)  theta = 1 + (1+phi)/alpha re-derived SYMBOLICALLY from the paper's Cagan
       demand + KI quantity rule (gap form). Exact match. Determinacy |theta|>1
       holds for all alpha>0, phi>=0.
- (ii) interest-rate analog root = phi (textbook Taylor). The level-vs-rate
       comparison is LEGITIMATE, not a switch: money-quantity rules anchor the
       price LEVEL; interest-rate rules leave the level a unit root and pin only
       inflation. This is a genuine, well-founded asymmetry.
- (iii) two-circuit determinacy threshold c* = 0.1271, verified via symbolic
       solve of the characteristic polynomial at |eig|=1 AND numerical bisection.
Stress-tested (see code/stress_proposition_7.py): robust to sticky prices,
adaptive expectations, stationary velocity shocks, and coupling within the
calibrated regime. Caveats (not failures): anchoring strength ~1/alpha; requires
the empirically-correct alpha>0 sign; breaks only under explosive velocity or
coupling above ~0.13.

## POSITIONING (honest placement in the literature)

### The core determinacy claim is a VARIANT OF A KNOWN FAMILY, not new:
- Woodford (1995), "Price Level Determinacy Without Control of a Monetary
  Aggregate" (NBER WP 5204) — the nearest and most important prior art; title is
  nearly the inverse of P7's framing. MUST be cited and engaged.
- Giannoni (2014); Bauducco & Caputo (2020) — price-level-targeting rules give
  determinacy WITHOUT the Taylor principle. Directly adjacent to P7's logic.
- Angeletos & Lian, "Determinacy without the Taylor Principle" — exit clauses
  fixing money supply become sufficient for determinacy.
- Benassy; balanced-budget + money-growth determinacy (FEDS 1997) — the same
  money-vs-interest asymmetry P7 uses.

### DIRECT CHALLENGE P7 must answer:
- Woodford's cash-in-advance result: constant MONEY-GROWTH regimes can EASILY
  produce indeterminacy AND sunspot equilibria (necessarily so for negative money
  growth). P7 must explain why its KI rule (quantity responding to the PRICE-GAP,
  not constant growth) escapes this. The gap-response feedback is likely the
  answer, but the paper should say so explicitly.

### What is PLAUSIBLY GENUINELY NOVEL in P7 (where to stake the contribution):
The TWO-CIRCUIT mechanism with an explicit, institutionally-grounded coupling
threshold: transactional circuit anchors the level; a quantified spillover
threshold (~0.13) governs when asset->consumer coupling breaks determinacy; and
that threshold is CONTROLLABLE by design (locked non-pledgeable floors keep
phi_liq small). No direct precedent found for this specific structure. Closest
cousin: Piazzesi & Schneider "Money and banking in a NK model" (convenience-yield
channel substitutes for policy as a stabilizing force) — related, not identical.

## RECOMMENDATION
Reframe P7's novelty claim:
  FROM  "determinacy without the Taylor principle" (established since Woodford 1995)
  TO    "a two-circuit money structure delivering price-LEVEL determinacy with a
         quantified, design-controllable asset->consumer spillover threshold."
And add explicit engagement with Woodford (1995) and the cash-in-advance
indeterminacy result, explaining why the KI price-gap-response rule avoids the
indeterminacy of constant-money-growth regimes.


## REFINEMENT (after reading Woodford 1995 in detail)
Woodford (1995)'s mechanism is the FISCAL theory of the price level: the level is
pinned by the government's intertemporal budget (real liabilities = PV of
surpluses). P7's anchor is MONETARY and contains NO fiscal term (theta depends
only on alpha and phi). So P7 is NOT a rediscovery of Woodford -- the two are
COMPLEMENTARY (different anchors, can coexist). This materially strengthens P7's
position versus the initial assessment.

Sharpened novelty claim (now in Paper 5, "Relation to the determinacy literature"):
  - vs Woodford 1995 (FTPL): P7 anchors monetarily, not fiscally. Complementary.
  - vs Giannoni 2014 / Bauducco-Caputo 2020 (price-level targeting): those are
    still INTEREST-RATE regimes attaining determinacy below the Taylor bound; P7's
    anchor is the QUANTITY of transactional money itself.
  - vs Woodford 1994 (cash-in-advance indeterminacy of constant-money-growth):
    P7 escapes because KI is a gap-RESPONSE quantity rule, not constant growth;
    the gap response + circuit segmentation remove the free coordinating dimension.
  - NOVEL: the two-circuit route -- transactional circuit pins the level, asset
    circuit walled off up to a quantified, design-controllable coupling threshold.

Paper 5 now cites: Woodford (1994), Woodford (1995), Giannoni (2014),
Bauducco & Caputo (2020), with the positioning paragraph engaging each.

STATUS: verification done (3 parts, independent) + stress-tested + positioned.
The result is sound and its novelty is now precisely and defensibly stated.


## TARGETED LITERATURE SEARCH (segmented-money / two-circuit determinacy)
Searched 4 framings. Findings ranked by closeness:
1. Piazzesi-Rogers-Schneider (2019), "Money and Banking in a NK Model" — CLOSEST
   antecedent. Money-side determinacy without Taylor, via an endogenous
   convenience-yield threshold. DIFFERENT from P7: PRS stays an interest-rate
   regime, anchors via a liquidity premium, threshold = money-supply rigidity.
   P7 = pure quantity rule, transactional money-demand channel, threshold =
   asset->consumer spillover. Now cited + distinguished in Paper 5.
2. Woodford 1995 (FTPL, fiscal anchor) — complementary. Cited.
3. Giannoni 2014 / Bauducco-Caputo 2020 (price-level targeting, interest-rate) — cited.
4. Benassy 2000 (pure interest-rate peg determinacy) — same family, not two-circuit.
5. NO precedent found for the two-circuit/segmented channel with an asset-consumer
   spillover threshold in a pure quantity-rule setting. This appears genuinely novel.

HONEST FINAL POSITION: P7 lives in a more crowded neighborhood than the first pass
suggested (PRS especially). The defensible novelty is NARROW and SPECIFIC: the
segmented-circuit channel + spillover threshold + pure quantity rule. Paper 5's
positioning paragraph now engages all of PRS, Woodford 1995/1994, Giannoni,
Bauducco-Caputo. NOT claimed: priority over "determinacy without Taylor" broadly.

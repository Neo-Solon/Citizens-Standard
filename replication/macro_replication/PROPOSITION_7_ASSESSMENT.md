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

## LOAD-BEARING TEST (is P7 a linchpin?)
Tested whether the framework's other claims DEPEND on P7 (code/test_p7_loadbearing.py
and code/test_regime_selection_needs_p7.py).

Dependency findings:
- Mode C's ~2% inflation / $108 dividend basis: DEPENDS on circuit SEPARATION
  (computed: with separation +1.85% on M^T; without, ~0% on M2 — the headline
  number is wrong without the two-circuit split).
- "Constitution selects the inflation regime" (the framework's central price
  claim): DEPENDS on DETERMINACY. Computationally confirmed — with P7 on, sunspot
  equilibria explode and are ruled out (200/200), so the selected target is unique;
  with P7 off, sunspots stay bounded (dispersion ~1.1) and the economy can
  self-fulfill an UNSELECTED inflation rate. Regime selection is empty without P7.
- Full-dividend 0% inflation (Paper 9 §7): the ACCOUNTING mean survives without P7,
  but the UNIQUENESS/STABILITY of that price path depends on P7.
- Full-reserve banking (Paper 6): P7 is the macroeconomic PAYOFF of the banking
  design — Paper 6 enforces separation institutionally; P7 shows that separation
  delivers price determinacy.
- Stable Floor (retirement values): INDEPENDENT of P7 (real-return accounting).

VERDICT: P7 is a LINCHPIN for the monetary / price-stability half of the framework
(regime selection, Mode C inflation, the meaning of "price stability", the banking
design's macro payoff). It is NOT load-bearing for the retirement/floor half.
Implication: P7 warrants MORE PROMINENCE within the existing papers (Paper 5 macro,
cross-referenced from Papers 1/6/9) — but still NOT a standalone spin-off paper.
The prominence belongs where the dependent claims live.

## ELEVATION + CROSS-REFERENCING (follow-through on the load-bearing finding)
Because the test showed P7 is load-bearing for the price/inflation half of the
framework, its role was made VISIBLE across the papers (not spun into a new paper):
- Paper 5 (P7's home): added a main-text framing sentence in Section 3.7 stating
  P7 "is not a technical by-product but the result on which the framework's price
  claims rest," and pointing to where those claims live (architecture, banking).
- Paper 1 (Architecture): the regime-selection claim now notes it is meaningful
  only because the chosen regime is the unique determinate equilibrium (2026e,
  Prop 7); the Mode C ~2% inflation claim now notes it presupposes circuit
  separation (2026e Prop 7 / 2026f banking).
- Paper 6 (Banking): already referenced Prop 7 as a macro consequence of the
  banking separation; left as-is (adequate).
Result: a bidirectional cross-reference web — dependent claims point TO P7, P7
points BACK to them, banking design feeds INTO P7. P7's prominence now matches its
structural role WITHOUT a standalone paper.

## PER-MODE REFINEMENT (does load-bearing vary by mode?)
Tested (architecture_replication/code/test_p7_loadbearing_by_mode.py). P7 has TWO
components with DIFFERENT mode-dependence:

- DETERMINACY (unique price path): load-bearing in ALL THREE modes. Every mode
  (A deflation, B 0%, C +2%) targets a distinct rate and claims delivery; that
  claim is empty without uniqueness regardless of mode. Universal.
- CIRCUIT SEPARATION (KI hits M^T not M2): load-bearing ONLY in Mode C (ki>0).
  Modes A/B have ki=0 -> no inflation channel to mis-attribute -> the separation
  dependency is VACUOUS for them. (Mode B's 0% is the k2=1 accounting identity,
  needing no separation argument.) Verified: Mode C +1.85% (M^T) vs -0.02% (M2).

So "P7 is only load-bearing under certain modes" is:
  - TRUE for the SEPARATION half (Mode C / any inflationary mode only).
  - FALSE for the DETERMINACY half (universal across all modes).

The cross-references reflect this correctly: the regime-selection link (Paper 1)
invokes determinacy at the mode-GENERAL claim; the Mode C link invokes separation
at the Mode-C-specific 2% figure. No change needed; mapping verified.

## EMPIRICAL THREAD (separation premise — resolved by connecting to existing evidence)
P7's determinacy rests on two empirical premises: (a) alpha>0 (Cagan, already cited),
and (b) circuit SEPARATION. Premise (b) was previously presented in Paper 5 as an
assumption, but the framework already has DIRECT empirical support for it in the
Paper 10 validation horserace (2026i), which was not connected to P7.

The support (documented in code/verify_p7_separation_evidence.py):
- High-inflation regime, in-sample: transaction-active aggregates (composition, M1,
  Divisia) carry a significant consumer-price signal (R^2 ~ 0.19-0.21, t ~ 2.7-2.9);
  broad M2 does not (R^2 ~ 0.04, t ~ 1.9).
- DECISIVE: encompassing regression (composition + M2) -> composition significant
  (t=2.26), M2 drops out (t=-0.31). Once transaction money is in, broad money adds
  nothing to consumer-price prediction. This is the two-circuit split in the data.
- Robust to PCE index (t=3.00).
- HONEST LIMIT: out-of-sample, the transactional aggregate does NOT beat naive
  persistence (RMSE 2.82 vs 2.69). In-sample structural, not an OOS forecasting edge.

Paper 5's P7 section now cites this (2026i) as CORROBORATION of the separation
premise, explicitly at its honest strength (in-sample, regime-dependent, not proof).
So the "open empirical thread" is narrowed: the separation premise is no longer bare
assumption -- it is assumption + in-sample evidence, with the OOS limit stated.
What remains genuinely open is only the priority/novelty question (needs an expert
lit review), which is separate and already honestly hedged in the paper.

# CS-to-Fractional-World FX Interface — Exploratory Research Record

**STATUS: EXPLORATORY. NOT a replication package for any published paper.**
**Headline finding: NULL-to-NEGATIVE. This does not support a CS FX-stability claim.**

This folder documents an honest, pre-registered attempt to empirically ground the question the
papers leave open (Paper 3 defers it; Paper 7 scopes to CS-to-CS only): **how does a CS economy's
exchange rate behave against the non-CS, floating-fiat world, and is it more stable?**

It is kept **separate from the paper replication packages on purpose.** Those packages support
existing published claims; this is exploratory work toward a *future, unwritten* layer, and its
result is a documented null. Folding it into a paper package would miscategorize a null as support.

## What was tested (all pre-registered, real FRED/BIS data)

1. **Line B — realized FX volatility, anchored vs floating** (7-currency panel, 2021–2026).
   Anchored ~2× less volatile than floating on average — but with overlap (DKK, a EUR-anchor,
   is more volatile vs USD than CAD, a floater) and a confound: "anchored" is relative to the
   anchor target, so only HKD (hard USD board) is truly USD-anchored. Suggestive, not clean.

2. **Line A — variance decomposition (PPP/UIP/residual)**, monthly. **FAILED the pre-registered
   falsification condition:** the CS-removable monetary share was ~7.5% (< 10% floor). At monthly
   frequency ~87–96% of FX variance is residual — the Meese-Rogoff puzzle. FX stability is NOT a
   demonstrable CS advantage at monthly frequency.

3. **PPP half-life test** (frozen protocol, 55yr data). Floating real exchange rates are
   near-random-walks (ADF cannot reject a unit root — the PPP puzzle, robust). The one hard-USD
   anchor (HKD) initially looked stationary — **but that was a nominal-peg artifact.** Once real
   Hong Kong CPI was added, HKD's *real* rate was no longer clearly stationary (ADF p=0.68). Even
   a hard nominal anchor did NOT deliver a stable real exchange rate.

## Honest net

The CS FX-stability claim is **not supported** by the available real-world analogues. The
strongest honest statement is a null-to-negative result. A hopeful (but untested) theoretical
inference remains: a CS currency anchors *inflation* — the very thing that wrecked HKD's real
rate — so it *might* be better positioned than HKD; but no CS-style currency exists to test, and
the analogue evidence we do have does not show the claimed stability.

**Consequence for the framework:** the audio/site international segment correctly stays
"under-specified, say so honestly." This work *strengthens* that hedge rather than lifting it.

## Files
- `fx_interface_replication/` — the Line A/B model + pre-registered protocol + code
- `FX_interface_PANEL_RESULT.json`, `FX_lineA_FALSIFICATION.json` — Line B / Line A records
- `ppp_halflife_protocol.md` — frozen PPP protocol
- `PPP_halflife_VERIFIED.json`, `PPP_withHKcpi_DECISIVE.json` — half-life results (the HK-CPI
  result is the decisive one: it overturned the apparent anchor advantage)
- `ppp_*.csv` — result tables

## What would move this toward a citable result (future work, not done)
Hong Kong CPI is now in hand (used above); still needed: more genuine USD anchors (SAR/AED + CPI),
median-unbiased half-life estimators with confidence intervals, and — because the CS object
(nominal float + rule-fixed inflation anchor) is unobserved — an explicit bracketing design rather
than a claim about any single observed currency.
